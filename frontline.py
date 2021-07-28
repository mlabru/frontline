# -*- coding: utf-8 -*-
"""
frontline

2021/may  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import datetime
import glob
import json
import logging
import pathlib
import shutil
import sys
import requests

# local
import fl_defs as df
import fl_icao_ll as ll
import fl_metsar_gen as mg
import fl_metar_parser as mp
import fl_send_bdc as sb

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# -------------------------------------------------------------------------------------------------
def make_metsar_from_data(fs_file, fs_icao_code, fs_hour, flst_dados_hora, ff_altitude, fo_metar, f_bdc):
    """
    generate METSAR from data

    :param fs_file (str): carrapato filename
    :param fs_icao_code (str): aerodrome ICAO Code
    :param fs_hour (str): time (H)
    :param flst_dados_hora (str): station data register
    :param ff_altitude (float): station altitude (ft)
    :param fo_metar (SMETAR): METAR from carrapato
    :param f_bdc (conn): connection to BDC
    """
    # for all station data...
    for ldct_reg in flst_dados_hora:
        # right hour ?
        if fs_hour == ldct_reg["HR_MEDICAO"].strip():
            # gera METSAR do registro
            mg.make_metsar(fs_file, fs_icao_code, ldct_reg, ff_altitude, fo_metar, f_bdc)
            # quit
            break

    # senão,...
    else:
        # gera METSAR from carrapato
        make_metsar_from_file(fs_file)
        # logger
        M_LOG.error("station hour not found. METSAR from METAF (carrapato).")

# -------------------------------------------------------------------------------------------------
def make_metsar_from_file(fs_file):
    """
    generate METSAR from carrapato file

    :param fs_file (str): carrapato filename
    """
    # output filename
    ls_out = fs_file.replace("carrapato", "frontline")

    # save METSAR
    shutil.copyfile(pathlib.PurePath(df.DS_TICKS_DIR).joinpath(fs_file),
                    pathlib.PurePath(df.DS_OUT_DIR).joinpath(ls_out))

# -------------------------------------------------------------------------------------------------
def trata_carrapato(fdt_gmt, fs_file, f_bdc):
    """
    trata carrapato

    :param fdt_gmt (datetime): date GMT
    :param fs_file (str): carrapato filename
    :param f_bdc (conn): connection to BDC
    """
    # get metaf data
    lo_metaf = mp.metar_parse(fs_file)
    assert lo_metaf

    # save to BDC
    sb.bdc_save_metaf(lo_metaf, f_bdc)

    # filename
    ls_file = pathlib.PurePath(fs_file).name

    # format date
    ls_dia = fdt_gmt.strftime("%Y-%m-%d")
    # format hour
    ls_hour = fdt_gmt.strftime("%H") + "00"

    # split file name
    llst_tmp = fs_file.split('_')

    # icao code
    ls_icao_code = llst_tmp[2].strip().upper()

    # get closer station
    ls_station, lf_altitude = ll.find_near_station(ls_icao_code)
    # M_LOG.info("near station of %s: %s @ %s (m)", str(ls_icao_code), str(ls_station), str(lf_altitude))

    # ok ?
    if ls_station is None:
        # gera METSAR from METAF (carrapato)
        make_metsar_from_file(ls_file)
        # logger
        M_LOG.warning("near station not found. METSAR from METAF (carrapato).")
        # return
        return

    # request de dados horários da estação
    l_response = requests.get('https://apitempo.inmet.gov.br/estacao/{0}/{0}/{1}'.format(ls_dia, ls_station))

    # ok ?
    if 200 == l_response.status_code:
        # make METSAR from station data
        make_metsar_from_data(ls_file, ls_icao_code, ls_hour, json.loads(l_response.text), lf_altitude, lo_metaf, f_bdc)

    # senão,...
    else:
        # gera METSAR from METAF (carrapato)
        make_metsar_from_file(ls_file)
        # logger
        M_LOG.error("station data not found. METSAR from METAF (carrapato).")

# -------------------------------------------------------------------------------------------------
def main():
    """
    main
    """
    # datetime object containing current date and time, but 3 hours ahead
    ldt_now_gmt = datetime.datetime.now() + datetime.timedelta(hours=df.DI_DIFF_GMT)

    # format full date
    ls_date = ldt_now_gmt.strftime("%Y%m%d%H")

    # connect BDC
    l_bdc = sb.bdc_connect()
    assert l_bdc

    # find all stations in directory...
    for ls_file in glob.glob("{}/saida_carrapato_????_{}.txt".format(df.DS_TICKS_DIR, ls_date)):
        # trata carrapato
        trata_carrapato(ldt_now_gmt, ls_file, l_bdc)

    # close BDC
    l_bdc.close()

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:
    # logger
    logging.basicConfig(level=df.DI_LOG_LEVEL)

    # disable logging
    # logging.disable(sys.maxint)

    # run application
    sys.exit(main())

# < the end >--------------------------------------------------------------------------------------

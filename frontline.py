# -*- coding: utf-8 -*-
"""
frontline

2021/may  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import datetime
import glob
import logging
import pathlib
import sys

# local
import fl_defs as df
import fl_data_inmet as im
import fl_data_redemet as rm
import fl_icao_ll as ll
import fl_metsar_gen as mg
import fl_metar_parser as mp
import fl_send_bdc as sb

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# -------------------------------------------------------------------------------------------------
def trata_carrapato(fdt_gmt, fs_file, f_bdc):
    """
    trata carrapato

    :param fdt_gmt (datetime): date GMT
    :param fs_file (str): carrapato filename
    :param f_bdc (conn): connection to BDC
    """
    # get metaf data
    lo_metaf = mp.metar_parse_file(fs_file)
    assert lo_metaf

    # save to BDC
    sb.bdc_save_metaf(lo_metaf, f_bdc)

    # filename
    ls_file = pathlib.PurePath(fs_file).name

    # split file name
    llst_tmp = fs_file.split('_')

    # icao code
    ls_icao_code = llst_tmp[2].strip().upper()

    # build date
    ls_date = fdt_gmt.strftime("%Y%m%d%H")

    # try to get data from REDEMET
    lo_metar = rm.redemet_get_location(ls_date, ls_icao_code)
    # M_LOG.debug("REDEMET lo_metar: %s", str(lo_metar))

    if lo_metar:
        # save to BDC
        sb.bdc_save_metar(lo_metar, f_bdc)

        # make METSAR from REDEMET data
        mg.make_metsar_from_metar(ls_file, ls_icao_code, lo_metar, lo_metaf, f_bdc)

    # senão, estação não encontrada na REDEMET. Tenta INMET
    else:
        # format date
        ls_dia = fdt_gmt.strftime("%Y-%m-%d")
        # format hour
        ls_hour = fdt_gmt.strftime("%H") + "00"

        # get closer station
        ls_station, lf_altitude = ll.find_near_station(ls_icao_code)

        # ok ?
        if ls_station is None:
            # gera METSAR from METAF (carrapato)
            mg.make_metsar_from_file(ls_file)
            # logger
            M_LOG.warning("near station not found. METSAR from METAF (carrapato).")
            # return
            return

        # try to get data from INMET
        llst_station_data = im.inmet_get_location(ls_dia, ls_station)
        # M_LOG.debug("INMET llst_station_data: %s", str(llst_station_data))

        if llst_station_data:
            # make METSAR from station data
            mg.make_metsar_from_station_data(ls_file, ls_icao_code, ls_hour, llst_station_data, lf_altitude, lo_metaf, f_bdc)

        # senão,...
        else:
            # gera METSAR from METAF (carrapato)
            mg.make_metsar_from_file(ls_file)

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

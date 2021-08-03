# -*- coding: utf-8 -*-
"""
frontline

2021/may  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import argparse
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
def arg_parse():
    """
    parse command line arguments
    arguments parse: <initial date> <final date> <ICAO code>

    :returns: arguments
    """
    # create parser
    l_parser = argparse.ArgumentParser(description="Fontline (Carrapato Killer).")
    assert l_parser

    # args
    l_parser.add_argument("-c", "--code", dest="code", action="store", default="x",
                          help="ICAO code.")
    l_parser.add_argument("-i", "--dini", dest="dini", action="store", default="x",
                          help="Initial date.")
    l_parser.add_argument("-f", "--dfnl", dest="dfnl", action="store", default="x",
                          help="Final date.")

    # return arguments
    return l_parser.parse_args()

# -------------------------------------------------------------------------------------------------
def get_date_range(f_args):
    """
    get initial and final dates

    :param f_args: received arguments

    :returns: initial date and delta in hours
    """
    # delta
    li_delta = 1

    # no date at all ?
    if ("x" == f_args.dini) and ("x" == f_args.dfnl):
        # datetime object containing current date and time, but 3 hours ahead (GMT)
        ldt_ini = datetime.datetime.now() + datetime.timedelta(hours=df.DI_DIFF_GMT)
        # build initial date
        ldt_ini = ldt_ini.replace(minute=0)

    # just initial date ?
    elif ("x" != f_args.dini) and ("x" == f_args.dfnl):
        # parse initial date
        ldt_ini = parse_date(f_args.dini)

        # datetime object containing current date and time, but 3 hours ahead (GMT)
        ldt_fnl = datetime.datetime.now() + datetime.timedelta(hours=df.DI_DIFF_GMT)
        # build initial date
        ldt_fnl = ldt_fnl.replace(minute=0)

        # calculate difference in hours
        li_delta = ldt_fnl - ldt_ini
        li_delta = int(li_delta.total_seconds() / 3600)

    # just final date ?
    elif ("x" == f_args.dini) and ("x" != f_args.dfnl):
        # parse final date
        ldt_fnl = parse_date(f_args.dfnl)

        # delta
        ldt_ini = ldt_fnl - datetime.timedelta(hours=1)

    # so, both dates
    else:
        # parse initial date
        ldt_ini = parse_date(f_args.dini)

        # parse final date
        ldt_fnl = parse_date(f_args.dfnl)

        # calculate difference
        li_delta = ldt_fnl - ldt_ini
        li_delta = int(li_delta.total_seconds() / 3600)

    # return initial date and delta in hours
    return ldt_ini, li_delta

# -------------------------------------------------------------------------------------------------
def parse_date(fs_data):
    """
    parse date

    :param fs_data: date to be parsed

    :returns: date in datetime format
    """
    try:
        # parse data
        ldt_date = datetime.datetime.strptime(fs_data, "%Y-%m-%dT%H:%M")
        # build initial date
        ldt_date = ldt_date.replace(minute=0)

    # em caso de erro,...
    except Exception as lerr:
        # logger
        M_LOG.error("Date format error: %s.", lerr)

        # abort
        sys.exit(-1) 

    # return date in datetime format
    return ldt_date

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
    sb.bdc_save_metaf(fdt_gmt, lo_metaf, f_bdc)

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

    if lo_metar:
        # save to BDC
        sb.bdc_save_metar(fdt_gmt, lo_metar, f_bdc)

        # make METSAR from REDEMET data
        mg.make_metsar_from_metar(fdt_gmt, ls_file, ls_icao_code, lo_metar, lo_metaf, f_bdc)

    # senão, estação não encontrada na REDEMET. Tenta INMET
    else:
        # format date
        ls_dia = fdt_gmt.strftime("%Y-%m-%d")

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

        if llst_station_data:
            # make METSAR from station data
            mg.make_metsar_from_station_data(fdt_gmt, ls_file, ls_icao_code, llst_station_data, lf_altitude, lo_metaf, f_bdc)

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
    # get program arguments
    l_args = arg_parse()

    # connect BDC
    l_bdc = sb.bdc_connect()
    assert l_bdc

    # station
    ls_station = "????" if "x" == l_args.code else str(l_args.code)

    # time delta
    ldt_1hour = datetime.timedelta(hours=1)

    # date range
    ldt_ini, li_delta = get_date_range(l_args)
    M_LOG.debug("ldt_ini: %s  li_delta: %d", ldt_ini, li_delta)

    # for all dates...
    for li_i in range(li_delta):
        # format full date
        ls_date = ldt_ini.strftime("%Y%m%d%H")
        # logger
        M_LOG.warning("Processando, estação: %s data: %s", ls_station, ls_date)

        # find all stations in directory...
        for ls_file in glob.glob("{}/saida_carrapato_{}_{}.txt".format(df.DS_TICKS_DIR, ls_station, ls_date)):
            # trata carrapato
            trata_carrapato(ldt_ini, ls_file, l_bdc)

        # save new initial
        ldt_ini += ldt_1hour

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

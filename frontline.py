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
import threading

# local
import fl_defs as df
import fl_data_inmet as im
import fl_data_redemet as rm
import fl_icao_ll as ll
import fl_metsar_gen as mg
import fl_metar_parser as mp
import fl_send_bdc as sb

# < logging >--------------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# create file handler which logs even debug messages
# M_LOG_FH = logging.FileHandler("frontline_{}.log".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")))
# M_LOG_FH.setLevel(df.DI_LOG_LEVEL)

# create formatter and add it to the handlers
# M_LOG_FRM = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# M_LOG_FH.setFormatter(M_LOG_FRM)

# add the handlers to the logger
# M_LOG.addHandler(M_LOG_FH)

# create console handler with a higher log level
# M_LOG_CH = logging.StreamHandler()
# M_LOG_CH.setLevel(df.DI_LOG_LEVEL)

# add formatter to the handler
# M_LOG_CH.setFormatter(M_LOG_FRM)

# add the handlers to the logger
# M_LOG.addHandler(M_LOG_CH)

# -------------------------------------------------------------------------------------------------
def arg_parse():
    """
    parse command line arguments
    arguments parse: <initial date> <final date> <ICAO code>

    :returns: arguments
    """
    # create parser
    l_parser = argparse.ArgumentParser(description="Frontline (Carrapato Killer).")
    assert l_parser

    # args
    l_parser.add_argument("-c", "--code", dest="code", action="store", default="x",
                          help="ICAO code.")
    l_parser.add_argument("-f", "--dfnl", dest="dfnl", action="store", default="x",
                          help="Final date.")
    l_parser.add_argument("-i", "--dini", dest="dini", action="store", default="x",
                          help="Initial date.")

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
        ldt_ini = ldt_ini

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
    return ldt_ini.replace(minute=0, second=0, microsecond=0), li_delta

# -------------------------------------------------------------------------------------------------
def get_station_code(fs_file):
    """
    get ICAO Code from file name

    :param fs_file: received file name

    :returns: ICAO Code
    """
    # split file name
    llst_tmp = fs_file.split('_')

    # return icao code
    return llst_tmp[2].strip().upper()

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
    except Exception as l_err:
        # logger
        M_LOG.error("Date format error: %s. Aborting.", l_err)

        # abort
        sys.exit(-1)

    # return date in datetime format
    return ldt_date

# -------------------------------------------------------------------------------------------------
def save_metar(fs_fout, fs_metar_mesg):
    """
    save METAR to file

    :param fs_fout (str): output filename
    :param fs_metar_mesg (str): METAR message
    """
    # create output file
    with open (pathlib.PurePath(df.DS_MET_DIR).joinpath(fs_fout), "w") as lfh_out:
        # write output file
        lfh_out.write(fs_metar_mesg)

# -------------------------------------------------------------------------------------------------
def trata_aerodromo(fdt_gmt, fs_icao_code, f_bdc):
    """
    trata aerodromo

    :param fdt_gmt (datetime): date GMT
    :param fs_icao_code (str): ICAO code
    :param f_bdc (conn): connection to BDC
    """
    # build date
    ls_date = fdt_gmt.strftime("%Y%m%d%H")

    # try to get data from REDEMET
    lo_metar = rm.redemet_get_location(ls_date, fs_icao_code)

    if lo_metar:
        # save to BDC
        sb.bdc_save_metar(fdt_gmt, lo_metar, f_bdc)
   
        # save METAR to file
        save_metar("metar_{}_{}.txt".format(fs_icao_code, ls_date), lo_metar.s_metar_mesg)

        # output filename
        ls_out = "saida_frontline_{}_{}.txt".format(fs_icao_code, ls_date)

        # make METSAR from REDEMET data
        mg.make_metsar_from_metar(fdt_gmt, ls_out, fs_icao_code, lo_metar, f_bdc)

    # senão,...
    else:
        # logger
        M_LOG.error("METAR for %s at %s not found. Skipping.", fs_icao_code, ls_date)

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
    ls_fname = pathlib.PurePath(fs_file).name

    # icao code
    ls_icao_code = get_station_code(ls_fname)

    # build date
    ls_date = fdt_gmt.strftime("%Y%m%d%H")

    # try to get data from REDEMET
    lo_metar = rm.redemet_get_location(ls_date, ls_icao_code)

    if lo_metar:
        # save to BDC
        sb.bdc_save_metar(fdt_gmt, lo_metar, f_bdc)

        # save METAR to file
        save_metar("metar_{}_{}.txt".format(ls_icao_code, ls_date), lo_metar.s_metar_mesg)

        # output filename
        ls_out = ls_fname.replace("carrapato", "frontline")

        # make METSAR from REDEMET data
        mg.ensamble_metar_metaf(fdt_gmt, ls_out, ls_icao_code, lo_metar, lo_metaf, f_bdc)

    # senão, estação não encontrada na REDEMET. Tenta INMET
    else:
        # format date
        ls_dia = fdt_gmt.strftime("%Y-%m-%d")

        # get closest station
        ls_station, lf_altitude = ll.find_near_station(ls_icao_code)

        if ls_station:
            # try to get data from INMET
            llst_station_data = im.inmet_get_location(ls_dia, ls_station)

            if llst_station_data:
                # make METSAR from station data
                mg.ensamble_station_data_metaf(fdt_gmt, ls_fname, ls_icao_code, llst_station_data, lf_altitude, lo_metaf, f_bdc)

            # senão,...
            else:
                # logger
                M_LOG.error("Data for %s not found. METSAR from METAF (carrapato).", ls_station)

                # gera METSAR from METAF (carrapato)
                mg.make_metsar_from_file(ls_fname)

        # senão,...
        else:
            # logger
            M_LOG.error("Near station from %s not found or too far. METSAR from METAF (carrapato).", ls_icao_code)

            # gera METSAR from METAF (carrapato)
            mg.make_metsar_from_file(ls_fname)

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

    # for all dates...
    for li_i in range(li_delta):
        # format full date
        ls_date = ldt_ini.strftime("%Y%m%d%H")

        # logger
        M_LOG.info("Processando, estação: %s data: %s.", ls_station, ls_date)

        # create trata_carrapato threads list
        llst_thr_carrapato = list()

        # find all stations in directory...
        for ls_file in glob.glob("{}/saida_carrapato_{}_{}.txt".format(df.DS_TICKS_DIR, ls_station, ls_date)):
            # logger
            M_LOG.debug("Create and start thread for carrapato %s.", ls_file)
            
            # create thread trata_carrapato
            l_thr = threading.Thread(target=trata_carrapato, args=(ldt_ini, ls_file, l_bdc))
            assert l_thr

            # save thread trata_carrapato
            llst_thr_carrapato.append((get_station_code(ls_file), l_thr))
            
            # exec thread trata_carrapato
            l_thr.start()

        # logger
        M_LOG.debug("Encontrados %d carrapatos.\n%s", len(llst_thr_carrapato), str(llst_thr_carrapato))
        
        # create carrapato ok list
        llst_carrapato_ok = list()

        # for all carrapato threads...
        for (ls_station, l_thr) in llst_thr_carrapato:
            # thread ok ?
            if l_thr:
                # wait for thread
                l_thr.join()

                # save in carrapato ok list
                llst_carrapato_ok.append(ls_station) 

        # logger
        M_LOG.debug("Encontrados %d aeródromos na REDEMET.\n%s", len(rm.DDCT_AERODROMOS), rm.DDCT_AERODROMOS)

        # create threads list
        llst_thr_aerodromo = list()

        # for all remaining aeródromos...
        for ls_code in rm.DDCT_AERODROMOS:
            # carrapato ok ?
            if ls_code in llst_carrapato_ok:
                # skip this one
                continue

            # logger
            M_LOG.debug("Create and start thread for aeródromo %s.", ls_code)
            
            # trata aeródromo
            l_thr = threading.Thread(target=trata_aerodromo, args=(ldt_ini, ls_code, l_bdc))
            assert l_thr

            # exec thread trata aeródromo
            llst_thr_aerodromo.append(l_thr)

            # exec thread trata aeródromo
            l_thr.start()

        # logger
        M_LOG.debug("Encontrados %d aeródromos.", len(llst_thr_aerodromo))
        M_LOG.debug("llst_thr_aerodromo: %s", str(llst_thr_aerodromo))
        
        # for all aeródromo threads...
        for l_thr in llst_thr_aerodromo:
            # thread ok ?
            if l_thr:
                # wait for thread
                l_thr.join()

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

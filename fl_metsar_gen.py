# -*- coding: utf-8 -*-
"""
fl_metsar_gen

2021/may  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import math
import pathlib
import shutil

# local
import fl_defs as df
import fl_send_bdc as sb

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# -------------------------------------------------------------------------------------------------
def grp_qnh(fdct_reg, ff_altitude, fo_metaf):
    """
    group QNH

    :param fdct_reg (dict): station register
    :param ff_altitude (float): station altitude (m)
    :param fo_metaf (SMETAR): METAR from model (METAF)
    """
    # pressão atmosférica ao nível da estação (mB)
    l_qfe = fdct_reg.get("PRE_INS", None)

    if l_qfe:
        # QNH
        lf_qnh = float(l_qfe) * math.exp(5.2561 * math.log(288 / (288 - (0.0065 * ff_altitude))))

    # senão,...
    else:
        # QNH
        lf_qnh = fo_metaf.i_pressure_hpa

    # return group QNH
    return "Q{:04d}".format(int(lf_qnh)), int(lf_qnh)

# -------------------------------------------------------------------------------------------------
def grp_temp(fdct_reg, fo_metaf):
    """
    group temp

    :param fdct_reg (dict): station register
    :param fo_metaf (SMETAR): METAR from model (METAF)
    """
    # temperatura do ar (bulbo seco) da estação
    l_tabs_stat = fdct_reg.get("TEM_INS", None)

    # nenhuma temperatura ?
    if (l_tabs_stat is None) and (fo_metaf.i_temperature_c is None):
        # sem temperatura (!!!REVER!!!)
        li_tabs = 0

    # só temperatura da estação ?
    elif (l_tabs_stat is not None) and (fo_metaf.i_temperature_c is None):
        # convert to int
        li_tabs = int(float(l_tabs_stat))

    # só temperatura do modelo ?
    elif (l_tabs_stat is None) and (fo_metaf.i_temperature_c is not None):
        # temperature in °C from model
        li_tabs = fo_metaf.i_temperature_c

    # senão, ambas
    else:
        # convert to int
        li_tabs_stat = int(float(l_tabs_stat))

        # temperature in °C from model
        li_tabs_model = fo_metaf.i_temperature_c

        # temperatura da estação no range +- 10° do modelo ?
        if (li_tabs_model - 10) <= li_tabs_stat <= (li_tabs_model + 10):
            # temperatura da estação
            li_tabs = li_tabs_stat

        # senão, do modelo
        else:
            # temperatura do modelo
            li_tabs = li_tabs_model

    # format
    ls_tabs = "{:02d}".format(abs(li_tabs))

    # below zero ?
    if li_tabs < 0:
        # put an M in front of
        ls_tabs = 'M' + ls_tabs

    # temperatura do ponto de orvalho da estação
    l_tpo_stat = fdct_reg.get("PTO_INS", None)

    # nenhuma temperatura ?
    if (l_tpo_stat is None) and (fo_metaf.i_dewpoint_c is None):
        # sem temperatura (!!!REVER!!!)
        li_tpo = 0

    # só temperatura da estação ?
    elif (l_tpo_stat is not None) and (fo_metaf.i_dewpoint_c is None):
        # convert to int
        li_tpo = int(float(l_tpo_stat))

    # só temperatura do modelo ?
    elif (l_tpo_stat is None) and (fo_metaf.i_dewpoint_c is not None):
        # dewpoint in °C from model
        li_tpo = fo_metaf.i_dewpoint_c

    # senão, ambas
    else:
        # convert to int
        li_tpo_stat = int(float(l_tpo_stat))

        # dewpoint in °C from model
        li_tpo_model = fo_metaf.i_dewpoint_c

        # temperatura da estação no range +- 10° do modelo ?
        if (li_tpo_model - 10) <= li_tpo_stat <= (li_tpo_model + 10):
            # temperatura da estação
            li_tpo = li_tpo_stat

        # senão, do modelo
        else:
            # temperatura do modelo
            li_tpo = li_tpo_model

    # format
    ls_tpo = "{:02d}".format(abs(li_tpo))

    # below zero ?
    if li_tpo < 0:
        # put an M in front of
        ls_tpo = 'M' + ls_tpo

    # return group temp
    return "{}/{}".format(ls_tabs, ls_tpo), li_tabs, li_tpo

# -------------------------------------------------------------------------------------------------
def grp_time(fdct_reg):
    """
    group time

    :param fdct_reg (dict): station register
    """
    # return group time
    return "{}{}Z".format(fdct_reg["DT_MEDICAO"][-2:],
                          fdct_reg["HR_MEDICAO"])

# -------------------------------------------------------------------------------------------------
def grp_vis(fo_metaf):
    """
    group visibility

    :param fo_metaf (SMETAR): METAR from model (METAF)
    """
    # visibility
    ls_vis = ""

    # visibility
    li_vis = None

    # have visibility ?
    if fo_metaf.i_visibility is None:
        # ceiling and visibility ok ?
        if fo_metaf.v_cavok:
            # visibility
            ls_vis = "CAVOK"

            # visibility
            li_vis = 99999

    # senão, have visibility
    else:
        # visibility
        ls_vis = "{:04d}".format(fo_metaf.i_visibility)

        # visibility
        li_vis = fo_metaf.i_visibility

    # return group visibility
    return ls_vis, li_vis

# -------------------------------------------------------------------------------------------------
def grp_wind(fdct_reg, fo_metaf):
    """
    group wind

    :param fdct_reg (dict): station register
    :param fo_metaf (SMETAR): METAR from model (METAF)
    """
    # vento, direção
    l_wdir = fdct_reg.get("VEN_DIR", None)

    if l_wdir:
        # convert to int
        li_wdir = int(l_wdir)

    # senão,...
    else:
        # wind direction in °C from model
        li_wdir = fo_metaf.i_wind_dir

    # group wind
    ls_wind = "{:03d}".format((li_wdir // 10) * 10)

    # vento, velocidade
    l_wvel = fdct_reg.get("VEN_VEL", None)

    if l_wvel:
        # convert to int
        li_wvel = int(float(l_wvel) * df.DF_MPS2KT)

    # senão,...
    else:
        # wind velocity in kt from model
        li_wvel = fo_metaf.i_wind_vel_kt

    # group wind
    ls_wind += "{:02d}".format(li_wvel) if li_wvel < 100 else "P99"

    # vento, rajada máxima
    l_wraj = fdct_reg.get("VEN_RAJ", None)

    if l_wraj:
        # gust of wind in m/s converted to kt
        li_wraj = int(float(l_wraj) * df.DF_MPS2KT)

    # senão,...
    elif fo_metaf.i_gust_kt:
        # wind gust in kt from model
        li_wraj = fo_metaf.i_gust_kt

    # senão,...
    else:
        # no gust of wind
        li_wraj = 0

    # rajada ?
    if li_wraj >= (li_wvel + 10):
        # format
        ls_wind += 'G'
        ls_wind += "{:02d}".format(li_wraj) if li_wraj < 100 else "P99"

    # return group wind
    return "{}KT".format(ls_wind), li_wvel, li_wdir, li_wraj

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
def make_metsar_from_station_data(fdt_gmt, fs_file, fs_icao_code, flst_station_data, ff_altitude, fo_metaf, f_bdc):
    """
    generate METSAR from station data

    :param fdt_gmt (datetime): processing date
    :param fs_file (str): carrapato filename
    :param fs_icao_code (str): aerodrome ICAO Code
    :param flst_station_data (lst): station data register
    :param ff_altitude (float): station altitude (ft)
    :param fo_metaf (SMETAR): METAF from carrapato
    :param f_bdc (conn): connection to BDC
    """
    # format hour
    ls_hour = fdt_gmt.strftime("%H") + "00"

    # for all station data...
    for ldct_reg in flst_station_data:
        # right hour ?
        if ls_hour == ldct_reg["HR_MEDICAO"].strip():
            # output filename
            ls_out = fs_file.replace("carrapato", "frontline")

            # create output file
            with open (pathlib.PurePath(df.DS_OUT_DIR).joinpath(ls_out), "w") as lfh_out:
                # time
                ls_time = grp_time(ldct_reg)

                # wind
                ls_wind, li_wvel, li_wdir, li_wraj = grp_wind(ldct_reg, fo_metaf)

                # visibility
                ls_vis, li_vis = grp_vis(fo_metaf)

                # temperature
                ls_temp, li_tabs, li_tpo = grp_temp(ldct_reg, fo_metaf)

                # pressure
                ls_qnh, li_qnh = grp_qnh(ldct_reg, ff_altitude, fo_metaf)

                # build message
                ls_mesg = "METSAR {} {} {} {} {} {}=".format(fs_icao_code, ls_time, ls_wind, ls_vis, ls_temp, ls_qnh)

                # write output file
                lfh_out.write(ls_mesg)

                # write METSAR to BDC
                sb.bdc_save_metsar(fdt_gmt,
                                   fs_icao_code,
                                   li_tabs, li_tpo,
                                   li_wvel, li_wdir, li_wraj,
                                   li_vis,
                                   li_qnh,
                                   ls_mesg,
                                   f_bdc)
            # quit
            break

    # senão,...
    else:
        # gera METSAR from carrapato
        make_metsar_from_file(fs_file)
        # logger
        M_LOG.error("station hour not found. METSAR from METAF (carrapato).")

# -------------------------------------------------------------------------------------------------
def make_metsar_from_metar(fdt_gmt, fs_file, fs_icao_code, fo_metar, fo_metaf, f_bdc):
    """
    generate METSAR from location METAR

    :param fdt_gmt (datetime): processing date
    :param fs_file (str): carrapato filename
    :param fs_icao_code (str): aerodrome ICAO Code
    :param fo_metar (SMETAR): location METAR
    :param fo_metaf (SMETAR): METAF from carrapato
    :param f_bdc (conn): connection to BDC
    """
    # output filename
    ls_out = fs_file.replace("carrapato", "frontline")

    # create output file
    with open (pathlib.PurePath(df.DS_OUT_DIR).joinpath(ls_out), "w") as lfh_out:
        # time
        ls_time = fo_metar.s_forecast_time

        # wind
        ls_wind = fo_metaf.s_wind        if fo_metar.s_wind        is None else fo_metar.s_wind
        li_wvel = fo_metaf.i_wind_vel_kt if fo_metar.i_wind_vel_kt is None else fo_metar.i_wind_vel_kt

        # vento sem direção ?
        if fo_metar.i_wind_dir is None:
            # direção do vento
            li_wdir = fo_metaf.i_wind_dir if fo_metar.i_wind_vel_kt is None else 270

        # senão, vento tem direção
        else:
            # direção do METAR
            li_wdir = fo_metar.i_wind_dir

        # rajada
        li_wraj = fo_metaf.i_gust_kt if fo_metar.i_gust_kt is None else fo_metar.i_gust_kt

        # wind var
        ls_wind += "" if fo_metar.s_wind_var is None else " " + fo_metar.s_wind_var

        # METAR have visibility or cavok ?
        if fo_metar.i_visibility or fo_metar.v_cavok:
            # visibility
            ls_vis = fo_metar.s_visibility
            # visibility
            li_vis = fo_metar.i_visibility if fo_metar.i_visibility is not None else 99999

        # senão, try METAF
        elif fo_metaf.i_visibility or fo_metaf.v_cavok:
            # visibility
            ls_vis = fo_metaf.s_visibility
            # visibility
            li_vis = fo_metaf.i_visibility if fo_metaf.i_visibility is not None else 99999

        # senão,...
        else:
            # visibility
            ls_vis = ""
            # visibility
            li_vis = None
            
        # temperature
        ls_temp = fo_metaf.s_temperature   if fo_metar.s_temperature   is None else fo_metar.s_temperature
        li_tabs = fo_metaf.i_temperature_c if fo_metar.i_temperature_c is None else fo_metar.i_temperature_c
        li_tpo  = fo_metaf.i_dewpoint_c    if fo_metar.i_dewpoint_c    is None else fo_metar.i_dewpoint_c

        # pressure
        ls_qnh = fo_metaf.s_pressure     if fo_metar.s_pressure     is None else fo_metar.s_pressure
        li_qnh = fo_metaf.i_pressure_hpa if fo_metar.i_pressure_hpa is None else fo_metar.i_pressure_hpa

        # build message
        ls_mesg = "METSAR {} {} {} {} {} {}=".format(fs_icao_code, ls_time, ls_wind, ls_vis, ls_temp, ls_qnh)

        # write output file
        lfh_out.write(ls_mesg)

        # write METSAR to BDC
        sb.bdc_save_metsar(fdt_gmt,
                           fs_icao_code,
                           li_tabs, li_tpo,
                           li_wvel, li_wdir, li_wraj,
                           li_vis,
                           li_qnh,
                           ls_mesg,
                           f_bdc)

# < the end >--------------------------------------------------------------------------------------

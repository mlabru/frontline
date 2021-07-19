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

# local
import fl_defs as df

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
    :param fo_metaf (SMETAR): METAR from model
    """
    # pressão atmosférica ao nível da estação (mB)
    l_qfe = fdct_reg.get("PRE_INS", None)

    if l_qfe:
        # QNH
        lf_qnh = float(l_qfe) * math.exp(5.2561 * math.log(288 / (288 - 0.0065 * ff_altitude)))

    # senão,...
    else:
        # QNH
        lf_qnh = fo_metaf.i_pressure_hpa

    # return group QNH
    return "Q{:04d}".format(int(lf_qnh))

# -------------------------------------------------------------------------------------------------
def grp_temp(fdct_reg, fo_metaf):
    """
    group temp

    :param fdct_reg (dict): station register
    :param fo_metaf (SMETAR): METAR from model
    """
    # temperatura do ar - bulbo seco
    l_tabs = fdct_reg.get("TEM_INS", None)

    if l_tabs is not None:
        # convert to int
        li_tabs = int(float(l_tabs))

    # senão,...
    elif fo_metaf.i_temperature_c is not None:
        # temperature in °C from model
        li_tabs = fo_metaf.i_temperature_c

    # senão,...
    else:
        # sem temperatura (!!!REVER!!!)
        li_tabs = 0
        
    # format
    ls_tabs = "{:02d}".format(abs(li_tabs))

    # below zero ?
    if li_tabs < 0:
        # put an M in front of
        ls_tabs = 'M' + ls_tabs

    # temperatura do ponto de orvalho
    l_tpo = fdct_reg.get("PTO_INS", None)

    if l_tpo is not None:
        # convert to int
        li_tpo = int(float(l_tpo))

    # senão,...
    elif fo_metaf.i_dewpoint_c is not None:
        # dewpoint in °C from model
        li_tpo = fo_metaf.i_dewpoint_c

    # senão,...
    else:
        # sem temperatura (!!!REVER!!!)
        li_tpo = 0
        
    # format
    ls_tpo = "{:02d}".format(abs(li_tpo))

    # below zero ?
    if li_tpo < 0:
        # put an M in front of
        ls_tpo = 'M' + ls_tpo

    # return group temp
    return "{}/{}".format(ls_tabs, ls_tpo)

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

    :param fo_metaf (SMETAR): METAR from model
    """
    # ceiling and visibility ok ?
    if fo_metaf.v_cavok:
        # visibility
        ls_vis = "CAVOK"

    # visibility ?
    elif fo_metaf.i_visibility:
        # visibility
        ls_vis = "{:04d}".format(fo_metaf.i_visibility)

    # return group visibility
    return ls_vis

# -------------------------------------------------------------------------------------------------
def grp_wind(fdct_reg, fo_metaf):
    """
    group wind

    :param fdct_reg (dict): station register
    :param fo_metaf (SMETAR): METAR from model
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
    ls_wind = "{:03d}".format(li_wdir)

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
    ls_wind += "{:02d}".format(li_wvel)

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
        ls_wind += "{:02d}".format(li_wraj)

    # return group wind
    return "{}KT".format(ls_wind)

# -------------------------------------------------------------------------------------------------
def make_metsar(fs_file, fs_icao_code, fdct_reg, ff_altitude, fo_metaf):
    """
    generate METSAR file from ensemble

    :param fs_file (str): carrapato filename
    :param fs_icao_code (str): aerodrome ICAO Code
    :param fdct_reg (dict): register
    :param ff_altitude (float): station altitude (m)
    :param fo_metaf (SMETAR): METAR from model
    """
    # output filename
    ls_out = fs_file.replace("carrapato", "frontline")

    # create output file
    with open (pathlib.PurePath(df.DS_OUT_DIR).joinpath(ls_out), "w") as lfh_out:
        # write output file
        lfh_out.write("METSAR {} {} {} {} {} {}=".format(fs_icao_code,
                                                         grp_time(fdct_reg),
                                                         grp_wind(fdct_reg, fo_metaf),
                                                         grp_vis(fo_metaf),
                                                         grp_temp(fdct_reg, fo_metaf),
                                                         grp_qnh(fdct_reg, ff_altitude, fo_metaf)))

# < the end >--------------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
"""
fl_send_bdc

2021.sep  mlabru  implement hidden security
2021.jul  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging
import os
import typing

# postgres
import psycopg2

# dotenv
import dotenv

# local
import fl_defs as df

# < environment >------------------------------------------------------------------------------

# take environment variables from .env
dotenv.load_dotenv()

# DB connection
DS_DB = os.getenv("DS_DB")
DS_HOST = os.getenv("DS_HOST")
DS_PASS = os.getenv("DS_PASS")
DS_USER = os.getenv("DS_USER")

# ---------------------------------------------------------------------------------------------
def bdc_connect(fs_host: typing.Optional[str]=DS_HOST,
                fs_db: typing.Optional[str]=DS_DB,
                fs_user: typing.Optional[str]=DS_USER,
                fs_pass: typing.Optional[str]=DS_PASS):
    """
    connect to BDC
    """
    # create connection
    l_bdc = psycopg2.connect(host=fs_host, database=fs_db, user=fs_user, password=fs_pass)
    assert l_bdc

    # return
    return l_bdc

# ---------------------------------------------------------------------------------------------
def bdc_save_metaf(fdt_gmt, fo_metaf, f_bdc):
    """
    write metaf data to BDC
           
    :param fdt_gmt (datetime): date GMT
    :param fo_metaf (SMETAR): carrapato METAF
    :param f_bdc (conn): connection to BDC
    """
    # build date & time
    ldt_date = fdt_gmt.date()
    ldt_time = fdt_gmt.time()

    # have visibility ?
    if fo_metaf.i_visibility is None:
        # visibility
        li_vis = df.DI_VIS_CAVOK if fo_metaf.v_cavok else "null"

    # senão, have visibility
    else:
        # visibility
        li_vis = fo_metaf.i_visibility

    # make query
    ls_query = "insert into metaf(sigla_aerodromo, dt_metaf, hr_metaf, temperatura_ar, " \
               "temperatura_po, velocidade_vento, direcao_vento, rajada, visibilidade, " \
               "qnh, mensagem) values ('{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, " \
               "'{}')".format(fo_metaf.s_icao_code, ldt_date, ldt_time,
               fo_metaf.i_temperature_c if fo_metaf.i_temperature_c is not None else "null",
               fo_metaf.i_dewpoint_c if fo_metaf.i_dewpoint_c is not None else "null",
               fo_metaf.i_wind_vel_kt if fo_metaf.i_wind_vel_kt is not None else "null",
               fo_metaf.i_wind_dir if fo_metaf.i_wind_dir is not None else "null",
               fo_metaf.i_gust_kt if fo_metaf.i_gust_kt is not None else "null",
               li_vis,
               fo_metaf.i_pressure_hpa if fo_metaf.i_pressure_hpa is not None else "null",
               fo_metaf.s_metar_mesg)

    # write to BDC
    bdc_write(f_bdc, ls_query)

# ---------------------------------------------------------------------------------------------
def bdc_save_metar(fdt_gmt, fo_metar, f_bdc):
    """
    write metar data to BDC

    :param fdt_gmt (datetime): date GMT
    :param fo_metar (SMETAR): METAR from location
    :param f_bdc (conn): connection to BDC
    """
    # build date & time
    ldt_date = fdt_gmt.date()
    ldt_time = fdt_gmt.time()

    # have visibility ?
    if fo_metar.i_visibility is None:
        # visibility
        li_vis = df.DI_VIS_CAVOK if fo_metar.v_cavok else "null"

    # senão, have visibility
    else:
        # visibility
        li_vis = fo_metar.i_visibility

    # make query
    ls_query = "insert into metar(sigla_aerodromo, dt_metar, hr_metar, temperatura_ar, " \
               "temperatura_po, velocidade_vento, direcao_vento, rajada, visibilidade, " \
               "qnh, mensagem) values ('{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, " \
               "'{}')".format( fo_metar.s_icao_code, ldt_date, ldt_time,
               fo_metar.i_temperature_c if fo_metar.i_temperature_c is not None else "null",
               fo_metar.i_dewpoint_c if fo_metar.i_dewpoint_c is not None else "null",
               fo_metar.i_wind_vel_kt if fo_metar.i_wind_vel_kt is not None else "null",
               fo_metar.i_wind_dir if fo_metar.i_wind_dir is not None else "null",
               fo_metar.i_gust_kt if fo_metar.i_gust_kt is not None else "null",
               li_vis,
               fo_metar.i_pressure_hpa if fo_metar.i_pressure_hpa is not None else "null",
               fo_metar.s_metar_mesg)

    # write to BDC
    bdc_write(f_bdc, ls_query)

# ---------------------------------------------------------------------------------------------
def bdc_save_metsar(fdt_gmt, fs_icao_code: str, fi_tabs: int, fi_tpo: int,
                    fi_wvel: int, fi_wdir: int, fi_wraj: int, fi_vis: int, 
                    fi_qnh: int, fs_mesg: str, f_bdc):
    """
    write metsar data to BDC

    :param fdt_gmt (datetime): date GMT
    :param fs_icao_code (str):
    :param fi_tabs (int): temperature
    :param fi_tpo (int): dewpoint
    :param fi_wvel (int): wind vel
    :param fi_wdir (int): wind dir
    :param fi_wraj (int): wind gust
    :param fi_vis (int): visibility
    :param fi_qnh (int): QNH
    :param fs_mesg (str): METAR from location
    :param f_bdc (conn): connection to BDC
    """
    # build date & time
    ldt_date = fdt_gmt.date()
    ldt_time = fdt_gmt.time()

    # make query
    ls_query = "insert into metsar(sigla_aerodromo, dt_metsar, hr_metsar, temperatura_ar, " \
               "temperatura_po, velocidade_vento, direcao_vento, rajada, visibilidade, " \
               "qnh, mensagem) values ('{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, " \
               "'{}')".format(fs_icao_code, ldt_date, ldt_time,
               fi_tabs if fi_tabs is not None else "null",
               fi_tpo if fi_tpo is not None else "null",
               fi_wvel if fi_wvel is not None else "null",
               fi_wdir if fi_wdir is not None else "null",
               fi_wraj if fi_wraj is not None else "null",
               fi_vis if fi_vis is not None else "null",
               fi_qnh if fi_qnh is not None else "null",
               fs_mesg)

    # write to BDC
    bdc_write(f_bdc, ls_query)

# ---------------------------------------------------------------------------------------------
def bdc_save_metsar_b(fdt_gmt, fs_icao_code, fi_tabs, fi_tpo,
                      fi_wvel, fi_wdir, fi_wraj, fi_vis, fi_qnh, fs_mesg, f_bdc):
    """
    write metsar data to BDC

    :param fdt_gmt (datetime): date GMT
    :param fs_icao_code (str):
    :param fi_tabs (int): temperature
    :param fi_tpo (int): dewpoint
    :param fi_wvel (int): wind vel
    :param fi_wdir (int): wind dir
    :param fi_wraj (int): wind gust
    :param fi_vis (int): visibility
    :param fi_qnh (int): QNH
    :param fs_mesg (str): METAR from location
    :param f_bdc (conn): connection to BDC
    """
    # build date & time
    ldt_date = fdt_gmt.date()
    ldt_time = fdt_gmt.time()

    # make query
    ls_query = "insert into metsar_b(sigla_aerodromo, dt_metsar, hr_metsar, temperatura_ar, " \
               "temperatura_po, velocidade_vento, direcao_vento, rajada, visibilidade, " \
               "qnh, mensagem) values ('{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, " \
               "'{}')".format(fs_icao_code, ldt_date, ldt_time,
               fi_tabs if fi_tabs is not None else "null",
               fi_tpo if fi_tpo is not None else "null",
               fi_wvel if fi_wvel is not None else "null",
               fi_wdir if fi_wdir is not None else "null",
               fi_wraj if fi_wraj is not None else "null",
               fi_vis if fi_vis is not None else "null",
               fi_qnh if fi_qnh is not None else "null",
               fs_mesg)

    # write to BDC
    bdc_write(f_bdc, ls_query)

# ---------------------------------------------------------------------------------------------
def bdc_write(f_bdc, fs_query):
    """
    execute query on BDC
    """
    # create cursor
    l_cursor = f_bdc.cursor()
    assert l_cursor

    # execute query
    l_cursor.execute(fs_query)

    # commit
    f_bdc.commit()

# < the end >----------------------------------------------------------------------------------

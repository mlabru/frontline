# -*- coding: utf-8 -*-
"""
fl_send_bdc

2021/jul  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import datetime
import logging

# postgres
import psycopg2

# local
import fl_defs as df

# < defines >--------------------------------------------------------------------------------------

# DB connection
DS_HOST = "172.18.30.21"
DS_USER = "dwclimatologia"
DS_PASS = "dwclimatologia"
DS_DB = "dw_climatologia"

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# -------------------------------------------------------------------------------------------------
def bdc_connect(fs_user=DS_USER, fs_pass=DS_PASS, fs_host=DS_HOST, fs_db=DS_DB):
    """
    connect to BDC
    """
    # create connection
    l_bdc = psycopg2.connect(host=fs_host, database=fs_db, user=fs_user, password=fs_pass)
    assert l_bdc

    # return
    return l_bdc

# -------------------------------------------------------------------------------------------------
def bdc_save_metaf(fo_metaf, f_bdc):
    """
    write metaf data to BDC
    """
    # convert date & time
    ldt_today = datetime.date.today()

    # metaf date
    ls_day = fo_metaf.s_forecast_time[:2]
    ls_hour = fo_metaf.s_forecast_time[2:4]
    ls_min = fo_metaf.s_forecast_time[4:6]

    # build date & time
    ldt_date = datetime.date(ldt_today.year, ldt_today.month, int(ls_day))
    ldt_time = datetime.time(int(ls_hour), int(ls_min))

    # have visibility ?
    if fo_metaf.i_visibility is None:
        # visibility
        li_vis = 99999 if fo_metaf.v_cavok else -99999

    # senão, have visibility
    else:
        # visibility
        li_vis = fo_metaf.i_visibility

    # make query
    ls_query = "insert into metaf(sigla_aerodromo, dt_metaf, hr_metaf, temperatura_ar, " \
               "temperatura_po, velocidade_vento, direcao_vento, rajada, visibilidade, " \
               "qnh) values ('{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {})".format(
               fo_metaf.s_icao_code,
               ldt_date,
               ldt_time,
               fo_metaf.i_temperature_c if fo_metaf.i_temperature_c is not None else "null",
               fo_metaf.i_dewpoint_c if fo_metaf.i_dewpoint_c is not None else "null",
               fo_metaf.i_wind_vel_kt if fo_metaf.i_wind_vel_kt is not None else "null",
               fo_metaf.i_wind_dir if fo_metaf.i_wind_dir is not None else "null",
               fo_metaf.i_gust_kt if fo_metaf.i_gust_kt is not None else "null",
               li_vis,
               fo_metaf.i_pressure_hpa if fo_metaf.i_pressure_hpa is not None else "null"
               )

    # write to BDC
    bdc_write(f_bdc, ls_query)
    M_LOG.info("save metaf: %s", str(ls_query))

# -------------------------------------------------------------------------------------------------
def bdc_save_metsar(fs_icao_code, fs_day, fs_time, fi_tabs, fi_tpo,
                    fi_wvel, fi_wdir, fi_wraj, fi_vis, fi_qnh, f_bdc):
    """
    write metsar data to BDC
    """
    # convert date & time
    ldt_today = datetime.date.today()

    # build date & time
    ldt_date = datetime.date(ldt_today.year, ldt_today.month, int(fs_day))
    ldt_time = datetime.time(int(fs_time[:2]), int(fs_time[2:]))

    # make query
    ls_query = "insert into metsar(sigla_aerodromo, dt_metsar, hr_metsar, temperatura_ar, " \
               "temperatura_po, velocidade_vento, direcao_vento, rajada, visibilidade, " \
               "qnh) values ('{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {})".format(
               fs_icao_code,
               ldt_date, ldt_time,
               fi_tabs, fi_tpo,
               fi_wvel, fi_wdir, fi_wraj,
               fi_vis,
               fi_qnh,
               )

    # write to BDC
    bdc_write(f_bdc, ls_query)
    M_LOG.info("save metsar: %s", str(ls_query))

# -------------------------------------------------------------------------------------------------
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

# < the end >--------------------------------------------------------------------------------------

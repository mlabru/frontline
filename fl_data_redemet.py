# -*- coding: utf-8 -*-
"""
fl_data_redemet

2021/jul  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import json
import requests

# local
import fl_defs as df
import fl_metar_parser as mp

# < defines >--------------------------------------------------------------------------------------

# REDEMET
DS_REDEMET_URL = "https://api-redemet.decea.mil.br/mensagens/metar/{2}?api_key={0}&data_ini={1}&data_fim={1}"

# aeródromos
DS_AERODROMOS_URL = "https://api-redemet.decea.mil.br/aerodromos/?api_key={0}&pais=Brasil"

# aeródromos dictionary
DDCT_AERODROMOS = {}

# -------------------------------------------------------------------------------------------------
import imp

# open secrets files
with open(".hidden/secrets.py", "rb") as lfh:
    # import module
    hs = imp.load_module(".hidden", lfh, ".hidden/secrets", (".py", "rb", imp.PY_SOURCE))

# request de dados de aeródromos
l_response = requests.get(DS_AERODROMOS_URL.format(hs.DS_REDEMET_KEY))

# ok ?
if 200 == l_response.status_code:
    # aeródromos data
    ldct_data = json.loads(l_response.text)

    # flag status
    lv_status = ldct_data.get("status", None)

    if lv_status is not None and lv_status:
        # aeródromos list
        llst_aerodromos = ldct_data.get("data", None)

        # for all aerodromos...
        for ldct_aerodromo in llst_aerodromos:
            # ICAO code
            ls_icao = ldct_aerodromo.get("cod", None)

            if ls_icao is not None:
                # lat
                ls_lat = ldct_aerodromo.get("lat_dec", None)
                lf_lat = float(ls_lat) if ls_lat else 0.
                # lng
                ls_lng = ldct_aerodromo.get("lon_dec", None)
                lf_lng = float(ls_lng) if ls_lng else 0.

                # save aeródromo
                DDCT_AERODROMOS[ls_icao.strip().upper()] = (lf_lat, lf_lng)

# -------------------------------------------------------------------------------------------------
def redemet_get_location(fs_date, fs_location):
    """
    recupera o METAR da localidade

    :param fs_date (str): date to search
    :param fs_location (str): location

    :returns: location data if found else None
    """
    # request de dados horários da estação
    l_response = requests.get(DS_REDEMET_URL.format(hs.DS_REDEMET_KEY, fs_date, fs_location))

    # ok ?
    if 200 == l_response.status_code:
        # REDEMET station data
        ldct_data = json.loads(l_response.text)

        if ldct_data:
            # data
            ldct_data = ldct_data.get("data", None)

            if ldct_data:
                # locations list
                llst_data = ldct_data.get("data", None)

                if llst_data:
                    # location data
                    ldct_loc = llst_data[0]

                    if ldct_loc:
                        # location METAR
                        ls_mens = ldct_loc.get("mens", None)

                        if ls_mens:
                            # parse METAR
                            return mp.metar_parse(ls_mens.strip())

    # return error
    return None

# < the end >--------------------------------------------------------------------------------------

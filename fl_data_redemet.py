# -*- coding: utf-8 -*-
"""
fl_data_redemet

2021/jul  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import json
import logging
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

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# -------------------------------------------------------------------------------------------------
import imp

# open secrets files
with open(".hidden/secrets.py", "rb") as lfh:
    # import module
    G_HS = imp.load_module(".hidden", lfh, ".hidden/secrets", (".py", "rb", imp.PY_SOURCE))

# request de dados de aeródromos
l_response = requests.get(DS_AERODROMOS_URL.format(G_HS.DS_REDEMET_KEY))

# ok ?
if 200 == l_response.status_code:
    try:
        # decode REDEMET station data
        ldct_data = json.loads(l_response.text)

    # em caso de erro...
    except json.decoder.JSONDecodeError as l_err:
        # logger
        M_LOG.error("REDEMET aerodromes list decoding error: %s.", l_err)

        # quit
        ldct_data = {}

    # logger
    M_LOG.debug("REDEMET aerodromes data: %s.", str(ldct_data))

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

# senão,...
else:
    # logger
    M_LOG.error("REDEMET aerodromes list empty or not found. Code: %s", str(l_response.status_code))

# -------------------------------------------------------------------------------------------------
def redemet_get_location(fs_date, fs_location):
    """
    recupera o METAR da localidade

    :param fs_date (str): date to search
    :param fs_location (str): location

    :returns: location data if found else None
    """
    # request de dados horários da estação
    l_response = requests.get(DS_REDEMET_URL.format(G_HS.DS_REDEMET_KEY, fs_date, fs_location))

    # ok ?
    if 200 == l_response.status_code:
        try:
            # decode REDEMET station data
            ldct_station = json.loads(l_response.text)

        # em caso de erro...
        except json.decoder.JSONDecodeError as l_err:
            # logger
            M_LOG.error("REDEMET station data decoding error: %s.", str(l_err))
            # quit
            ldct_station = {}
            
        # flag status
        lv_status = ldct_station.get("status", None)

        if lv_status is not None and lv_status:
            # station data
            ldct_data = ldct_station.get("data", None)

            if ldct_data:
                # metars list
                llst_metars = ldct_data.get("data", None)

                if llst_metars:
                    # location data
                    ldct_location = llst_metars[0]

                    if ldct_location:
                        # location METAR
                        ls_mens = ldct_location.get("mens", None)

                        if ls_mens:
                            # parse METAR
                            return mp.metar_parse(ls_mens.strip())

                        # senão, no ls_mens
                        else:
                            # logger
                            M_LOG.error("REDEMET station data for %s have no mens field: %s", str(fs_location), str(ldct_location))

                    # senão, no ldct_location
                    else:
                        # logger
                        M_LOG.error("REDEMET station data for %s have no/empty location METAR: %s", str(fs_location), str(llst_metars))
                                
                # senão, no llst_metars
                else:
                    # logger
                    M_LOG.error("REDEMET station data for %s have no/empty METARs list: %s", str(fs_location), str(ldct_data))
                            
            # senão, no ldct_data
            else:
                # logger
                M_LOG.error("REDEMET station data for %s have no data field: %s", str(fs_location), str(ldct_station))

        # senão, no lv_status
        else:
            # logger
            M_LOG.error("REDEMET station data for %s status error: %s", str(fs_location), str(ldct_station))

    # senão,...
    else:
        # logger
        M_LOG.error("REDEMET station data for %s not found. Code: %s", str(fs_location), str(l_response.status_code))

    # return error
    return None

# < the end >--------------------------------------------------------------------------------------

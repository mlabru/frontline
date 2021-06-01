# -*- coding: utf-8 -*-
"""
fl_icao_ll

2021/may  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import json
import logging
import math
import requests

# local
import fl_defs as df

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# -------------------------------------------------------------------------------------------------
#
## request de dados de estações manuais
#response = requests.get("https://apitempo.inmet.gov.br/estacoes/M")
#
## ok ?
#if 200 == response.status_code:
#    # lista de estações manuais
#    llst_stations = json.loads(response.text)
#
#    # for all stations...
#    for ldct_station in llst_stations:
#        # exists altitude ?
#        if ldct_station["VL_ALTITUDE"] is not None:
#            # station lat/lng/alt
#            df.DDCT_STATIONS_LL[ldct_station["CD_ESTACAO"]] = (float(ldct_station["VL_LATITUDE"]),
#                                                               float(ldct_station["VL_LONGITUDE"]),
#                                                               float(ldct_station["VL_ALTITUDE"]))
#
#        # senão,...
#        else:
#            # station lat/lng
#            df.DDCT_STATIONS_LL[ldct_station["CD_ESTACAO"]] = (float(ldct_station["VL_LATITUDE"]),
#                                                               float(ldct_station["VL_LONGITUDE"]), 0.)

# request de dados de estações tomáticas
response = requests.get("https://apitempo.inmet.gov.br/estacoes/T")

# ok ?
if 200 == response.status_code:
    # lista de estações tomáticas
    llst_stations = json.loads(response.text)

    # for all stations...
    for ldct_station in llst_stations:
        # flag operacional
        ls_oper = ldct_station.get("CD_SITUACAO", None)

        # operacional ?
        if ls_oper is None or ("Operante" != ls_oper):
            # next
            continue

        # exists altitude ?
        if ldct_station["VL_ALTITUDE"] is not None:
            # station lat/lng/alt
            df.DDCT_STATIONS_LL[ldct_station["CD_ESTACAO"]] = (float(ldct_station["VL_LATITUDE"]),
                                                               float(ldct_station["VL_LONGITUDE"]),
                                                               float(ldct_station["VL_ALTITUDE"]))

        # senão,...
        else:
            # station lat/lng
            df.DDCT_STATIONS_LL[ldct_station["CD_ESTACAO"]] = (float(ldct_station["VL_LATITUDE"]),
                                                               float(ldct_station["VL_LONGITUDE"]), 0.)

# -------------------------------------------------------------------------------------------------
def find_near_station(fs_icao_code):
    """
    find near station from ICAO Code

    :param fs_icao_code (str): aerodrome ICAO Code
    """
    # aerodrome lat/lng
    lt_ll = df.DDCT_ICAO_LL.get(fs_icao_code, None)

    # ok ?
    if lt_ll is None:
        # logger
        M_LOG.error("ICAO Code %s not found in table.", fs_icao_code)
        # return
        return None, None

    # station
    ls_station = None
    # altitude
    lf_altitude = None

    # distance
    lf_dist = float("inf")
    # aerodrome lat/lng
    lf_lat, lf_lng = lt_ll

    # for all stations...
    for lkey, lval in df.DDCT_STATIONS_LL.items():
        # great circle distance
        lf_haver = haversine(lf_lat, lf_lng, lval[0], lval[1])

        # found nearest ?
        if lf_haver < lf_dist:
            # new near distance
            lf_dist = lf_haver
            # save station
            ls_station = lkey
            # altitude
            lf_altitude = lval[2]

    # return nearest station
    return ls_station, lf_altitude

# -------------------------------------------------------------------------------------------------
def haversine(ff_lat_1, ff_lng_1, ff_lat_2, ff_lng_2):
    """
    calculate the great circle distance between two points on the earth (specified in decimal degrees)

    :param ff_lat_1 (float): latitude 1
    :param ff_lng_1 (float): longitude 1
    :param ff_lat_2 (float): latitude 2
    :param ff_lng_2 (float): longitude 2
    """
    # convert decimal degrees to radians
    ff_lat_1, ff_lng_1, ff_lat_2, ff_lng_2 = map(math.radians, [ff_lat_1, ff_lng_1, ff_lat_2, ff_lng_2])

    # deltas
    lf_dlat = ff_lat_2 - ff_lat_1
    lf_dlng = ff_lng_2 - ff_lng_1

    # haversine formula
    lf_a = math.sin(lf_dlat / 2) ** 2 + math.cos(ff_lat_1) * math.cos(ff_lat_2) * math.sin(lf_dlng / 2) ** 2

    # return distance
    return 2 * df.DI_RADIUS * math.asin(math.sqrt(lf_a))

# < the end >--------------------------------------------------------------------------------------

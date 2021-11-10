# -*- coding: utf-8 -*-
"""
fl_icao_ll

2021/may  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import functools
import json
import logging
import math
import requests

# local
import fl_defs as df

# < defines >--------------------------------------------------------------------------------------

# maximum distance (km)
DI_MAX_DIST = 50

# ICAO Code lat/lng dictionary
DDCT_ICAO_LL = {"SBAA": (-8.348611111111111,  -49.303055),
                "SBAE": (-22.157777777777778, -49.068335),
                "SBAQ": (-21.805400451204797, -48.13897953190799),
                "SBAU": (-21.136305462661042, -50.42620925959953),
                "SBAX": (-19.560555555555556, -46.965556),
                "SBBG": (-31.390833333333333, -54.109724),
                "SBCH": (-27.131898804314726, -52.659896787113155),
                "SBCI": (-7.320555555555555,  -47.458611),
                "SBCX": (-29.189459318951368, -51.158922352236885),
                "SBDB": (-22.178121614149024, -51.41647160121517),
                "SBEK": (-6.235277777777778,  -57.775833),
                "SBGV": (-18.896944444444443, -41.986114),
                "SBGW": (-22.791666666666668, -45.204445),
                "SBIC": (-3.126388888888889,  -58.481667),
                "SBIP": (-19.470555555555553, -42.488055),
                "SBJA": (-28.676642915247406, -49.06537950666578),
                "SBJE": (-2.901904541564605,  -40.3287859757039),
                "SBJI": (-10.870555555555557, -61.846667),
                "SBKP": (-23.006944444444443, -47.134444),
                "SBLE": (-12.482222222222223, -41.276946),
                "SBLJ": (-27.78222222,        -50.281667),
                "SBLP": (-13.261388888888888, -43.4075),
                "SBMT": (-23.506666666666668, -46.633889),
                "SBMY": (-5.816944444444444,  -61.283889),
                "SBNM": (-28.28016736573942,  -54.16959799741611),
                "SBPF": (-28.24527777777778,  -52.328615),
                "SBPO": (-26.044445154154392, -51.7298125376385),
                "SBRD": (-16.58823576001801,  -54.72137721609497),
                "SBSJ": (-23.228888888888886, -45.871111),
                "SBSO": (-12.479771888439883, -55.67480161613318),
                "SBSP": (-23.62611111111111,  -46.656384),
                "SBTG": (-20.7519836888291,   -51.68242143452621),
                "SBTK": (-8.154722222222222,  -70.782778),
                "SBVC": (-14.91029371086807,  -40.9170599565889),
                "SBVG": (-21.58888888888889,  -45.473336),
                "SBYS": (-21.984444444444446, -47.344166),
                "SDAG": (-22.975277777777777, -44.307222),
                "SDIY": (-12.200555555555555, -38.900556),
                "SNBR": (-12.075564660517104, -45.010320793688656),
                "SNBV": (-2.5234654216848043, -47.5200471320579),
                "SNDV": (-20.181944444444447, -44.87),
                "SNGI": (-14.208055555555555, -42.746111),
                "SNHS": (-8.061388888888889,  -38.328615),
                "SNPD": (-18.672222222222224, -46.491389),
                "SNTF": (-17.524444444444445, -39.668333),
                "SNZR": (-17.243055555555557, -46.881389),
                "SSGG": (-25.38572234448335,  -51.51928880037018),
                "SSKW": (-11.489001366808235, -61.44861489760928),
                "SSUM": (-23.799166666666668, -53.313888),
                "SWEI": (-6.637499999999999,  -69.883054),
                "SWGN": (-7.2283333333333335, -48.240835),
                "SWKO": (-4.133888888888889,  -63.131111),
                "SWLC": (-17.834722222222222, -50.956111),
                "SWPI": (-2.6694444444444443, -56.771111),
                "SBGR": (-23.435556,          -46.473056),
                "SNVB": (-13.296389,          -38.9925)}

# stations lat/lng dictionary
DDCT_STATIONS_LL = {}

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# -------------------------------------------------------------------------------------------------
# request de dados de estações "tomáticas"
M_RESPONSE = requests.get("https://apitempo.inmet.gov.br/estacoes/T")

# ok ?
if 200 == M_RESPONSE.status_code:
    try:
        # lista de estações tomáticas
        MLST_STATIONS = json.loads(M_RESPONSE.text)

    # em caso de erro...
    except json.decoder.JSONDecodeError as M_ERR:
        # logger
        M_LOG.error("INMET station data decoding error: %s", str(M_ERR))

        # quit
        MLST_STATIONS = []
   
    # for all stations...
    for MDCT_STATION in MLST_STATIONS:
        # flag operacional
        MS_OPER = MDCT_STATION.get("CD_SITUACAO", None)

        # operacional ?
        if MS_OPER is None or ("Operante" != MS_OPER):
            # next
            continue

        # exists altitude ?
        if MDCT_STATION["VL_ALTITUDE"] is not None:
            # station lat/lng/alt
            DDCT_STATIONS_LL[MDCT_STATION["CD_ESTACAO"]] = (float(MDCT_STATION["VL_LATITUDE"]),
                                                            float(MDCT_STATION["VL_LONGITUDE"]),
                                                            float(MDCT_STATION["VL_ALTITUDE"]))

        # senão,...
        else:
            # station lat/lng/0
            DDCT_STATIONS_LL[MDCT_STATION["CD_ESTACAO"]] = (float(MDCT_STATION["VL_LATITUDE"]),
                                                            float(MDCT_STATION["VL_LONGITUDE"]), 0.)

# senão,...
else:
    # logger
    M_LOG.error("INMET automatic stations data not found. Code: %s", str(M_RESPONSE.status_code))

# -------------------------------------------------------------------------------------------------
@functools.lru_cache(maxsize=128)
def find_near_station(fs_icao_code):
    """
    find near station from ICAO Code

    :param fs_icao_code (str): aerodrome ICAO Code
    """
    # aerodrome lat/lng
    lt_ll = DDCT_ICAO_LL.get(fs_icao_code, None)

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
    for lkey, lval in DDCT_STATIONS_LL.items():
        # great circle distance
        lf_haver = _haversine(lf_lat, lf_lng, lval[0], lval[1])

        # found nearest ?
        if lf_haver < lf_dist:
            # new near distance
            lf_dist = lf_haver
            # save station
            ls_station = lkey
            # altitude
            lf_altitude = lval[2]

    # logger
    M_LOG.warning("Near station of %s is %s @ dst: %6.2f(km) alt: %6.2f(m)", fs_icao_code, ls_station, lf_dist, lf_altitude)

    # in distance constraint ?
    if lf_dist > DI_MAX_DIST:
        # logger
        M_LOG.warning("Near station too far: %s -> %s (%6.2f km).", str(fs_icao_code), str(ls_station), lf_dist)
        # return error
        return None, None
        
    # return nearest station
    return ls_station, lf_altitude

# -------------------------------------------------------------------------------------------------
def _haversine(ff_lat_1, ff_lng_1, ff_lat_2, ff_lng_2):
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

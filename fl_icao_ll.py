# -*- coding: utf-8 -*-
"""
fl_icao_ll

2021.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import functools
import json
import logging
import math
import requests

# local
import fl_defs as df

# < constants >--------------------------------------------------------------------------------

# maximum distance (km)
DI_MAX_DIST = 50

# ICAO Code lat/lng dictionary
DDCT_ICAO_LL = {"SBAA": (-8.348611, -49.303056),
                "SBAC": (-4.568611111, -37.80472222),
                "SBAE": (-22.15, -49.06),
                "SBAF": (-22.87, -43.38),
                "SBAN": (-16.23, -48.97),
                "SBAR": (-10.98527778, -37.07333333),
                "SBAT": (-9.866388889, -56.105),
                "SBAX": (-19.56, -46.96),
                "SBAX": (-19.56, -46.97),
                "SBBE": (-1.384722222, -48.47888889),
                "SBBG": (-31.39, -54.1),
                "SBBH": (-19.85, -43.95),
                "SBBI": (-25.4, -49.23),
                "SBBP": (-22.97, -46.53),
                "SBBR": (-15.87, -47.91),
                "SBBU": (-22.34, -49.05),
                "SBBV": ( 2.841388889, -60.69222222),
                "SBBW": (-15.86, -52.38),
                "SBCA": (-25, -53.5),
                "SBCB": (-22.92, -42.07),
                "SBCC": (-9.333333333, -54.96472222),
                "SBCF": (-19.62, -43.97),
                "SBCG": (-20.46, -54.67),
                "SBCH": (-27.13, -52.66),
                "SBCI": (-7.320556, -47.458611),
                "SBCJ": (-6.115277778, -50.00138889),
                "SBCN": (-17.72, -48.61),
                "SBCO": (-29.94, -51.14),
                "SBCP": (-21.7, -41.3),
                "SBCR": (-19.01, -57.67),
                "SBCT": (-25.53, -49.17),
                "SBCX": (-29.19, -51.18),
                "SBCY": (-15.65, -56.11),
                "SBCZ": (-7.599444444, -72.76944444),
                "SBDB": (-21.24, -56.4525),
                "SBDN": (-22.17, -51.41),
                "SBDO": (-22.2, -54.92),
                "SBEG": (-3.041111111, -60.05055556),
                "SBEK": (-6.24, -57.78),
                "SBEN": (-22.7, -40.693056),
                "SBES": (-22.81, -42.09),
                "SBFI": (-25.6, -54.48),
                "SBFL": (-27.67, -48.55),
                "SBFN": (-3.854722, -32.428333),
                "SBFZ": (-3.775833333, -38.53222222),
                "SBGL": (-22.8131, -43.249),
                "SBGO": (-16.63, -49.22),
                "SBGR": (-23.43, -46.66),
                "SBGV": (-18.89, -41.98),
                "SBGV": (-18.89, -41.986111),
                "SBGW": (-22.79, -45.2),
                "SBHT": (-3.250833333, -52.25222222),
                "SBIC": (-3.13, -58.48),
                "SBIH": (-4.242222222, -56.00083333),
                "SBIL": (-14.81, -39.03),
                "SBIP": (-19.47, -42.488056),
                "SBIZ": (-5.530555556, -47.45833333),
                "SBJA": (-28.67, -49.06),
                "SBJD": (-23.18, -46.94),
                "SBJE": (-2.9, -40.32),
                "SBJI": (-10.870556, -61.846667),
                "SBJP": (-7.148333333, -34.95027778),
                "SBJR": (-22.98, -43.37),
                "SBJU": (-7.219166667, -39.26944444),
                "SBJV": (-26.22, -48.79),
                "SBKG": (-7.269166667, -35.895),
                "SBKP": (-23.01, -47.13),
                "SBLB": (-22.1, -39.916944),
                "SBLE": (-12.482222, -41.276944),
                "SBLJ": (-27.78, -50.28),
                "SBLO": (-23.33, -51.13),
                "SBLP": (-13.26, -43.41),
                "SBMA": (-5.368055556, -49.13805556),
                "SBME": (-22.34, -41.76),
                "SBMG": (-22.34, -41.76),
                "SBMK": (-16.7, -43.82),
                "SBML": (-22.19, -49.92),
                "SBMM": (-22.35, -40.090278),
                "SBMN": (-3.145833333, -59.985),
                "SBMO": (-9.510833333, -35.79166667),
                "SBMQ": ( 0.050833333, -51.07027778),
                "SBMT": (-23.51, -46.63),
                "SBMT": (-23.5, -46.63),
                "SBMY": (-5.816944, -61.283889),
                "SBNF": (-26.87, -48.65),
                "SBNM": (-28.28, -54.168333),
                "SBNT": (-5.908333333, -35.24916667),
                "SBOI": ( 3.861388889, -51.79611111),
                "SBPA": (-29.99, -51.17),
                "SBPB": (-2.893888889, -41.73027778),
                "SBPF": (-28.24, -52.32),
                "SBPF": (-28.25, -52.33),
                "SBPG": (-25.18, -50.14),
                "SBPJ": (-10.29, -48.35777778),
                "SBPK": (-31.71, -52.33),
                "SBPL": (-9.3675, -40.56361111),
                "SBPP": (-22.54, -55.7),
                "SBPS": (-16.43, -39.08),
                "SBPV": (-8.713611111, -63.90277778),
                "SBRB": (-9.868333333, -67.89805556),
                "SBRD": (-16.58, -54.72),
                "SBRF": (-8.126388889, -34.92277778),
                "SBRJ": (-22.91, -43.16),
                "SBRP": (-21.13, -47.77),
                "SBSC": (-22.93, -43.71),
                "SBSG": (-5.768888889, -35.36638889),
                "SBSJ": (-23.23, -45.87),
                "SBSL": (-2.586944444, -44.23611111),
                "SBSM": (-29.71, -53.69),
                "SBSN": (-2.424722222, -54.78583333),
                "SBSO": (-12.479771, -55.674801),
                "SBSP": (-23.62, -46.656389),
                "SBSR": (-20.81, -49.4),
                "SBST": (-23.92, -46.29),
                "SBSV": (-12.90861111, -38.3225),
                "SBTA": (-23.03, -45.51),
                "SBTD": (-24.68, -53.69),
                "SBTE": (-5.060555556, -42.82444444),
                "SBTF": (-3.380277778, -64.72527778),
                "SBTG": (-20.75, -51.68),
                "SBTK": (-8.154722, -70.782778),
                "SBTT": (-4.250555556, -69.93777778),
                "SBTU": (-3.776944, -49.719722),
                "SBUA": (-0.148055556, -66.98583333),
                "SBUG": (-29.78, -57.03),
                "SBUL": (-18.88, -48.22),
                "SBUR": (-19.76, -47.96),
                "SBVC": (-14.910293, -40.917059),
                "SBVC": (-14.91, -40.91),
                "SBVG": (-21.59, -45.47),
                "SBVH": (-12.69416667, -60.09722222),
                "SBVT": (-20.25, -40.28),
                "SBYS": (-21.98, -47.34),
                "SBZM": (-21.51, -43.17),
                "SDAG": (-22.97, -44.307222),
                "SDAG": (-22.98, -44.31),
                "SDIY": (-12.200556, -38.900556),
                "SNBR": (-12.079167, -45.009444),
                "SNDV": (-20.18, -44.87),
                "SNGI": (-14.208056, -42.746111),
                "SNHS": (-8.061389, -38.328611),
                "SNPD": (-18.67, -46.491389),
                "SNRU": (-8.284444, -36.010833),
                "SNTF": (-17.52, -39.668333),
                "SNVB": (-2.5234654, -47.520047),
                "SNZR": (-17.24, -46.881389),
                "SSKW": (-11.489, -61.44861),
                "SSUM": (-23.79, -53.313889),
                "SWEI": (-6.6375, -69.883056),
                "SWGN": (-7.228333, -48.240833),
                "SWKO": (-4.133889, -63.131111),
                "SWLC": (-17.83, -50.956111),
                "SWPI": (-2.669444, -56.771111)}

# stations lat/lng dictionary
DDCT_STATIONS_LL = {}

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------------------------
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
    M_LOG.warning("Near station of %s is %s @ dst: %6.2f(km) alt: %6.2f(m)",
                  fs_icao_code, ls_station, lf_dist, lf_altitude)

    # in distance constraint ?
    if lf_dist > DI_MAX_DIST:
        # logger
        M_LOG.warning("Near station too far: %s -> %s (%6.2f km).",
                      str(fs_icao_code), str(ls_station), lf_dist)
        # return error
        return None, None
        
    # return nearest station
    return ls_station, lf_altitude

# ---------------------------------------------------------------------------------------------
def _haversine(ff_lat_1, ff_lng_1, ff_lat_2, ff_lng_2):
    """
    calculate the great circle distance between two points on the earth (specified in decimal degrees)

    :param ff_lat_1 (float): latitude 1
    :param ff_lng_1 (float): longitude 1
    :param ff_lat_2 (float): latitude 2
    :param ff_lng_2 (float): longitude 2
    """
    # convert decimal degrees to radians
    ff_lat_1, ff_lng_1, ff_lat_2, ff_lng_2 = map(math.radians, [ff_lat_1, ff_lng_1,
                                                                ff_lat_2, ff_lng_2])
    # deltas
    lf_dlat = ff_lat_2 - ff_lat_1
    lf_dlng = ff_lng_2 - ff_lng_1

    # haversine formula
    lf_a = math.sin(lf_dlat / 2) ** 2 + \
           math.cos(ff_lat_1) * math.cos(ff_lat_2) * math.sin(lf_dlng / 2) ** 2

    # return distance
    return 2 * df.DI_RADIUS * math.asin(math.sqrt(lf_a))

# < the end >----------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
"""
fl_defs

2021/may  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# < defines >--------------------------------------------------------------------------------------

# logging level
DI_LOG_LEVEL = logging.WARNING

# GMT is ahead of us
DI_DIFF_GMT = 3

# radius of earth in kilometers. Use 3956 for miles
DI_RADIUS = 6371


# ft -> m
DF_FT2M = 0.3048

# kt -> m/s
DF_KT2MPS = 0.514444444

# m/s -> kt
DF_MPS2KT = 1.943844492


# frontlines directory
DS_OUT_DIR = "frontlines"

# carrapatos directory
DS_TICKS_DIR = "carrapatos"


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

# weahter state messages
DDCT_WEATHER = {"DZ":     "Drizzle.",
                "-DZ":    "Light drizzle.",
                "+DZ":    "Heavy drizzle.",
                "RA":     "Rain.",
                "-RA":    "Light rain.",
                "+RA":    "Heavy rain.",
                "SN":     "Snow.",
                "-SN":    "Light snow.",
                "+SN":    "Heavy snow.",
                "SG":     "Snow grains.",
                "-SG":    "Light snow grains.",
                "+SG":    "Heavy snow grains.",
                "PL":     "Ice pellets.",
                "-PL":    "Light Ice pellets.",
                "+PL":    "Heavy Ice pellets.",
                "GS":     "Samll hail.",
                "-GS":    "Light Samll hail.",
                "+GS":    "Heavy Samll hail.",
                "GR":     "Hail.",
                "-GR":    "Light hail.",
                "+GR":    "Heavy hail.",
                "RASN":   "Rain and snow.",
                "-RASN":  "Light rain and snow.",
                "+RASN":  "Heavy rain and snow.",
                "SNRA":   "Snow and rain.",
                "-SNRA":  "Light snow and rain.",
                "+SNRA":  "Heavy snow and rain.",
                "SHSN":   "Snow showers.",
                "-SHSN":  "Light snow showers.",
                "+SHSN":  "Heavy snow showers.",
                "SHRA":   "Rain showers.",
                "-SHRA":  "Light rain showers.",
                "+SHRA":  "Heavy rain showers.",
                "SHGR":   "Hail showers.",
                "-SHGR":  "Light hail showers.",
                "+SHGR":  "Heavy hail showers.",
                "FZRA":   "Freezing rain.",
                "-FZRA":  "Light freezing rain.",
                "+FZRA":  "Heavy freezing rain.",
                "FZDZ":   "Freezing drizzle.",
                "-FZDZ":  "Light freezing drizzle.",
                "+FZDZ":  "Heavy freezing drizzle.",
                "TSRA":   "Thunderstorm with rain.",
                "-TSRA":  "Light thunderstorm with rain.",
                "+TSRA":  "Heavy thunderstorm with rain.",
                "TSGR":   "Thunderstorm with hail.",
                "-TSGR":  "Light thunderstorm with hail.",
                "+TSGR":  "Heavy thunderstorm with hail.",
                "TSGS:":  "Thunderstorm with small hail.",
                "-TSGS:": "Light thunderstorm with small hail.",
                "+TSGS:": "Heavy thunderstorm with small hail.",
                "TSSN:":  "Thunderstorm with snow.",
                "-TSSN:": "Light thunderstorm with snow.",
                "+TSSN:": "Heavy thunderstorm with snow.",
                "DS:":    "Duststorm.",
                "-DS:":   "Light duststorm.",
                "+DS:":   "Heavy duststorm.",
                "SS:":    "Sandstorm.",
                "-SS:":   "Light sandstorm.",
                "+SS:":   "Heavy sandstorm.",
                "FG:":    "Fog.",
                "FZFG:":  "Freezing fog.",
                "VCFG:":  "Fog in vicinity.",
                "MIFG:":  "Shallow fog.",
                "PRFG:":  "Aerodrome partially covered by fog.",
                "BCFG:":  "Fog patches.",
                "BR:":    "Mist.",
                "HZ:":    "Haze.",
                "FU:":    "Smoke.",
                "DRSN:":  "Low drifting snow.",
                "DRSA:":  "Low drifting sand.",
                "DRDU:":  "Low drifting dust.",
                "DU:":    "Dust.",
                "BLSN:":  "Blowing snow.",
                "BLDU:":  "Blowing dust.",
                "SQ:":    "Squall.",
                "IC:":    "Ice crystals.",
                "TS:":    "Thunderstorm.",
                "VCTS:":  "Thunderstorm in vicinity.",
                "VA:":    "Volcanic ash."}

# < the end >--------------------------------------------------------------------------------------

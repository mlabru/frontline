# -*- coding: utf-8 -*-
"""
fl_defs

2021/may  1.0  mlabru  initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# < defines >--------------------------------------------------------------------------------------

# logging level
DI_LOG_LEVEL = logging.WARNING
# DI_LOG_LEVEL = logging.DEBUG

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


# METARs directory
DS_MET_DIR = "metars"

# frontlines directory
DS_OUT_DIR = "frontlines"

# carrapatos directory
DS_TICKS_DIR = "carrapatos"


# maximum visibility (CAVOK)
DI_VIS_CAVOK = 10000

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

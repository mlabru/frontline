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

# REDEMET API key
DS_REDEMET_KEY = "w70wXiIZBBMVFhBFS6ApwrC9x24ZU7T7RsdIbZ9f"

# REDEMET
DS_REDEMET_URL = "https://api-redemet.decea.mil.br/mensagens/metar/{2}?api_key={0}&data_ini={1}&data_fim={1}"

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# -------------------------------------------------------------------------------------------------
def redemet_get_location(fs_date, fs_location):
    """
    recupera o METAR da localidade

    :param fs_date (str): date to search
    :param fs_location (str): location

    :returns: location data if found else None
    """
    # request de dados horários da estação
    l_response = requests.get(DS_REDEMET_URL.format(DS_REDEMET_KEY, fs_date, fs_location))

    # ok ?
    if 200 == l_response.status_code:
        # REDEMET station data
        ldct_data = json.loads(l_response.text)
        M_LOG.debug("ldct_data: %s", ldct_data)

        if ldct_data:
            # data
            ldct_data = ldct_data.get("data", None)
            M_LOG.debug("ldct_data: %s", ldct_data)

            if ldct_data:
                # locations list
                llst_data = ldct_data.get("data", None)
                M_LOG.debug("llst_data: %s", llst_data)

                if llst_data:
                    # location data
                    ldct_loc = llst_data[0]
                    M_LOG.debug("ldct_loc: %s", ldct_loc)

                    if ldct_loc:
                        # location METAR
                        ls_mens = ldct_loc.get("mens", None)
                        M_LOG.debug("ls_mens: %s", ls_mens)

                        if ls_mens:
                            # parse METAR
                            return mp.metar_parse(ls_mens.strip())

    # return error
    return None

# < the end >--------------------------------------------------------------------------------------

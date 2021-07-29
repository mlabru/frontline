# -*- coding: utf-8 -*-
"""
fl_data_inmet

2021/jul  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import json
import logging
import requests

# local
import fl_defs as df

# < defines >--------------------------------------------------------------------------------------

# INMET
DS_INMET_URL = "https://apitempo.inmet.gov.br/estacao/{0}/{0}/{1}"

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# -------------------------------------------------------------------------------------------------
def inmet_get_location(fs_dia, fs_station):
    """
    recupera os dados da localidade
    """
    # request de dados horários da estação
    l_response = requests.get(DS_INMET_URL.format(fs_dia, fs_station))

    # ok ?
    if 200 == l_response.status_code:
        # return data
        return json.loads(l_response.text)

    # return error
    return None

# < the end >--------------------------------------------------------------------------------------

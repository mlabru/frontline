# -*- coding: utf-8 -*-
"""
fl_data_inmet

2021/jul  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import functools
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
@functools.lru_cache(maxsize=2048)
def inmet_get_location(fs_date, fs_station):
    """
    recupera os dados da localidade

    :param fs_date (str): date to search
    :param fs_station (str): station

    :returns: station data if found else None
    """
    # request de dados horários da estação
    l_response = requests.get(DS_INMET_URL.format(fs_date, fs_station))

    # ok ?
    if 200 == l_response.status_code:
        try:
            # decode data
            l_ans = json.loads(l_response.text)

            # return data
            return l_ans

        # em caso de erro...
        except JSONDecodeError as l_err:
            # logger
            M_LOG.error("JSON decoding error")

    # return error
    return None

# < the end >--------------------------------------------------------------------------------------

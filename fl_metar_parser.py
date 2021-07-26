# -*- coding: utf-8 -*-
"""
fl_metar_parser

2021/may  1.0  mlabru   initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import re

# local
import fl_defs as df

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# < SMetar >---------------------------------------------------------------------------------------

class SMetar:
    """
    string parsing of weather station
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_metar_data):
        """
        constructor
        """
        # metar data
        self._s_metar_data = fs_metar_data

        # cloudiness
        self._v_cavok = None
        self._v_nsc = None
        self._v_skc = None
        self._v_vv = None

        self._v_bkn = None
        self._f_bkn_m = None
        self._i_bkn_feet = None

        self._v_few = None
        self._f_few_m = None
        self._i_few_feet = None

        self._v_ovc = None
        self._f_ovc_m = None
        self._i_ovc_feet = None

        self._v_sct = None
        self._f_sct_m = None
        self._i_sct_feet = None

        # forecast time
        self._s_forecast_time = None

        # icao code
        self._s_icao_code = None

        # pressure
        self._i_pressure_hpa = None
        self._i_pressure_inhg = None

        # remarks
        self._v_a02 = None
        self._v_maint = None
        self._v_pwino = None

        # report type
        self._v_auto = None
        self._v_corr = None

        # temperature
        self._i_dewpoint_c = None
        self._i_dewpoint_f = None
        self._i_temperature_c = None
        self._i_temperature_f = None

        # trends
        self._v_becmg = None
        self._v_nosig = None
        self._v_tempo = None

        # visibility
        self._i_visibility = None

        # weather
        self._s_weather = None
        self._s_weather_text = None

        # wind type
        self._i_gust_kt = None
        self._i_gust_mps = None
        self._i_wind_dir = None
        self._i_wind_dir_max = None
        self._i_wind_dir_min = None
        self._i_wind_var_kt = None
        self._i_wind_var_mps = None
        self._i_wind_vel_kt = None
        self._i_wind_vel_mps = None

    # ---------------------------------------------------------------------------------------------
    def clouds_type(self):
        """
        determining the type of cloudiness
        """
        # search for type of cloudiness
        l_result = re.findall(r"SKC[0-9]{3}|NSC[0-9]{3}|FEW[0-9]{3}|SCT[0-9]{3}"
                              "|BKN[0-9]{3}|OVC[0-9]{3}|VV[0-9]{3}", self._s_metar_data)

        for ls_type_cloud in l_result:
            # skc ?
            if "SKC" == ls_type_cloud:
                # skc
                self._v_skc = True

                # logger
                # M_LOG.info("Clouds: Sky is clear.")

            # nsc ?
            if "NSC" == ls_type_cloud:
                # nsc
                self._v_nsc = True

                # logger
                # M_LOG.info("Clouds: No significant cloud clouds.")

            # few ?
            if "FEW" == ls_type_cloud[:-3]:
                # few
                self._i_few_feet = (int(ls_type_cloud[-3:]) * 100)
                self._f_few_m = round(self._i_few_feet * df.DF_FT2M, 2)
                # few
                self._v_few = True

                # logger
                # M_LOG.info("Clouds: Few clouds at %d feet (%f meter).", self._i_few_feet, self._f_few_m)

            # sct ?
            if "SCT" == ls_type_cloud[:-3]:
                # sct
                self._i_sct_feet = (int(ls_type_cloud[-3:]) * 100)
                self._f_sct_m = round(self._i_sct_feet * df.DF_FT2M, 2)
                # sct
                self._v_sct = True

                # logger
                # M_LOG.info("Clouds: Scattered clouds at %d feet (%f meter).", self._i_sct_feet, self._f_sct_m)

            # bkn ?
            if "BKN" == ls_type_cloud[:-3]:
                # bkn
                self._i_bkn_feet = (int(ls_type_cloud[-3:]) * 100)
                self._f_bkn_m = round(self._i_bkn_feet * df.DF_FT2M, 2)
                # pwino
                self._v_bkn = True

                # logger
                # M_LOG.info("Clouds: Broken clouds at %d feet (%f meter).", self._i_bkn_feet, self._f_bkn_m)

            # ovc ?
            if "OVC" == ls_type_cloud[:-3]:
                # ovc
                self._i_ovc_feet = (int(ls_type_cloud[-3:]) * 100)
                self._f_ovc_m = round(self._i_ovc_feet * df.DF_FT2M, 2)
                # ovc
                self._v_ovc = True

                # logger
                # M_LOG.info("Clouds: Overcast clouds at %d feet (%f meter).", self._i_ovc_feet, self._f_ovc_m)

            # vv ?
            if "VV" == ls_type_cloud[:-3]:
                # vv
                self._v_vv = True

                # logger
                # M_LOG.info("Clouds: Clouds cannot be seen because of fog or heavy precipitation.")

    # ---------------------------------------------------------------------------------------------
    def forecast_time(self):
        """
        search for the reporting time
        """

        # search for forecast time
        l_result = re.search(r"[0-9]{6}[Z]", self._s_metar_data)

        # forecast time
        self._s_forecast_time = str(l_result[0])

        # logger
        # M_LOG.info("Time issued: %s %s:%s.", l_result[0][:2], l_result[0][2:4], l_result[0][4:6])

    # ---------------------------------------------------------------------------------------------
    def icao_code(self):
        """
        ICAO Airport Index Search Method
        """
        # search for icao code
        l_result = re.search(r"[A-Z]{4}", self._s_metar_data)

        # icao code
        self._s_icao_code = str(l_result[0])

        # logger
        # M_LOG.info("Identifier: %s.", self._s_icao_code)

    # ---------------------------------------------------------------------------------------------
    def pressure(self):
        """
        pressure search method
        """
        # search for QNH (hPa)
        l_result = re.search(r"[Q][0-9]{4}", self._s_metar_data)

        if l_result:
            # pressure_(hpa)
            self._i_pressure_hpa = int(l_result[0][1:])

            # logger
            # M_LOG.info("Pressure: QNH %d hPa.", self._i_pressure_hpa)

        # search for QNH (inHg)
        l_result = re.search(r"[A][0-9]{4}", self._s_metar_data)

        if l_result:
            # pressure_(inHg)
            self._i_pressure_inhg = float(l_result[0][1:-2] + "." + l_result[0][3:])

            # logger
            # M_LOG.info("Pressure: Sea level pressure is %d inHg.", self._i_pressure_inhg)

    # ---------------------------------------------------------------------------------------------
    def remarks(self):
        """
        notes
        """
        # search for notes
        l_result = re.search(r"AO2", self._s_metar_data)

        if l_result:
            # a02
            self._v_a02 = True

            # logger
            # M_LOG.info("This station is automated with a precipitation discriminator (rain/snow) sensor.")

        # search for notes
        l_result = re.search(r"PWINO", self._s_metar_data)

        if l_result:
            # pwino
            self._v_pwino = True

            # logger
            # M_LOG.info("Precipitation identifier sensor not available.")

        # search for notes
        l_result = re.search(r"\$", self._s_metar_data)

        if l_result:
            # maint
            self._v_maint = True

            # logger
            # M_LOG.info("System needs maintance.")

    # ---------------------------------------------------------------------------------------------
    def report_type(self):
        """
        determining the type of report

        - AUTO - if it is formed by the machine
        - COR  - if it is a correction
        """
        # search for report type
        l_result = re.search(r"COR", self._s_metar_data)

        if l_result:
            # correction ?
            if "COR" == l_result[0]:
                # maint
                self._v_corr = True

                # logger
                # M_LOG.info("Report type: This is a correction report")

        # search for report type
        l_result = re.search(r"AUTO", self._s_metar_data)

        if l_result:
            # auto ?
            if "AUTO" == l_result[0]:
                # maint
                self._v_auto = True

                # logger
                # M_LOG.info("Report type: This is a fully automated report")

    # ---------------------------------------------------------------------------------------------
    def temperature(self):
        """
        find the temperature and dewpoints
        """
        # search for temperature
        l_result = re.search(r"[0-9]{2}[/][0-9]{2}|M[0-9]{2}[/]M[0-9]{2}|[0-9]{2}[/]M[0-9]{2}", self._s_metar_data)

        if l_result:
            # for a negative temperature in Celsius, replace M to -
            l_result = re.split(r"\/", l_result[0].replace('M', '-'))

            # temperature
            self._i_temperature_c = int(l_result[0])

            # convert °C to °F (temperature)
            self._i_temperature_f = int((self._i_temperature_c * 9 / 5) + 32)

            # dewpoint
            self._i_dewpoint_c = int(l_result[1])

            # convert °C to °F (dewpoint)
            self._i_dewpoint_f = int((self._i_dewpoint_c * 9 / 5) + 32)

            # logger
            # M_LOG.info("Temperature %d°C (%d°F) Dewpoint %d°C (%d°F).", self._i_temperature_c,
            #                                                             self._i_temperature_f,
            #                                                             self._i_dewpoint_c,
            #                                                             self._i_dewpoint_f)

    # ---------------------------------------------------------------------------------------------
    def trends(self):
        """
        forecasting changes
        """
        # search for forecasting changes
        l_result = re.search(r"NOSIG|BECMG|TEMPO", self._s_metar_data)

        if l_result:
            # nosig ?
            if "NOSIG" == l_result[0]:
                # nosig
                self._v_nosig = True

                # logger
                # M_LOG.info("Trends: No significant change is expected to the reported conditions within the next 2 hours.")

            # becmg ?
            if "BECMG" == l_result[0]:
                # becmg
                self._v_becmg = True

                # logger
                # M_LOG.info("Trends: Sustained significant changes in weather conditions are expected.")

            # tempo ?
            if "TEMPO" == l_result[0]:
                # tempo
                self._v_tempo = True

                # logger
                # M_LOG.info("Trends: Temporary significant changes in weather conditions are expected.")

    # ---------------------------------------------------------------------------------------------
    def visibility(self):
        """
        determining visibility conditions
        """
        # search for visibility
        l_result = re.search(r"\s[0-9]{4}\s|CAVOK", self._s_metar_data)

        if l_result:
            # cavok ?
            if "CAVOK" == l_result[0]:
                # cavok
                self._v_cavok = True

                # logger
                # M_LOG.info("Visibility: Ceiling And Visibility OK.")

            # senão,...
            else:
                # 9999 ?
                if "9999" == l_result[0].replace(' ', ''):
                    # visibility
                    self._i_visibility = 9999

                    # logger
                    # M_LOG.info("Visibility: 10km or more.")

                # senão,...
                else:
                    # visibility
                    self._i_visibility = int(l_result[0].replace(' ', ''))

                    # logger
                    # M_LOG.info("Visibility: %d meter.", self._i_visibility)

    # ---------------------------------------------------------------------------------------------
    def weather_type(self):
        """
        weather type determination
        """
        # search for weather
        l_result = re.search(r"""[\-\+]DZ|DZ|[\-\+]RA|RA|[\-\+]SN|SN|[\-\+]SG|SG|[\-\+]PL|PL
                                |[\-\+]GS|GS|[\-\+]DS|DS|[\-\+]SS|SS|DU|SQ|BR|HZ|FU|IC|TS|FG
                                |VA|BLSN|FZFG|VCFG|MIFG|PRFG|BCFG|DRSN|DRSA|DRDU|BLDU|VCTS
                                |[\-\+]RASN|RASN|[\-\+]SNRA|SNRA|[\-\+]SHSN|SHSN|[\-\+]SHRA|SHRA
                                |[\-\+]SHGR|SHGR|[\-\+]TSGR|TSGR|[\-\+]FZRA|FZRA|[\-\+]FZDZ|FZDZ
                                |[\-\+]TSRA|TSRA|[\-\+]SHGR|SHGR|[\-\+]TSGS|TSGS|[\-\+]TSSN|TSSN
                                """, self._s_metar_data)

        if l_result:
            # weather
            self._s_weather = str(l_result[0])

            # for all messages...
            self._s_weather_text = df.DDCT_WEATHER.get(self._s_weather, None)

            if self._s_weather_text:
                pass

                # logger
                # M_LOG.info("Weather: %s.", str(self._s_weather_text))

    # ---------------------------------------------------------------------------------------------
    def wind_type(self):
        """
        determination of speed and wind guide
        """
        # search for velocity (mps)
        l_results = re.search(r"[0-9]{5}MPS", self._s_metar_data)

        if l_results:
            # wind direction
            self._i_wind_dir = int(l_results[0][:3])
            # wind velocity (m/s)
            self._i_wind_vel_mps = int(l_results[0][3:-3])
            # wind velocity (kt)
            self._i_wind_vel_kt = int(round(self._i_wind_vel_mps * df.DF_MPS2KT, 0))

            # logger
            # M_LOG.info("Wind: Winds from %d° at %d mps (%d knots).", self._i_wind_dir,
            #                                                          self._i_wind_vel_mps,
            #                                                          self._i_wind_vel_kt)

        # search for velocity (kt)
        l_results = re.search(r"[0-9]{5}KT", self._s_metar_data)

        if l_results:
            # wind direction
            self._i_wind_dir = int(l_results[0][:3])
            # wind velocity (kt)
            self._i_wind_vel_kt = int(l_results[0][3:-2])
            # wind velocity (m/s)
            self._i_wind_vel_mps = int(round(self._i_wind_vel_kt * df.DF_KT2MPS, 0))

            # logger
            # M_LOG.info("Wind: Winds from %d° at %d knots (%d mps).", self._i_wind_dir,
            #                                                          self._i_wind_vel_kt,
            #                                                          self._i_wind_vel_mps)

        # search for gust (mps)
        l_results = re.search(r"[0-9]{5}G[0-9]{2}MPS", self._s_metar_data)

        if l_results:
            # wind direction
            self._i_wind_dir = int(l_results[0][:3])
            # wind velocity (m/s)
            self._i_wind_vel_mps = int(l_results[0][3:5])
            # wind velocity (kt)
            self._i_wind_vel_kt = int(round(self._i_wind_vel_mps * df.DF_MPS2KT, 0))

            # gust (m/s)
            self._i_gust_mps = int(l_results[0][-5:-3])
            # gust (kt)
            self._i_gust_kt = int(round(self._i_gust_mps * df.DF_MPS2KT, 0))

            # logger
            # M_LOG.info("Wind: Winds from %d° at %d mps with gusts up to %d mps (%d knots).", self._i_wind_dir,
            #                                                                                  self._i_wind_vel_mps,
            #                                                                                  self._i_gust_mps,
            #                                                                                  self._i_gust_kt)

        # search for gust (kt)
        l_results = re.search(r"[0-9]{5}G[0-9]{2}KT", self._s_metar_data)

        if l_results:
            # wind direction
            self._i_wind_dir = int(l_results[0][:3])
            # wind velocity (kt)
            self._i_wind_vel_kt = int(l_results[0][3:5])
            # wind velocity (m/s)
            self._i_wind_vel_mps = int(round(self._i_wind_vel_kt * df.DF_KT2MPS, 0))

            # gust (kt)
            self._i_gust_kt = int(l_results[0][-4:-2])
            # gust (m/s)
            self._i_gust_mps = int(round(self._i_gust_kt * df.DF_KT2MPS, 0))

            # logger
            # M_LOG.info("Wind: Winds from %d° at %d knots with gusts up to %d knots (%d mps).", self._i_wind_dir,
            #                                                                                    self._i_wind_vel_kt,
            #                                                                                    self._i_gust_kt,
            #                                                                                    self._i_gust_mps)

        # search for min/max (kt)
        l_results = re.search(r"[0-9]{3}V[0-9]{3}", self._s_metar_data)

        if l_results:
            # wind direction min
            self._i_wind_dir_min = int(l_results[0][:3])
            # wind direction max
            self._i_wind_dir_max = int(l_results[0][4:])

            # logger
            # M_LOG.info("Variable winds direction between %d° and %d°.", self._i_wind_dir_min,
            #                                                             self._i_wind_dir_max)

        # search for variable (kt)
        l_results = re.search(r"VRB[0-9]{2}MPS", self._s_metar_data)

        if l_results:
            # wind velocity (m/s)
            self._i_wind_var_mps = int(l_results[0][3:-3])
            # wind velocity (kt)
            self._i_wind_var_kt = int(round(self._i_wind_var_mps * df.DF_MPS2KT, 0))

            # logger
            # M_LOG.info("Variable winds directions at %d mps (%d knots).", self._i_wind_var_mps,
            #                                                               self._i_wind_var_kt)

        # search for variable (kt)
        l_results = re.search(r"VRB[0-9]{2}KT", self._s_metar_data)

        if l_results:
            # wind velocity (kt)
            self._i_wind_var_kt = int(l_results[0][3:-2])
            # wind velocity (m/s)
            self._i_wind_var_mps = int(round(self._i_wind_var_kt * df.DF_KT2MPS, 0))

            # logger
            # M_LOG.info("Variable winds directions at %d knots (%d mps).", self._i_wind_var_kt,
            #                                                               self._i_wind_var_mps)

    # ---------------------------------------------------------------------------------------------
    def cut_id(self):
        """
        cut off the message id
        """
        self._s_metar_data = self._s_metar_data.split(' ')[1:]
        self._s_metar_data = str.join(',', self._s_metar_data)
        self._s_metar_data = self._s_metar_data.replace(',', ' ')

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def v_cavok(self):
        """ceiling and visibility flag"""
        return self._v_cavok

    # ---------------------------------------------------------------------------------------------
    @property
    def i_dewpoint_c(self):
        """dewpoint in °C"""
        return self._i_dewpoint_c

    # ---------------------------------------------------------------------------------------------
    @property
    def s_forecast_time(self):
        """forecast time"""
        return self._s_forecast_time

    # ---------------------------------------------------------------------------------------------
    @property
    def i_gust_kt(self):
        """gust of wind in kt"""
        return self._i_gust_kt

    # ---------------------------------------------------------------------------------------------
    @property
    def s_icao_code(self):
        """icao code"""
        return self._s_icao_code

    # ---------------------------------------------------------------------------------------------
    @property
    def i_pressure_hpa(self):
        """pressure in hPa"""
        return self._i_pressure_hpa

    # ---------------------------------------------------------------------------------------------
    @property
    def i_temperature_c(self):
        """temperature in °C"""
        return self._i_temperature_c

    # ---------------------------------------------------------------------------------------------
    @property
    def i_visibility(self):
        """visibility in m"""
        return self._i_visibility

    # ---------------------------------------------------------------------------------------------
    @property
    def i_wind_dir(self):
        """wind direction in °"""
        return self._i_wind_dir

    # ---------------------------------------------------------------------------------------------
    @property
    def i_wind_vel_kt(self):
        """wind velocity in kt"""
        return self._i_wind_vel_kt

# -------------------------------------------------------------------------------------------------
def _get_metar_data(fs_station_file):
    """
    read a string from a file with a metar
    """
    # open carrapato for read metaf data
    with open(fs_station_file, "r") as lfh_md:
        # load file
        ls_line = lfh_md.read()

    # METAF or METAR data ?
    if ls_line.startswith("METAF") or ls_line.startswith("METAR"):
        # get metar data
        ls_line = ls_line[5:]

    # return
    return ls_line.strip()

# -------------------------------------------------------------------------------------------------
def metar_parse(fs_station_file):
    """
    metar parse
    """
    # transfer a line with data to SMetar
    lo_metar = SMetar(_get_metar_data(fs_station_file))
    assert lo_metar

    # airport index
    lo_metar.icao_code()

    # type of formation
    lo_metar.report_type()

    # report formation
    lo_metar.forecast_time()

    # speed and wind direction
    lo_metar.wind_type()

    # visibility conditions
    lo_metar.visibility()

    # cloudy
    lo_metar.clouds_type()

    # temperature
    lo_metar.temperature()

    # pressure
    lo_metar.pressure()

    # weather
    lo_metar.weather_type()

    # forecasts
    lo_metar.trends()

    # notes
    lo_metar.remarks()

    # return
    return lo_metar

# < the end >--------------------------------------------------------------------------------------

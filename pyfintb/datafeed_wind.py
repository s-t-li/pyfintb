#!/usr/bin/env python
# coding: utf-8

from pyfintb.datetools import to_str_date, to_pd_timestamp, gen_pd_datetime_idx, td_count, TODAY
from pyfintb.utils import to_list, list_slice

# Wind API Documentation：
# visit https://www.windquant.com/qntcloud/help
# or type "API" on Wind Financial Terminal
from WindPy import *
wind_start = w.start(waitTime=10)  # timeout ~10s

import pandas as pd

import warnings as wn
def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'
wn.formatwarning = custom_formatwarning

class Wind():
    def __init__(self, data_usage_limit_per_week=5000000):
        self._DATA_USAGE_LIMIT_PER_WEEK = data_usage_limit_per_week
        self._DATA_USAGE_WARN = self._DATA_USAGE_LIMIT_PER_WEEK * 0.01
        self._PIECE_LEN = 1000
        self._MAX_MAT_SIZE = 1000 * 1000
        self._FUNC_DATA_USAGE_LIMIT = {"wsd": 100000, "wss": 100000, "wsee": 1000,}
        self._windapi_err_detail = {
            -40520000: {"symbol": "WQERR_BASE", "info": "一般性错误"},
            -40520001: {"symbol": "WQERR_UNKNOWN", "info": "未知错误"},
            -40520002: {"symbol": "WQERR_INTERNAL_ERROR", "info": "内部错误"},
            -40520003: {"symbol": "WQERR_SYSTEM_REASON", "info": "操作系统原因"},
            -40520004: {"symbol": "WQERR_LOGON_FAILED", "info": "登录失败"},
            -40520005: {"symbol": "WQERR_LOGON_NOAUTH", "info": "无登录权限"},
            -40520006: {"symbol": "WQERR_USER_CANCEL", "info": "用户取消"},
            -40520007: {"symbol": "WQERR_NO_DATA_AVAILABLE", "info": "没有可用数据"},
            -40520008: {"symbol": "WQERR_TIMEOUT", "info": "请求超时"},
            -40520009: {"symbol": "WQERR_LOST_WBOX", "info": "Wbox错误"},
            -40520010: {"symbol": "WQERR_ITEM_NOT_FOUND", "info": "未找到相关内容"},
            -40520011: {"symbol": "WQERR_SERVICE_NOT_FOUND", "info": "未找到相关服务"},
            -40520012: {"symbol": "WQERR_ID_NOT_FOUND", "info": "未找到相关ID"},
            -40520013: {"symbol": "WQERR_LOGON_CONFLICT", "info": "已在本机使用其他账号登录，故无法使用指定账号登录"},
            -40520014: {"symbol": "WQERR_LOGON_NO_WIM", "info": "未登录使用WIM工具，故无法登录"},
            -40520015: {"symbol": "WQERR_TOO_MANY_LOGON_FAILURE", "info": "连续登录失败次数过多"},
            -40521000: {"symbol": "WQERR_IOERROR_CLASS", "info": "网络数据存取错误"},
            -40521001: {"symbol": "WQERR_IO_ERROR", "info": "IO操作错误"},
            -40521002: {"symbol": "WQERR_SERVICE_NOT_AVAL", "info": "后台服务器不可用"},
            -40521003: {"symbol": "WQERR_CONNECT_FAILED", "info": "网络连接失败"},
            -40521004: {"symbol": "WQERR_SEND_FAILED", "info": "请求发送失败"},
            -40521005: {"symbol": "WQERR_RECEIVE_FAILED", "info": "数据接收失败"},
            -40521006: {"symbol": "WQERR_NETWORK_ERROR", "info": "网络错误"},
            -40521007: {"symbol": "WQERR_SERVER_REFUSED", "info": "服务器拒绝请求"},
            -40521008: {"symbol": "WQERR_SVR_BAD_RESPONSE", "info": "错误的应答"},
            -40521009: {"symbol": "WQERR_DECODE_FAILED", "info": "数据解码失败"},
            -40521010: {"symbol": "WQERR_INTERNET_TIMEOUT", "info": "网络超时"},
            -40521011: {"symbol": "WQERR_ACCESS_FREQUENTLY", "info": "频繁访问"},
            -40521012: {"symbol": "WQERR_SERVER_INTERNAL_ERROR", "info": "服务器内部错误"},
            -40522000: {"symbol": "WQERR_INVALID_CLASS", "info": "请求输入错误"},
            -40522001: {"symbol": "WQERR_ILLEGAL_SESSION", "info": "无合法会话"},
            -40522002: {"symbol": "WQERR_ILLEGAL_SERVICE", "info": "非法数据服务"},
            -40522003: {"symbol": "WQERR_ILLEGAL_REQUEST", "info": "非法请求"},
            -40522004: {"symbol": "WQERR_WINDCODE_SYNTAX_ERR", "info": "万得代码语法错误"},
            -40522005: {"symbol": "WQERR_ILLEGAL_WINDCODE", "info": "不支持的万得代码"},
            -40522006: {"symbol": "WQERR_INDICATOR_SYNTAX_ERR", "info": "指标语法错误"},
            -40522007: {"symbol": "WQERR_ILLEGAL_INDICATOR", "info": "不支持的指标"},
            -40522008: {"symbol": "WQERR_OPTION_SYNTAX_ERR", "info": "指标参数语法错误"},
            -40522009: {"symbol": "WQERR_ILLEGAL_OPTION", "info": "不支持的指标参数"},
            -40522010: {"symbol": "WQERR_DATE_TIME_SYNTAX_ERR", "info": "日期与时间语法错误"},
            -40522011: {"symbol": "WQERR_INVALID_DATE_TIME", "info": "不支持的日期与时间"},
            -40522012: {"symbol": "WQERR_ILLEGAL_ARG", "info": "不支持的请求参数"},
            -40522013: {"symbol": "WQERR_INDEX_OUT_OF_RANGE", "info": "数组下标越界"},
            -40522014: {"symbol": "WQERR_DUPLICATE_WQID", "info": "重复的WQID"},
            -40522015: {"symbol": "WQERR_UNSUPPORTED_NOAUTH", "info": "请求无相应权限"},
            -40522016: {"symbol": "WQERR_UNSUPPORTED_DATA_TYPE", "info": "不支持的数据类型"},
            -40522017: {"symbol": "WQERR_DATA_QUOTA_EXCEED", "info": "数据提取量超限"},
            -40522018: {"symbol": "WQERR_ILLEGAL_ARG_COMBINATION", "info": "不支持的请求参数"},
        }

    def _windapi_err_raise(self, err_code):
        if err_code == 0:
            pass
        else:
            info = self._windapi_err_detail[err_code]["info"]
            raise Exception("Wind API Error ID {}: {}".format(err_code, info))
    
    # convert Wind data object to pandas DataFrame    
    def _wdata2dataframe(self, wdata):
        self._windapi_err_raise(wdata.ErrorCode)
        field = wdata.Fields
        code = wdata.Codes
        time = wdata.Times
        data = wdata.Data
        datetime_idx = pd.to_datetime(time)
        if len(field) == 1:
            col = code
        else:
            if len(code) == 1:
                col = field
            else:
                col = pd.MultiIndex.from_product([field, code], names=['field', 'code'])
        if len(time) == 1:
            if len(field) == 1:
                result_df = pd.DataFrame(data, index=datetime_idx, columns=col)
            else:
                result_df = pd.DataFrame(data, index=col, columns=datetime_idx).T
        else:
            result_df = pd.DataFrame(data, index=col, columns=datetime_idx).T
        return result_df

    # if is Wind sector ID
    def is_wind_sectorid(self, wcode):
        for i in to_list(wcode):
            # rule: length of string is 16 #AND# no dots in the string
            if (len(i) == 16) and ("." not in i):
                continue
            else:
                return False
        return True

    # if is Wind EDB ID
    def is_wind_edbid(self, wcode):
        for i in to_list(wcode):
            # rule: length of string is 8 #AND# no dots in the string #AND# starting with M, S or G
            if (len(i) == 8) and ("." not in i) and (i[0].upper() in ["M", "S", "G"]):
                continue
            else:
                return False
        return True

    # get components of Wind code
    def wind_components(self, wcode, show_name=False, date=TODAY):
        code = to_list(wcode)
        query = "sectorid=" if self.is_wind_sectorid(code) else "windcode="
        wdata_obj = w.wset("sectorconstituent", "date="+to_str_date(date), query+code[0])
        self._windapi_err_raise(wdata_obj.ErrorCode)
        if wdata_obj.Data == []:
            return []
        cpn_code_list = wdata_obj.Data[1]
        cpn_name_list = wdata_obj.Data[2]
        if show_name:
            cpn_code_dict = dict(zip(cpn_code_list, cpn_name_list))
            return cpn_code_dict
        else:
            return cpn_code_list

    # get the name of Wind code
    def wind_name(self, wcode, eng=False):
        code = to_list(wcode)
        lang = "sec_englishname" if eng else "sec_name"
        wdata_obj = w.wss(code, lang)
        self._windapi_err_raise(wdata_obj.ErrorCode)
        name = wdata_obj.Data[0]
        if name[0] is None:
            wn.warn("The input code is not a standard Wind code.")
            return []
        else:
            return name

    # get time series data
    def wind_series(self, wcode, field, start_date, end_date=TODAY, col=None, **kwargs):
        if field.upper() == "EDB": # get data from Wind Economic Database
            return self.wind_edb(wcode, start_date, end_date, col=col, **kwargs)
        code = to_list(wcode)
        field = to_list(field)
        code_len = len(code)
        field_len = len(field)
        date_len = td_count(start_date, end_date, days="alldays") # conservative count
        one_fetch_size = code_len * date_len
        all_fetch_size = field_len * one_fetch_size
        if all_fetch_size >= self._DATA_USAGE_LIMIT_PER_WEEK:
            wn.warn("Data usage this time exceeds max usage limitation per week.")
            return None
        if all_fetch_size >= self._DATA_USAGE_WARN:
            wn.warn("Data usage this time: almost {0} cells".format(all_fetch_size))
        result_df = pd.DataFrame()
        if one_fetch_size < self._FUNC_DATA_USAGE_LIMIT["wsd"]: # if exceed max data matrix size limitation
            if ((code_len > 1) and (field_len > 1)):
                for f in field:
                    wdata_obj = w.wsd(code, f, to_str_date(start_date), to_str_date(end_date), **kwargs)
                    wdata_df = self._wdata2dataframe(wdata_obj)
                    result_df = pd.concat([result_df, wdata_df], axis=1)
                    
                if col is None:
                    result_df.columns = pd.MultiIndex.from_product([field, code], names=['field', 'code'])
                else:
                    col = to_list(col)
                    result_df.columns = pd.MultiIndex.from_product([field, col], names=['field', 'code'])
            else:
                wdata_obj = w.wsd(code, field, to_str_date(start_date), to_str_date(end_date), **kwargs)
                result_df = self._wdata2dataframe(wdata_obj)
                if col is None:
                    result_df.columns = code if field_len == 1 else field
                else:
                    col = to_list(col)
                    result_df.columns = col if field_len == 1 else field
        else:
            date_idx = gen_pd_datetime_idx(start_date, end_date, **kwargs)
            for sub_date_range in list_slice(date_idx, self._PIECE_LEN):
                sub_start_date = sub_date_range[0]
                sub_end_date = sub_date_range[-1]
                sub_df = pd.DataFrame()
                for sub_code in list_slice(code, self._FUNC_DATA_USAGE_LIMIT["wsd"]//self._PIECE_LEN):
                    for f in field:
                        wdata_obj = w.wsd(sub_code, f, to_str_date(sub_start_date), to_str_date(sub_end_date), **kwargs)
                        wdata_df = self._wdata2dataframe(wdata_obj)
                        wdata_df.columns = pd.MultiIndex.from_product([[f], sub_code], names=['field', 'code'])
                        sub_df = pd.concat([sub_df, wdata_df], axis=1)
                result_df = result_df.append(sub_df)
            if ((code_len > 1) and (field_len > 1)):
                if col is None:
                    result_df.columns = pd.MultiIndex.from_product([field, code], names=['field', 'code'])
                else:
                    col = to_list(col)
                    result_df.columns = pd.MultiIndex.from_product([field, col], names=['field', 'code'])
            else:
                if col is None:
                    result_df.columns = code if field_len == 1 else field
                else:
                    col = to_list(col)
                    result_df.columns = col if field_len == 1 else field
        result_df.index = pd.DatetimeIndex(result_df.index)
        result_df.index.freq = result_df.index.inferred_freq
        return result_df

    # get macroeconomic data from Wind EDB
    def wind_edb(self, wcode, start_date, end_date=TODAY, period=None, col=None, **kwargs):
        code = to_list(wcode)
        code_len = len(code)
        date_len = td_count(start_date, end_date, days="alldays") # conservative count
        all_fetch_size = code_len * date_len
        if all_fetch_size >= self._DATA_USAGE_LIMIT_PER_WEEK:
            wn.warn("Data usage this time exceeds max usage limitation per week.")
            return None
        if all_fetch_size >= self._DATA_USAGE_WARN:
            wn.warn("Data usage this time: almost {0} cells".format(all_fetch_size))
        wdata_obj = w.edb(code, start_date, end_date, **kwargs)
        wdata_df = self._wdata2dataframe(wdata_obj)
        if period is None:
            if col is not None:
                col = to_list(col)
                wdata_df.columns = col
            return wdata_df
        else:
            temp_idx = pd.date_range(to_pd_timestamp(start_date), to_pd_timestamp(end_date))
            resample_df = pd.DataFrame(wdata_df, index=temp_idx).resample(period).last().ffill()
            resample_df.columns = code if col is None else col
            resample_df.index.freq = resample_df.index.inferred_freq
            f_v_idx = resample_df.first_valid_index()
            l_v_idx = resample_df.last_valid_index()
            return resample_df.loc[f_v_idx:l_v_idx]

    # get cross-sectional data
    def wind_crosec(self, wcode, field, **kwargs):
        if self.is_wind_sectorid(wcode):
            return self.wind_sector_crosec(wcode, field, **kwargs)
        else:
            code = to_list(wcode)
            field = to_list(field)
            code_len = len(code)
            field_len = len(field)
            all_fetch_size = code_len * field_len
            if all_fetch_size >= self._DATA_USAGE_LIMIT_PER_WEEK:
                wn.warn("Data usage this time exceeds max usage limitation per week.")
                return None
            if all_fetch_size >= self._DATA_USAGE_WARN:
                wn.warn("Data usage this time: almost {0} cells".format(all_fetch_size))
            if all_fetch_size < self._FUNC_DATA_USAGE_LIMIT["wss"]: # if exceed max data matrix size limitation
                err_code, wdata_df = w.wss(code, field, usedf=True, **kwargs)
                self._windapi_err_raise(err_code)
                return wdata_df
            else:
                wn.warn("Data usage this time: almost {0} cells".format(all_fetch_size))
                result_df = pd.DataFrame()
                for sub_code in list_slice(code, PIECE_LEN):
                    sub_df = pd.DataFrame()
                    for sub_field in list_slice(field, self._FUNC_DATA_USAGE_LIMIT["wss"]//PIECE_LEN):
                        err_code, wdata_df = w.wss(sub_code, sub_field, usedf=True, **kwargs)
                        self._windapi_err_raise(err_code)
                        sub_df = pd.concat([sub_df, wdata_df], axis=1)

                    result_df = result_df.append(sub_df)
                return result_df

    # get sector cross-sectional data via Wind API
    def wind_sector_crosec(self, wcode, field, **kwargs):
        code = to_list(wcode)
        field = to_list(field)
        code_len = len(code)
        field_len = len(field)
        all_fetch_size = code_len * field_len
        result_df = pd.DataFrame()
        if all_fetch_size < self._FUNC_DATA_USAGE_LIMIT["wsee"]: # if exceed max data matrix size limitation
            err_code, wdata_df = w.wsee(code, field, usedf=True, **kwargs)
            wdata_df.columns = field
            return wdata_df
        else:
            wn.warn("Data usage this time: almost {0} cells".format(all_fetch_size))
            for sub_code in list_slice(code, self._FUNC_DATA_USAGE_LIMIT["wsee"]//field_len):
                err_code, wdata_df = w.wsee(sub_code, field, usedf=True, **kwargs)
                self._windapi_err_raise(err_code)      
                result_df = result_df.append(wdata_df)
        result_df.columns = field
        return result_df

    # get panel data via Wind API
    def wind_panel(self, wcode, field, start_date, end_date, **kwargs):
        code = to_list(wcode)
        field = to_list(field)
        date_idx = gen_pd_datetime_idx(start_date, end_date, **kwargs)
        result_df_multiidx = pd.MultiIndex.from_product([date_idx, code], names=["date", "code"])
        result_df = pd.DataFrame()
        for i in date_idx:
            wdata_df = self.wind_crosec(wcode, field, tradedate=i, **kwargs)     
            result_df = result_df.append(wdata_df)
        result_df.index = result_df_multiidx
        return result_df

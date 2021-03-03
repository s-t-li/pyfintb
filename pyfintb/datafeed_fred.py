#!/usr/bin/env python
# coding: utf-8

from pyfintb.datetools import to_py_datetime, TODAY
from pyfintb.utils import to_list

import sys
import xml.etree.ElementTree as ET
if sys.version_info[0] >= 3:
    import urllib.request as url_request
    import urllib.parse as url_parse
    import urllib.error as url_error
else:
    import urllib2 as url_request
    import urllib as url_parse
    import urllib2 as url_error

import pandas as pd

urlopen = url_request.urlopen
urlencode = url_parse.urlencode
HTTPError = url_error.HTTPError

class Fred(object):
    earliest_realtime_start = '1776-07-04'
    latest_realtime_end = '9999-12-31'
    nan_char = '.'
    max_results_per_request = 1000
    root_url = 'https://api.stlouisfed.org/fred'

    def __init__(self, api_key=None, api_key_file=None):
        self.api_key = None
        if api_key is not None:
            self.api_key = api_key
        elif api_key_file is not None:
            f = open(api_key_file, 'r')
            self.api_key = f.readline().strip()
            f.close()

    def __fetch_data(self, url):
        url += '&api_key=' + self.api_key
        try:
            response = urlopen(url)
            root = ET.fromstring(response.read())
        except HTTPError as exc:
            root = ET.fromstring(exc.read())
            raise ValueError(root.get('message'))
        return root

    def fred_id_info(self, fredcode):
        url = "%s/series?series_id=%s" % (self.root_url, fredcode)
        root = self.__fetch_data(url)
        if root is None or not len(root):
            raise ValueError('No info exists for series id: ' + fredcode)
        info = pd.Series(list(root)[0].attrib)
        return info

    def fred_series(self, fredcode, start_date, end_date=TODAY, period=None, col=None, **kwargs):
        start_date = to_py_datetime(start_date)
        end_date = to_py_datetime(end_date)
        
        url = "%s/series/observations?" % (self.root_url)
        url += '&observation_start=' + start_date.strftime('%Y-%m-%d')
        url += '&observation_end=' + end_date.strftime('%Y-%m-%d')
        
        result_df = pd.DataFrame()
        for i in to_list(fredcode):
            temp_url = url + "&series_id=%s" % (i)
            if period is None:
                pass
            else:
                temp_url += "&frequency=%s" % (period)
            if kwargs.keys():
                temp_url += '&' + urlencode(kwargs)
            root = self.__fetch_data(temp_url)
            if root is None:
                raise ValueError('No data exists for series id: ' + fredcode)
            data = {}
            for child in root:
                val = child.get('value')
                if val == self.nan_char:
                    val = float('NaN')
                else:
                    val = float(val)
                data[pd.to_datetime(child.get('date'))] = val
            df = pd.DataFrame.from_dict(data, orient='index', columns=[i])
            result_df = pd.concat([result_df, df], axis=1)
        if col is None:
            pass
        else:
            result_df.columns = to_list(col)
        return result_df
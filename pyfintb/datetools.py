from WindPy import *
w.start(waitTime=10, showmenu=False)

import numpy as np
import pandas as pd
from pandas.tseries.offsets import DateOffset
import datetime as dt
import QuantLib as ql

### CALENDAR DATE CONST - PASS 2021-02-20 --------------------------------------
TODAY = pd.to_datetime('today').normalize() # date of today, basic date const
YESTERDAY = TODAY - DateOffset(days=1)
TOMORROW = TODAY + DateOffset(days=1)

# last period end
# L = Last, M = Month, Q = Quarter, Y = Year
# e.g. LME = LAST MONTH END
LME = TODAY - pd.offsets.MonthEnd()
LQE = TODAY - pd.offsets.QuarterEnd()
LYE = TODAY - pd.offsets.YearEnd()

# current period begin
# C = Current, M = Month, Q = Quarter, Y = Year
# e.g. CYB = CURRENT YEAR BEGIN
CMB = TODAY - pd.offsets.MonthBegin()
CQB = TODAY - pd.offsets.QuarterBegin()
CYB = TODAY - pd.offsets.YearBegin()

# ealier n periods
# E = Ealier, W = Week, M = Month, Y = Year
# e.g. E3Y = EALIER 3 YEAR, EnP = EALIER n periods
E1W = TODAY - DateOffset(weeks=1)
E2W = TODAY - DateOffset(weeks=2)
E3W = TODAY - DateOffset(weeks=3)

E1M = TODAY - DateOffset(months=1)
E2M = TODAY - DateOffset(months=2)
E3M = TODAY - DateOffset(months=3)
E4M = TODAY - DateOffset(months=4)
E5M = TODAY - DateOffset(months=5)
E6M = TODAY - DateOffset(months=6)
E7M = TODAY - DateOffset(months=7)
E8M = TODAY - DateOffset(months=8)
E9M = TODAY - DateOffset(months=9)
E10M = TODAY - DateOffset(months=10)
E11M = TODAY - DateOffset(months=11)
E12M = TODAY - DateOffset(months=12)

E1Y = TODAY - DateOffset(years=1)
E2Y = TODAY - DateOffset(years=2)
E3Y = TODAY - DateOffset(years=3)
E4Y = TODAY - DateOffset(years=4)
E5Y = TODAY - DateOffset(years=5)
E6Y = TODAY - DateOffset(years=6)
E7Y = TODAY - DateOffset(years=7)
E8Y = TODAY - DateOffset(years=8)
E9Y = TODAY - DateOffset(years=9)
E10Y = TODAY - DateOffset(years=10)
E15Y = TODAY - DateOffset(years=15)
E20Y = TODAY - DateOffset(years=20)
E25Y = TODAY - DateOffset(years=25)
E30Y = TODAY - DateOffset(years=30)
E35Y = TODAY - DateOffset(years=35)
E40Y = TODAY - DateOffset(years=40)
E45Y = TODAY - DateOffset(years=45)
E50Y = TODAY - DateOffset(years=50)

### DATE CONVERSION - PASS 20200206 --------------------------------------------
### between: str, dt.date, pd.ts, np.dt64, ql.date

# convert to pandas.Timestamp
def to_pd_timestamp(date):
    if isinstance(date, (str, dt.date, dt.datetime, np.datetime64)):
        return pd.to_datetime(date)
    elif isinstance(date, (ql.Date)):
        return pd.to_datetime(date.to_date())
    elif isinstance(date, (pd.Timestamp)):
        return date
    else:
        raise Exception("Unrecognized date format.")

# convert to python datetime.date
def to_py_datetime(date):
    if isinstance(date, str):
        return dt.datetime.strptime(date, "%Y-%m-%d")
    elif isinstance(date, (pd.Timestamp)):
        return date.to_pydatetime()
    elif isinstance(date, (np.datetime64)):
        return date.item()
    elif isinstance(date, (ql.Date)):
        return date.to_date()
    elif isinstance(date, (dt.date, dt.datetime)):
        return date
    else:
        raise Exception("Unrecognized date format.")

# convert to QuantLib.Date
def to_ql_date(date):
    if isinstance(date, str):
        date = dtu.parser.parse(date)
        return ql.Date(date.day, date.month, date.year)
    elif isinstance(date, (dt.date, dt.datetime, pd.Timestamp)):
        return ql.Date(date.day, date.month, date.year)
    elif isinstance(date, (np.datetime64)):
        date = date.item()
        return ql.Date(date.day, date.month, date.year)
    elif isinstance(date, (ql.Date)):
        return date
    else:
        raise Exception("Unrecognized date format.")
        
# convert to date string
def to_str_date(date, fmt="%Y-%m-%d"):
    if isinstance(date, (dt.date, dt.datetime, pd.Timestamp)):
        return date.strftime(fmt)
    elif isinstance(date, (np.datetime64)):
        return np.datetime_as_string(date, unit="D")
    elif isinstance(date, (ql.Date)):
        return f"{str(date.year())}{str(date.month()):0>2}{str(date.dayOfMonth()):0>2}"
    elif isinstance(date, str):
        return date
    else:
        raise Exception("Unrecognized date format.")

### generate pandas.DatetimeIndex
def gen_pd_datetime_idx(start_date, end_date=TODAY, **kwargs):
    wind_obj = w.tdays(to_str_date(start_date), to_str_date(end_date),
                       **kwargs)
    if wind_obj.Data:
        idx = pd.DatetimeIndex(wind_obj.Data[0])
        idx.freq = idx.inferred_freq
        return idx
    else:
        return None
    
### parse Wind date macro to 'offset n' and 'period'
# e.g. "5M" -> 5 and "M", "-10Y" -> -10 and "Y"
def parse_wind_date_macro(macro):
    n = 0
    prd = "TD"
    if isinstance(macro, int):
        n = macro
    elif macro[-2:].upper() == "TD":
        n = int(macro[:-2])
    else:
        prd = macro[-1:].upper()
        n = int(macro[:-1])
    return n, prd

### NUMBERS OF DAYS WITH SPECIFIC PERIOD - PASS 2021-02-20 ---------------------
# quickly and approximately get trading days count in a period
def td_per_period(prd):
    if isinstance(prd, int):
        return prd
    return {"w": 5, "m": 21, "q": 63, "s": 125, "y": 245,}[prd]

# quickly and approximately get periods count in a year
def periods_per_year(prd):
    if isinstance(prd, int):
        return prd
    return {"td": 250, "d": 365, "w": 52, "m": 12, "q": 4, "s": 2, "y": 1,}[prd]

# trading days constants of an exchange
TDPYR_SSE = 243 # Shanghai Stock Exchange
TDPYR_SZSE = 243 # Shenzhen Stock Exchange
TDPYR_HKEX = 256 # Stock Exchange of Hong Kong

TDPYR_SHFE = 243 # Shanghai Futures Exchange
TDPYR_DCE = 243 # Dalian Commodity Exchange
TDPYR_ZCE = 243 # Zhengzhou Commodity Exchange
TDPYR_CFFE = 243 # China Financial Futures Exchange

TDPYR_NYSE = 252 # New York Stock Exchange
TDPYR_NASDAQ = 252 # Nasdaq
TDPYR_AMEX = 252 # American Stock Exchange

TDPYR_CME = 252 # Chicago Mercantile Exchange
TDPYR_COMEX = 252 # New York Mercantile Exchange
TDPYR_CBOT = 252 # Chicago Board of Trade
TDPYR_NYBOT = 252 # New York Board of Trade

TDPYR_LSE = 253 # London Stock Exchange
TDPYR_LME = 253 # London Metal Exchange
TDPYR_IPE = 256 # International Petroleum Exchange

TDPYR_TSE = 245 # Japan Exchange Group

# date offset - PASS 2021-02-20
def date_offset(n, prd, base=TODAY):
    prd = prd.lower()
    base = to_pd_timestamp(base)
    if prd == "y":
        offset = DateOffset(years=n)
    if prd == "m":
        offset = DateOffset(months=n)
    if prd == "w":
        offset = DateOffset(weeks=n)
    return base + offset

# generate pandas.DatetimeIndex - PASS 2021-02-20
def gen_pd_datetime_idx(start_date, end_date=TODAY, **kwargs):
    wind_obj = w.tdays(to_str_date(start_date), to_str_date(end_date),
                       **kwargs)
    if wind_obj.Data:
        idx = pd.DatetimeIndex(wind_obj.Data[0])
        idx.freq = idx.inferred_freq
        return idx
    else:
        return None
    
# parse Wind date macro to 'offset' and 'period' - PASS 2021-02-20
# e.g. "5M" -> 5 and "M", "-10Y" -> -10 and "Y"
def parse_wind_date_macro(macro):
    offset = 0
    prd = "TD"
    if isinstance(macro, int):
        offset = macro
    elif macro[-2:].upper() == "TD":
        offset = int(macro[:-2])
    else:
        prd = macro[-1:].upper()
        offset = int(macro[:-1])
    return offset, prd

### TRADING DAY FUNCTIONS USING WIND API - PASS 2021-02-20 ---------------------

# get previous nearest trading day
def td_prev(date=TODAY, **kwargs): 
    wind_obj = w.tdays("ED-0TD", to_str_date(date), **kwargs)    
    return to_pd_timestamp(wind_obj.Times[0]) # pandas.Timestamp

PTD = td_prev() # date of previous trading day from today, const

# get next trading day
def td_next(date=TODAY, **kwargs):    
    wind_obj = w.tdays(to_str_date(to_pd_timestamp(date) + DateOffset(days=1)), "SD+1TD",
                       **kwargs)
    return to_pd_timestamp(wind_obj.Times[0]) # pandas.Timestamp

NTD = td_next() # date of next trading day from today, const

# if is trading day
def td_is(date=TODAY, **kwargs):
    td_n = td_prev(date, **kwargs)
    if td_n == to_pd_timestamp(date):
        return True
    else:
        return False

# get shifted trading day
# use Wind date macros as offset, ref. Wind API documentation
def td_offset(n, prd, base=TODAY, exchange="SSE", **kwargs):
    prd = prd.lower()
    wind_obj = w.tdaysoffset(n, to_str_date(base), period=prd,
                             tradingcalendar=exchange, **kwargs)
    return to_pd_timestamp(wind_obj.Times[0]) # pandas.Timestamp

# count the number of trading days in a period
def td_count(start_date, end_date=TODAY, **kwargs):
    count = w.tdayscount(to_str_date(start_date), to_str_date(end_date),
                         **kwargs).Data[0][0]
    return count

# get trading days count per year in an exchange
# use the average of trading days each year in last 10 years
def td_per_year(exchange=None):
    year_list = [str((TODAY - DateOffset(years=i)).year) for i in range(10)]
    n = 0
    for i in year_list:
        count = td_count(i+"-01-01", i+"-12-31", tradingcalendar=exchange)
        n = n + count
    return round(n/10)
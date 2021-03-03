#from pyfintb.datafeed_chinabond import Chinabond
from pyfintb.datafeed_fred import Fred
from pyfintb.datafeed_wind import Wind

#cb = Chinabond()
#chinabond_yield_curve_name = cb.chinabond_yield_curve_name
#chinabond_yield_curve = cb.chinabond_yield_curve
#chinabond_yield = cb.chinabond_yield
#chinabond_yield_series = cb.chinabond_yield_series

fred = Fred("API KEY")
fred_series = fred.fred_series
fred_id_info = fred.fred_id_info

wind = Wind()
is_wind_sectorid = wind.is_wind_sectorid
is_wind_edbid = wind.is_wind_edbid
wind_components = wind.wind_components
wind_name = wind.wind_name
wind_series = wind.wind_series
wind_edb = wind.wind_edb
wind_crosec = wind.wind_crosec
wind_sector_crosec = wind.wind_sector_crosec
wind_panel = wind.wind_panel

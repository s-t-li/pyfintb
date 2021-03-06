# pyfintb

**一个面向金融分析师日常工作需求，专门用于数据读取、绘制图表、业绩分析、组合测算的易用Python工具包**

**An easy-to-use Python financial toolbox for financial analysts**

- alpha / 2021-02-27 / under heavy development 
- 开发初衷与原则：**高效、易用、轻量**
- √ 适用的场景：宏观研究、证券研究、组合业绩评估、资产配置等
- × 不适用的场景：需要快速数据响应和处理的工作，如实时行情监测、高频交易等

### 重要提示

- 此工具包仅限个人使用，请勿用于任何商业用途
- 使用此工具包需先自行购买开通Wind API，Bloomberg API等付费数据服务权限
- 开发者未对工具包的功能进行全面、严格的测试，不保证各项功能在任何情况下都可以正常使用，不保证使用此工具包获取的数据的完整性和准确性，使用此工具包带来的任何后果和责任与开发者无关
- *欢迎留言，作者将认真听取您的建议和意见，并进行持续更新*

### 工具包构成

现有构成：

> - datafeed：集中调用datafeed_wind，datafeed_fred，datafeed_chinabond等实现从各数据源（Wind，FRED，中债）读取数据，并返回统一的数据格式（注：datafeed_chinabond.py暂不公开发布）
> - datetools：处理日期时间数据（目前主要依托Wind API）
> - plottools：基于matplotlib/seaborn的常用金融图表绘制工具
> - utils：其他支持型工具函数

以下功能在开发过程中，后期将逐步整合至工具包中，并对现有文件架构进行调整：

> - datafeed_quandl：对Quandl API进行封装与功能整合、完善
> - datafeed_bloomberg：对Bloomberg Python API进行封装与功能整合、完善
> - pfprfm：包含投资组合业绩分析所需的统计模型
> - pfopt：包含进行资产配置所需的各类统计工具和最优化模型

### 关于数据格式

工具包优先使用pandas DataFrame/Series格式，将各数据源返回的数据全部统一转换为该格式，并针对单日期、单字段等数据进行自动格式优化转换。统一数据格式如下:

**时间序列（time series）：**

单字段、多代码：

|   |**code_1**|...|**code_m**|
|-|-:|-:|-:|
|**date_1**|*data*|...|*data*|
|...|...|...|...|
|**date_t**|*data*|...|*data*|

多字段、多代码：

|   |field_1| | |...|field_n| | |
|-|-:|-:|-:|-:|-:|-:|-:|
|   |**code_1**|...|**code_m**|...|**code_1**|...|**code_m**|
|**date_1**|*data*|...|*data*|...|*data*|...|*data*|
|...|...|...|...|...|...|...|...|
|**date_t**|*data*|...|*data*|...|*data*|...|*data*|

**截面（cross section）：**

|   |**code_1**|...|**code_m**|
|-|-:|-:|-:|
|**field_1**|*data*|...|*data*|
|...|...|...|...|
|**field_n**|*data*|...|*data*|

**面板（panel）：**

|   |  |**code_1**|...|**code_m**|
|-|-:|-:|-:|-:|
|**date_1**|**field_1**|*data*|...|*data*|
| |...|...|...|...|
| |**field_n**|*data*|...|*data*|
|...|...|...|...|...|
|**date_t**|**field_1**|*data*|...|*data*|
| |...|...|...|...|
| |**field_n**|*data*|...|*data*|

### 关于时间（日期）格式

工具包统一（或优先）使用pandas Timestamp时间格式。

# A. 开始使用

## 0. 初始化

使用如下语句调用：

``` python
from pyfintb.datafeed import *
from pyfintb.datetools import *
# 或
from pyfintb.datetools import TODAY, to_pd_timestamp
```

## 1. 金融/经济数据查询

### 1.1 Wind数据源

- 数据权限：需自行购买并开通Wind API使用权限
- 数据查询错误：如遇数据查询错误，函数会自动返回Wind API的错误代码以及对应的错误含义
- 数据量使用提示（测试中）：Wind API分为普通版、高级版、VIP版三种服务，分别对应7×24小时滚动数据查询上限为（按2020年产品手册）：500万单元格、1000万单元格、2000万单元格。当单次查询数据量过大时，工具包的函数会自动提示数据查询量。

#### 1.1.1 获取Wind代码对应的名称

``` python
wind_name(wcode, eng=False)
```

#### 参数：

 - wcode：string，list

 Wind代码：普通代码（如沪深300指数：000300.SH）或板块代码（如Wind中国公募开放式基金板块代码：2001000000000000），目前仅支持单代码查询，若输入包含多个代码的字符串或列表，则只查询第一个代码。

 - eng：bool，默认为False

 是否返回英文名称，默认为返回中文名称。

#### 返回值：

- list

查询单代码或多代码均返回list。

#### 示例：

```python
# 查询000906.SH的中文名称
wind_name("000906.sh") 

# 查询TLT.O的英文名称
wind_name("TLT.O", True) 
```

---

#### 1.1.2 获取指数或板块成分的Wind代码和中文名称

``` python
wind_components(wcode, show_name=False, date=TODAY)
```

#### 参数：

 - wcode：string，list

 Wind代码：普通代码（如沪深300指数：000300.SH）或板块代码（如Wind中国公募开放式基金板块代码：2001000000000000），目前仅支持单代码查询，若输入包含多个代码的字符串或列表，则只查询第一个代码。

 - date：python datetime，pandas Timestamp，numpy datetime64，QuantLib date，支持Wind日期宏（用法详见Wind API文档），支持内置日期常量（后文详述），关于Wind日期宏的使用请参考*Z.提示*

 查询日期：默认为最近交易日。

 - show_name：bool，默认为False

 是否显示成分名称，默认不显示，True将以字典格式返回成份代码和成份名称（key为代码，value为名称）。

#### 返回值：

- list 或 dict

若show_name=False，返回成份代码列表，可直接作为wind_series等函数的输入值；若show_name = True，返回成份代码和成份名称构成的字典。

#### 示例：

```python
# 指数成分查询：
# 查询沪深300指数在最近交易日的成份股
wind_components("000300.sh") 

# 查询中证800指数在上月末的成份股，LME=last month end（上月末）
# 以下返回成份股代码列表
wind_components(["000906.sh"], LME)
# 以下返回成份股代码和成份股名称构成的字典
wind_components("000906.sh", show_name=True) 

# 板块成分查询：
# 查询全部Wind中国公募开放式基金的代码
wind_components("2001000000000000", show_name=True)
```

---

#### 1.1.3 查询市场行情时间序列数据

``` python
wind_series(wcode, field, start_date, end_date=TODAY, col=None, **kwargs)
```

#### 参数：

- wcode：string，list

字符串或列表格式的Wind代码，包括普通代码（如沪深300指数：000300.SH），板块代码（如Wind中国公募开放式基金板块：2001000000000000），宏观经济数据代码（如中国GDP不变价当季同比：M0039354）；支持多代码查询，但不支持普通代码、板块代码或宏观经济数据代码混查（如["000300.SH", "M0039354"]）。

- field：string，list

 字符串或列表格式的查询字段，支持多字段查询；如字段名为“edb”（不区分大小写），则自动查询经济数据库数据，功能等同于使用wind_edb()。

- start_date，end_date：多种日期时间格式：python datetime，pandas Timestamp，numpy datetime64，QuantLib date；支持Wind日期宏（用法详见Wind API文档），支持内置日期常量（后文详述），关于Wind日期宏的使用请参考*Z.提示*

 查询的起止时间，对于市场行情数据，默认截止时间为最近交易日，对于宏观经济数据等，默认截止时间为当日。

- col : string，list

 对数据表列的自定义名称，长度需与代码长度一致；如不定义，则使用所查询的代码作为列名。

- **kwargs

 支持原Wind API函数的各可选参数，具体用法请参考Wind API文档。

#### 返回值：

- pandas DataFrame

 同时查询多代码、多字段时，pandas DataFrame数据表的列标签自动分为field和code两级，field对应字段，code对应代码；由于此数据结构较为复杂，在引用时可读性低，故不建议使用多代码、多字段查询。

#### 示例：

``` python
# 普通数据单代码+多字段查询：
# 查询沪深300指数自2020年1月1日至2020年9月30日区间内的收盘价和成交量（以下代码实现相同功能）
# 可使用字符串或列表作为输入参数，不区分大小写
wind_series("000300.SH", "CLOSE, VOLUME", "2020-01-01", "2020-09-30")
wind_series(["000300.sh"], ["close", "VOLUME"], "2020-01-01", "2020-09-30")
# 使用工具包内置常用时间宏，CYB=current year begin（当年年初）,CQ3E=current 3rd quarter end（当年3季度末）
wind_series("000300.sh", "CLOSE, volume", CYB, CQ3E)

# 普通数据单多代码+多字段查询：
# 查询中证500指数和中证800指数自2020年1月1日至2020年9月30日区间内的开盘价和收盘价
wind_series(["000905.sh", "000906.sh"], "open, close", "2020-01-01", "2020-09-30")
# 查询美股通用电气过去5年每月末的估值（PE_TTM）
wind_series("ge.n", "pe_ttm", "ED-5Y", TODAY, period="m", tradingcalendar="NYSE")

# 宏观经济数据库查询
# 查询过去2年至今的中国工业增加值当月同比和银行间同业拆借7天加权利率（以下代码实现功能相同）
wind_series("M0000545, M0041664", "EDB", "-2Y", TODAY, col=["IP_YOY", "R007"])
```

#### 1.1.4 查询宏观经济（Wind EDB）时间序列数据

``` python
wind_edb(wcode, start_date, end_date=TODAY, period=None, col=None, **kwargs)
```

#### 参数：

 - wcode：string，list

 字符串或列表格式的Wind EDB指标代码；支持多代码查询。

 - start_date，end_date：多种日期时间格式：python datetime，pandas Timestamp，numpy datetime64，QuantLib date；支持Wind日期宏（用法详见Wind API文档），支持内置日期常量（后文详述），关于Wind日期宏的使用请参考*Z.提示*

 查询的起止时间，默认截止时间为当日。

 - period：string，默认为None

 数据时间周期，y=年，q=季度，m=月，w=周，d=日；默认为None，即返回edb函数返回的原始数据，若指定周期，则对edb函数返回的原始时间序列进行变频（resampling）。注意：在Wind EDB中读取市场行情数据（如沪深300指数收盘点位，对应EDB代码M0020209）时，若不指定period，则返回数据对应的日期为“不规则的”交易所日历日，若设定period为某个特定时间周期，此函数会自动将交易所日历日与自然日对齐，并按照forward filling方法填充非交易日的数据，这样处理是为了保证行情数据能够与同频率的宏观经济数据在日期上对齐，以便进行时间序列计算或画图。

- col : string，list

 对数据表列的自定义名称，长度需与代码长度一致；如不定义，则使用所查询的代码作为列名。

 - **kwargs

 支持原Wind API函数的各可选参数，具体用法请参考Wind API文档。

#### 返回值：

- pandas DataFrame

#### 示例：

``` python
# 查询过去2年至今的中国工业增加值当月同比和银行间同业拆借7天加权利率（以下代码实现功能相同）
wind_edb(["M0000545", "M0041664"], "-2Y", TODAY)
wind_series("M0000545, M0041664", "EDB", "-2Y", TODAY)
```

---

#### 1.1.5 查询截面数据（测试中）

``` python
wind_crosec(wcode, field, **kwargs) # 普通截面数据查询
```

#### 参数：

 - wcode：string，list

 字符串或列表格式的Wind代码，包括普通代码和板块代码；支持多代码查询

 - field：string，list

 字符串或列表格式的查询字段，支持多字段查询；不建议使用多代码、多指标查询，避免数据表结构过于复杂

 - **kwargs

 支持原Wind API函数的各可选参数；查询截面数据的可选参数规则多样，请先查询Wind API文档或使用Wind终端的代码生成器（快捷键：CG）查询

---

#### 返回值：

- pandas DataFrame

#### 示例：

```python
# 板块成分查询：
# 查询全部Wind中国公募开放式基金的一级分类和二级分类
fund_code = wind_components("2001000000000000")[:100] # Wind中国公募开放式基金（取钱100）
fields = [
    "fund_firstinvesttype", # 基金类别-证监会规则
    "fund_investtype2", # 基金类别-Wind规则：证监会规则下的细类（二级：fundtype=2）
    ]
fund_type = wind_crosec(fund_code, fields, tradedate=TODAY, fundtype=2)
```

#### 1.1.6 查询面板数据查询（开发中）

``` python
wind_panel(wcode, field, start_date, end_date=TODAY, **kwargs)
```

---

### 1.2 FRED数据源

致谢：基于[fredapi: Python API for FRED (Federal Reserve Economic Data)](https://github.com/mortada/fredapi "fredapi: Python API for FRED (Federal Reserve Economic Data")构建

#### 1.2.1 宏观经济或市场行情时间序列数据查询

``` python
fred_series(fredcode, start_date, end_date=TODAY, **kwargs)
```

#### 参数：

 - fredcode：string，list

 字符串格式的FRED代码；支持不多代码查询

 - start_date，end_date：多种日期时间格式：python datetime，pandas Timestamp，numpy datetime64，QuantLib date；不支持Wind日期宏，支持内置日期常量（后文详述），关于Wind日期宏的使用请参考*Z.提示*

 查询的起止时间，对于市场行情数据，默认截止时间为最近交易日，对于宏观经济数据等，默认截止时间为当日

 - **kwargs

 支持FRED API的各可选参数，具体用法请参考[FRED文档](https://fred.stlouisfed.org/docs/api/fred/series_observations.html "FRED文档")

#### 返回值：

- pandas DataFrame
##### 示例：

```python
# 查询2020年初至今的美国国债10年期-2年期利差（周频）
fred_series("T10Y2Y", "2020-01-01", TODAY, frequency="w")

# 查询ICE BofA美国高收益债券OAS
fred_series("BAMLH0A0HYM2", "2021-01-01", "2021-01-31")
```

#### 1.2.2 FRED指标信息查询

``` python
fred_id_info(fredcode)
```

#### 参数：

 - fredcode：string，list

 字符串格式的FRED代码；支持不多代码查询

#### 返回值：

- pandas Series

#### 示例：

```python
# 查询代码为"T10Y2Y"（美国国债10年期-2年期利差）指标的详情信息
fred_id_info("T10Y2Y")
```

## 2. 日期处理

 - 支持Wind日期宏和内置日期常量
 - 返回日期的格式均为pandas Timestamp
 - 默认按上海证券交易所交易日历（Wind参数名为“sse”）进行计算，可输入可选参数调整至不同交易所交易日历，具体方法参考Wind Python API文档

### 2.1 交易日处理

函数功能较为简单，不再具体说明参数，使用方法参考下方示例：

``` python
# 返回最近交易日
td_prev() # 默认为今日
td_prev("2020-09-09")

# 返回下一个交易日
td_next() # 默认为今日
td_next("2010-08-08")

# 判断该日期是否为交易日
td_is() # 默认为今日
td_is("2020-01-01")

# 返回向前或向后指定距离的交易日
td_offset("-3y", "2020-09-09") # 2020年9月9日向前3年的最近交易日
td_offset("1M", YESTERDAY) # 昨天向后1月的最近交易日，YESTERDAY为内置日期常量

# 计算两个时间点之间的天数
td_count("-1Y", LQE) # 一年前至上季度末之间的交易日天数
td_count("2020-03-03", CMB, days="alldays") # 2020年3月3日至本月初的日历日天数
```

### 2.2 内置日期常量

内置日期常量，功能与Wind日期宏近似，格式均为pandas Timestamp，值为日历日日期，可直接作为各函数的输入参数。

常量内容如下：
|常量名（均为大写）|对应日期（日历日）|
|---|---|
|TODAY|今日|
|YESTERDAY|昨日|
|TOMORROW|明日|
|LMB, LME|上月初, 上月末|
|LQB, LQE|上季度初, 上季度末|
|LYB, LYE|上年初, 上年末|
|CMB, CME|当月初, 当月末|
|CQB, CQE|当季初, 当季末|
|CYB, CYE|当年初, 当年末|
|LQ1B ... LQ4B|去年1季度初 ... 去年4季度初|
|LQ1E ... LQ4E|去年1季度末 ... 去年4季度末|
|CQ1B ... CQ4B|当年1季度初 ... 当年4季度初|
|CQ1E ... CQ4E|当年1季度末 ... 当年4季度末|
|E1W|1周前|
|E2W|2周前|
|E3W|3周前|
|E1M, E2M ... E12M|1月前, 2月前 ... 12月前（含各月）|
|E1Y, E2Y ... E10Y|1年前, 2年前 ... 10年前（含各年）|
|E15Y, E20Y ... E50Y|15年前, 20年前 ... 50年前（每5年递增）|

命名规则（助记规则）：

 - LME = Last Month End：L = Last, M = Month, Q = Quarter, Y = Year
 - CYB = Current Year Begin：C = Current, M = Month, Q = Quarter, Y = Year
 - CQ1E = Current 1st Quarter End
 - E3Y = Ealier 3 Year, E*n*P = Ealier *n* Periods：E = Ealier, W = Week, M = Month, Y = Year

### 2.3 内置交易所每年交易日数常量

为实现精确的计算，内置主要交易所每年交易日数常量（格式为整数），该数据为交易所过去10年（样本为2010年-2019年）每年交易日数的算术平均数的近似整数，具体如下：

| 常量名（均为大写） | 交易所英文名称                   | 交易日数 |
| ------------------ | -------------------------------- | --------: |
| TDPYR_SSE          | Shanghai Stock Exchange          | 243      |
| TDPYR_SZSE         | Shenzhen Stock Exchange          | 243      |
| TDPYR_HKEX         | Stock Exchange of Hong Kong      | 256      |
| TDPYR_SHFE         | Shanghai Futures Exchange        | 243      |
| TDPYR_DCE          | Dalian Commodity Exchange        | 243      |
| TDPYR_ZCE          | Zhengzhou Commodity Exchange     | 243      |
| TDPYR_CFFE         | China Financial Futures Exchange | 243      |
| TDPYR_NYSE         | New York Stock Exchange          | 252      |
| TDPYR_NASDAQ       | Nasdaq                           | 252      |
| TDPYR_AMEX         | American Stock Exchange          | 252      |
| TDPYR_CME          | Chicago Mercantile Exchange      | 252      |
| TDPYR_COMEX        | New York Mercantile Exchange     | 252      |
| TDPYR_CBOT         | Chicago Board of Trade           | 252      |
| TDPYR_NYBOT        | New York Board of Trade          | 252      |
| TDPYR_LSE          | London Stock Exchange            | 253      |
| TDPYR_LME          | London Metal Exchange            | 253      |
| TDPYR_IPE          | International Petroleum Exchange | 256      |
| TDPYR_TSE          | Japan Exchange Group             | 245      |

说明：上表常量名称命名规则为"TDPYR_交易所简称"，TDPYR为Trading Days Per YeaR，交易所简称与Wind API内置的简称一致

---

## 3. 其他功能

### 3.1 指标间快速计算
``` python
cols_calc(formula, data)
```
支持使用“Patsy算式”（类似R formulas）进行指标间计算，极大提高宏观经济数据等的处理效率，例如：
计算M1-M2剪刀差，原始数据为包含M1同比增速和M2同比增速的名为data的pandas DataFrame，列名分别为m1_yoy, m2_yoy
则可使用cols_calc()函数得到M1-M2剪刀差时间序列的pandas DataFrame：

```python
# 第一步：读取M2，M1同比数据
data = wind_series("M0001385, M0001383", "EDB", "2010-01-01", "2020-01-01")
data.columns = ["m2_yoy", "m1_yoy"]
# 第二步：直接结算M1-M2剪刀差
m2m1_diff = cols_calc("m2_yoy - m1_yoy", data)
```

除四则运算外，还支持numpy，pandas内置的各种运算符或函数，如：

```python
# 以下算式或不具有经济学含义，仅用于示例说明
cols_calc("np.log(m2_yoy) - m1_yoy", data)
cols_calc("m2_yoy.rolling(5).mean() + m1_yoy.pct_change(2)", data)
```

关于“Patsy算式”具体用法可参考[Patsy文档](https://patsy.readthedocs.io/en/latest/formulas.html "Patsy文档")。

### 3.2 年度截面数据groupby

支持将周频、月频、季频时间序列数据按所属年份分拆，并按照指定频率对齐，用于分析某时间序列的在年内的季度变化特性：

``` python
df_groupby_year(df, period="m", method="last"):
```

#### 参数：

 - df：pandas DataFrame

 待拆分的时间序列数据，仅支持单列

 - period：string

 数据时间周期，y=年，q=季度，m=月，w=周，d=日；默认为月；可进行降频处理，不支持升频处理
 
 - method：string
 
 对数据进行降频处理时，支持两种方式：method="mean"取区间内平均值，method="last"取区间内最后一个值；默认为"last"

#### 返回值：

- pandas DataFrame

 返回的DataFrame的index为时间（如月数：1、2...12，周数：1、2...52等），columns为年份

#### 示例：

```python
# 将2015年至2020年的中国制造业PMI拆分至各年
df = wind_edb("M0017126", "2015-01-01", "2020-12-31", col="CHN_NBS_MNF_PMI")
df_groupby_year(df)
```

---

# Z. 提示

### 不推荐使用Wind日期宏（Date Macros）

Wind API提供日期宏功能，特定的字符串代表对应的日期（如"LME"表示上月末的日期），能够让使用者较简便地书写代码。但是不推荐使用Wind日期宏，主要原因在于日期宏为字符串格式，仅能够被Wind API内置函数识别，无法直接参与其他计算，并且在对Wind API内置函数进行功能封装时，容易造成难以预计的错误。推荐使用此工具包内置的日期常量，格式均为pandas Timestamp，能够参与各类计算。

### 不推荐单次查询过大的数据量

Wind API内置函数有单次查询数据量上限，如（wsd单次查询数据量为8000单元格，其他详见Wind API文档），此工具包通过循环查询+自动拼接的方式可以实现“理论上”单次任意查询量，但仍不推荐单次查询过大的数据量（如全部A股在过去5年的收盘价数据对应约300万单元格的数据量），原因如下：1、由于进行循环查询，可能导致查询较慢，当网络不稳定时易造成查询失败；2、大量查询会占用过多数据流量，超限后会导致未来7x24小时无法再使用Wind API中的大部分函数查询功能；3、由于第2项原因，开发者难以对超大数据查询进行足够的测试，因此可能存在功能不稳定的情况。

### 对代码格式的判断可能有误

为了进一步简化Wind API函数的使用操作，此工具包中部分函数会对输入的Wind代码进行自动识别。由于Wind未公开普通Wind代码（如股票代码、基金代码、债券代码等）、板块代码（如全部A股板块代码、中国开放式公募基金板块代码等）、宏观经济数据库代码（如工业增加值当月同比代码）的命名规则，此工具包仅依据可查的代码总结其命名规律。因此在通过代码格式判断其类别时，可能存在判断有误的情况（尽管已经进行了大量的测试）。

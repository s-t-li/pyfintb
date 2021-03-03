import patsy
import pandas as pd

# convert a string with commas(,) to a list
# regularize a list by remove spaces( ) in it
def to_list(x):
    neat_list = list()
    if isinstance(x, str):
        neat_list = x.replace(" ", "").split(",")
    elif isinstance(x, (list, type({}.keys()), type({}.values()))):
        for i, v in enumerate(x):
            if " " in v:
                x[i] = x[i].replace(" ", "")
        neat_list = list(filter(None, x))
    return neat_list

# covert a pandas.Series to a 1-D numpy.ndarray
def flatten(arr):
    return arr if not isinstance(arr, pd.Series) else arr.values

def list_slice(list_like, piece_len = 1000):
    list_len = len(list_like)
    for i in range(0, list_len, piece_len):
        yield list_like[i:i+piece_len]
        
def cols_calc(formula, dataframe, col=None):
    formula_like = "I(" + formula + ")-1"
    result = patsy.dmatrix(formula_like, dataframe, NA_action='drop', return_type="dataframe")
    result.columns = [formula] if col is None else [col]
    return result

def df_groupby_year(df, period="m", method="last"):
    df.columns = ["value"]
    df["year"] = df.index.year
    df["quarter"] = df.index.quarter
    df["month"] = df.index.month
    df["week"] = df.index.isocalendar().week
    df = df.reset_index()
    if method == "last":
        agg = df.groupby([pd.Grouper(freq=period, key="index")]).last().groupby("year")
    if method == "mean":
        agg = df.groupby([pd.Grouper(freq=period, key="index")]).mean().groupby("year") 
    
    result_df = pd.DataFrame()
    for year, i in agg:
        i.index = i[{"y": "year", "q": "quarter", "m": "month", "w": "week"}[period.lower()]]
        sub_df = i[["value"]]
        sub_df.columns = [year]
        result_df = pd.concat([result_df, sub_df], axis=1)
    return result_df
        
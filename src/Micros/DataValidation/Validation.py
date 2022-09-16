import pandas as pd 

def is_text(series: pd.Series) -> bool:
    return str(series.dtype) == "string"

def is_numeric(series: pd.Series) -> bool:
    return str(series.dtype) == "Int64" or str(series.dtype) == "Float64"

def is_datetime(series: pd.Series) -> bool:
    return str(series.dtype) == "DateTime64"

import pandas as pd 

def is_text(series: pd.Series) -> bool:
    return \
        str(series.dtype) == "string" \
        or str(series.dtype) == "String"

def is_number(series: pd.Series) -> bool:
    return \
        str(series.dtype) == "int64" \
        or str(series.dtype) == "Int64" \
        or str(series.dtype) == "float64"\
        or str(series.dtype) == "Float64"

def is_object(series: pd.Series) -> bool:
    return \
        str(series.dtype) == "object" \
        or str(series.dtype) == "Object" 

def is_datetime(series: pd.Series) -> bool:
    return \
        str(series.dtype) == "datetime64[ns]" \
        or str(series.dtype) == "DateTime64[ns]"

import pandas as pd 
import re

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

def is_year(series: pd.Series) -> bool:
    for _, value in series.iteritems():
        if re.search(r"^[\d][\d][\d][\d]$", value) == None:
            return False

    return True

def is_date(series: pd.Series) -> bool:
    for _, value in series.iteritems():
        if re.search(r"^[\d]+[-][\d][\d][-][\d][\d]$", value) == None:
            return False

    return True
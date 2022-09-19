from typing import Any

from bs4 import BeautifulSoup
import requests

from Application.Config.Endpoints import EP_XE_RATE
from Application.Config.Paths import PATH_CURRENCY_CODES
from Application.Config.Paths import PATH_CURRENCY_RATES

import dateparser
import numpy as np
import pandas as pd

def convert_strings() -> None:
    return NotImplemented

def convert_numbers() -> None: 
    return NotImplemented

def convert_datetimes(value: Any) -> None:  
    if type(value) == float:
        if np.isnan(value):
            return np.NaN

    if type(value) == str and value != "—":
        return dateparser.parse(value).strftime("%Y-%m-%d")

def convert_currencies(value: Any, src: str = None, des: str = "USD") -> float:
    currency_codes_df = pd.read_json(PATH_CURRENCY_CODES)
    currency_rates_df = pd.read_json(PATH_CURRENCY_RATES)

    for index, symbol in currency_rates_df["From"].iteritems():            
        if src == symbol and des == currency_rates_df["To"].iloc[index]:
            rate = currency_rates_df["Rate"].iloc[index]
            return float(value) * currency_rates_df["Rate"].iloc[index] 

    return np.NaN

def update_exchange_rates() -> None:
    currency_codes_df = pd.read_json(PATH_CURRENCY_CODES, encoding="utf-8-sig")
    currency_rates_df = pd.DataFrame(columns=["Amount", "From", "To", "Rate"])
    for _, code in currency_codes_df["Code"].iteritems():
        src = code
        des = "USD"

        endpoint = EP_XE_RATE.replace("{src}", src).replace("{des}", des)
        response = requests.get(endpoint)
        soup = BeautifulSoup(response.text, "lxml")
        element = soup.select_one("#__next > div:nth-child(2) > div.fluid-container__BaseFluidContainer-qoidzu-0.gJBOzk > section > div:nth-child(2) > div > main > form > div:nth-child(2) > div:nth-child(1) > p.result__BigRate-sc-1bsijpp-1.iGrAod")
        ex_rate = float(element.text
            .replace(" US Dollars", "")
            .replace(" US Dollar", "").strip())                

        print(f"Exchange rate from {src} to {des}: {ex_rate:.3f}")

        currency_rates_df.loc[len(currency_rates_df.index)] = [1, src, des, ex_rate]

    currency_rates_df.to_json(PATH_CURRENCY_RATES)

    return None 
from typing import Any
from datetime import datetime
import os, re

import numpy as np
import pandas as pd   

from Functions.DataAnalysis import Converter
from Functions.DataAnalysis import Analyzer
from Functions.DataAnalysis import Validator

def convert_currency(value: Any, src: str = None, des: str = "USD") -> float:

    if src == None:      
        if type(value) == float:                
            if np.isnan(value):
                return np.NaN  

        if type(value) == str:   
            if "$" in value \
                and "A$" not in value \
                and "CA$" not in value \
                and "HK$" not in value \
                and "MX$" not in value \
                and "NT$" not in value \
                and "NZ$" not in value \
                and "R$" not in value:                   
                src = "USD"
                value = value.replace("$", "")
                return float(value)
            if "A$" in value and "CA$" not in value: 
                src = "AUD"
                value = value.replace("A$", "") 
            if "CA$" in value: 
                src = "CAD"
                value = value.replace("CA$", "") 
            if "HK$" in value: 
                src = "HKD"
                value = value.replace("HK$", "") 
            if "MX$" in value: 
                src = "MXN"
                value = value.replace("MX$", "") 
            if "NT$" in value: 
                src = "TWD"
                value = value.replace("NT$", "")                     
            if "NZ$" in value: 
                src = "NZD"
                value = value.replace("NZ$", "")                     
            if "R$" in value: 
                src = "BRL"
                value = value.replace("R$", "") 
            if "€" in value: 
                src = "EUR"
                value = value.replace("€", "")
            if "£" in value: 
                src = "GBP"
                value = value.replace("£", "")
            if "₹" in value: 
                src = "INR"
                value = value.replace("₹", "")
            if "₪" in value: 
                src = "ILS"
                value = value.replace("₪", "")
            if "₩" in value: 
                src = "KRW"
                value = value.replace("₩", "")
            if "₱" in value:
                src = "PHP"
                value = value.replace("₱", "")
            if "¥" in value and "CN¥" not in value: 
                src = "JPY"
                value = value.replace("¥", "")
            if "CN¥" in value: 
                src = "CNY"
                value = value.replace("CN¥", "")
            if "SGD" in value: 
                src = "SGD"
                value = value.replace("SGD", "")
            if "CHF" in value: 
                src = "CHF"
                value = value.replace("CHF", "")
            if "NAD" in value: 
                src = "NAD"
                value = value.replace("NAD", "")
            if "SDG" in value: 
                src = "SDG"
                value = value.replace("SDG", "")
            if "SEK" in value: 
                src = "SEK"
                value = value.replace("SEK", "")
            if "ZAR" in value: 
                src = "ZAR"
                value = value.replace("ZAR", "")
            if "IDR" in value:
                src = "IDR"
                value = value.replace("IDR", "")
            if "HUF" in value:
                src = "HUF"
                value = value.replace("HUF", "")
            if "AED" in value:
                src = "AED"
                value = value.replace("AED", "")
            if "PLN" in value:
                src = "PLN"
                value = value.replace("PLN", "")
            if "MYR" in value:
                src = "MYR"
                value = value.replace("MYR", "")
            if "RUB" in value:
                src = "RUB"
                value = value.replace("RUB", "")
            if "NGN" in value:
                src = "NGN"
                value = value.replace("NGN", "")
            if "LKR" in value:
                src = "LKR"
                value = value.replace("LKR", "")
            if "BDT" in value:
                src = "BDT"
                value = value.replace("BDT", "")
            if "EGP" in value:
                src = "EGP"
                value = value.replace("EGP", "")
            if "NOK" in value:
                src = "NOK"
                value = value.replace("NOK", "")
            if "SAR" in value:
                src = "SAR"
                value = value.replace("SAR", "")
            if "TRY" in value:
                src = "SAR"
                value = value.replace("TRY", "")

    rate = Converter.convert_currency(value, src, des)
    if src == None: src = "USD"
    print(f"Exchange rate from {src} to {des}: {rate:.3f}")
    return float(value) * rate 

class CrunchBaseAcquisitionData:

    def collect() -> None:
        return NotImplemented 

    def clean() -> None:

        print("Enter input file path: ", end="")
        i_fil = input().replace("\"", "")  

        print("Enter output folder path: ", end="")
        o_fol = input().replace("\"", "")  

        print("Enter output file name: ", end="")
        o_fil = input().replace(" ", "")  

        try:
            df = pd.read_csv(i_fil, encoding="utf-8-sig")
        except:
            raise Exception("cannot read data from file")

        df = df.replace(r"—", np.NaN)     
        df = df.convert_dtypes()  
        
        df["Price"] = df["Price"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)
        
        df["Acquiree Total Funding Amount"] = df["Acquiree Total Funding Amount"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)             
        
        df["Acquirer Total Funding Amount"] = df["Acquirer Total Funding Amount"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Announced Date"] = df["Announced Date"]\
            .apply(Converter.convert_date)

        df["Acquiree Funding Status"] = df["Acquiree Funding Status"]\
            .apply(lambda x: x.replace("&amp;", "&") if type(x) == str else np.NaN)

        df["Acquirer Funding Status"] = df["Acquirer Funding Status"]\
            .apply(lambda x: x.replace("&amp;", "&") if type(x) == str else np.NaN)

        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}"))

        return None

    def select() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")
        o_fil = input("Enter output file name: ").replace(" ", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")
        
        ### 3
        df = df[fields]

        ### 4
        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"                
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None

    def describe() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")
        
        ### 3
        df = df[fields]

        for label, series in df.iteritems():
            try:  
                check_value = series.iloc[series.first_valid_index()]
                if re.search(r"^[\d]+[-][\d][\d][-][\d][\d]$", check_value) != None:          
                    df[label] = pd.to_datetime(df[label])
                if re.search(r"^[$][\d,.]+$", check_value) != None:
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace("$", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)
                if re.search(r"^[\d,.]+$", check_value) != None:          
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)  
            except:
                continue
        
        df = df.convert_dtypes()

        ### 4
        print("\nGENERAL INFORMATION:")
        print("=" * os.get_terminal_size().columns)

        df.info(verbose=True)

        ### 5
        print("\nDETAILED DATA TABLE:")
        print("=" * os.get_terminal_size().columns)
        print(df, end="\n\n")

        ### 6
        for label, series in df.iteritems():
            if Validator.is_number(series) == True:
                numerical_df = Analyzer.describe_numbers(series)
                print(f"{numerical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"
                numerical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

            if Validator.is_text(series) == True:
                categorical_df = Analyzer.describe_text(series)
                print(f"{categorical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"                
                categorical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None

    def visualize() -> None:
        pass 

class CrunchBaseCompanyData: 

    def collect() -> None:
        return NotImplemented 

    def clean() -> None: 
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Clean companies dataset collected from CrunchBase
        >>> param: None # no param required 
        >>> funct: 0    # read companies data from file
        >>> funct: 1    # clean data, fill and drop NaN values
        >>> funct: 2    # apply elementwise function for type conversion
        >>> funct: 3    # apply conversion functions for datetime
        >>> funct: 4    # apply conversion functions for currencies
        >>> funct: 5    # export cleaned data to file with timestamp
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 0
        print("Enter input file path: ", end="")
        i_fil = input().replace("\"", "")  

        print("Enter output folder path: ", end="")
        o_fol = input().replace("\"", "")  

        print("Enter output file name: ", end="")
        o_fil = input().replace(" ", "")  

        try:
            df = pd.read_csv(i_fil, encoding="utf-8-sig")
        except:
            raise Exception("cannot read data from file")

        ### 1        
        df = df.replace(r"—", np.NaN)     
        df = df.convert_dtypes()

        ### 2
        df["Founded Year"] = df["Founded Year"]\
            .apply(Converter.convert_date)
        df["Founded Year"] = df["Founded Year"]\
            .apply(lambda x: f"{x}"[:4] if type(x) == str else np.NaN)

        ### 3
        df["Exit Date"] = df["Exit Date"]\
            .apply(Converter.convert_date)

        df["Closed Date"] = df["Closed Date"]\
            .apply(Converter.convert_date)

        df["Last Funding Date"] = df["Last Funding Date"]\
            .apply(Converter.convert_date)

        df["Announced Date"] = df["Announced Date"]\
            .apply(Converter.convert_date)

        df["IPO Date"] = df["IPO Date"]\
            .apply(Converter.convert_date)

        df["Delisted Date"] = df["Delisted Date"]\
            .apply(Converter.convert_date)

        df["Last Leadership Hiring Date"] = df["Last Leadership Hiring Date"]\
            .apply(Converter.convert_date)

        df["Last Layoff Mention Date"] = df["Last Layoff Mention Date"]\
            .apply(Converter.convert_date)

        df["Date of Most Recent Valuation"] = df["Date of Most Recent Valuation"]\
            .apply(Converter.convert_date)

        df["Announced Date"] = df["Announced Date"]\
            .apply(Converter.convert_date)

        df["IPO Date"] = df["IPO Date"]\
            .apply(Converter.convert_date)

        df["Delisted Date"] = df["Delisted Date"]\
            .apply(Converter.convert_date)

        df["Last Leadership Hiring Date"] = df["Last Leadership Hiring Date"]\
            .apply(Converter.convert_date)

        df["Last Layoff Mention Date"] = df["Last Layoff Mention Date"]\
            .apply(Converter.convert_date)

        df["Date of Most Recent Valuation"] = df["Date of Most Recent Valuation"]\
            .apply(Converter.convert_date)

        df["Accelerator Application Deadline"] = df["Accelerator Application Deadline"]\
            .apply(Converter.convert_date)

        ### 4
        df["Last Funding Amount"] = df["Last Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)
        
        df["Last Equity Funding Amount"] = df["Last Equity Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)
        
        df["Total Equity Funding Amount"] = df["Total Equity Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)
        
        df["Total Funding Amount"] = df["Total Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Price"] = df["Price"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Money Raised at IPO"] = df["Money Raised at IPO"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Valuation at IPO"] = df["Valuation at IPO"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)     

        df["Funding Status"] = df["Funding Status"]\
            .apply(lambda x: x.replace("&amp;", "&") if type(x) == str else np.NaN)

        df["Acquisition Terms"] = df["Acquisition Terms"]\
            .apply(lambda x: x.replace("&amp;", "&") if type(x) == str else np.NaN)

        ### 5
        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}"))

        return None

    def select() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")
        o_fil = input("Enter output file name: ").replace(" ", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")
        
        ### 3
        df = df[fields]

        ### 4
        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"                
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None

    def describe() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Describe numerical and categorical data for selected fields 
        >>> param: str  # path to file
        >>> funct: 1    # read data from file into data frame
        >>> funct: 2    # inquire user input for data fields
        >>> funct: 3    # convert data fields to correct types
        >>> funct: 4    # show general information about data
        >>> funct: 5    # describe data fields by their types
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")

        df = df[fields]

        ### 3
        for label, series in df.iteritems():

            try:  
                check_value = series.iloc[series.first_valid_index()]
                if re.search(r"^[\d]+[-][\d][\d][-][\d][\d]$", check_value) != None:          
                    df[label] = pd.to_datetime(df[label])
                if re.search(r"^[$][\d,.]+$", check_value) != None:
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace("$", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)
                if re.search(r"^[\d,.]+$", check_value) != None:          
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)     
            except:
                continue

        df = df.convert_dtypes()

        ### 4
        print("\nGENERAL INFORMATION:")
        print("=" * os.get_terminal_size().columns)

        df.info(verbose=True)
        print(end="\n\n")

        ### 5
        print("\nDETAILED DATA TABLE:")
        print("=" * os.get_terminal_size().columns)
        print(df, end="\n\n")

        ### 6
        for label, series in df.iteritems():
            if Validator.is_number(series) == True:
                numerical_df = Analyzer.describe_numbers(series)
                print(f"{numerical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"
                numerical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

            if Validator.is_text(series) == True:
                categorical_df = Analyzer.describe_text(series)
                print(f"{categorical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"                
                categorical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None

    def visualize() -> None:
        pass 

class CrunchBaseContactData:

    def collect() -> None:
        return NotImplemented 

    def clean() -> None:
        print("Enter input file path: ", end="")
        i_fil = input().replace("\"", "")  

        print("Enter output folder path: ", end="")
        o_fol = input().replace("\"", "")  

        print("Enter output file name: ", end="")
        o_fil = input().replace(" ", "")  

        try:
            df = pd.read_csv(i_fil, encoding="utf-8-sig")
        except:
            raise Exception("cannot read data from file")

        df = df.replace(r"—", np.NaN)     
        df = df.convert_dtypes()

        df["Number of Contact Emails"] = pd.to_numeric(df["Number of Contact Emails"])        
        df["Number of Contact Phones"] = pd.to_numeric(df["Number of Contact Phones"])

        df["Organization Last Funding Date"] = df["Organization Last Funding Date"]\
            .apply(Converter.convert_date)

        df["Organization Last Funding Amount"] = df["Organization Last Funding Amount"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)                 

        df["Organization Total Funding Amount"] = df["Organization Total Funding Amount"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Job Departments"] = df["Job Departments"]\
            .apply(lambda x: x.replace("&nbsp;", " ") if type(x) == str else np.NaN)

        df["Job Departments"] = df["Job Departments"]\
            .apply(lambda x: x.replace("&amp;", "&") if type(x) == str else np.NaN)

        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}"))

        return None  

    def select() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")
        o_fil = input("Enter output file name: ").replace(" ", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")
        
        ### 3
        df = df[fields]

        ### 4
        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"                
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None

    def desribe() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Describe numerical and categorical data for selected fields 
        >>> param: str  # path to file
        >>> funct: 1    # read data from file into data frame
        >>> funct: 2    # inquire user input for data fields
        >>> funct: 3    # convert data fields to correct types
        >>> funct: 4    # show general information about data
        >>> funct: 5    # describe data fields by their types
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")

        df = df[fields]

        ### 3
        for label, series in df.iteritems():

            try:  
                check_value = series.iloc[series.first_valid_index()]
                if re.search(r"^[\d]+[-][\d][\d][-][\d][\d]$", check_value) != None:          
                    df[label] = pd.to_datetime(df[label])
                if re.search(r"^[$][\d,.]+$", check_value) != None:
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace("$", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)
                if re.search(r"^[\d,.]+$", check_value) != None:          
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)     
            except:
                continue

        df = df.convert_dtypes()

        ### 4
        print("\nGENERAL INFORMATION:")
        print("=" * os.get_terminal_size().columns)

        df.info(verbose=True)
        print(end="\n\n")

        ### 5
        print("\nDETAILED DATA TABLE:")
        print("=" * os.get_terminal_size().columns)
        print(df, end="\n\n")

        ### 6
        for label, series in df.iteritems():
            if Validator.is_number(series) == True:
                numerical_df = Analyzer.describe_numbers(series)
                print(f"{numerical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"
                numerical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

            if Validator.is_text(series) == True:
                categorical_df = Analyzer.describe_text(series)
                print(f"{categorical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"                
                categorical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None  

    def visualize() -> None:
        return None  

class CrunchBaseEventData:

    def collect() -> None:
        return NotImplemented 

    def clean() -> None:

        print("Enter input file path: ", end="")
        i_fil = input().replace("\"", "")  

        print("Enter output folder path: ", end="")
        o_fol = input().replace("\"", "")  

        print("Enter output file name: ", end="")
        o_fil = input().replace(" ", "")  

        try:
            df = pd.read_csv(i_fil, encoding="utf-8-sig")
        except:
            raise Exception("cannot read data from file")

        df = df.replace(r"—", np.NaN)     
        df = df.convert_dtypes()

        df["Start Date"] = df["Start Date"]\
            .apply(Converter.convert_date)
        df["End Date"] = df["End Date"]\
            .apply(Converter.convert_date)

        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}"))

        return None  

    def select() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")
        o_fil = input("Enter output file name: ").replace(" ", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")
        
        ### 3
        df = df[fields]

        ### 4
        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"                
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None

    def desribe() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Describe numerical and categorical data for selected fields 
        >>> param: str  # path to file
        >>> funct: 1    # read data from file into data frame
        >>> funct: 2    # inquire user input for data fields
        >>> funct: 3    # convert data fields to correct types
        >>> funct: 4    # show general information about data
        >>> funct: 5    # describe data fields by their types
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")

        df = df[fields]

        ### 3
        for label, series in df.iteritems():

            try:  
                check_value = series.iloc[series.first_valid_index()]
                if re.search(r"^[\d]+[-][\d][\d][-][\d][\d]$", check_value) != None:          
                    df[label] = pd.to_datetime(df[label])
                if re.search(r"^[$][\d,.]+$", check_value) != None:
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace("$", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)
                if re.search(r"^[\d,.]+$", check_value) != None:          
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)     
            except:
                continue

        df = df.convert_dtypes()

        ### 4
        print("\nGENERAL INFORMATION:")
        print("=" * os.get_terminal_size().columns)

        df.info(verbose=True)
        print(end="\n\n")

        ### 5
        print("\nDETAILED DATA TABLE:")
        print("=" * os.get_terminal_size().columns)
        print(df, end="\n\n")

        ### 6
        for label, series in df.iteritems():
            if Validator.is_number(series) == True:
                numerical_df = Analyzer.describe_numbers(series)
                print(f"{numerical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"
                numerical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

            if Validator.is_text(series) == True:
                categorical_df = Analyzer.describe_text(series)
                print(f"{categorical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"                
                categorical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None  

    def visualize() -> None:
        return None

class CrunchBaseFundingData:

    def collect() -> None:
        return NotImplemented 

    def clean() -> None:

        print("Enter input file path: ", end="")
        i_fil = input().replace("\"", "")  

        print("Enter output folder path: ", end="")
        o_fol = input().replace("\"", "")  

        print("Enter output file name: ", end="")
        o_fil = input().replace(" ", "")  

        try:
            df = pd.read_csv(i_fil, encoding="utf-8-sig")
        except:
            raise Exception("cannot read data from file")

        df = df.replace(r"—", np.NaN)     
        df = df.convert_dtypes()

        df["CB Rank (Funding Rounds)"] = df["CB Rank (Funding Rounds)"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN)

        df["Money Raised"] = df["Money Raised"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN) 

        df["Pre-Money Valuation"] = df["Pre-Money Valuation"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN) 

        df["Total Funding Amount"] = df["Total Funding Amount"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN) 

        df["Money Raised"] = df["Money Raised"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)
        
        df["Pre-Money Valuation"] = df["Pre-Money Valuation"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Total Funding Amount"] = df["Total Funding Amount"]\
            .apply(lambda x: x.replace(",", "") if type(x) == str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Announced Date"] = df["Announced Date"].apply(Converter.convert_date)

        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}"))

        return None 

    def select() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")
        o_fil = input("Enter output file name: ").replace(" ", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")
        
        ### 3
        df = df[fields]

        ### 4
        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"                
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None

    def desribe() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Describe numerical and categorical data for selected fields 
        >>> param: str  # path to file
        >>> funct: 1    # read data from file into data frame
        >>> funct: 2    # inquire user input for data fields
        >>> funct: 3    # convert data fields to correct types
        >>> funct: 4    # show general information about data
        >>> funct: 5    # describe data fields by their types
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")

        df = df[fields]

        ### 3
        for label, series in df.iteritems():

            try:  
                check_value = series.iloc[series.first_valid_index()]
                if re.search(r"^[\d]+[-][\d][\d][-][\d][\d]$", check_value) != None:          
                    df[label] = pd.to_datetime(df[label])
                if re.search(r"^[$][\d,.]+$", check_value) != None:
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace("$", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)
                if re.search(r"^[\d,.]+$", check_value) != None:          
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)     
            except:
                continue

        df = df.convert_dtypes()

        ### 4
        print("\nGENERAL INFORMATION:")
        print("=" * os.get_terminal_size().columns)

        df.info(verbose=True)
        print(end="\n\n")

        ### 5
        print("\nDETAILED DATA TABLE:")
        print("=" * os.get_terminal_size().columns)
        print(df, end="\n\n")

        ### 6
        for label, series in df.iteritems():
            if Validator.is_number(series) == True:
                numerical_df = Analyzer.describe_numbers(series)
                print(f"{numerical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"
                numerical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

            if Validator.is_text(series) == True:
                categorical_df = Analyzer.describe_text(series)
                print(f"{categorical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"                
                categorical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None  

    def visualize() -> None:
        pass

class CrunchBaseHubData:

    def collect() -> None:
        return NotImplemented 

    def clean() -> None:

        print("Enter input file path: ", end="")
        i_fil = input().replace("\"", "")  

        print("Enter output folder path: ", end="")
        o_fol = input().replace("\"", "")  

        print("Enter output file name: ", end="")
        o_fil = input().replace(" ", "")  

        try:
            df = pd.read_csv(i_fil, encoding="utf-8-sig")
        except:
            raise Exception("cannot read data from file")

        df = df.replace(r"—", np.NaN)     
        df = df.convert_dtypes()
 
        df["Average Founded Date"] = df["Average Founded Date"]\
            .apply(Converter.convert_date)

        df["Average IPO Date"] = df["Average IPO Date"]\
            .apply(Converter.convert_date)

        df["Average Last Funding Date"] = df["Average Last Funding Date"]\
            .apply(Converter.convert_date)

        df["Last Updated"] = df["Last Updated"]\
            .apply(Converter.convert_datetime)

        df["Total Funding Amount"] = df["Total Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Median Total Funding Amount"] = df["Median Total Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Total Equity Funding Amount"] = df["Total Equity Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Total Amount Raised in IPO"] = df["Total Amount Raised in IPO"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Median Amount Raised in IPO"] = df["Median Amount Raised in IPO"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Total IPO Valuation"] = df["Total IPO Valuation"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Median IPO Valuation"] = df["Median IPO Valuation"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Total Acquired Price"] = df["Total Acquired Price"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Median Acquired Price"] = df["Median Acquired Price"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Total Fund Raised"] = df["Total Fund Raised"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}"))

        return None 

    def select() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")
        o_fil = input("Enter output file name: ").replace(" ", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")
        
        ### 3
        df = df[fields]

        ### 4
        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"                
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None

    def desribe() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Describe numerical and categorical data for selected fields 
        >>> param: str  # path to file
        >>> funct: 1    # read data from file into data frame
        >>> funct: 2    # inquire user input for data fields
        >>> funct: 3    # convert data fields to correct types
        >>> funct: 4    # show general information about data
        >>> funct: 5    # describe data fields by their types
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")

        df = df[fields]

        ### 3
        for label, series in df.iteritems():

            try:  
                check_value = series.iloc[series.first_valid_index()]
                if re.search(r"^[\d]+[-][\d][\d][-][\d][\d]$", check_value) != None:          
                    df[label] = pd.to_datetime(df[label])
                if re.search(r"^[$][\d,.]+$", check_value) != None:
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace("$", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)
                if re.search(r"^[\d,.]+$", check_value) != None:          
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)     
            except:
                continue

        df = df.convert_dtypes()

        ### 4
        print("\nGENERAL INFORMATION:")
        print("=" * os.get_terminal_size().columns)

        df.info(verbose=True)
        print(end="\n\n")

        ### 5
        print("\nDETAILED DATA TABLE:")
        print("=" * os.get_terminal_size().columns)
        print(df, end="\n\n")

        ### 6
        for label, series in df.iteritems():
            if Validator.is_number(series) == True:
                numerical_df = Analyzer.describe_numbers(series)
                print(f"{numerical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"
                numerical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

            if Validator.is_text(series) == True:
                categorical_df = Analyzer.describe_text(series)
                print(f"{categorical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"                
                categorical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None  

    def visualize() -> None:
        pass 

class CrunchBaseInvestorData:

    def collect() -> None:
        return NotImplemented 

    def clean() -> None:

        print("Enter input file path: ", end="")
        i_fil = input().replace("\"", "")  

        print("Enter output folder path: ", end="")
        o_fol = input().replace("\"", "")  

        print("Enter output file name: ", end="")
        o_fil = input().replace(" ", "")  

        try:
            df = pd.read_csv(i_fil, encoding="utf-8-sig")
        except:
            raise Exception("cannot read data from file")

        df = df.replace(r"—", np.NaN)     
        df = df.convert_dtypes()  

        df["Founded Date"] = df["Founded Date"]\
            .apply(Converter.convert_date)
        df["Exit Date"] = df["Exit Date"]\
            .apply(Converter.convert_date)
        df["Closed Date"] = df["Closed Date"]\
            .apply(Converter.convert_date)
        df["Date of Most Recent Valuation"] = df["Date of Most Recent Valuation"]\
            .apply(Converter.convert_date)
        df["IPO Date"] = df["IPO Date"]\
            .apply(Converter.convert_date)
        df["Delisted Date"] = df["Delisted Date"]\
            .apply(Converter.convert_date)
        df["Last Funding Date"] = df["Last Funding Date"]\
            .apply(Converter.convert_date)
 
        df["IT Spend"] = df["IT Spend"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)      
        df["Last Funding Amount"] = df["Last Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)      
        df["Last Equity Funding Amount"] = df["Last Equity Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)      
        df["Total Equity Funding Amount"] = df["Total Equity Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)      
        df["Total Funding Amount"] = df["Total Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)       

        df["Monthly Raised IPO"] = df["Monthly Raised IPO"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)  

        df["Valuation at IPO"] = df["Valuation at IPO"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)   

        df["Funding Status"] = df["Funding Status"]\
            .apply(lambda x: x.replace("&amp;", "&") if type(x) == str else np.NaN)

        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}"))

        return None 

    def select() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")
        o_fil = input("Enter output file name: ").replace(" ", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")
        
        ### 3
        df = df[fields]

        ### 4
        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"                
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None

    def desribe() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Describe numerical and categorical data for selected fields 
        >>> param: str  # path to file
        >>> funct: 1    # read data from file into data frame
        >>> funct: 2    # inquire user input for data fields
        >>> funct: 3    # convert data fields to correct types
        >>> funct: 4    # show general information about data
        >>> funct: 5    # describe data fields by their types
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")

        df = df[fields]

        ### 3
        for label, series in df.iteritems():

            try:  
                check_value = series.iloc[series.first_valid_index()]
                if re.search(r"^[\d]+[-][\d][\d][-][\d][\d]$", check_value) != None:          
                    df[label] = pd.to_datetime(df[label])
                if re.search(r"^[$][\d,.]+$", check_value) != None:
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace("$", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)
                if re.search(r"^[\d,.]+$", check_value) != None:          
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)     
            except:
                continue

        df = df.convert_dtypes()

        ### 4
        print("\nGENERAL INFORMATION:")
        print("=" * os.get_terminal_size().columns)

        df.info(verbose=True)
        print(end="\n\n")

        ### 5
        print("\nDETAILED DATA TABLE:")
        print("=" * os.get_terminal_size().columns)
        print(df, end="\n\n")

        ### 6
        for label, series in df.iteritems():
            if Validator.is_number(series) == True:
                numerical_df = Analyzer.describe_numbers(series)
                print(f"{numerical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"
                numerical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

            if Validator.is_text(series) == True:
                categorical_df = Analyzer.describe_text(series)
                print(f"{categorical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"                
                categorical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None  

    def visualize() -> None:
        pass 

class CrunchBasePeopleData:

    def collect() -> None:
        return NotImplemented 

    def clean() -> None:

        print("Enter input file path: ", end="")
        i_fil = input().replace("\"", "")  

        print("Enter output folder path: ", end="")
        o_fol = input().replace("\"", "")  

        print("Enter output file name: ", end="")
        o_fil = input().replace(" ", "")  

        try:
            df = pd.read_csv(i_fil, encoding="utf-8-sig")
        except:
            raise Exception("cannot read data from file")

        df = df.replace(r"—", np.NaN)     
        df = df.convert_dtypes()  

        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}"))

        return None 

    def select() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")
        o_fil = input("Enter output file name: ").replace(" ", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")
        
        ### 3
        df = df[fields]

        ### 4
        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"                
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None

    def desribe() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Describe numerical and categorical data for selected fields 
        >>> param: str  # path to file
        >>> funct: 1    # read data from file into data frame
        >>> funct: 2    # inquire user input for data fields
        >>> funct: 3    # convert data fields to correct types
        >>> funct: 4    # show general information about data
        >>> funct: 5    # describe data fields by their types
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")

        df = df[fields]

        ### 3
        for label, series in df.iteritems():

            try:  
                check_value = series.iloc[series.first_valid_index()]
                if re.search(r"^[\d]+[-][\d][\d][-][\d][\d]$", check_value) != None:          
                    df[label] = pd.to_datetime(df[label])
                if re.search(r"^[$][\d,.]+$", check_value) != None:
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace("$", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)
                if re.search(r"^[\d,.]+$", check_value) != None:          
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)     
            except:
                continue

        df = df.convert_dtypes()

        ### 4
        print("\nGENERAL INFORMATION:")
        print("=" * os.get_terminal_size().columns)

        df.info(verbose=True)
        print(end="\n\n")

        ### 5
        print("\nDETAILED DATA TABLE:")
        print("=" * os.get_terminal_size().columns)
        print(df, end="\n\n")

        ### 6
        for label, series in df.iteritems():
            if Validator.is_number(series) == True:
                numerical_df = Analyzer.describe_numbers(series)
                print(f"{numerical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"
                numerical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

            if Validator.is_text(series) == True:
                categorical_df = Analyzer.describe_text(series)
                print(f"{categorical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"                
                categorical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None  

    def visualize() -> None:
        pass

class CrunchBaseSchoolData:

    def collect() -> None:
        return NotImplemented 

    def clean() -> None: 
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Clean companies dataset collected from CrunchBase
        >>> param: None # no param required 
        >>> funct: 0    # read companies data from file
        >>> funct: 1    # clean data, fill and drop NaN values
        >>> funct: 2    # apply elementwise function for type conversion
        >>> funct: 3    # apply conversion functions for datetime
        >>> funct: 4    # apply conversion functions for currencies
        >>> funct: 5    # export cleaned data to file with timestamp
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 0
        print("Enter input file path: ", end="")
        i_fil = input().replace("\"", "")  

        print("Enter output folder path: ", end="")
        o_fol = input().replace("\"", "")  

        print("Enter output file name: ", end="")
        o_fil = input().replace(" ", "")  

        try:
            df = pd.read_csv(i_fil, encoding="utf-8-sig")
        except:
            raise Exception("cannot read data from file")

        ### 1        
        df = df.replace(r"—", np.NaN)     
        df = df.convert_dtypes()

        ### 2
        df["Founded Year"] = df["Founded Year"]\
            .apply(Converter.convert_date)
        df["Founded Year"] = df["Founded Year"]\
            .apply(lambda x: f"{x}"[:4] if type(x) == str else np.NaN)

        ### 3
        df["Exit Date"] = df["Exit Date"]\
            .apply(Converter.convert_date)

        df["Closed Date"] = df["Closed Date"]\
            .apply(Converter.convert_date)

        df["Last Funding Date"] = df["Last Funding Date"]\
            .apply(Converter.convert_date)

        df["Announced Date"] = df["Announced Date"]\
            .apply(Converter.convert_date)

        df["IPO Date"] = df["IPO Date"]\
            .apply(Converter.convert_date)

        df["Delisted Date"] = df["Delisted Date"]\
            .apply(Converter.convert_date)

        df["Last Leadership Hiring Date"] = df["Last Leadership Hiring Date"]\
            .apply(Converter.convert_date)

        df["Last Layoff Mention Date"] = df["Last Layoff Mention Date"]\
            .apply(Converter.convert_date)

        df["Date of Most Recent Valuation"] = df["Date of Most Recent Valuation"]\
            .apply(Converter.convert_date)

        df["Announced Date"] = df["Announced Date"]\
            .apply(Converter.convert_date)

        df["IPO Date"] = df["IPO Date"]\
            .apply(Converter.convert_date)

        df["Delisted Date"] = df["Delisted Date"]\
            .apply(Converter.convert_date)

        df["Last Leadership Hiring Date"] = df["Last Leadership Hiring Date"]\
            .apply(Converter.convert_date)

        df["Last Layoff Mention Date"] = df["Last Layoff Mention Date"]\
            .apply(Converter.convert_date)

        df["Date of Most Recent Valuation"] = df["Date of Most Recent Valuation"]\
            .apply(Converter.convert_date)

        df["Accelerator Application Deadline"] = df["Accelerator Application Deadline"]\
            .apply(Converter.convert_date)

        ### 4
        df["Last Funding Amount"] = df["Last Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)
        
        df["Last Equity Funding Amount"] = df["Last Equity Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)
        
        df["Total Equity Funding Amount"] = df["Total Equity Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)
        
        df["Total Funding Amount"] = df["Total Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Price"] = df["Price"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Money Raised at IPO"] = df["Money Raised at IPO"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)

        df["Valuation at IPO"] = df["Valuation at IPO"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
            .apply(convert_currency)\
            .apply(lambda x: "$" + "{0:,}".format(x) if np.isnan(x) == False else np.NaN)     

        df["Funding Status"] = df["Funding Status"]\
            .apply(lambda x: x.replace("&amp;", "&") if type(x) == str else np.NaN)
            
        ### 5
        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}"))

        return None

    def select() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")
        o_fil = input("Enter output file name: ").replace(" ", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")
        
        ### 3
        df = df[fields]

        ### 4
        o_fil = f"{o_fol}\\Dataset @{o_fil} #-------------- .csv"                
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None

    def desribe() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Describe numerical and categorical data for selected fields 
        >>> param: str  # path to file
        >>> funct: 1    # read data from file into data frame
        >>> funct: 2    # inquire user input for data fields
        >>> funct: 3    # convert data fields to correct types
        >>> funct: 4    # show general information about data
        >>> funct: 5    # describe data fields by their types
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 1
        i_fil = input("Enter input file path: ").replace("\"", "")
        o_fol = input("Enter output folder path: ").replace("\"", "")

        df = pd.DataFrame()
        try: 
            if ".csv" in os.path.basename(i_fil):
                df = pd.read_csv(i_fil, parse_dates=True)

            if ".json" in os.path.basename(i_fil):
                df = pd.read_json(i_fil, parse_dates=True)

            if ".xml" in os.path.basename(i_fil):
                df = pd.read_xml(i_fil, parse_dates=True)

            if ".html" in os.path.basename(i_fil): 
                df = pd.read_html(i_fil, parse_dates=True)

        except: 
            raise Exception(f"cannot read file {i_fil}")

        ### 2
        fields = input("Enter data fields: ")
        fields = [field.strip() for field in fields.split(",")]

        for field in fields:
            if field not in df.columns:
                raise Exception(f"field not found {field}")

        df = df[fields]

        ### 3
        for label, series in df.iteritems():

            try:  
                check_value = series.iloc[series.first_valid_index()]
                if re.search(r"^[\d]+[-][\d][\d][-][\d][\d]$", check_value) != None:          
                    df[label] = pd.to_datetime(df[label])
                if re.search(r"^[$][\d,.]+$", check_value) != None:
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace("$", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)
                if re.search(r"^[\d,.]+$", check_value) != None:          
                    df[str(label)] = df[str(label)]\
                        .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)\
                        .apply(lambda x: float(x) if type(x)==str else np.NaN)     
            except:
                continue

        df = df.convert_dtypes()

        ### 4
        print("\nGENERAL INFORMATION:")
        print("=" * os.get_terminal_size().columns)

        df.info(verbose=True)
        print(end="\n\n")

        ### 5
        print("\nDETAILED DATA TABLE:")
        print("=" * os.get_terminal_size().columns)
        print(df, end="\n\n")

        ### 6
        for label, series in df.iteritems():
            if Validator.is_number(series) == True:
                numerical_df = Analyzer.describe_numbers(series)
                print(f"{numerical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"
                numerical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

            if Validator.is_text(series) == True:
                categorical_df = Analyzer.describe_text(series)
                print(f"{categorical_df}", end="\n\n")

                o_fil = f"{o_fol}\\Dataset @{str(label).replace(' ', '')}Analysis #-------------- .csv"                
                categorical_df.to_csv(o_fil, index=False, encoding="utf-8-sig")

                timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
                os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}")) 

        return None  

    def visualize() -> None:
        pass 

class CrunchBaseDatabase:

    CREATE_SCHEMA_QUERY = """..."""
    CREATE_SCHEMA_QUERY = """..."""
    CREATE_SCHEMA_QUERY = """..."""
    CREATE_SCHEMA_QUERY = """..."""
    CREATE_SCHEMA_QUERY = """..."""
    
    CREATE_SCHEMA_QUERY = """..."""
    CREATE_SCHEMA_QUERY = """..."""
    CREATE_SCHEMA_QUERY = """..."""
    CREATE_SCHEMA_QUERY = """..."""
    CREATE_SCHEMA_QUERY = """..."""

from bs4 import BeautifulSoup
from datetime import datetime
import os, re

print("Enter input file: ", end="")
i_fil = input().replace("\"", "")

print("Enter output file: ", end="")
o_fil = input().replace("\"", "")

with open(i_fil, mode="r", encoding="utf8") as file:
    lines = file.readlines()
    urls = [line.replace("\"", "").strip() for line in lines]

TITLE_CSS = "#body > div.row > div.col-lg-9.col-md-8.col-sm-7.col-xs-12 > div > header > h1"
LOCATION_CSS = "#body > div.row > div.col-lg-9.col-md-8.col-sm-7.col-xs-12 > div > div.row.row-eq-height.job-info.m0 > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2)"
SALARY_CSS = "#body > div.row > div.col-lg-9.col-md-8.col-sm-7.col-xs-12 > div > div.row.row-eq-height.job-info.m0 > div:nth-child(1) > table > tbody > tr:nth-child(4)"
JOB_TYPE_CSS = "#body > div.row > div.col-lg-9.col-md-8.col-sm-7.col-xs-12 > div > div.row.row-eq-height.job-info.m0 > div:nth-child(1) > table > tbody > tr:nth-child(3) > td:nth-child(2)"
PHONE_CSS = "#body > div.row > div.col-lg-9.col-md-8.col-sm-7.col-xs-12 > div > div.row.row-eq-height.job-info.m0 > div:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(2) > a"
EMAIL_CSS = "#consultant-info > table > tbody > tr:nth-child(2) > td:nth-child(2) > a"
DATE_POSTED_CSS = "#consultant-info > table > tbody > tr:nth-child(4) > td:nth-child(2)"
DESCRIPTION_CSS = "#body > div.row > div.col-lg-9.col-md-8.col-sm-7.col-xs-12 > div > div.desc > article"
URL_CSS = "head > link:nth-child(4)"

selectors = [TITLE_CSS, LOCATION_CSS, SALARY_CSS, JOB_TYPE_CSS, PHONE_CSS, EMAIL_CSS, DATE_POSTED_CSS,DESCRIPTION_CSS]

dataframe = []
dataframe.append("Job Title,Location,Salary,Job Type,Phone,Email,Date Posted,Description,URL")

for url in urls:
    print(url)

    try:
        with open(url, mode="r", encoding="utf-8-sig") as file:
            html = file.read()
            soup = BeautifulSoup(html, "lxml")
    except:
        print("ERROR: Cannot open file")
        continue

    dataline = []
    for selector in selectors: 
        try: 
            element = soup.select_one(selector)
            text = element.text 
            text = text.replace("\"", "\"\"")
            text = text.replace("- ", "•")
            text = text.replace("● ", "•")
            dataline.append("\"" + text.strip() + "\"")
        except:
            print(f"ERROR: Element not found {selector}")
            dataline.append("Null")
    
    try:
        element = soup.select_one(URL_CSS)
        url = element.get('href')
        dataline.append(url)
    except:
        dataline.append("Null")

    dataframe.append(",".join(dataline))

with open(o_fil, mode="w", encoding="utf-8-sig") as file:
    dataframe = [row + "\n" for row in dataframe]
    file.writelines(dataframe)

timestamp = datetime.fromtimestamp(os.path.getctime(o_fil))
timestamp = timestamp.strftime("%Y%m%d%H%M%S")

os.rename(o_fil, re.sub(r"[#][\d]+", f"#{timestamp}", o_fil))

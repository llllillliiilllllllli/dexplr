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

TITLE_CSS = "#ctl00_mainContent_ctl00_ctl00_pnlInnerWrap > div > section > div > div > div.col-lg-8 > div > div.box-head > h1"
LOCATION_CSS = "#tab-1 > div.job-description.locations > div > ul > li"
SALARY_CSS = "#ctl00_mainContent_ctl00_ctl00_pnlInnerWrap > div > section > div > div > div.col-lg-8 > div > div.box-head > div > p.negotiate.text-orange"
DATE_CSS = "#ctl00_mainContent_ctl00_ctl00_pnlInnerWrap > div > section > div > div > div.col-lg-4 > div.box-job-info.background-light-blue > div:nth-child(2) > p"
JOB_LEVEL_CSS = "#ctl00_mainContent_ctl00_ctl00_pnlInnerWrap > div > section > div > div > div.col-lg-4 > div.box-job-info.background-light-blue > div:nth-child(3) > p"
JOB_CATEGOTY_CSS = "#ctl00_mainContent_ctl00_ctl00_pnlInnerWrap > div > section > div > div > div.col-lg-4 > div.box-job-info.background-light-blue > div:nth-child(4) > p"
SKILL_CSS = "#ctl00_mainContent_ctl00_ctl00_pnlInnerWrap > div > section > div > div > div.col-lg-4 > div.box-job-info.background-light-blue > div:nth-child(5) > p"
LANGUAGE_CSS = "#ctl00_mainContent_ctl00_ctl00_pnlInnerWrap > div > section > div > div > div.col-lg-4 > div.box-job-info.background-light-blue > div:nth-child(6) > p"
DESCRIPTION_CSS = "#tab-1 > div.job-description.description > div"
REQUIREMENT_CSS = "#tab-1 > div.job-description.requirements > div"
URL_CSS = "#ctl00_Head1 > link:nth-child(6)"

selectors = [TITLE_CSS, LOCATION_CSS, SALARY_CSS, DATE_CSS, JOB_LEVEL_CSS, JOB_CATEGOTY_CSS, SKILL_CSS, LANGUAGE_CSS, DESCRIPTION_CSS, REQUIREMENT_CSS]

dataframe = []
dataframe.append("Job Title,Location,Salary,Posted Date,Job Level,Job Category,Skill,Preferred Language,Job Description,Job Requirements,URL")

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
            dataline.append("\"" + text + "\"")
        except:
            print(f"ERROR: Element not found {selector}")
    
    try:
        element = soup.select_one(URL_CSS)
        url = element.get('href')
    except:
        url = "Null"

    dataframe.append(",".join(dataline) + "," + url)

with open(o_fil, mode="w", encoding="utf-8-sig") as file:
    dataframe = [row + "\n" for row in dataframe]
    file.writelines(dataframe)

timestamp = datetime.fromtimestamp(os.path.getctime(o_fil))
timestamp = timestamp.strftime("%Y%m%d%H%M%S")

os.rename(o_fil, re.sub(r"[#][\d]+", f"#{timestamp}", o_fil))

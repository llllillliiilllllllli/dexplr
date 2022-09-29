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

xpaths = [
    "/html/body/div[2]/div/main/article/div/section[1]/div[2]/h1",
    "/html/body/div[2]/div/main/article/div/section[1]/div[2]/div/div[1]/div/p/text()",
    "/html/body/div[2]/div/main/article/div/section[1]/div[2]/div/div[3]/div/p/text()",
    "/html/body/div[2]/div/main/article/div/section[1]/div[2]/div/div[5]/div/p/text()",
    "/html/body/div[2]/div/main/article/div/section[1]/div[2]/div/div[2]/div/p/text()",
    "/html/body/div[2]/div/main/article/div/section[1]/div[2]/div/div[4]/div/p/text()",
    "/html/body/div[2]/div/main/article/div/section[1]/div[2]/div/div[6]/div/p/text()",
]

selectors = [
    "body > div.site-wrapper > div > main > article > div > section.row.job-details__header > div:nth-child(2) > h1",
    "body > div.site-wrapper > div > main > article > div > section.row.job-details__header > div:nth-child(2) > div > div:nth-child(1) > div > p",
    "body > div.site-wrapper > div > main > article > div > section.row.job-details__header > div:nth-child(2) > div > div:nth-child(3) > div > p",    
    "body > div.site-wrapper > div > main > article > div > section.row.job-details__header > div:nth-child(2) > div > div:nth-child(5) > div > p",    
    "body > div.site-wrapper > div > main > article > div > section.row.job-details__header > div:nth-child(2) > div > div:nth-child(2) > div > p",    
    "body > div.site-wrapper > div > main > article > div > section.row.job-details__header > div:nth-child(2) > div > div:nth-child(4) > div > p",    
    "body > div.site-wrapper > div > main > article > div > section.row.job-details__header > div:nth-child(2) > div > div:nth-child(6) > div > p",    
]

contact = "body > div.site-wrapper > div > main > article > div > section.row.job-details__description > div > div > div > div.col-md-7 > div > div > p:nth-child(15) > span:nth-child(1)"
phone = "body > div.site-wrapper > div > main > article > div > section.row.job-details__description > div > div > div > div.col-md-7 > div > div > p:nth-child(15) > span:nth-child(1)"
email = "body > div.site-wrapper > div > main > article > div > section.row.job-details__description > div > div > div > div.col-md-7 > div > div > p:nth-child(15) > a"

dataframe = []
dataframe.append("Job Title,Location,Salary,Experience,Job Type,Job Category,Industry,Job Responsibilities,Experience Requirements,Education Requirements,Contact Person,Phone,Email,URL")

for url in urls:
    print(url)
    try:
        with open(url, mode="r", encoding="utf8") as file:
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
            text = text.replace("Location", "")  
            text = text.replace("Salary", "") 
            text = text.replace("Experience", "")
            text = text.replace("Job type", "")  
            text = text.replace("Category", "") 
            text = text.replace("Industry", "")
            dataline.append("\"" + text + "\"")
        except:
            print(f"ERROR: Element not found {selector}")
            dataline.append("Null")

    text = soup.get_text()

    try: 
        temp = text.split("Job Responsibilities")[1]
        reponsibility = temp.split("Experience requirements")[0]
        dataline.append("\"" + reponsibility.strip() + "\"")
    except: 
        dataline.append("Null")

    try: 
        temp = temp.split("Experience requirements")[1]
        experience = temp.split("Education requirements")[0]
        dataline.append("\"" + experience.strip() + "\"")
    except: 
        dataline.append("Null")
    
    try: 
        temp = temp.split("Education requirements")[1]
        education = temp.split("Contact Person")[0]
        education = education.replace("\"","\"\"")
        dataline.append("\"" + education.strip() + "\"")
    except: 
        dataline.append("Null")

    try: 
        contact = re.search(r"[\w]+[.][\w]+(@adecco.com)", text).group(0)
        contact = contact.replace("@adecco.com", "").replace(".", " ").capitalize()
        dataline.append("\"" + contact.strip() + "\"")
    except:
        dataline.append("Null")

    try:
        phone = re.search(r"[+][8][4][\s\d]+", text).group(0)
        dataline.append("\"" + phone.strip() + "\"")
    except:
        dataline.append("Null")

    try: 
        email = re.search(r"[\w]+[.][\w]+(@adecco.com)", text).group(0)
        dataline.append("\"" + email.strip() + "\"")
    except:
        dataline.append("Null")
    
    dataframe.append(",".join(dataline) + "," + url)

with open(o_fil, mode="w", encoding="utf8") as file:
    dataframe = [row + "\n" for row in dataframe]
    file.writelines(dataframe)

timestamp = datetime.fromtimestamp(os.path.getctime(o_fil))
timestamp = timestamp.strftime("%Y%m%d%H%M%S")

os.rename(o_fil, re.sub(r"[#][\d]+", f"#{timestamp}", o_fil))
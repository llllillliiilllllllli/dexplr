### PROGRAM: Download webpages with given urls

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

print("Enter input file: ", end="")
i_fil = input().replace("\"", "")

print("Enter output folder: ", end="")
o_fol = input().replace("\"", "")

with open(i_fil, mode="r", encoding="utf8") as file:
    lines = file.readlines()
    urls = [line.replace("\"", "").strip() for line in lines]

service = Service(EdgeChromiumDriverManager().install())
options = Options()
#options.add_argument("--disable-extensions")
#options.add_argument("--disable-gpu")
#options.add_argument("--no-sandbox") # linux only
options.add_argument("--headless")

driver = webdriver.Edge(options=options, service=service)

for url in urls:
    driver.get(url)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S") 
    title = url.replace("https://navigossearch.com/", "")  
    title = title.replace("-", " ").title().replace(" ", "") 

    with open(f"{o_fol}\\Webpage @{title} #{timestamp} .html", mode="w", encoding="utf8") as file:
        file.write(driver.page_source)
from bs4 import BeautifulSoup

print("Enter input file: ", end="")
i_fil = input().replace("\"", "")

with open(i_fil, mode="r", encoding="utf-8-sig") as file:
    urls = file.readlines()
    urls = [url.replace("\"", "").strip() for url in urls]

for url in urls:

    with open(url, mode="r", encoding="utf-8-sig") as file:
        html = file.read()
        soup = BeautifulSoup(html, "lxml")

    for link in soup.find_all('a'):
        print(link.get('href'))

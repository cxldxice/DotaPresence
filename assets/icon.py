import requests
import fake_useragent
import bs4
import base64


ua = fake_useragent.UserAgent().random
url = "https://dota2.fandom.com/wiki/Minimap#Icons"


html = requests.get(
    url=url,
    headers={"user-agent": ua},
).text


soup = bs4.BeautifulSoup(html, "html.parser")


hero_table = soup.find("table", class_="wikitable")
for icon in hero_table.find_all("a"):
    name = icon["href"].replace("/wiki/", "") + ".png"
    src = icon.find("img")["data-src"]


    # print(src)
    img = requests.get(src).content

    with open(f"./assets/icons/{name}", "wb") as icon_file:
        icon_file.write(img)

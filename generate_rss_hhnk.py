from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
import time

# URL van HHNK-werkzaamheden
url = 'https://www.hhnk.nl/werk-in-de-buurt-zaanstad'

# Chrome headless setup
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# Open de pagina
driver.get(url)
time.sleep(5)  # Laat de pagina volledig laden

# HTML ophalen en parsen
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Begin RSS-feed
rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
ET.SubElement(channel, 'title').text = 'HHNK Werk in de Buurt – Zaanstad'
ET.SubElement(channel, 'link').text = url
ET.SubElement(channel, 'description').text = 'RSS feed van actuele werkzaamheden in Zaanstad door HHNK'

# Datum voor pubDate (nu)
now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

# Alle items scrapen
for li in soup.select('li.ThreeColumns_threeColumnsItem__uZFkS'):
    a_tag = li.select_one('h2 a')
    desc_tag = li.select_one('div p')
    
    if a_tag and a_tag.text:
        title = a_tag.text.strip()
        link = 'https://www.hhnk.nl' + a_tag['href']
        description = desc_tag.text.strip() if desc_tag else 'Geen omschrijving beschikbaar.'

        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = title
        ET.SubElement(item, 'link').text = link
        ET.SubElement(item, 'description').text = description
        ET.SubElement(item, 'pubDate').text = now
        ET.SubElement(item, 'guid').text = link

driver.quit()

# Schrijf naar bestand
tree = ET.ElementTree(rss)
tree.write('hhnk_feed.xml', encoding='utf-8', xml_declaration=True)

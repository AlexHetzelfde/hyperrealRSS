from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time

# Configureer headless Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# URL van de iBabs-pagina
url = 'https://zaanstad.bestuurlijkeinformatie.nl/Reports/Details/58e397b1-0b36-49e2-90ed-325405f27f72'

# Open de pagina met de headless browser
driver.get(url)
time.sleep(5)  # wacht even zodat JS zijn werk kan doen

# Haal de volledige HTML op
html = driver.page_source
driver.quit()

# Parse de HTML
soup = BeautifulSoup(html, 'html.parser')

# Maak RSS feed
rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
ET.SubElement(channel, 'title').text = 'Zaanstad iBabs RSS Feed'
ET.SubElement(channel, 'link').text = url
ET.SubElement(channel, 'description').text = 'Automatisch gegenereerde feed van Zaanstad stukken'

# Filter op datum (bijvoorbeeld afgelopen 2 dagen)
date_threshold = datetime.now() - timedelta(days=2)

for row in soup.select('tbody tr'):
    pub_date_element = row.select_one('td:nth-child(1) a')
    if pub_date_element and pub_date_element.text:
        try:
            pub_date = datetime.strptime(pub_date_element.text, '%d-%m-%Y')
            if pub_date >= date_threshold:
                rss_item = ET.SubElement(channel, 'item')
                # Titel
                title_element = row.select_one('td:nth-child(2)')
                if title_element and title_element.text:
                    ET.SubElement(rss_item, 'title').text = title_element.text.strip()
                # Link
                ET.SubElement(rss_item, 'link').text = 'https://zaanstad.bestuurlijkeinformatie.nl' + pub_date_element['href']
                # Beschrijving
                desc_element = row.select_one('td:nth-child(4)')
                if desc_element and desc_element.text:
                    ET.SubElement(rss_item, 'description').text = desc_element.text.strip()
                # Datum
                ET.SubElement(rss_item, 'pubDate').text = pub_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        except ValueError:
            print("Datum kon niet gelezen worden:", pub_date_element.text)

# Schrijf RSS naar bestand
tree = ET.ElementTree(rss)
tree.write('feed.xml', encoding='utf-8', xml_declaration=True)

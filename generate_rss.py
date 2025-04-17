from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time

# Lijst van URLs
urls = [
    'https://zaanstad.bestuurlijkeinformatie.nl/Reports/Details/58e397b1-0b36-49e2-90ed-325405f27f72',  # Eerste link
    'https://zaanstad.bestuurlijkeinformatie.nl/Reports/Details/8ea04074-52e6-4284-bd1a-66e378b40ec1'   # Tweede link
]

# Configureer Chrome opties
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# Maak RSS-feed
rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
ET.SubElement(channel, 'title').text = 'Zaanstad iBabs Gecombineerde RSS Feed'
ET.SubElement(channel, 'link').text = urls[0]
ET.SubElement(channel, 'description').text = 'Gecombineerde feed van meerdere Zaanstad stukken'

# Filter op datum (2 dagen + vandaag)
now = datetime.now()
date_threshold = now - timedelta(days=2)

# Functie om data van elke pagina te scrapen
def scrape_url(url):
    driver.get(url)
    time.sleep(5)  # Laat JS laden
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Debug: opslaan van de HTML voor de tweede link
    if url == urls[1]:
        with open("debug_extra_page.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

    for row in soup.select('tbody tr'):
        pub_date_element = row.select_one('td:nth-child(1) a')
        if pub_date_element and pub_date_element.text:
            try:
                pub_date = datetime.strptime(pub_date_element.text.strip(), '%d-%m-%Y')
                if pub_date.date() >= date_threshold.date():
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
                    # Unieke ID
                    ET.SubElement(rss_item, 'guid').text = pub_date_element['href']
            except ValueError:
                print("Kon datum niet parsen:", pub_date_element.text)

# Scrape beide URLs
for url in urls:
    scrape_url(url)

driver.quit()

# Schrijf naar XML bestand
tree = ET.ElementTree(rss)
tree.write('combined_feed.xml', encoding='utf-8', xml_declaration=True)

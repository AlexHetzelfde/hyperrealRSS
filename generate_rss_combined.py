from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time

# Lijst van URLs
urls = [
    'https://zaanstad.bestuurlijkeinformatie.nl/Reports/Details/58e397b1-0b36-49e2-90ed-325405f27f72',  # Werkt
    'https://zaanstad.bestuurlijkeinformatie.nl/Reports/Details/8ea04074-52e6-4284-bd1a-66e378b40ec1'   # Structuur verschilt
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

# Filter op datum (vandaag + 2 dagen terug)
now = datetime.now()
date_threshold = now - timedelta(days=2)

# Scrape-functie
def scrape_url(url):
    driver.get(url)
    time.sleep(5)  # Laat JavaScript laden
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for row in soup.select('tbody tr'):
        cells = row.find_all('td')
        link_element = row.select_one('a[href^="/Reports/Item/"]')
        if not link_element or len(cells) < 3:
            continue

        href = link_element['href']
        link_text = link_element.text.strip()

        try:
            # Structuur 1: link bevat datum
            pub_date = datetime.strptime(link_text, '%d-%m-%Y')
            if pub_date.date() >= date_threshold.date():
                title = cells[1].text.strip() if len(cells) > 1 else 'Geen titel'
                description = cells[3].text.strip() if len(cells) > 3 else ''
        except ValueError:
            # Structuur 2: datum staat elders
            try:
                pub_date = datetime.strptime(cells[2].text.strip(), '%d-%m-%Y')
                if pub_date.date() >= date_threshold.date():
                    title = link_text
                    description = cells[4].text.strip() if len(cells) > 4 else ''
            except ValueError:
                continue  # Overslaan als geen datum te vinden is

        # Voeg item toe aan RSS-feed
        rss_item = ET.SubElement(channel, 'item')
        ET.SubElement(rss_item, 'title').text = title
        ET.SubElement(rss_item, 'link').text = 'https://zaanstad.bestuurlijkeinformatie.nl' + href
        ET.SubElement(rss_item, 'description').text = description
        ET.SubElement(rss_item, 'pubDate').text = pub_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        ET.SubElement(rss_item, 'guid').text = href

# Verwerk alle URLs
for url in urls:
    scrape_url(url)

driver.quit()

# Schrijf naar XML bestand
tree = ET.ElementTree(rss)
tree.write('combined_feed.xml', encoding='utf-8', xml_declaration=True)

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime

# URL van de iBabs-pagina
url = 'https://zaanstad.bestuurlijkeinformatie.nl/Reports/Details/58e397b1-0b36-49e2-90ed-325405f27f72'

# Haal de inhoud van de pagina op
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Maak een nieuw RSS-feed element
rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')

# Voeg kanaal informatie toe
title = ET.SubElement(channel, 'title')
title.text = 'iBabs RSS Feed'
link = ET.SubElement(channel, 'link')
link.text = url
description = ET.SubElement(channel, 'description')
description.text = 'RSS feed gegenereerd van iBabs pagina'

# Voeg items toe aan de RSS-feed
for row in soup.select('tbody tr'):
    rss_item = ET.SubElement(channel, 'item')
    item_title = ET.SubElement(rss_item, 'title')
    item_title.text = row.select_one('td:nth-child(7)').text  # Titel van het item
    item_link = ET.SubElement(rss_item, 'link')
    item_link.text = url  # Gebruik de URL van de pagina als link
    item_description = ET.SubElement(rss_item, 'description')
    item_description.text = row.select_one('td:nth-child(4)').text  # Beschrijving van het item
    item_pubDate = ET.SubElement(rss_item, 'pubDate')
    item_pubDate.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

# Schrijf de RSS-feed naar een bestand
tree = ET.ElementTree(rss)
tree.write('feed.xml', encoding='utf-8', xml_declaration=True)

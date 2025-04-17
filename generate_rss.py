import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

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

# Bereken de datum van eergisteren
date_threshold = datetime.now() - timedelta(days=2)

# Voeg items toe aan de RSS-feed
for row in soup.select('tbody tr'):
    pub_date_element = row.select_one('td:nth-child(5)')
    if pub_date_element and pub_date_element.text:
        try:
            pub_date = datetime.strptime(pub_date_element.text, '%Y/%m/%d')
            if pub_date >= date_threshold:
                rss_item = ET.SubElement(channel, 'item')
                
                # Titel van het item
                title_element = row.select_one('td:nth-child(2)')
                if title_element and title_element.text:
                    item_title = ET.SubElement(rss_item, 'title')
                    item_title.text = title_element.text
                
                # Link van het item
                item_link = ET.SubElement(rss_item, 'link')
                item_link.text = url  # Gebruik de URL van de pagina als link
                
                # Beschrijving van het item
                description_element = row.select_one('td:nth-child(4)')
                if description_element and description_element.text:
                    item_description = ET.SubElement(rss_item, 'description')
                    item_description.text = description_element.text
                
                # Publicatiedatum van het item
                item_pubDate = ET.SubElement(rss_item, 'pubDate')
                item_pubDate.text = pub_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        except ValueError:
            print(f"Fout bij het parsen van de datum: {pub_date_element.text}")

# Schrijf de RSS-feed naar een bestand
tree = ET.ElementTree(rss)
tree.write('feed.xml', encoding='utf-8', xml_declaration=True)

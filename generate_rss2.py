from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time

urls = [
    'https://zaanstad.bestuurlijkeinformatie.nl/Reports/Details/8ea04074-52e6-4284-bd1a-66e378b40ec1'
]

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
ET.SubElement(channel, 'title').text = 'Zaanstad iBabs RSS Feed Extra'
ET.SubElement(channel, 'link').text = urls[0]
ET.SubElement(channel, 'description').text = 'Feed van iBabs Zaanstad - Extra Pagina'

now = datetime.now()
date_threshold = now - timedelta(days=2)

for url in urls:
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for row in soup.select('tbody tr'):
        pub_date_element = row.select_one('td:nth-child(1) a')
        if pub_date_element and pub_date_element.text:
            try:
                pub_date = datetime.strptime(pub_date_element.text.strip(), '%d-%m-%Y')
                if pub_date.date() >= date_threshold.date():
                    rss_item = ET.SubElement(channel, 'item')
                    title_element = row.select_one('td:nth-child(2)')
                    if title_element and title_element.text:
                        ET.SubElement(rss_item, 'title').text = title_element.text.strip()
                    ET.SubElement(rss_item, 'link').text = 'https://zaanstad.bestuurlijkeinformatie.nl' + pub_date_element['href']
                    desc_element = row.select_one('td:nth-child(4)')
                    if desc_element and desc_element.text:
                        ET.SubElement(rss_item, 'description').text = desc_element.text.strip()
                    ET.SubElement(rss_item, 'pubDate').text = pub_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
                    ET.SubElement(rss_item, 'guid').text = pub_date_element['href']
            except ValueError:
                print("Kon datum niet parsen:", pub_date_element.text)

driver.quit()
tree = ET.ElementTree(rss)
tree.write('feed_extra.xml', encoding='utf-8', xml_declaration=True)

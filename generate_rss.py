items = [
    {
        'date': '17-04-2025',
        'title': 'Bezwaarbrief Boschjesstraat',
        'link': 'https://zaanstad.bestuurlijkeinformatie.nl/Reports/Item/1a414256-230b-4a86-81fc-e2285f9ba8ad',
        'description': 'Ter kennisname, afdoening door college B&W, de raad ontvangt een kopie van de afdoening'
    },
    # Voeg hier andere items toe in hetzelfde formaat
]

for item in items:
    entry = feed.add_entry()
    entry.title(item['title'])
    entry.link(href=item['link'])
    entry.pubDate(datetime.strptime(item['date'], '%d-%m-%Y'))
    entry.description(item['description'])

rss_feed = feed.rss_str()

# Opslaan als XML bestand
with open('rss.xml', 'wb') as f:
    f.write(rss_feed)

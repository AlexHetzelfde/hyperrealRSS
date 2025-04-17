import feedgen.feed
from datetime import datetime

# Maak een nieuwe RSS-feed aan
feed = feedgen.feed.FeedGenerator()
feed.title('Zaanstad iBabs Updates')
feed.link(href='https://www.zaanstad.nl')
feed.description('Updates van de Zaanstad iBabs pagina.')
feed.language('nl')

# Voeg een item toe aan de feed
entry = feed.add_entry()
entry.title('Bezwaarbrief Boschjesstraat')
entry.link(href='https://zaanstad.bestuurlijkeinformatie.nl/Reports/Item/1a414256-230b-4a86-81fc-e2285f9ba8ad')
entry.pubDate(datetime.strptime('17-04-2025', '%d-%m-%Y'))
entry.description('Ter kennisname, afdoening door college B&W, de raad ontvangt een kopie van de afdoening')

# Genereer het RSS-bestand
rss_feed = feed.rss_str()

# Sla het op als een XML bestand
with open('rss.xml', 'wb') as f:
    f.write(rss_feed)

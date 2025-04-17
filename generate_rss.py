import datetime
from feedgen.feed import FeedGenerator

# Hier komt in de toekomst scraping van iBabs
# Voor nu: voorbeeldfeed met dummy data

fg = FeedGenerator()
fg.title("Zaanstad iBabs Documenten")
fg.link(href='https://zaanstad.bestuurlijkeinformatie.nl/', rel='alternate')
fg.description("Laatste documenten van de gemeente Zaanstad via iBabs")

fg.language("nl")
entry = fg.add_entry()
entry.title("Voorbeelditem van Zaanstad")
entry.link(href="https://zaanstad.bestuurlijkeinformatie.nl/")
entry.description("Dit is een voorbeelditem")
entry.pubDate(datetime.datetime.now())

fg.rss_file("rss.xml")

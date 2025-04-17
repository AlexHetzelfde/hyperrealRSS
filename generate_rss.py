import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import datetime

# De iBabs-pagina's die je wilt scrapen
PAGES = {
    "Collegeberichten": "https://zaanstad.bestuurlijkeinformatie.nl/Reports/Details/8ea04074-52e6-4284-bd1a-66e378b40ec1",
    "Ingekomen stukken": "https://zaanstad.bestuurlijkeinformatie.nl/Reports/Details/58e397b1-0b36-49e2-90ed-325405f27f72",
    "Schriftelijke vragen": "https://zaanstad.bestuurlijkeinformatie.nl/Reports/Details/36b1b6ca-8c4b-4d88-b910-a1edba601ac1",
}

# Initialiseer de feed
fg = FeedGenerator()
fg.title("Zaanstad iBabs Feed")
fg.link(href="https://zaanstad.bestuurlijkeinformatie.nl", rel='alternate')
fg.description("Automatisch gegenereerde feed met Collegeberichten, Ingekomen stukken en Schriftelijke vragen van Zaanstad")
fg.language("nl")

# Verwerk elke pagina
for category, url in PAGES.items():
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    # Zoek naar de documenten op de pagina (meestal in een <table>)
    rows = soup.select("table tbody tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        title = cols[0].get_text(strip=True)
        date_str = cols[1].get_text(strip=True)

        # Probeer de datum om te zetten
        try:
            pub_date = datetime.datetime.strptime(date_str, "%d-%m-%Y")
            pub_date = pub_date.replace(tzinfo=datetime.timezone.utc)
        except Exception:
            pub_date = datetime.datetime.now(datetime.timezone.utc)

        # Zoek naar een link
        link_tag = cols[0].find("a")
        if link_tag and "href" in link_tag.attrs:
            link = "https://zaanstad.bestuurlijkeinformatie.nl" + link_tag["href"]
        else:
            link = url  # fallback naar de pagina zelf

        # Voeg toe aan feed
        fe = fg.add_entry()
        fe.title(f"[{category}] {title}")
        fe.link(href=link)
        fe.pubDate(pub_date)

# Sla de feed op als rss.xml
fg.rss_file("rss.xml")

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

# -------------------------
# DEFINE COMPANIES FIRST
# -------------------------
companies = [
    {"name": "HSBC", "url": "https://www.hsbc.com/careers/students-and-graduates"},
    {"name": "Barclays", "url": "https://home.barclays/careers/students-graduates"},
    {"name": "Lloyds", "url": "https://www.lloydsbankinggroup.com/careers"},
    {"name": "NatWest", "url": "https://jobs.natwestgroup.com"},
    
    {"name": "Unilever", "url": "https://careers.unilever.com"},
    {"name": "Tesco", "url": "https://www.tesco-careers.com"},
    {"name": "Sainsburys", "url": "https://sainsburys.jobs"},
    {"name": "Diageo", "url": "https://careers.diageo.com"},
    
    {"name": "Shell", "url": "https://www.shell.com/careers"},
    {"name": "BP", "url": "https://www.bp.com/careers"},
    {"name": "Rio Tinto", "url": "https://www.riotinto.com/careers"},
    {"name": "Glencore", "url": "https://www.glencore.com/careers"},
    
    {"name": "RELX", "url": "https://www.relx.com/careers"},
    {"name": "Sage", "url": "https://www.sage.com/en-gb/company/careers"},
    {"name": "Experian", "url": "https://www.experianplc.com/careers"},
    {"name": "LSEG", "url": "https://www.lseg.com/en/careers"},
    
    {"name": "AstraZeneca", "url": "https://careers.astrazeneca.com"},
    {"name": "GSK", "url": "https://www.gsk.com/en-gb/careers"},
    {"name": "Reckitt", "url": "https://careers.reckitt.com"},
    
    {"name": "Vodafone", "url": "https://careers.vodafone.com"},
    {"name": "BT", "url": "https://www.bt.com/careers"},
    
    {"name": "BAE Systems", "url": "https://www.baesystems.com/en/careers"},
    {"name": "Rolls-Royce", "url": "https://careers.rolls-royce.com"},
    
    {"name": "Aviva", "url": "https://careers.aviva.com"},
    {"name": "Legal & General", "url": "https://careers.legalandgeneralgroup.com"},
    
    {"name": "Next", "url": "https://careers.next.co.uk"},
    {"name": "JD Sports", "url": "https://careers.jdplc.com"},
    
    {"name": "Compass Group", "url": "https://www.compass-group.com/en/careers.html"},
    {"name": "Whitbread", "url": "https://careers.whitbread.com"}
]

# -------------------------
# SETTINGS
# -------------------------
keywords = ["intern", "internship", "summer", "placement"]

results = []

# -------------------------
# FUNCTION
# -------------------------
def scrape_company(company):
    print(f"Checking {company['name']}...")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(company["url"], headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    full_link = urljoin(company["url"], href)

    links = soup.find_all("a")

    for link in links:
        text = link.get_text().lower()
        href = link.get("href")  # DEFINE FIRST

    if not href:
        continue

        text_combined = text + href.lower()

        if any(k in text_combined for k in keywords):
            full_link = urljoin(company["url"], href)

            results.append({
            "company": company["name"],
            "title": text.strip(),
            "location": "Check link",
            "link": full_link
             })

# -------------------------
# RUN
# -------------------------
for company in companies:
    scrape_company(company)

# -------------------------
# SAVE
# -------------------------
df = pd.DataFrame(results)
df.to_csv("careers_scrape.csv", index=False)

print("Done")
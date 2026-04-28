
An automated, data-driven intelligence tool designed to scrape, clean, and rank early-career opportunities (Internships, Placements, Graduate Schemes) across high-tier companies in the UK & Europe. 

Built with Python, Playwright, Pandas, and Streamlit, this project demonstrates a robust ETL (Extract, Transform, Load) pipeline scaling from raw HTML extraction to a final interactive dashboard.

## How is it useful

Manually checking 50+ career portal pages every week for roles heavily relies on luck. Existing aggregators are often slow, crowded with spam, or charge premium fees to access their structured data.

This platform solves that by:
1. Automatically extracting data using robust dynamic and static scraping techniques.
2. Standardising job types and locations algorithmically.
3. Scoring opportunities based on relevancy (prioritising tech, finance, analytics, and tier-1 brands).


* **Hybrid Scraping Engine:** Utilises `Requests` + `BeautifulSoup` for static ATS systems and `Playwright` headless browsers for dynamic Single Page Applications.
* **Automated Data Cleaning:** Normalises location nomenclature, deducts role type via heuristics, and deduplicates URL endpoints efficiently via `Pandas`.
* **Algorithmic Ranking:** Surfaces top-tier roles (Tier-1 banks, FAANG, quant firms) via an internal scoring mechanism (+2 for brand, +2 for target roles like 'data' and 'software').
* **Modern Interface:** Includes a fully responsive `Streamlit` dashboard featuring a glassmorphism design, real-time filtering, metric tracking, and CSV exports.

## Tech 
* **Language:** Python 3.9+
* **Data Manipulation:** Pandas
* **Web Scraping:** Playwright, BeautifulSoup4, Requests
* **Frontend UI:** Streamlit

## How to install & run locally

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Job_scraper
   ```

2. **Install dependencies:**
   Ensure you have python installed.
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Install Playwright browsers:**
   Playwright requires its own local browser binaries to parse dynamic sites.
   ```bash
   python3 -m playwright install chromium
   ```

4. **Launch the Dashboard:**
   ```bash
   streamlit run app/dashboard.py
   ```

5. **Running the ETL Pipeline:**
   Inside the Streamlit dashboard, use the sidebar's **"Refresh Data Aggregation"** button to execute `src/main.py` directly, which triggers the entire scraping, cleaning, and scoring flow.


## Future Improvements

* **Expansion to LinkedIn APIs:** Utilizing LinkedIn Data APIs to bypass scraping protections.
* **Serverless Deployment:** Automating the daily scrape via AWS Lambda or GitHub Actions cron jobs and pushing the CSV output to AWS S3.
* **LLM Integration:** Using OpenAI/Gemini to read actual job descriptions from the links.


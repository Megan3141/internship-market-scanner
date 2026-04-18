import os
import pandas as pd
from scraper import InternshipScraper
from cleaner import DataCleaner
from scorer import RelevancyScorer

def run_pipeline():
    """
    Executes the full pipeline:
    1. Scrape data (Hybrid: Playwright + Requests + Fallback)
    2. Clean and standardize data
    3. Score and rank data
    4. Save to final output
    """
    print("--- Starting Pipeline ---")
    
    # 1. Scrape
    print("1. Scraping data...")
    scraper = InternshipScraper()
    raw_df = scraper.run()
    
    os.makedirs(os.path.join(os.path.dirname(__file__), "../data"), exist_ok=True)
    raw_df.to_csv(os.path.join(os.path.dirname(__file__), "../data/raw_listings.csv"), index=False)
    
    # 2. Clean
    print(f"2. Cleaning {len(raw_df)} records...")
    cleaner = DataCleaner()
    clean_df = cleaner.process(raw_df)
    
    # 3. Score
    print("3. Scoring Relevancy...")
    scorer = RelevancyScorer()
    scored_df = scorer.process(clean_df)
    
    # 4. Output
    output_path = os.path.join(os.path.dirname(__file__), "../data/clean_listings.csv")
    scored_df.to_csv(output_path, index=False)
    print(f"--- Pipeline Finished. Saved {len(scored_df)} polished listings to {output_path} ---")

if __name__ == "__main__":
    run_pipeline()

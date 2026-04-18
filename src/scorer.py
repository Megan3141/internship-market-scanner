import pandas as pd

class RelevancyScorer:
    """
    Ranks internships to surface the absolute best opportunities for students
    interested in tech, data, or finance within top-tier companies.
    """
    def __init__(self):
        self.tier_1_brands = [
            "Google", "DeepMind", "Amazon", "Microsoft", "Apple", "Meta",
            "Goldman Sachs", "J.P. Morgan", "Morgan Stanley", "BlackRock",
            "Bloomberg", "Palantir", "Jane Street", "Deliveroo", "Monzo", "Revolut",
            "Spotify", "Barclays"
        ]
        
        self.target_keywords = ["data", "software", "engineer", "quant", "finance", "analytics", "ai", "machine learning", "product", "applied scientist"]

    def process(self, df):
        if df.empty:
            return df
            
        df['Relevance Score'] = df.apply(self._calculate_score, axis=1)
        
        df = df.sort_values(by="Relevance Score", ascending=False).reset_index(drop=True)
        return df

    def _calculate_score(self, row):
        score = 0
        company = str(row.get('Company', ''))
        title = str(row.get('Role Title', '')).lower()
        country = str(row.get('Country', ''))
        job_type = str(row.get('Type', ''))
        
        # 1. Tier-1 Brand (+2 Points)
        if any(brand.lower() == company.lower() for brand in self.tier_1_brands):
            score += 2
            
        # 2. Target Role Tech/Finance Focus (+2 Points)
        if any(keyword in title for keyword in self.target_keywords):
            score += 2
            
        # 3. Dedicated UK Location (+1 Point)
        if country == "United Kingdom":
            score += 1
            
        # 4. Strictly Intership or Placement (+1 Point)
        if job_type in ["Summer Internship", "Industrial Placement"]:
            score += 1

        return score

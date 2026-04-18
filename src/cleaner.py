import pandas as pd
import re

class DataCleaner:
    def __init__(self):
        # Predefined mappings to standardize extracted location strings
        self.location_mapping = {
            "london": "London",
            "edinburgh": "Edinburgh",
            "manchester": "Manchester",
            "bristol": "Bristol",
            "cambridge": "Cambridge",
            "oxford": "Oxford",
            "belfast": "Belfast",
            "remote": "Remote",
            "uk": "United Kingdom",
            "dublin": "Dublin"
        }

    def process(self, df):
        """ Cleans and standardises the raw dataframe. """
        # We need to make sure 'Raw Role Title' exists
        if 'Raw Role Title' not in df.columns:
            # Maybe it's already clean or we're processing an incorrectly shaped df
            return df
            
        df['Role Title'] = df['Raw Role Title'].str.strip()
        
        # Infer the Job Type based on terminology
        df['Type'] = df['Role Title'].apply(self._determine_type)
        
        # Infer the Location (since a lot of scrapers just get title & link, we extract location from title if present)
        df['Location'] = df['Role Title'].apply(self._extract_location)
        
        # Country deduction based on known UK cities
        uk_cities = ["London", "Edinburgh", "Manchester", "Bristol", "Cambridge", "Oxford", "Belfast", "United Kingdom"]
        df['Country'] = df['Location'].apply(
            lambda loc: "United Kingdom" if loc in uk_cities else ("Ireland" if loc == "Dublin" else "Multiple/Unknown")
        )
        
        # Clean company names
        df['Company'] = df['Company'].str.strip()
        df['Company'] = df['Company'].replace({"JP Morgan": "J.P. Morgan", "Goldman Sachs": "Goldman Sachs"})

        # Final column selection
        keep_cols = [
            "Company", "Role Title", "Location", "Country", "Type", 
            "Source Website", "Application Link", "Date Found"
        ]
        df_clean = df[keep_cols]
        
        # User request: filter strictly for interns/placements
        intern_types = ['Summer Internship', 'Industrial Placement', 'Internship']
        df_clean = df_clean[df_clean['Type'].isin(intern_types)].reset_index(drop=True)
        
        return df_clean

    def _determine_type(self, title):
        t = str(title).lower()
        if 'grad' in t:
            return 'Graduate Scheme'
        elif 'placement' in t or 'industrial' in t:
            return 'Industrial Placement'
        elif 'summer' in t or 'intern' in t:
            return 'Summer Internship'
        else:
            return 'Internship' # Defaulting to internship given the main focus

    def _extract_location(self, title):
        t = str(title).lower()
        # Find the first matching location
        for key, correct_name in self.location_mapping.items():
            if key in t:
                return correct_name
        return "Multiple/Unknown (UK/EU)"

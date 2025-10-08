import pandas as pd
from src.profile_filtering_system.components.title_elimination import title_elimination
from src.profile_filtering_system.components.summary_jobdesc_elimination import summary_jobdesc_elimination
from src.profile_filtering_system.components.company_exclusion import company_exclusion
from src.profile_filtering_system.components.english_only import english_only
from src.profile_filtering_system.components.location_filter import location_filter
from src.profile_filtering_system.components.company_category import company_category
from src.profile_filtering_system.components.seniority_filter import seniority_filter
from src.profile_filtering_system.components.keyword_extraction import extract_classified_keywords, extract_profile_keywords
from src.profile_filtering_system.components.keyword_matching import keyword_match_classified, keyword_match
from src.profile_filtering_system.components.llm_reason import generate_llm_reason
from src.profile_filtering_system.utils.common import return_if_empty

class ProfilesFiltering:
    def __init__(self, topic, sub_topic, event_location=None, additional_countries=None, use_classified_keywords=True):
        self.topic = topic
        self.sub_topic = sub_topic
        self.event_location = event_location
        self.additional_countries = additional_countries or []
        self.use_classified_keywords = use_classified_keywords

    def filter(self, df, companies_to_remove, companies_a, companies_b, verbose=True):
        # Check for required columns
        required_cols = ['title', 'companyName', 'summary', 'location']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            if verbose: print(f"ERROR: Missing required columns: {missing_cols}")
            return df.iloc[0:0]  # Return empty dataframe with same structure
            
        # Optional columns - add if missing
        if 'titleDescription' not in df.columns:
            df['titleDescription'] = ''
        if 'companyLocation' not in df.columns:
            df['companyLocation'] = df.get('location', '')
            
        if verbose: print(f"Initial rows: {len(df)}")
        
        # 1. Title elimination
        df = title_elimination(df)
        if verbose: print(f"After title elimination: {len(df)} rows")
        if return_if_empty(df) is not None:
            return df
            
        # 2. Summary/Job description elimination  
        df = summary_jobdesc_elimination(df)
        if verbose: print(f"After summary/jobdesc elimination: {len(df)} rows")
        if return_if_empty(df) is not None:
            return df
            
        # 3. Company exclusion
        df = company_exclusion(df, companies_to_remove)
        if verbose: print(f"After company exclusion: {len(df)} rows")
        if return_if_empty(df) is not None:
            return df
            
        # 4. English only filter
        df = english_only(df)
        if verbose: print(f"After english only: {len(df)} rows")
        if return_if_empty(df) is not None:
            return df
            
        # 5. Location filter
        df = location_filter(df, self.event_location, self.additional_countries)
        if verbose: print(f"After location filter: {len(df)} rows")
        if return_if_empty(df) is not None:
            return df
            
        # 6. Company category assignment
        df = company_category(df, companies_a, companies_b)
        if verbose: print(f"After company category: {len(df)} rows")
        if return_if_empty(df) is not None:
            return df
            
        # 7. Seniority filter
        df = seniority_filter(df)
        if verbose: print(f"After seniority filter: {len(df)} rows")
        if return_if_empty(df) is not None:
            return df
            
        # 8. Keyword extraction and matching
        if self.use_classified_keywords:
            # Use new classified keyword system according to client requirements
            classified_keywords = extract_classified_keywords(self.topic, self.sub_topic)
            class_a_keywords = classified_keywords['class_a']
            class_b_keywords = classified_keywords['class_b']
            
            if verbose:
                print(f"Class A Keywords (from '{self.topic}'): {class_a_keywords}")
                print(f"Class B Keywords (from '{self.sub_topic}'): {class_b_keywords}")
            
            # Apply keyword matching with detailed criteria tracking
            keyword_results = df.apply(lambda row: keyword_match_classified(row, class_a_keywords, class_b_keywords), axis=1)
            
            # Filter profiles that pass at least one criteria
            df = df[keyword_results.apply(lambda x: x['passes'])].copy()
            
            # Add criteria information to dataframe
            df['keyword_criteria_passed'] = keyword_results.apply(lambda x: ', '.join(x['criteria_passed']) if x['criteria_passed'] else 'None')
            df['criteria_a_passed'] = keyword_results.apply(lambda x: x['criteria_a'])
            df['criteria_b_passed'] = keyword_results.apply(lambda x: x['criteria_b'])
            df['criteria_c_passed'] = keyword_results.apply(lambda x: x['criteria_c'])
            
        else:
            # Use legacy keyword matching system
            keywords = extract_profile_keywords(self.topic, self.sub_topic)
            if verbose:
                print(f"Legacy Keywords: {keywords}")
            df = df[df.apply(lambda row: keyword_match(row, keywords), axis=1)].copy()
            df['keyword_criteria_passed'] = 'Legacy keyword matching'
        
        if verbose: print(f"After keyword matching: {len(df)} rows")
        if return_if_empty(df) is not None:
            return df
            
        # 9. Generate criteria tracking and LLM reasoning
        def get_criteria_passed(row):
            criteria = []
            if row.get('title', ''):
                criteria.append('Has valid title')
            if row.get('summary', ''):
                criteria.append('Has summary')
            if row.get('Companies Category', ''):
                criteria.append(f"Company category: {row.get('Companies Category')}")
            if hasattr(row, 'keyword_criteria_passed') and row['keyword_criteria_passed'] != 'None':
                criteria.append(f"Keyword criteria: {row['keyword_criteria_passed']}")
            return ', '.join(criteria)
        
        df['criteria_passed'] = df.apply(get_criteria_passed, axis=1)
        df['llm_reason'] = df.apply(lambda row: generate_llm_reason(row, self.topic, self.sub_topic, self.event_location, row['criteria_passed']), axis=1)
        
        # Clean up temporary columns but keep keyword criteria for analysis
        df = df.drop(columns=['criteria_passed'])
        
        if verbose: print(f"After llm_reason: {len(df)} rows")
        return df

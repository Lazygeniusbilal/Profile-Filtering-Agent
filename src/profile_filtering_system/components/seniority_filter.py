"""
Seniority filter component - filters based on job title seniority levels
"""
import pandas as pd
from src.profile_filtering_system.constants import cat_a, cat_b, cat_c


def seniority_filter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter profiles based on seniority requirements per company category
    
    Args:
        df: Input DataFrame with Companies Category column
        
    Returns:
        Filtered DataFrame
    """
    def match_title(row):
        t = str(row['title']).lower()
        if row['Companies Category'] == "Category A":
            return any(word in t for word in cat_a)
        elif row['Companies Category'] == "Category B":
            return any(word in t for word in cat_b)
        elif row['Companies Category'] == "Category C":
            return any(word in t for word in cat_c)
        return False
    
    filtered_df = df[df.apply(match_title, axis=1)]
    return filtered_df

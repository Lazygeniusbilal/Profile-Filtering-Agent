"""
Summary and job description elimination component
"""
import pandas as pd
from src.profile_filtering_system.constants import profile_elimination_words, columns_list


def summary_jobdesc_elimination(df: pd.DataFrame) -> pd.DataFrame:
    """
    Exclude profiles based on unwanted keywords in summary and titleDescription
    
    Args:
        df: Input DataFrame
        
    Returns:
        Filtered DataFrame
    """
    words_pattern = "|".join(profile_elimination_words)
    
    # Filter summary column
    df = df[df['summary'].fillna('').str.lower().str.contains(words_pattern, na=False) == False]
    
    # Filter titleDescription column if exists
    if 'titleDescription' in df.columns:
        df = df[df['titleDescription'].fillna('').str.lower().str.contains(words_pattern, na=False) == False]
    
    return df

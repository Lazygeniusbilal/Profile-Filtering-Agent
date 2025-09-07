"""
Title elimination component - filters out profiles based on unwanted titles
"""
import pandas as pd
from src.profile_filtering_system.constants import title_to_remove


def title_elimination(df: pd.DataFrame) -> pd.DataFrame:
    """
    Exclude profiles based on unwanted titles
    
    Args:
        df: Input DataFrame
        
    Returns:
        Filtered DataFrame
    """
    pattern = "|".join(title_to_remove)
    filtered_df = df[df['title'].fillna('').str.lower().str.contains(pattern, na=False) == False]
    return filtered_df

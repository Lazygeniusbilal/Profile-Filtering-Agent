"""
Company exclusion component - removes profiles from blacklisted companies
"""
import pandas as pd


def company_exclusion(df: pd.DataFrame, companies_to_remove_df: pd.DataFrame) -> pd.DataFrame:
    """
    Exclude profiles from blacklisted companies
    
    Args:
        df: Input DataFrame
        companies_to_remove_df: DataFrame containing companies to exclude
        
    Returns:
        Filtered DataFrame
    """
    filtered_df = df[df['companyName'].fillna('').isin(companies_to_remove_df['Account Name']) == False]
    return filtered_df

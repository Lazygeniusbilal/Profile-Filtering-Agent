"""
Company category assignment component
"""
import pandas as pd


def company_category(df: pd.DataFrame, companies_a_df: pd.DataFrame, companies_b_df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign company categories (A, B, C) based on company lists
    
    Args:
        df: Input DataFrame
        companies_a_df: DataFrame containing Category A companies
        companies_b_df: DataFrame containing Category B companies
        
    Returns:
        DataFrame with Companies Category column added
    """
    df = df.copy()
    df["Companies Category"] = df['companyName'].str.lower().apply(
        lambda x: "Category A" if x in companies_a_df['company'].str.lower().values
        else "Category B" if x in companies_b_df['company'].str.lower().values
        else "Category C"
    )
    return df

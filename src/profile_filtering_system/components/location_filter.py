"""
Location filter component - filters profiles based on company location
"""
import pandas as pd
from src.profile_filtering_system.constants import eu_countries


def location_filter(df: pd.DataFrame, event_location: str, additional_countries: list = None) -> pd.DataFrame:
    """
    Filter profiles based on company location relative to event location
    
    Args:
        df: Input DataFrame
        event_location: Event location string (can be None for EU default)
        additional_countries: List of additional countries to include beyond EU defaults
        
    Returns:
        Filtered DataFrame
    """
    countries_to_match = [c.lower() for c in eu_countries]
    
    # Add additional countries if provided
    if additional_countries:
        countries_to_match.extend([c.lower() for c in additional_countries])
    
    # Ensure companyLocation column exists and is properly formatted
    if 'companyLocation' not in df.columns:
        df['companyLocation'] = df.get('location', '')
    
    df['companyLocation'] = df['companyLocation'].fillna('').str.lower()
    
    # If no event location specified, use EU + additional countries only
    if not event_location or not event_location.strip():
        mask = df['companyLocation'].apply(lambda loc: any(country in loc for country in countries_to_match))
        return df[mask]
    
    user_location = event_location.strip().lower()
    
    if user_location in ["china", "usa", "united states", "united states of america"]:
        countries_to_match += ["china", "united states", "usa"]
        mask = df['companyLocation'].apply(lambda loc: any(country in loc for country in countries_to_match))
        df = df[mask]
    else:
        mask = df['companyLocation'].apply(lambda loc: any(country in loc for country in countries_to_match))
        df = df[mask]
        df = df[~df['companyLocation'].str.strip().str.endswith(('united states', 'usa', 'china'))]
    
    return df

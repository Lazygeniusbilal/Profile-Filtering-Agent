"""
Location filter component - filters profiles based on company location
"""
import pandas as pd
from src.profile_filtering_system.constants import eu_countries


def location_filter(df: pd.DataFrame, event_location: str = None, additional_countries: list = None) -> pd.DataFrame:
    """
    Filter profiles based on company location relative to event location
    
    Args:
        df: Input DataFrame
        event_location: Event location string (optional - if None, uses default EU countries)
        additional_countries: Optional list of additional countries to include in search
        
    Returns:
        Filtered DataFrame
    """
    # Start with default EU countries
    countries_to_match = [c.lower() for c in eu_countries]
    
    # Handle event location (optional)
    user_location = event_location.strip().lower() if event_location else None
    
    # Add additional countries if provided
    if additional_countries:
        additional_lower = [c.lower() for c in additional_countries if c.strip()]
        countries_to_match.extend(additional_lower)
    
    # Ensure companyLocation column exists and is properly formatted
    if 'companyLocation' not in df.columns:
        df['companyLocation'] = df.get('location', '')
    
    df['companyLocation'] = df['companyLocation'].fillna('').str.lower()
    
    # Special handling for China, USA, etc. - only if event location is specified
    if user_location and user_location in ["china", "usa", "united states", "united states of america"]:
        countries_to_match += ["china", "united states", "usa"]
        mask = df['companyLocation'].apply(lambda loc: any(country in loc for country in countries_to_match))
        df = df[mask]
    else:
        # Default behavior - search in EU + additional countries
        mask = df['companyLocation'].apply(lambda loc: any(country in loc for country in countries_to_match))
        df = df[mask]
        # Exclude US/China unless specifically requested via event location or additional countries
        if (not user_location or user_location not in ["china", "usa", "united states", "united states of america"]) and \
           (not additional_countries or not any(c.lower() in ["china", "usa", "united states"] for c in additional_countries)):
            df = df[~df['companyLocation'].str.strip().str.endswith(('united states', 'usa', 'china'))]
    
    return df

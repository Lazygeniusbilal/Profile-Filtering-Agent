"""
Keyword matching component - matches profiles against extracted keywords
"""
import re
import pandas as pd


def count_keyword_matches(text: str, keywords: list) -> int:
    """
    Count keyword matches in text
    
    Args:
        text: Text to search in
        keywords: List of keywords to match
        
    Returns:
        Number of matching keywords
    """
    text_words = re.findall(r'\w+', text.lower())
    return sum(1 for kw in keywords if kw in text_words)


def keyword_match(row: pd.Series, keywords: list) -> bool:
    """
    Check if a profile row matches keyword criteria
    
    Args:
        row: DataFrame row (profile)
        keywords: List of keywords to match against
        
    Returns:
        True if profile matches criteria, False otherwise
    """
    title = str(row.get('title', '')).lower()
    summary = str(row.get('summary', '')).lower()
    description = str(row.get('description', '')).lower()
    combined_summary_desc = summary + " " + description
    combined_all = title + " " + combined_summary_desc

    # Three matching rules from working app.py
    rule1 = count_keyword_matches(combined_all, keywords) >= 2
    rule2 = (count_keyword_matches(title, keywords) >= 1 and 
             count_keyword_matches(combined_summary_desc, keywords) >= 1)
    rule3 = count_keyword_matches(combined_summary_desc, keywords) >= 2

    return rule1 or rule2 or rule3

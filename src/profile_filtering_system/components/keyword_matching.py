import re
import pandas as pd


def count_keyword_matches_in_text(text: str, keywords: list) -> int:
    """
    Count keyword matches in text
    
    Args:
        text: Text to search in
        keywords: List of keywords to match
        
    Returns:
        Number of matching keywords
    """
    if not text or not keywords:
        return 0
    text_words = re.findall(r'\w+', text.lower())
    return sum(1 for kw in keywords if kw.lower() in text_words)


def get_matching_keywords(text: str, keywords: list) -> list:
    """
    Get list of keywords that match in text
    
    Args:
        text: Text to search in
        keywords: List of keywords to match
        
    Returns:
        List of matching keywords
    """
    if not text or not keywords:
        return []
    text_words = [word.lower() for word in re.findall(r'\w+', text.lower())]
    return [kw for kw in keywords if kw.lower() in text_words]


def check_criteria_a(title: str, description: str, class_a_keywords: list, class_b_keywords: list) -> bool:
    """
    Criteria A: One keyword from Class A + one from Class B (in title/description)
    
    Args:
        title: Profile title
        description: Profile description  
        class_a_keywords: List of Class A keywords
        class_b_keywords: List of Class B keywords
        
    Returns:
        True if criteria A is satisfied
    """
    title_desc_text = (title + " " + description).lower()
    
    class_a_matches = count_keyword_matches_in_text(title_desc_text, class_a_keywords)
    class_b_matches = count_keyword_matches_in_text(title_desc_text, class_b_keywords)
    
    return class_a_matches >= 1 and class_b_matches >= 1


def check_criteria_b(title: str, description: str, class_a_keywords: list, class_b_keywords: list) -> bool:
    """
    Criteria B: One keyword from Class A + one more from either Class A or B (in title/description)
    
    Args:
        title: Profile title
        description: Profile description
        class_a_keywords: List of Class A keywords  
        class_b_keywords: List of Class B keywords
        
    Returns:
        True if criteria B is satisfied
    """
    title_desc_text = (title + " " + description).lower()
    
    class_a_matches = count_keyword_matches_in_text(title_desc_text, class_a_keywords)
    class_b_matches = count_keyword_matches_in_text(title_desc_text, class_b_keywords)
    
    # Need at least 1 Class A keyword + at least 1 more keyword from either class
    total_matches = class_a_matches + class_b_matches
    
    return class_a_matches >= 1 and total_matches >= 2


def check_criteria_c(summary: str, class_a_keywords: list, class_b_keywords: list) -> bool:
    """
    Criteria C: 1 Class A keyword + 2 keywords from either class (in summary)
    
    Args:
        summary: Profile summary
        class_a_keywords: List of Class A keywords
        class_b_keywords: List of Class B keywords
        
    Returns:
        True if criteria C is satisfied
    """
    if not summary:
        return False
        
    summary_text = summary.lower()
    
    class_a_matches = count_keyword_matches_in_text(summary_text, class_a_keywords)
    class_b_matches = count_keyword_matches_in_text(summary_text, class_b_keywords)
    
    # Need at least 1 Class A keyword + total of 3 keywords (1 Class A + 2 more)
    total_matches = class_a_matches + class_b_matches
    
    return class_a_matches >= 1 and total_matches >= 3


def keyword_match_classified(row: pd.Series, class_a_keywords: list, class_b_keywords: list) -> dict:
    """
    Check if a profile row matches any of the three keyword criteria
    
    Args:
        row: DataFrame row (profile)
        class_a_keywords: List of Class A keywords (from event name)
        class_b_keywords: List of Class B keywords (from event subtitle)
        
    Returns:
        Dictionary with match status and criteria passed
    """
    title = str(row.get('title', ''))
    summary = str(row.get('summary', ''))
    description = str(row.get('titleDescription', ''))
    
    # Check each criteria
    criteria_a = check_criteria_a(title, description, class_a_keywords, class_b_keywords)
    criteria_b = check_criteria_b(title, description, class_a_keywords, class_b_keywords)
    criteria_c = check_criteria_c(summary, class_a_keywords, class_b_keywords)
    
    # Profile passes if it satisfies at least one criteria
    passes = criteria_a or criteria_b or criteria_c
    
    # Track which criteria were passed
    criteria_passed = []
    if criteria_a:
        criteria_passed.append("Criteria A")
    if criteria_b:
        criteria_passed.append("Criteria B")
    if criteria_c:
        criteria_passed.append("Criteria C")
    
    return {
        'passes': passes,
        'criteria_passed': criteria_passed,
        'criteria_a': criteria_a,
        'criteria_b': criteria_b,
        'criteria_c': criteria_c
    }


# Legacy function for backward compatibility
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

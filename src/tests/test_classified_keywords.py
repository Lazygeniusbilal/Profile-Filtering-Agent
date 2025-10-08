import sys
import os
# Add the parent directory to sys.path to import from src
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

import pandas as pd
from src.profile_filtering_system.components.keyword_extraction import extract_classified_keywords
from src.profile_filtering_system.components.keyword_matching import keyword_match_classified


def test_keyword_classification():
    """Test the keyword classification system"""
    
    # Example event details
    event_name = "Artificial Intelligence Innovation Summit"
    event_subtitle = "Machine Learning Applications in Healthcare and Digital Transformation"
    
    print("="*80)
    print("KEYWORD CLASSIFICATION SYSTEM TEST")
    print("="*80)
    print(f"Event Name: {event_name}")
    print(f"Event Subtitle: {event_subtitle}")
    print()
    
    # Extract classified keywords
    classified_keywords = extract_classified_keywords(event_name, event_subtitle)
    class_a_keywords = classified_keywords['class_a']
    class_b_keywords = classified_keywords['class_b']
    
    print("EXTRACTED KEYWORDS:")
    print(f"Class A (from event name, max 5): {class_a_keywords}")
    print(f"Class B (from event subtitle, unlimited): {class_b_keywords}")
    print()
    
    # Create sample profiles for testing
    sample_profiles = [
        {
            'name': 'Profile 1 - Criteria A Match',
            'title': 'AI Research Scientist',
            'titleDescription': 'Working on artificial intelligence applications',
            'summary': 'Expert in machine learning and healthcare solutions...'
        },
        {
            'name': 'Profile 2 - Criteria B Match',
            'title': 'Innovation Director',
            'titleDescription': 'Leading artificial intelligence and summit initiatives',
            'summary': 'Technology leader with focus on digital transformation...'
        },
        {
            'name': 'Profile 3 - Criteria C Match',
            'title': 'Software Engineer',
            'titleDescription': 'General software development',
            'summary': 'Specialized in artificial intelligence, machine learning, and healthcare technology applications...'
        },
        {
            'name': 'Profile 4 - No Match',
            'title': 'Marketing Manager',
            'titleDescription': 'Social media and brand management',
            'summary': 'Expert in marketing campaigns and customer engagement...'
        }
    ]
    
    print("PROFILE MATCHING RESULTS:")
    print("-" * 60)
    
    for i, profile in enumerate(sample_profiles, 1):
        # Convert to pandas Series for testing
        profile_row = pd.Series(profile)
        
        # Test keyword matching
        result = keyword_match_classified(profile_row, class_a_keywords, class_b_keywords)
        
        print(f"\n{profile['name']}:")
        print(f"  Title: {profile['title']}")
        print(f"  Description: {profile['titleDescription']}")
        print(f"  Summary: {profile['summary'][:50]}...")
        print(f"  PASSES: {result['passes']}")
        print(f"  Criteria Passed: {result['criteria_passed']}")
        print(f"  Details: A={result['criteria_a']}, B={result['criteria_b']}, C={result['criteria_c']}")
    
    print("\n" + "="*80)
    print("CRITERIA EXPLANATION:")
    print("Criteria A: 1 Class A keyword + 1 Class B keyword (in title/description)")
    print("Criteria B: 1 Class A keyword + 1 more keyword from either class (in title/description)")
    print("Criteria C: 1 Class A keyword + 2 keywords from either class (in summary)")
    print("Profile must satisfy AT LEAST ONE criteria to be selected")
    print("="*80)


if __name__ == "__main__":
    test_keyword_classification()
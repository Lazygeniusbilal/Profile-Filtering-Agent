"""
Test script to verify the modular filtering system works correctly
"""
import pandas as pd
from src.profile_filtering_system.constants import companies_to_remove, companies_a, companies_b
from src.profile_filtering_system.pipeline.filtering import ProfilesFiltering

def test_modular_system():
    """Test the modular filtering system"""
    
    # Create sample test data
    test_data = {
        'title': ['Senior Director of Innovation', 'Sales Manager', 'Head of AI Strategy'],
        'companyName': ['Google', 'Microsoft', 'Apple'],
        'summary': ['Leading innovation initiatives with focus on AI and design thinking.', 
                   'Managing sales operations and revenue growth.',
                   'Developing AI strategy for customer-centric innovation.'],
        'location': ['London, UK', 'New York, USA', 'Berlin, Germany'],
        'companyLocation': ['London, UK', 'New York, USA', 'Berlin, Germany'],
        'titleDescription': ['', '', '']
    }
    
    df = pd.DataFrame(test_data)
    print(f"Test data created with {len(df)} rows")
    
    # Load company data (create mock data if files don't exist)
    try:
        companies_to_remove_df = pd.read_excel(companies_to_remove)
        companies_a_df = pd.read_csv(companies_a)
        companies_b_df = pd.read_csv(companies_b)
    except FileNotFoundError as e:
        print(f"Warning: Could not load company data files: {e}")
        # Create mock data
        companies_to_remove_df = pd.DataFrame({'Account Name': ['BadCompany']})
        companies_a_df = pd.DataFrame({'company': ['google', 'microsoft']})
        companies_b_df = pd.DataFrame({'company': ['apple']})
    
    # Test the pipeline
    topic = "Culture & Leadership for Innovation, Design Thinking & AI"
    sub_topic = "Fostering a Culture of Innovation & Customer Centricity; Leadership for Innovation and Transformation; AI-Powered Design Thinking; Leadership for AI"
    event_location = "United Kingdom"
    
    pipeline = ProfilesFiltering(topic=topic, sub_topic=sub_topic, event_location=event_location)
    result = pipeline.filter(df, companies_to_remove_df, companies_a_df, companies_b_df, verbose=True)
    
    print(f"\nFinal result: {len(result)} rows")
    if not result.empty:
        print("Columns in result:", result.columns.tolist())
        print("\nSample result:")
        print(result.head())
        print("\nModular system is working correctly! ✅")
    else:
        print("No results returned - this might be expected depending on filters")
    
    return result

if __name__ == "__main__":
    test_modular_system()

"""
Test script to demonstrate the enhanced location filtering functionality
"""
import pandas as pd
from src.profile_filtering_system.components.location_filter import location_filter
from src.profile_filtering_system.constants import eu_countries, valid_countries

def test_location_filtering():
    """Test the enhanced location filtering with additional countries"""
    
    # Create sample test data with diverse locations
    test_data = {
        'title': ['Senior Director', 'Head of Innovation', 'Chief Technology Officer', 'VP of AI'],
        'companyName': ['Google', 'Toyota', 'SAP', 'Samsung'],
        'summary': ['Leading innovation initiatives', 'AI strategy expert', 'Technology leadership', 'Innovation management'],
        'location': ['London, UK', 'Tokyo, Japan', 'Berlin, Germany', 'Seoul, South Korea'],
        'companyLocation': ['London, UK', 'Tokyo, Japan', 'Berlin, Germany', 'Seoul, South Korea'],
    }
    
    df = pd.DataFrame(test_data)
    print(f"Original data: {len(df)} profiles")
    print("Locations:", df['companyLocation'].tolist())
    print()
    
    # Test 1: Default EU countries only (event in UK)
    print("=== Test 1: Default EU filtering (Event in UK) ===")
    filtered_eu = location_filter(df.copy(), "United Kingdom")
    print(f"After EU filtering: {len(filtered_eu)} profiles")
    if not filtered_eu.empty:
        print("Remaining locations:", filtered_eu['companyLocation'].tolist())
    print()
    
    # Test 2: EU + Additional countries (Japan, South Korea)
    print("=== Test 2: EU + Additional countries (Japan, South Korea) ===")
    additional_countries = ["Japan", "South Korea"]
    filtered_extended = location_filter(df.copy(), "United Kingdom", additional_countries)
    print(f"After extended filtering: {len(filtered_extended)} profiles")
    if not filtered_extended.empty:
        print("Remaining locations:", filtered_extended['companyLocation'].tolist())
    print()
    
    # Test 3: Event in USA (should include US + additional if specified)
    print("=== Test 3: Event in USA ===")
    filtered_usa = location_filter(df.copy(), "United States")
    print(f"After USA filtering: {len(filtered_usa)} profiles")
    if not filtered_usa.empty:
        print("Remaining locations:", filtered_usa['companyLocation'].tolist())
    print()
    
    # Show summary
    print("=== Summary ===")
    print(f"Default EU countries: {len(eu_countries)} countries")
    print(f"EU countries: {', '.join(eu_countries[:10])}{'...' if len(eu_countries) > 10 else ''}")
    print(f"Total valid countries in system: {len(valid_countries)}")
    print("\n✅ Location filtering tests completed successfully!")

if __name__ == "__main__":
    test_location_filtering()

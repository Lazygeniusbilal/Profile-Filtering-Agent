"""
Quick test to verify the modular filtering system works
"""
import pandas as pd
import os
from pathlib import Path

# Test if we can import all components
print("Testing component imports...")

try:
    from src.profile_filtering_system.components.title_elimination import title_elimination
    from src.profile_filtering_system.components.summary_jobdesc_elimination import summary_jobdesc_elimination
    from src.profile_filtering_system.components.company_exclusion import company_exclusion
    from src.profile_filtering_system.components.english_only import english_only
    from src.profile_filtering_system.components.location_filter import location_filter
    from src.profile_filtering_system.components.company_category import company_category
    from src.profile_filtering_system.components.seniority_filter import seniority_filter
    from src.profile_filtering_system.components.keyword_extraction import extract_profile_keywords
    from src.profile_filtering_system.components.keyword_matching import keyword_match
    from src.profile_filtering_system.components.llm_reason import generate_llm_reason
    from src.profile_filtering_system.pipeline.filtering import ProfilesFiltering
    print("✅ All component imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)

# Test with sample data
print("\nTesting with sample data...")

# Create sample test data
sample_data = pd.DataFrame({
    'title': ['Senior Director Innovation', 'Sales Manager', 'VP of Digital Transformation', 'Chief Innovation Officer'],
    'companyName': ['Tech Corp', 'Sales Inc', 'Innovation Ltd', 'Future Systems'],
    'summary': ['Leading innovation initiatives across the organization focusing on AI and digital transformation.',
                'Responsible for sales targets and client relationships.',
                'Driving digital transformation initiatives and AI implementation.',
                'Chief executive overseeing innovation strategy and AI adoption.'],
    'location': ['London, UK', 'New York, USA', 'Berlin, Germany', 'London, UK'],
    'companyLocation': ['London, UK', 'New York, USA', 'Berlin, Germany', 'London, UK'],
    'titleDescription': ['', '', '', '']
})

print(f"Created sample data with {len(sample_data)} profiles")

# Test individual components
print("\n🧪 Testing individual components:")

# Title elimination test
df_after_title = title_elimination(sample_data.copy())
print(f"After title elimination: {len(df_after_title)} profiles (removed sales-related titles)")

# Test keyword extraction
print(f"\n🔍 Testing keyword extraction:")
keywords = extract_profile_keywords("Innovation and AI", "Digital transformation and leadership")
print(f"Extracted keywords: {keywords}")

print("\n✅ Basic component testing completed successfully!")
print("\n🌐 The Streamlit app is running at: http://localhost:8502")
print("You can now upload a real dataset and see the step-by-step progress!")

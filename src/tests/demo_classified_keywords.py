def demo_keyword_classification():
    """Demonstrate the new keyword classification system"""
    
    print("="*80)
    print("CLASSIFIED KEYWORD SYSTEM DEMONSTRATION")
    print("="*80)
    
    # Example event details
    event_name = "Artificial Intelligence Innovation Summit"
    event_subtitle = "Machine Learning Applications in Healthcare and Digital Transformation"
    
    print(f"Event Name: {event_name}")
    print(f"Event Subtitle: {event_subtitle}")
    print()
    
    # Simulated keyword extraction (would normally use NLTK or LLM)
    class_a_keywords = ["artificial", "intelligence", "innovation", "summit", "technology"]
    class_b_keywords = ["machine", "learning", "applications", "healthcare", "digital", "transformation", "medical", "data"]
    
    print("EXTRACTED KEYWORDS:")
    print(f"Class A (from event name, max 5): {class_a_keywords}")
    print(f"Class B (from event subtitle, unlimited): {class_b_keywords}")
    print()
    
    # Test profiles
    test_profiles = [
        {
            'name': 'Profile 1 - Strong Criteria A Match',
            'title': 'AI Research Scientist',
            'description': 'Working on artificial intelligence applications in healthcare',
            'summary': 'Expert in machine learning algorithms and medical data analysis...'
        },
        {
            'name': 'Profile 2 - Criteria B Match',
            'title': 'Innovation Director',
            'description': 'Leading artificial intelligence and digital transformation initiatives',
            'summary': 'Technology leader with focus on summit organization...'
        },
        {
            'name': 'Profile 3 - Criteria C Match',
            'title': 'Software Engineer',
            'description': 'General software development work',
            'summary': 'Specialized in artificial intelligence, machine learning, and healthcare technology applications with deep expertise in innovation...'
        },
        {
            'name': 'Profile 4 - No Match',
            'title': 'Marketing Manager',
            'description': 'Social media and brand management',
            'summary': 'Expert in marketing campaigns and customer engagement strategies...'
        }
    ]
    
    def count_keywords_in_text(text, keywords):
        """Simple keyword counting function"""
        if not text:
            return 0, []
        text_lower = text.lower()
        found = [kw for kw in keywords if kw.lower() in text_lower]
        return len(found), found
    
    def check_criteria_a(title, description, class_a, class_b):
        """Criteria A: 1 Class A + 1 Class B in title/description"""
        combined = f"{title} {description}"
        a_count, a_found = count_keywords_in_text(combined, class_a)
        b_count, b_found = count_keywords_in_text(combined, class_b)
        return a_count >= 1 and b_count >= 1, a_found, b_found
    
    def check_criteria_b(title, description, class_a, class_b):
        """Criteria B: 1 Class A + 1 more from either class in title/description"""
        combined = f"{title} {description}"
        a_count, a_found = count_keywords_in_text(combined, class_a)
        b_count, b_found = count_keywords_in_text(combined, class_b)
        total_count = a_count + b_count
        return a_count >= 1 and total_count >= 2, a_found, b_found
    
    def check_criteria_c(summary, class_a, class_b):
        """Criteria C: 1 Class A + 2 more from either class in summary"""
        if not summary:
            return False, [], []
        a_count, a_found = count_keywords_in_text(summary, class_a)
        b_count, b_found = count_keywords_in_text(summary, class_b)
        total_count = a_count + b_count
        return a_count >= 1 and total_count >= 3, a_found, b_found
    
    print("PROFILE MATCHING RESULTS:")
    print("-" * 80)
    
    for profile in test_profiles:
        print(f"\n{profile['name']}:")
        print(f"  Title: {profile['title']}")
        print(f"  Description: {profile['description']}")
        print(f"  Summary: {profile['summary'][:60]}...")
        
        # Check each criteria
        criteria_a_pass, a_found_a, b_found_a = check_criteria_a(
            profile['title'], profile['description'], class_a_keywords, class_b_keywords
        )
        criteria_b_pass, a_found_b, b_found_b = check_criteria_b(
            profile['title'], profile['description'], class_a_keywords, class_b_keywords
        )
        criteria_c_pass, a_found_c, b_found_c = check_criteria_c(
            profile['summary'], class_a_keywords, class_b_keywords
        )
        
        overall_pass = criteria_a_pass or criteria_b_pass or criteria_c_pass
        
        print(f"  OVERALL RESULT: {'✅ PASSES' if overall_pass else '❌ REJECTED'}")
        
        if criteria_a_pass:
            print(f"    ✅ Criteria A: Found Class A {a_found_a} + Class B {b_found_a} in title/description")
        else:
            print(f"    ❌ Criteria A: Not satisfied")
            
        if criteria_b_pass:
            print(f"    ✅ Criteria B: Found Class A {a_found_b} + more keywords {a_found_b + b_found_b} in title/description")
        else:
            print(f"    ❌ Criteria B: Not satisfied")
            
        if criteria_c_pass:
            print(f"    ✅ Criteria C: Found Class A {a_found_c} + total {a_found_c + b_found_c} keywords in summary")
        else:
            print(f"    ❌ Criteria C: Not satisfied")
    
    print("\n" + "="*80)
    print("CRITERIA EXPLANATION:")
    print("Criteria A: 1 Class A keyword + 1 Class B keyword (in title/description)")
    print("Criteria B: 1 Class A keyword + 1 more keyword from either class (in title/description)")
    print("Criteria C: 1 Class A keyword + 2 keywords from either class (in summary)")
    print("Profile must satisfy AT LEAST ONE criteria to be selected")
    print("="*80)


if __name__ == "__main__":
    demo_keyword_classification()
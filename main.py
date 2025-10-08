import streamlit as st
import pandas as pd
from pathlib import Path
from src.profile_filtering_system.constants import companies_to_remove, companies_a, companies_b
from src.profile_filtering_system.pipeline.filtering import ProfilesFiltering
from src.profile_filtering_system.utils.common import streamlit_file_handler

# Ensure NLTK data is downloaded for Streamlit Cloud deployment
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
nltk_downloads = [
    'punkt',
    'stopwords', 
    'averaged_perceptron_tagger',
    'averaged_perceptron_tagger_eng',
    'punkt_tab'
]

for item in nltk_downloads:
    try:
        nltk.data.find(f'tokenizers/{item}' if 'punkt' in item else 
                      f'corpora/{item}' if item == 'stopwords' else 
                      f'taggers/{item}')
    except LookupError:
        try:
            st.download(item, quiet=True)
        except Exception as e:
            st.warning(f"Could not download NLTK data: {item}. Error: {e}")


def calculate_ai_score(row):
    """
    Calculate AI score for ranking profiles - higher score = better candidate
    Uses multiple factors to determine quality of match
    """
    score = 0
    
    # Criteria scoring (40% of total score)
    if row.get('criteria_a_passed', False):
        score += 15  # Highest priority - both Class A and B keywords
    if row.get('criteria_b_passed', False):
        score += 12  # High priority - Class A + additional keywords
    if row.get('criteria_c_passed', False):
        score += 8   # Good - keywords in summary
    
    # Company category scoring (25% of total score)
    company_category = row.get('Companies Category', '')
    if company_category == 'Category A':
        score += 12
    elif company_category == 'Category B':
        score += 8
    elif company_category == 'Category C':
        score += 4
    
    # Content quality scoring (35% of total score)
    # Title relevance
    title_len = len(str(row.get('title', '')))
    if title_len > 10:
        score += min(8, title_len // 5)  # Up to 8 points for title length
    
    # Summary quality
    summary_len = len(str(row.get('summary', '')))
    if summary_len > 50:
        score += min(12, summary_len // 25)  # Up to 12 points for summary depth
    
    # Keyword criteria count bonus
    criteria_count = sum([
        row.get('criteria_a_passed', False),
        row.get('criteria_b_passed', False), 
        row.get('criteria_c_passed', False)
    ])
    score += criteria_count * 3  # Bonus for multiple criteria matches
    
    return score


def get_top_25_percent(df):
    """
    Get top 25% of profiles based on AI scoring
    """
    if df.empty:
        return df
    
    # Calculate AI scores for each profile
    df_scored = df.copy()
    df_scored['ai_score'] = df_scored.apply(calculate_ai_score, axis=1)
    
    # Sort by score (highest first) and take top 25%
    df_sorted = df_scored.sort_values('ai_score', ascending=False)
    top_25_count = max(1, len(df_sorted) // 4)  # At least 1 profile
    top_25_df = df_sorted.head(top_25_count)
    
    # Remove the ai_score column before returning
    if 'ai_score' in top_25_df.columns:
        top_25_df = top_25_df.drop(columns=['ai_score'])
    
    return top_25_df


st.set_page_config(
    page_title="Speaker Profile Filtering Tool", 
    layout="wide",
    page_icon="🎤",
    initial_sidebar_state="expanded"
)

st.title("🎤 AI-Powered Speaker Profile Filtering Tool")

st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    border-left: 5px solid #ffd700;
">
    <h3 style="color: #ffd700; margin-bottom: 15px; font-weight: bold;">🎯 What this tool does:</h3>
    <p style="font-size: 16px; line-height: 1.6; margin-bottom: 0; color: #ffffff;">
        This intelligent tool filters thousands of professional profiles to identify the perfect speakers for your events. 
        Using AI-powered analysis, it considers job titles, company categories, location relevance, and topic expertise to 
        deliver a curated list of potential speakers.
    </p>
</div>
""", unsafe_allow_html=True)

# --- File Uploads ---
st.header("1. 📁 Upload Your Data")

upload_col1, upload_col2 = st.columns([2, 1])

with upload_col1:
    input_file = st.file_uploader(
        "Upload your profiles CSV or Excel file", 
        type=["csv", "xlsx", "xls"],
        help="Upload a file containing professional profiles to filter"
    )

with upload_col2:
    if input_file:
        st.success("✅ File uploaded successfully!")
        file_details = {
            "filename": input_file.name,
            "filetype": input_file.type,
            "filesize": f"{input_file.size / 1024:.1f} KB"
        }
        st.json(file_details)

# --- Event Details ---
st.header("2. 🌍 Event Details")

col1, col2 = st.columns(2)

with col1:
    event_location = st.text_input(
        "Event Location (Optional)", 
        placeholder="e.g., United Kingdom, China, USA (leave empty for EU default)",
        help="Enter the country where your event will be held. This helps filter speakers from relevant regions. Leave empty to use EU countries by default."
    )
    
    if event_location:
        # Add some basic validation and helpful hints
        from src.profile_filtering_system.constants import valid_countries
        if any(char.isdigit() for char in event_location):
            st.error("❌ Country name should not contain numbers. Please enter a valid country name.")
        elif event_location.strip().lower() not in [c.lower() for c in valid_countries]:
            st.warning("⚠️ This doesn't look like a recognized country name. Please check your input.")
        else:
            st.success(f"✅ Event location set to: {event_location}")

with col2:
    # Add some quick location suggestions
    st.markdown("**Quick Suggestions:**")
    location_suggestions = ["United Kingdom", "United States", "China", "Germany", "France", "Australia"]
    
    cols = st.columns(3)
    for i, suggestion in enumerate(location_suggestions):
        with cols[i % 3]:
            if st.button(suggestion, key=f"loc_{i}"):
                # Use session state to store the selection
                event_location = suggestion

# Location filtering options
st.subheader("🌐 Speaker Location Preferences")

# Show default EU countries
from src.profile_filtering_system.constants import eu_countries
st.info(f"📍 **Default search regions:** By default, we search for speakers from EU countries: {', '.join(eu_countries[:5])}... (and {len(eu_countries)-5} more)")

# Option to add additional countries
additional_countries = st.text_input(
    "Additional Countries (Optional)",
    placeholder="e.g., Japan, Brazil, South Korea",
    help="Add more countries to search for speakers. Separate multiple countries with commas. Leave empty to use only EU + event location."
)

if additional_countries:
    # Validate additional countries
    additional_list = [country.strip() for country in additional_countries.split(',')]
    from src.profile_filtering_system.constants import valid_countries
    
    valid_additional = []
    invalid_additional = []
    
    for country in additional_list:
        if country.lower() in [c.lower() for c in valid_countries]:
            valid_additional.append(country)
        else:
            invalid_additional.append(country)
    
    if valid_additional:
        st.success(f"✅ Valid additional countries: {', '.join(valid_additional)}")
    
    if invalid_additional:
        st.warning(f"⚠️ Invalid country names (will be ignored): {', '.join(invalid_additional)}")
else:
    valid_additional = []

# Show summary of countries that will be searched
search_summary = []
if event_location:
    search_summary.append(f"**Event location:** {event_location}")
else:
    search_summary.append(f"**Default search:** EU countries only")
search_summary.append(f"**EU countries:** {len(eu_countries)} countries")
if valid_additional:
    search_summary.append(f"**Additional countries:** {', '.join(valid_additional)}")

with st.expander("📋 Countries Summary - Click to see full list"):
    st.markdown("**Speaker search will include these countries:**")
    for item in search_summary:
        st.markdown(f"• {item}")
    
    if len(eu_countries) > 0:
        st.markdown("**EU Countries:**")
        st.write(", ".join(eu_countries))

# Event topic inputs
topic = st.text_area(
    "🎯 Event Topic", 
    value="Culture & Leadership for Innovation, Design Thinking & AI",
    height=100,
    help="Describe the main topic of your event. This will be used to match speaker expertise."
)

sub_topic = st.text_area(
    "📋 Event Subtopic(s)", 
    value="Fostering a Culture of Innovation & Customer Centricity; Leadership for Innovation and Transformation; AI-Powered Design Thinking; Leadership for AI; Trust & Psyc. Safety",
    height=120,
    help="List specific subtopics or areas of focus. Separate multiple topics with semicolons."
)

# Add topic suggestions
with st.expander("💡 Topic Ideas & Examples"):
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    ">
        <h4 style="color: #fdcb6e; margin-bottom: 15px;">🌟 Popular Event Topics:</h4>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
            <div>• Leadership & Management</div>
            <div>• Digital Transformation</div>
            <div>• Innovation & Technology</div>
            <div>• Customer Experience</div>
            <div>• Sustainability & ESG</div>
            <div>• Data & Analytics</div>
            <div>• Artificial Intelligence</div>
            <div>• Diversity & Inclusion</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if 'filtered_df' not in st.session_state:
    st.session_state['filtered_df'] = None

# --- Run Filtering Section ---
st.header("3. 🚀 Run Analysis")

# Check if all required inputs are provided (event_location is now optional)
ready_to_run = bool(input_file and topic)

if ready_to_run:
    st.success("✅ All required information provided. Ready to analyze!")
    if not event_location:
        st.info("ℹ️ No specific event location provided - will search EU countries + any additional countries specified.")
else:
    missing_items = []
    if not input_file:
        missing_items.append("📁 Data file")
    if not topic:
        missing_items.append("🎯 Event topic")
    
    st.warning(f"⚠️ Please provide: {', '.join(missing_items)}")

# Create a prominent run button
run_col1, run_col2, run_col3 = st.columns([1, 2, 1])
with run_col2:
    run_button = st.button(
        "🔍 Start Profile Analysis", 
        disabled=not ready_to_run,
        use_container_width=True,
        type="primary"
    )

if run_button:
    if not input_file:
        st.error("Please upload your profiles CSV or Excel file.")
        st.stop()
    df = streamlit_file_handler(input_file)
    if df is None:
        st.stop()
    st.info(f"Initial rows: {len(df)}")
    
    # Store original data in session state for multi-sheet download
    st.session_state['original_df'] = df.copy()
    
    # Check for required columns
    required_cols = ['title', 'companyName', 'summary', 'location']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Missing required columns in uploaded file: {', '.join(missing_cols)}")
        st.stop()
    
    # Add optional columns if missing
    if 'companyLocation' not in df.columns:
        df['companyLocation'] = df.get('location', '')
    if 'titleDescription' not in df.columns:
        df['titleDescription'] = ''

    # Load company data
    companies_to_remove_df = pd.read_excel(companies_to_remove)
    companies_a_df = pd.read_csv(companies_a)
    companies_b_df = pd.read_csv(companies_b)

    # Create a progress container
    progress_container = st.container()
    
    with progress_container:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        ">
            <h3 style="color: #fdcb6e; margin-bottom: 10px;">🔄 Filtering Progress</h3>
            <p style="margin: 0; font-size: 16px;">Processing your profiles step by step...</p>
        </div>
        """, unsafe_allow_html=True)
        
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Initialize progress tracking
    total_steps = 9
    current_step = 0
    
    # Update progress function
    def update_progress(step_name, remaining_rows, step_num):
        progress = step_num / total_steps
        progress_bar.progress(progress)
        status_text.text(f"Step {step_num}/{total_steps}: {step_name} - {remaining_rows:,} profiles remaining")
        if remaining_rows > 0:
            st.info(f"✅ {step_name}: {remaining_rows:,} profiles remaining")
        else:
            st.warning(f"⚠️ {step_name}: No profiles remaining - stopping here")
    
    # Run the modular pipeline with progress tracking
    filtered_df = None  # Initialize filtered_df before try block
    try:
        # Handle optional event_location
        event_loc = event_location if event_location and event_location.strip() else None
        
        # Use the new classified keyword system
        pipeline = ProfilesFiltering(
            topic=topic, 
            sub_topic=sub_topic, 
            event_location=event_loc, 
            additional_countries=valid_additional,
            use_classified_keywords=True  # Enable new classified keyword system
        )
        
        # We'll create a custom filter method that shows progress
        df_working = df.copy()
        
        # Step 1: Title elimination
        current_step += 1
        from src.profile_filtering_system.components.title_elimination import title_elimination
        df_working = title_elimination(df_working)
        update_progress("Title Elimination", len(df_working), current_step)
        if df_working.empty:
            st.error("No profiles left after title elimination. Please check your data or criteria.")
            st.stop()
        
        # Step 2: Summary/Job description elimination
        current_step += 1
        from src.profile_filtering_system.components.summary_jobdesc_elimination import summary_jobdesc_elimination
        df_working = summary_jobdesc_elimination(df_working)
        update_progress("Summary & Job Description Filter", len(df_working), current_step)
        if df_working.empty:
            st.error("No profiles left after summary filtering. Please check your data or criteria.")
            st.stop()
        
        # Step 3: Company exclusion
        current_step += 1
        from src.profile_filtering_system.components.company_exclusion import company_exclusion
        df_working = company_exclusion(df_working, companies_to_remove_df)
        update_progress("Company Exclusion", len(df_working), current_step)
        if df_working.empty:
            st.error("No profiles left after company exclusion. Please check your data or criteria.")
            st.stop()
        
        # Step 4: English language filter
        current_step += 1
        from src.profile_filtering_system.components.english_only import english_only
        df_working = english_only(df_working)
        update_progress("English Language Filter", len(df_working), current_step)
        if df_working.empty:
            st.error("No profiles left after English language filtering. Please check your data.")
            st.stop()
        
        # Step 5: Location filter
        current_step += 1
        from src.profile_filtering_system.components.location_filter import location_filter
        df_working = location_filter(df_working, event_loc, valid_additional)
        update_progress("Location Filter", len(df_working), current_step)
        if df_working.empty:
            st.error("No profiles left after location filtering. Please check your location settings or add more countries.")
            st.stop()
        
        # Step 6: Company category assignment
        current_step += 1
        from src.profile_filtering_system.components.company_category import company_category
        df_working = company_category(df_working, companies_a_df, companies_b_df)
        update_progress("Company Category Assignment", len(df_working), current_step)
        
        # Step 7: Seniority filter
        current_step += 1
        from src.profile_filtering_system.components.seniority_filter import seniority_filter
        df_working = seniority_filter(df_working)
        update_progress("Seniority Filter", len(df_working), current_step)
        if df_working.empty:
            st.error("No profiles left after seniority filtering. Please check your seniority requirements.")
            st.stop()
        
        # Step 8: Keyword matching (using new classified system)
        current_step += 1
        from src.profile_filtering_system.components.keyword_extraction import extract_classified_keywords
        from src.profile_filtering_system.components.keyword_matching import keyword_match_classified
        
        # Extract classified keywords
        classified_keywords = extract_classified_keywords(topic, sub_topic)
        class_a_keywords = classified_keywords['class_a']
        class_b_keywords = classified_keywords['class_b']
        
        st.info(f"🔍 Class A Keywords (from '{topic}'): {', '.join(class_a_keywords)}")
        st.info(f"🔍 Class B Keywords (from '{sub_topic}'): {', '.join(class_b_keywords)}")
        
        # Apply keyword matching with detailed criteria tracking
        keyword_results = df_working.apply(lambda row: keyword_match_classified(row, class_a_keywords, class_b_keywords), axis=1)
        
        # Filter profiles that pass at least one criteria
        df_working = df_working[keyword_results.apply(lambda x: x['passes'])].copy()
        
        # Add criteria information to dataframe
        df_working['keyword_criteria_passed'] = keyword_results.apply(lambda x: ', '.join(x['criteria_passed']) if x['criteria_passed'] else 'None')
        df_working['criteria_a_passed'] = keyword_results.apply(lambda x: x['criteria_a'])
        df_working['criteria_b_passed'] = keyword_results.apply(lambda x: x['criteria_b'])
        df_working['criteria_c_passed'] = keyword_results.apply(lambda x: x['criteria_c'])
        
        update_progress("Classified Keyword Matching", len(df_working), current_step)
        if df_working.empty:
            st.error("No profiles left after classified keyword matching. Please adjust your topic/subtopic or criteria.")
            st.stop()
            
        # Step 9: LLM reasoning
        current_step += 1
        from src.profile_filtering_system.components.llm_reason import generate_llm_reason
        
        def get_criteria_passed(row):
            criteria = []
            if row.get('title', ''):
                criteria.append('Valid title')
            if row.get('summary', ''):
                criteria.append('Has summary')
            if row.get('Companies Category', ''):
                criteria.append(f"{row.get('Companies Category')}")
            if hasattr(row, 'keyword_criteria_passed') and row.get('keyword_criteria_passed', 'None') != 'None':
                criteria.append(f"Keyword: {row['keyword_criteria_passed']}")
            return ', '.join(criteria)
        
        df_working['criteria_passed'] = df_working.apply(get_criteria_passed, axis=1)
        
        # Add progress for LLM reasoning
        progress_text = st.empty()
        reasoning_progress = st.progress(0)
        
        llm_reasons = []
        total_rows = len(df_working)
        
        for idx, (_, row) in enumerate(df_working.iterrows()):
            progress_text.text(f"Generating AI explanations... {idx+1}/{total_rows}")
            reasoning_progress.progress((idx + 1) / total_rows)
            reason = generate_llm_reason(row, topic, sub_topic, event_loc or "Global/EU", row['criteria_passed'])
            llm_reasons.append(reason)
        
        df_working['llm_reason'] = llm_reasons
        df_working = df_working.drop(columns=['criteria_passed'])
        
        update_progress("AI Reasoning Complete", len(df_working), current_step)
        
        # Complete the progress
        progress_bar.progress(1.0)
        status_text.text("✅ Filtering Complete!")
        
        filtered_df = df_working
        
    except Exception as e:
        st.error(f"An error occurred during filtering: {str(e)}")
        st.stop()
    
    st.session_state['filtered_df'] = filtered_df.copy() if filtered_df is not None else None
    if filtered_df is not None and not filtered_df.empty:
        st.success(f"🎉 Filtering complete! Found {len(filtered_df)} potential speakers from {len(df)} initial profiles.")
        
        # Show summary statistics
        st.subheader("📊 Filtering Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Initial Profiles", f"{len(df):,}")
        with col2:
            st.metric("Final Profiles", f"{len(filtered_df):,}")
        with col3:
            retention_rate = (len(filtered_df) / len(df)) * 100
            st.metric("Retention Rate", f"{retention_rate:.1f}%")
        with col4:
            category_counts = filtered_df['Companies Category'].value_counts()
            most_common = category_counts.index[0] if not category_counts.empty else "N/A"
            st.metric("Top Category", most_common)
    else:
        st.warning("No profiles found after filtering.")

# --- Output and Checkbox (always visible if filtered_df exists) ---
if st.session_state.get('filtered_df') is not None:
    st.header("🎯 Filtered Results")
    
    # Control panel
    col1, col2 = st.columns([3, 1])
    with col1:
        companies_c_rows = st.checkbox("Include Companies C", value=True, 
                                     help="Toggle to include/exclude Category C companies")
    with col2:
        show_reasoning = st.checkbox("Show AI Reasoning", value=False,
                                   help="Display AI-generated explanations in the table view (always included in downloads)")
    
    df = st.session_state['filtered_df']
    if companies_c_rows:
        df_filtered = df
    else:
        df_filtered = df[~(df['Companies Category'] == "Category C")]
    
    # Show category breakdown
    if not df_filtered.empty:
        st.subheader("📈 Results Breakdown")
        category_counts = df_filtered['Companies Category'].value_counts()
        
        # Calculate top 25% count
        top_25_count = max(1, len(df_filtered) // 4)
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Show category breakdown
        for i, (category, count) in enumerate(category_counts.items()):
            color = "🟢" if category == "Category A" else "🟡" if category == "Category B" else "🔵"
            cols = [col1, col2, col3]
            with cols[i % 3]:
                st.metric(f"{color} {category}", f"{count:,} profiles")
        
        # Show AI Top 25% count
        with col4:
            st.metric("🤖 AI Top 25%", f"{top_25_count:,} profiles")
    
    # Prepare display columns (for viewing only)
    display_cols = list(df_filtered.columns)
    if 'llm_reason' in df_filtered.columns:
        if not show_reasoning:
            display_cols = [col for col in df_filtered.columns if col != 'llm_reason']
        else:
            # Move llm_reason to the end for visibility
            display_cols = [col for col in df_filtered.columns if col != 'llm_reason'] + ['llm_reason']
    
    # Prepare download columns (always include llm_reason for client)
    download_cols = list(df_filtered.columns)
    if 'llm_reason' in df_filtered.columns:
        # Move llm_reason to the end for download
        download_cols = [col for col in df_filtered.columns if col != 'llm_reason'] + ['llm_reason']
    
    # Display results with pagination
    st.subheader(f"📋 Results ({len(df_filtered):,} profiles)")
    
    # Add search functionality
    search_term = st.text_input("🔍 Search profiles:", placeholder="Search by title, company, or summary...")
    if search_term:
        mask = (
            df_filtered['title'].str.contains(search_term, case=False, na=False) |
            df_filtered['companyName'].str.contains(search_term, case=False, na=False) |
            df_filtered['summary'].str.contains(search_term, case=False, na=False)
        )
        df_display = df_filtered[mask]
        st.info(f"Found {len(df_display)} profiles matching '{search_term}'")
    else:
        df_display = df_filtered
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📋 All Results", "🤖 AI Top 25%"])
    
    with tab1:
        # Show all results
        if not df_display.empty:
            st.dataframe(
                df_display[display_cols].head(100), 
                use_container_width=True,
                height=400
            )
            
            if len(df_display) > 100:
                st.info(f"Showing first 100 of {len(df_display)} results. Use search to filter further.")
        else:
            st.warning("No profiles match your search criteria.")
    
    with tab2:
        # Show AI Top 25%
        top_25_df = get_top_25_percent(df_filtered if not search_term else df_display)
        
        if not top_25_df.empty:
            st.info(f"🤖 **AI-Selected Top Candidates:** These {len(top_25_df)} profiles scored highest based on keyword relevance, company category, and content quality.")
            st.dataframe(
                top_25_df[display_cols], 
                use_container_width=True,
                height=400
            )
        else:
            st.warning("No profiles in top 25% selection.")
    
    # Download section
    st.subheader("💾 Download Results")
    if 'llm_reason' in df_filtered.columns and not show_reasoning:
        st.info("💡 **Tip:** AI reasoning explanations are always included in downloads, even when not displayed in the table above.")
    
    # Add info about multi-file CSV format
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    ">
        <h4 style="color: #fdcb6e; margin-bottom: 10px;">📊 CSV Download Options:</h4>
        <div style="line-height: 1.6;">
            <strong>Option 1:</strong> All Profiles (original uploaded data)<br>
            <strong>Option 2:</strong> AI Recommended (top 25% of filtered results)<br>
            <strong>Option 3:</strong> Approved Candidates (all filtered results)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV download for original data
        if 'original_df' in st.session_state and st.session_state['original_df'] is not None:
            original_data = st.session_state['original_df']
            original_csv = original_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 All Profiles CSV",
                data=original_csv,
                file_name=f"all_profiles_{len(original_data)}_original.csv",
                mime="text/csv",
                help="Download all original uploaded profiles"
            )
        else:
            st.info("Original data not available")
    
    with col2:
        # CSV download for AI Top 25%
        top_25_df = get_top_25_percent(df_filtered)
        if not top_25_df.empty:
            top_25_csv = top_25_df[download_cols].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="🤖 AI Top 25% CSV",
                data=top_25_csv,
                file_name=f"ai_recommended_top25_{len(top_25_df)}_profiles.csv",
                mime="text/csv",
                help="Download AI-selected top 25% candidates"
            )
        else:
            st.info("No top 25% data available")
    
    with col3:
        # CSV download for all filtered results
        filtered_csv = df_filtered[download_cols].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="✅ Approved Candidates CSV",
            data=filtered_csv,
            file_name=f"approved_candidates_{len(df_filtered)}_filtered.csv",
            mime="text/csv",
            help="Download all filtered/approved candidates"
        )
else:
    st.info("👆 Please upload a file and run filtering to see results.")
    
    # Show example of expected file format
    with st.expander("📋 Expected File Format"):
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
        ">
            <h4 style="color: #fdcb6e; margin-bottom: 15px;">📄 Required File Columns:</h4>
            <div style="line-height: 1.8;">
                <strong>Required columns:</strong><br>
                • <strong>title</strong>: Job title<br>
                • <strong>companyName</strong>: Company name<br>
                • <strong>summary</strong>: Profile summary/description<br>
                • <strong>location</strong>: Profile location<br><br>
                <strong>Optional columns:</strong><br>
                • <strong>companyLocation</strong>: Company location (uses location if missing)<br>
                • <strong>titleDescription</strong>: Job description
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show sample data format
        sample_data = pd.DataFrame({
            'title': ['Senior Director Innovation', 'VP of Digital Transformation'],
            'companyName': ['Tech Corp', 'Innovation Inc'],
            'summary': ['Leading innovation initiatives...', 'Driving digital transformation...'],
            'location': ['London, UK', 'New York, USA'],
            'companyLocation': ['London, UK', 'New York, USA'],
            'titleDescription': ['Responsible for...', 'Oversees digital...']
        })
        st.dataframe(sample_data, use_container_width=True)
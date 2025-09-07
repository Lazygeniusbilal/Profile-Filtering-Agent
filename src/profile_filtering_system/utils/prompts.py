# Prompt for LLM to generate a natural language reason for profile selection (criteria-aware)
reason_generation_llm_prompt = '''
You are an expert assistant for filtering professional profiles for event speaker selection.

Task:
Given the following profile information, event requirements, and the list of filtering criteria that this profile passed, generate a concise, clear, and factual explanation for why this profile was selected. Reference the specific criteria/rules it passed. Be brief and avoid generic statements.

Input:
- Profile: {profile}
- Event Topic: {topic}
- Event Subtopic: {sub_topic}
- Event Location: {event_location}
- Criteria Passed: {criteria_passed}

Output:
A short sentence explaining why this profile was selected, mentioning the relevant criteria.
'''
# In this file we will mention all the prompts we will need for the project

keyword_extraction_prompt = """
You are an expert assistant for filtering professional profiles.

Task:
Given a text extract only the most relevant and meaningful keywords that best represent the person's expertise, skills, or main topics.

Guidance:
- Only return **single words** (not multi-word phrases).
- Exclude generic, vague, or overly broad words (e.g., business, organization, management, process, system, operations, etc.).
- Focus on nouns and adjectives that are specific to the domain, expertise, or technical skills.
- Do not include stopwords or common English words.
- Return the keywords as a comma-separated list, ordered by importance if possible.
- Be concise: only include the best keywords that would help in filtering or matching profiles for events.
"""


# Prompt for LLM to generate a natural language reason for profile selection (criteria-aware)
reason_generation_llm_prompt = '''
You are an expert assistant for filtering professional profiles for event speaker selection.

Task:
Given the following profile information, event requirements, and the list of filtering criteria that this profile passed, generate a concise, clear, and factual explanation for why this profile was selected. Reference the specific criteria/rules it passed. Be brief and avoid generic statements.

Input:
- Profile: {profile}
- Event Topic: {topic}
- Event Subtopic: {sub_topic}
- Event Location: {event_location}
- Criteria Passed: {criteria_passed}

Output:
A short sentence explaining why this profile was selected, mentioning the relevant criteria.
'''


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

class_a_keyword_prompt = """
You are an expert assistant for extracting keywords from event names for speaker profile filtering.

Task:
Extract exactly 5 or fewer keywords from the event name that best represent the core topic and include relevant synonyms.

Requirements:
- Maximum 5 keywords
- Include synonyms and variations of main concepts
- Focus on domain-specific terms
- Single words only (no phrases)
- Exclude generic business terms
- Return as comma-separated list
- Prioritize most important/specific terms first

Example:
Event Name: "Artificial Intelligence Innovation Summit"
Output: artificial, intelligence, AI, innovation, technology
"""

class_b_keyword_prompt = """
You are an expert assistant for extracting keywords from event subtitles for speaker profile filtering.

Task:
Extract all relevant keywords from the event subtitle that represent specific topics, skills, or domains.

Requirements:
- No limit on number of keywords
- Include all relevant domain-specific terms
- Single words only (no phrases)
- Exclude generic business terms and stopwords
- Return as comma-separated list
- Focus on technical terms, skills, and specific topics

Example:
Event Subtitle: "Machine Learning Applications in Healthcare and Digital Transformation"
Output: machine, learning, applications, healthcare, digital, transformation, technology, medical, data, algorithms
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


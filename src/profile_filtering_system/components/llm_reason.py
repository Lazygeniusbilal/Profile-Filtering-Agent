"""
LLM reasoning component - generates explanations for profile selection
"""
import pandas as pd
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.profile_filtering_system.utils.prompts import reason_generation_llm_prompt
from src.profile_filtering_system.utils.common import OPENAI_SECRET_KEY

load_dotenv()


def generate_llm_reason(row: pd.Series, topic: str, sub_topic: str, event_location: str, criteria_passed: str) -> str:
    """
    Generate LLM-powered explanation for why a profile was selected
    
    Args:
        row: Profile row
        topic: Event topic
        sub_topic: Event subtopic
        event_location: Event location
        criteria_passed: String describing which criteria this profile passed
        
    Returns:
        Generated explanation string
    """
    llm_model = ChatOpenAI(api_key=OPENAI_SECRET_KEY)
    
    profile = {
        'title': row.get('title', ''),
        'companyName': row.get('companyName', ''),
        'summary': row.get('summary', ''),
        'description': row.get('description', ''),
        'location': row.get('location', ''),
        'companyLocation': row.get('companyLocation', ''),
        'Companies Category': row.get('Companies Category', '')
    }
    
    prompt = reason_generation_llm_prompt.format(
        profile=profile,
        topic=topic,
        sub_topic=sub_topic,
        event_location=event_location,
        criteria_passed=criteria_passed
    )
    
    response = llm_model.invoke(prompt)
    if hasattr(response, 'content'):
        return response.content.strip()
    return str(response).strip()

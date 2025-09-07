import pandas as pd
from src.profile_filtering_system.utils.prompts import reason_generation_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

def generate_llm_reason(row, topic, sub_topic, event_location):
    profile = {
        'title': row.get('title', ''),
        'companyName': row.get('companyName', ''),
        'summary': row.get('summary', ''),
        'description': row.get('description', ''),
        'location': row.get('location', ''),
        'companyLocation': row.get('companyLocation', ''),
        'Companies Category': row.get('Companies Category', '')
    }
    prompt = reason_generation_prompt.format(
        profile=profile,
        topic=topic,
        sub_topic=sub_topic,
        event_location=event_location
    )
    response = model.invoke(prompt)
    if hasattr(response, 'content'):
        return response.content.strip()
    return str(response).strip()

def add_llm_reason_column(df, topic, sub_topic, event_location):
    df = df.copy()
    df['llm_reason'] = df.apply(lambda row: generate_llm_reason(row, topic, sub_topic, event_location), axis=1)
    return df

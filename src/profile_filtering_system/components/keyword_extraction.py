"""
Keyword extraction component using both NLTK and LLM approaches
"""
import re
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.profile_filtering_system.constants import GENERIC_WORDS
from src.profile_filtering_system.utils.prompts import keyword_extraction_prompt

# Ensure NLTK data is available
try:
    stopwords.words('english')
    pos_tag(['test'])  # Test if tagger is available
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('averaged_perceptron_tagger_eng')

load_dotenv()


def extract_profile_keywords(topic: str, sub_topic: str) -> list:
    """
    Extract keywords using NLTK (traditional approach from working app.py)
    
    Args:
        topic: Event topic
        sub_topic: Event subtopic
        
    Returns:
        List of keywords
    """
    stop_words = set(stopwords.words("english"))
    
    text = topic + ' ' + sub_topic
    tokens = word_tokenize(text.lower())
    tagged = pos_tag(tokens)
    words = []
    for word, tag in tagged:
        if (
            word.isalpha() and 
            word not in stop_words and 
            word not in GENERIC_WORDS and 
            tag.startswith(("NN", "JJ"))  # keep nouns & adjectives
        ):
            words.append(word)
    words.append("innovation")  # always include
    return list(set(words))


def extract_profile_keywords_llm(topic: str, sub_topic: str) -> list:
    """
    Extract keywords using LLM approach
    
    Args:
        topic: Event topic
        sub_topic: Event subtopic
        
    Returns:
        List of keywords
    """
    # Extract keywords using LLM (gpt-3.5-turbo approach)
    SECRET_KEY = "sk-proj-" + "kkNzvfQ0JMBJl8P-v1lLbZ-S3ijDTUfBrmoxaAhdaskrBNSE5WDZTgehCyntoNm3WG3AgrczAoT3BlbkFJTtCuKsYJQ9uBDQrRdIasviq63E_8_2OEo-EzZOhv4f4tEVFZPOxXZlNAQ6ntgH7n-vN_oBxxAA"
    llm_model = ChatOpenAI(
        model="gpt-3.5-turbo", 
        temperature=0,
        api_key=SECRET_KEY
    )
    
    text = topic + ' ' + sub_topic
    full_prompt = f"{keyword_extraction_prompt}\n\nText: {text}"
    response = llm_model.invoke(full_prompt)
    keywords_str = response.content if hasattr(response, "content") else str(response)
    keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
    return keywords

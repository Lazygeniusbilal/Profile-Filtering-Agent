import re
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.profile_filtering_system.constants import GENERIC_WORDS
from src.profile_filtering_system.utils.prompts import keyword_extraction_prompt, class_a_keyword_prompt, class_b_keyword_prompt
from src.profile_filtering_system.utils.common import OPENAI_SECRET_KEY

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


def extract_class_a_keywords(event_name: str) -> list:
    """
    Extract Class A keywords from event name (maximum 5, include synonyms)
    
    Args:
        event_name: Main event topic/name
        
    Returns:
        List of Class A keywords (max 5)
    """
    stop_words = set(stopwords.words("english"))
    
    tokens = word_tokenize(event_name.lower())
    tagged = pos_tag(tokens)
    keywords = []
    
    for word, tag in tagged:
        if (
            word.isalpha() and 
            word not in stop_words and 
            word not in GENERIC_WORDS and 
            tag.startswith(("NN", "JJ"))  # keep nouns & adjectives
        ):
            keywords.append(word)
    
    # Limit to maximum 5 keywords
    class_a_keywords = list(set(keywords))[:5]
    return class_a_keywords


def extract_class_b_keywords(event_subtitle: str) -> list:
    """
    Extract Class B keywords from event subtitle (no limits)
    
    Args:
        event_subtitle: Event subtitle/description
        
    Returns:
        List of Class B keywords (unlimited)
    """
    stop_words = set(stopwords.words("english"))
    
    tokens = word_tokenize(event_subtitle.lower())
    tagged = pos_tag(tokens)
    keywords = []
    
    for word, tag in tagged:
        if (
            word.isalpha() and 
            word not in stop_words and 
            word not in GENERIC_WORDS and 
            tag.startswith(("NN", "JJ"))  # keep nouns & adjectives
        ):
            keywords.append(word)
    
    return list(set(keywords))


def extract_classified_keywords(topic: str, sub_topic: str) -> dict:
    """
    Extract keywords classified according to client requirements
    
    Args:
        topic: Event topic (for Class A keywords)
        sub_topic: Event subtopic (for Class B keywords)
        
    Returns:
        Dictionary with 'class_a' and 'class_b' keyword lists
    """
    class_a = extract_class_a_keywords(topic)
    class_b = extract_class_b_keywords(sub_topic)
    
    return {
        'class_a': class_a,
        'class_b': class_b
    }


def extract_class_a_keywords_llm(event_name: str) -> list:
    """
    Extract Class A keywords using LLM (max 5, include synonyms)
    
    Args:
        event_name: Main event topic/name
        
    Returns:
        List of Class A keywords (max 5)
    """
    llm_model = ChatOpenAI(
        model="gpt-3.5-turbo", 
        temperature=0,
        api_key=OPENAI_SECRET_KEY
    )
    
    full_prompt = f"{class_a_keyword_prompt}\n\nEvent Name: {event_name}"
    response = llm_model.invoke(full_prompt)
    keywords_str = response.content if hasattr(response, "content") else str(response)
    keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
    
    # Limit to maximum 5 keywords
    return keywords[:5]


def extract_class_b_keywords_llm(event_subtitle: str) -> list:
    """
    Extract Class B keywords using LLM (unlimited)
    
    Args:
        event_subtitle: Event subtitle/description
        
    Returns:
        List of Class B keywords (unlimited)
    """
    llm_model = ChatOpenAI(
        model="gpt-3.5-turbo", 
        temperature=0,
        api_key=OPENAI_SECRET_KEY
    )
    
    full_prompt = f"{class_b_keyword_prompt}\n\nEvent Subtitle: {event_subtitle}"
    response = llm_model.invoke(full_prompt)
    keywords_str = response.content if hasattr(response, "content") else str(response)
    keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
    
    return keywords


def extract_classified_keywords_llm(topic: str, sub_topic: str) -> dict:
    """
    Extract classified keywords using LLM approach
    
    Args:
        topic: Event topic (for Class A keywords)
        sub_topic: Event subtopic (for Class B keywords)
        
    Returns:
        Dictionary with 'class_a' and 'class_b' keyword lists
    """
    class_a = extract_class_a_keywords_llm(topic)
    class_b = extract_class_b_keywords_llm(sub_topic)
    
    return {
        'class_a': class_a,
        'class_b': class_b
    }


# Legacy functions for backward compatibility
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
    llm_model = ChatOpenAI(
        model="gpt-3.5-turbo", 
        temperature=0,
        api_key=OPENAI_SECRET_KEY
    )
    
    text = topic + ' ' + sub_topic
    full_prompt = f"{keyword_extraction_prompt}\n\nText: {text}"
    response = llm_model.invoke(full_prompt)
    keywords_str = response.content if hasattr(response, "content") else str(response)
    keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
    return keywords

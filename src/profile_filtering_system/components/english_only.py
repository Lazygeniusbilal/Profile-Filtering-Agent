"""
English language filter component
"""
import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


def english_only(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter profiles to keep only English language content
    
    Args:
        df: Input DataFrame
        
    Returns:
        Filtered DataFrame with only English profiles
    """
    def is_english(text):
        try:
            return detect(str(text)) == 'en'
        except LangDetectException:
            return False
    
    filtered_df = df[df['summary'].fillna('').apply(is_english)]
    return filtered_df

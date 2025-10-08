
import io
import os
import streamlit as st
import pandas as pd
from pathlib import Path
from ensure import ensure_annotations

# Centralized OpenAI API key
OPENAI_SECRET_KEY = "sk-proj-" + "kkNzvfQ0JMBJl8P-v1lLbZ-S3ijDTUfBrmoxaAhdaskrBNSE5WDZTgehCyntoNm3WG3AgrczAoT3BlbkFJTtCuKsYJQ9uBDQrRdIasviq63E_8_2OEo-EzZOhv4f4tEVFZPOxXZlNAQ6ntgH7n-vN_oBxxAA"

def streamlit_file_handler(uploaded_file):
    """
    Handles Streamlit UploadedFile objects for CSV and Excel files.
    Returns a pandas DataFrame.
    """
    try:
        file_suffix = Path(uploaded_file.name).suffix.lower()
        if file_suffix == '.csv':
            df = pd.read_csv(uploaded_file)
        elif file_suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a CSV or Excel file.")
            return None
        return df
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None



@ensure_annotations
def file_reader(file_path: Path) -> pd.DataFrame:
    
    # try catch block
    try:
        # check if file path exists
        if os.path.exists(file_path):
            file_suffix = Path(file_path.name).suffix.lower()
            
            # check if it is .csv
            if file_suffix == '.csv':
                df= pd.read_csv(file_path)
            # check if it is excel file
            elif file_suffix in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            # that file extension is not readable
            else:
                print("File Extension doesnt exists with dataframe.")
        return df
    except Exception as e:
        print(e)
                
def return_if_empty(df):
    """
    Utility: If DataFrame is empty, return it immediately (for use in pipelines).
    """
    if df.empty:
        return df
    return None
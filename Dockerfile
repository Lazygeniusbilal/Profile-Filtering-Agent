# Use the official lightweight Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Download NLTK data (required for the app)
RUN python -c "import nltk; nltk.download('punkt', download_dir='/usr/local/nltk_data'); nltk.download('stopwords', download_dir='/usr/local/nltk_data'); nltk.download('punkt_tab', download_dir='/usr/local/nltk_data')"

# Set NLTK data path
ENV NLTK_DATA=/usr/local/nltk_data

# Copy only necessary files
COPY main.py ./
COPY src/ ./src/
COPY data/ ./data/

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

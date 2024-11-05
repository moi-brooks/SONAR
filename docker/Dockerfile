# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements/base.txt requirements/base.txt
COPY requirements/prod.txt requirements/prod.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements/prod.txt

# Install NLP models
RUN python -m spacy download en_core_web_lg
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Copy source code
COPY src/ /app/src/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
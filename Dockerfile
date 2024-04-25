FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Expose port you want your app on
EXPOSE 8501

# Upgrade pip and install requirements
COPY . .
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy app code and set working directory
COPY streamlit_app.py .

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "–server.port=8501", "–server.address=0.0.0.0"]
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY .streamlit/ ./.streamlit/
COPY src/ ./src/
COPY utils/ ./utils/
COPY assets/ ./assets/
COPY models/ ./models/
COPY app.py ./

# Render injects PORT env var; default to 10000 (Render's default)
ENV PORT=10000
EXPOSE $PORT

HEALTHCHECK CMD curl --fail http://localhost:${PORT}/_stcore/health

CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0

FROM python:3.11-slim

# Install LibreOffice and dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-java-common \
    default-jre-headless \
    poppler-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure storage directories exist for local mode
RUN mkdir -p storage/input storage/output

ENV PORT=8000
EXPOSE 8000

CMD ["python", "-m", "app.main"]

FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY smart_doc.py .

RUN mkdir -p test_data

CMD ["python", "smart_doc.py"]
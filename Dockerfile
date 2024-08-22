FROM python:3.10.14

RUN apt update -y

RUN apt install tesseract-ocr -y

RUN pip install torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu --no-cache-dir

COPY requirements.txt .
COPY main.py .

RUN pip install -r requirements.txt --no-cache-dir

CMD fastapi run main.py --port 8080
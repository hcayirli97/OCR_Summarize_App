import warnings
warnings.filterwarnings("ignore")
from fastapi import FastAPI, UploadFile, File

import pytesseract
from PIL import Image
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import pipeline
import io

app = FastAPI()

@app.on_event("startup")
def on_startup():
    global summarizer
    summarizer = pipeline("summarization", model="stevhliu/my_awesome_billsum_model")

@app.post("/OCR_Summarizer")
async def ocr_summerize(image_file: UploadFile = File(...)):
    image_content = await image_file.read()
    image = Image.open(io.BytesIO(image_content))

    prefix = "summarize: "
    extractedInformation = pytesseract.image_to_string(image)
    text = extractedInformation.replace("\n", " ")
    summerize_text = summarizer(prefix + text, max_length=100)[0]['summary_text']

    return {"OCR Output": text, "Summarize Output": summerize_text}


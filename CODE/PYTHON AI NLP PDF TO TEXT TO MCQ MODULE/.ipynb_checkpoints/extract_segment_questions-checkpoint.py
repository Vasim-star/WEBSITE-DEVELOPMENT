import re
from pdfplumber import open as pdf_open
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Step 1: Extract text from PDF
def extract_text(pdf_path):
    with pdf_open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Step 2: Segment text into potential questions
def segment_questions(text):
    return re.split(r'\n\d+\.', text)  # Splits at numbered questions like "1."

# Step 3: Classify segments into question types
def classify_segments(segments):
    model_name = "bert-base-uncased"  # Load pre-trained or fine-tuned BERT
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)  # MCQ, Numerical, Other
    
    predictions = []
    for segment in segments:
        inputs = tokenizer(segment, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        logits = outputs.logits
        label = torch.argmax(logits).item()
        predictions.append((segment, label))
    return predictions

# Step 4: Run the pipeline
pdf_path = "B:\PERSONAL DOCS\BUSSINESS MODEL\ONLINE EXAMINATION BUSINESS\CODE\PYTHON AI NLP PDF TO TEXT TO MCQ MODULE\extract_segment_questions.py"
text = extract_text(pdf_path)
segments = segment_questions(text)
classified_segments = classify_segments(segments)

for segment, label in classified_segments:
    print(f"Segment: {segment[:50]}... | Label: {label}")

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pdfminer
import pdfplumber
import io
import os
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import re

def clean_extracted_text(text):
    """function to clean extracted text"""
    
    clean_txt = text.replace('\n', ' ')
    clean_txt = text.replace('\t', ' ')
    clean_txt = text.replace('\x0c', ' ')   
    clean_txt = re.sub(r'\s+', ' ', text.strip()) # remove duplicated blank spaces
    return clean_txt




def pdfminer_text_extraction(pdf_path):
    
    """
    This function extracts text from pdf file using pdfminer lib and return text as string.
    :param pdf_path: path to pdf file.
    :return: text string containing text of pdf.
    """
    resource_manager = PDFResourceManager()
    output_string = io.StringIO()
    converter = TextConverter(resource_manager, output_string)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)

        text = output_string.getvalue()

    # close open handles
    converter.close()
    output_string.close()

    if text:
        return text
    return None


print(os.getcwd())


pdf_path = "B:\PERSONAL DOCS\BUSSINESS MODEL\ONLINE EXAMINATION BUSINESS\CODE\PYTHON AI NLP PDF TO TEXT TO MCQ MODULE\CAT2000.pdf"

text = pdfminer_text_extraction(pdf_path)

print("Sample extracted text using pdfminer:\n\n",text[:1000])

cleaned_text= clean_extracted_text(text)
print("Sample cleaned text after extraction using pdfminer:\n\n", cleaned_text[:1000])
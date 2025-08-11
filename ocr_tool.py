import os
from pathlib import Path
from PIL import Image
import pytesseract
from docx import Document
import fitz

# Optional: Set Tesseract path for Windows users
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\hp\AppData\Local\Tesseract-OCR\tesseract.exe'

def convert_image_to_txt(image_path, output_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Image converted to {output_path}")

def convert_pdf_to_txt(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        for page in doc:
            text = page.get_text()
            f.write(text)
    print(f"PDF converted to {output_path}")

def convert_docx_to_txt(docx_path, output_path):
    doc = Document(docx_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        for para in doc.paragraphs:
            f.write(para.text + '\n')
    print(f"DOCX converted to {output_path}")

def convert_file(input_file):
    input_path = Path(input_file)
    ext = input_path.suffix.lower()
    output_path = input_path.with_suffix('.txt')

    if ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif']:
        convert_image_to_txt(input_file, output_path)
    elif ext == '.pdf':
        convert_pdf_to_txt(input_file, output_path)
    elif ext == '.docx':
        convert_docx_to_txt(input_file, output_path)
    else:
        print(f"[!] Unsupported file type: {ext}")

# Example usage
# if __name__ == "__main__":
#     # Replace with your actual file path
#     input_file = "input_files/Project Details.pdf"
#     convert_file(input_file)

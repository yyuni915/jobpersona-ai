import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file.file)
    return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])

# def fetch_url_text(url: str) -> str:
#     response = requests.get(url, timeout=10)
#     soup = BeautifulSoup(response.text, "html.parser")
#     return soup.get_text(separator="\n")
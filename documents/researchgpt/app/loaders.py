from pypdf import PdfReader
from docx import Document
import requests
from bs4 import BeautifulSoup
def load_pdf(file_path: str) -> str:
    """
    Reads a PDF file and returns all its text as a single string.
    """
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text
def load_docx(file_path: str) -> str:
    """
    Reads a Word (.docx) file and returns all its text as a single string.
    """
    doc = Document(file_path)
    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text
def load_website(url: str) -> str:
    """
    Downloads a webpage and returns its visible text content.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    return "\n".join(lines)
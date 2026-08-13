import pymupdf
import os


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        text =  f.read()
    return text, 1, len(text.split())
    


def extract_text_from_pdf(file_path: str) -> str:
    document = pymupdf.open(file_path)
    text = ''
    
    for page in document:
        text += page.get_text()

    word_count = len(text.split())
    page_count = len(document)
    document.close()

    return text, page_count, word_count


def extract_text(file_path: str) -> str:

    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.txt':
        return extract_text_from_txt(file_path)

    elif ext == '.pdf':
        return extract_text_from_pdf(file_path)

    else:
        raise ValueError('Unsupported file type uploaded')

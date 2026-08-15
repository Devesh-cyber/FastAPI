import fitz


async def extract_content(file_path: str, file_type):
    '''
    Extract content from the file
    '''

    if file_type == 'pdf':
        pdf = fitz.open(file_path)
        data = ''
        for page in pdf:
            data += page.get_text()
        pdf.close()
        return data

    elif file_type == 'txt':
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()

        return data
    return None
  
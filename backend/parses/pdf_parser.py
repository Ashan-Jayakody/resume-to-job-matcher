from pypdf import PdfReader
import io

# function to extract the data from the pdf
def extract_text_from_pdf(file_bytes: bytes) ->str:
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading pdf: {e}")
        return ""
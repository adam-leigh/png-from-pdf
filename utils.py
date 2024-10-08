from datetime import datetime
import os

def save_uploaded_pdf(pdf_file):
    """Save the uploaded PDF to a temporary location."""
    if not os.path.exists("temp"):
        os.makedirs("temp")
    filename = f"{datetime.now().strftime('%s')}_{pdf_file.filename}"
    file_path = os.path.join("temp", filename)
    pdf_file.save(file_path)
    return file_path

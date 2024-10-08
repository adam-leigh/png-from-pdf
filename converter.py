from datetime import datetime
import io
import os
import zipfile

import fitz

def convert_pdf_to_png(pdf_path, dpi=200):
    """
    Convert a PDF file to PNG images and return a zip file containing the images.
    """
    doc = open_pdf(pdf_path)
    zip_buffer = create_zip_buffer()
    
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for page_num in range(len(doc)):
            page = load_pdf_page(doc, page_num)
            matrix = calculate_zoom_matrix(dpi)
            img_data = render_page_to_png(page, matrix)
            add_image_to_zip(zip_file, img_data, page_num)
    
    doc.close()
    zip_filename = generate_zip_filename(pdf_path)
    zip_buffer.seek(0)
    
    return zip_buffer, zip_filename

def open_pdf(pdf_path):
    """Open the PDF file and return the document object."""
    return fitz.open(pdf_path)

def create_zip_buffer():
    """Create a BytesIO object to store the zip file."""
    return io.BytesIO()

def load_pdf_page(doc, page_num):
    """Load a specific page from the PDF document."""
    return doc.load_page(page_num)

def calculate_zoom_matrix(dpi):
    """Calculate the zoom matrix based on the DPI."""
    zoom = dpi / 72
    return fitz.Matrix(zoom, zoom)

def render_page_to_png(page, matrix):
    """Render a PDF page to a PNG image in bytes."""
    pix = page.get_pixmap(matrix=matrix)
    return pix.tobytes("png")

def add_image_to_zip(zip_file, img_data, page_num):
    """Add the PNG image to the zip file with a filename based on the page number."""
    img_filename = f"page_{page_num + 1}.png"
    zip_file.writestr(img_filename, img_data)

def generate_zip_filename(pdf_path):
    """Generate a unique zip filename based on the PDF filename and current timestamp."""
    pdf_filename = os.path.basename(pdf_path)
    return f"{os.path.splitext(pdf_filename)[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"


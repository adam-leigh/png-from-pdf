from flask import Flask, request, jsonify, render_template, send_file
import os

from converter import convert_pdf_to_png
from utils import save_uploaded_pdf

app = Flask(__name__)


@app.route('/')
def index():
    """Render the index.html template."""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def convert_pdf():
    """Handle PDF POST request and convert it to PNG images."""
    if 'pdf_file' not in request.files:
        return jsonify({"error": "No PDF provided"}), 400
    
    pdf_file = request.files['pdf_file']
    pdf_path = save_uploaded_pdf(pdf_file)
    
    try:
        zip_buffer, zip_filename = convert_pdf_to_png(pdf_path, dpi=200)
        
        os.remove(pdf_path)
        
        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
    except Exception as e:
        os.remove(pdf_path)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

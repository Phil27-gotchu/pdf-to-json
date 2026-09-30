


from flask import Flask, jsonify, render_template, request
from pypdf.errors import PdfReadError

from converter import pdf_to_json

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
app.json.sort_keys = False


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/convert")
def convert():
    upload = request.files.get("pdf")
    if upload is None or not upload.filename:
        return jsonify(error="No file uploaded"), 400
    if not upload.filename.lower().endswith(".pdf"):
        return jsonify(error="Only PDF files are supported"), 400
    try:
        result = pdf_to_json(upload.stream, upload.filename)
    except PdfReadError:
        return jsonify(error="Could not read this PDF"), 400
    return jsonify(result)


@app.errorhandler(413)
def too_large(error):
    return jsonify(error="File is larger than 20 MB"), 413
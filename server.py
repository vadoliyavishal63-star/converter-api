from flask import Flask, request, send_file
from pdf2docx import Converter
from PIL import Image
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "ConvertEase API Running"

# -------------------------
# PDF TO WORD
# -------------------------
@app.route("/pdf-to-word", methods=["POST"])
def pdf_to_word():
    file = request.files["file"]
    input_file = "input.pdf"
    output_file = "output.docx"

    file.save(input_file)

    cv = Converter(input_file)
    cv.convert(output_file)
    cv.close()

    return send_file(output_file, as_attachment=True)


# -------------------------
# PDF TO JPG
# -------------------------
@app.route("/pdf-to-jpg", methods=["POST"])
def pdf_to_jpg():
    from pdf2image import convert_from_path

    file = request.files["file"]
    file.save("input.pdf")

    images = convert_from_path("input.pdf")
    images[0].save("output.jpg", "JPEG")

    return send_file("output.jpg", as_attachment=True)


# -------------------------
# JPG TO PDF
# -------------------------
@app.route("/jpg-to-pdf", methods=["POST"])
def jpg_to_pdf():
    file = request.files["file"]
    file.save("input.jpg")

    img = Image.open("input.jpg")
    img.convert("RGB").save("output.pdf")

    return send_file("output.pdf", as_attachment=True)


# -------------------------
# MERGE PDF
# -------------------------
@app.route("/merge-pdf", methods=["POST"])
def merge_pdf():
    files = request.files.getlist("files")

    merger = PdfMerger()

    for file in files:
        file.save(file.filename)
        merger.append(file.filename)

    merger.write("merged.pdf")
    merger.close()

    return send_file("merged.pdf", as_attachment=True)


# -------------------------
# SPLIT PDF
# -------------------------
@app.route("/split-pdf", methods=["POST"])
def split_pdf():
    file = request.files["file"]
    file.save("input.pdf")

    reader = PdfReader("input.pdf")
    writer = PdfWriter()

    writer.add_page(reader.pages[0])

    with open("split.pdf", "wb") as f:
        writer.write(f)

    return send_file("split.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
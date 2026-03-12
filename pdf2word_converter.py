import sys
import os
from pdf2docx import Converter

def convert_pdf_to_word(pdf_file, docx_file):
    try:
        # Convert PDF to Word
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        print(f"Conversion successful: {docx_file}")
        return True
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf2word_converter.py <input_pdf> <output_docx>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_docx = sys.argv[2]

    if not os.path.exists(input_pdf):
        print(f"Error: Input file not found: {input_pdf}", file=sys.stderr)
        sys.exit(1)

    success = convert_pdf_to_word(input_pdf, output_docx)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

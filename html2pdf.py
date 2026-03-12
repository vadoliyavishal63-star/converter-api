import sys
import os
from xhtml2pdf import pisa

def convert_html_to_pdf(source_html, output_filename):
    # utility function
    with open(source_html, "r", encoding='utf-8', errors='ignore') as source_file:
        source_content = source_file.read()

    with open(output_filename, "wb") as result_file:
        pisa_status = pisa.CreatePDF(
            source_content,
            dest=result_file
        )

    if pisa_status.err:
        print(f"Error during conversion: {pisa_status.err}")
        return False
    
    print(f"Conversion successful: {output_filename}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python html2pdf.py <input_html> <output_pdf>")
        sys.exit(1)

    input_html = sys.argv[1]
    output_pdf = sys.argv[2]

    if not os.path.exists(input_html):
        print(f"Error: Input file not found: {input_html}", file=sys.stderr)
        sys.exit(1)

    success = convert_html_to_pdf(input_html, output_pdf)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

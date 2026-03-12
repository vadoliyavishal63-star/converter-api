import sys
import os
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        # self.cell(0, 10, 'Text to PDF', 0, 1, 'C')

def convert_text_to_pdf(input_text, output_pdf):
    try:
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=11)
        
        with open(input_text, "r", encoding='utf-8', errors='replace') as f:
            for line in f:
                # FPDF (original and fpdf2) works best with latin-1 for standard fonts
                # We need to sanitize the input to avoid "Latin-1 codec can't encode character"
                # The previous error "single character" suggests an issue with cell() vs multi_cell() or font width calc.
                # Let's try to ensure clean latin-1 text.
                
                text = line.encode('latin-1', 'replace').decode('latin-1')
                # Remove tabs
                text = text.replace('\t', '    ')
                
                # Write line
                pdf.multi_cell(0, 5, text=text)
                
        pdf.output(output_pdf)
        print(f"Conversion successful: {output_pdf}")
        return True
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python text2pdf.py <input_txt> <output_pdf>")
        sys.exit(1)

    input_txt = sys.argv[1]
    output_pdf = sys.argv[2]

    if not os.path.exists(input_txt):
        print(f"Error: Input file not found: {input_txt}", file=sys.stderr)
        sys.exit(1)

    success = convert_text_to_pdf(input_txt, output_pdf)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

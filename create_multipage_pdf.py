from fpdf import FPDF
import sys

pdf = FPDF()
for i in range(1, 6):
    pdf.add_page()
    pdf.set_font("helvetica", size=24)
    pdf.cell(0, 10, f"Page {i}", 0, 1, 'C')

pdf.output("multipage_test.pdf")
print("multipage_test.pdf created")

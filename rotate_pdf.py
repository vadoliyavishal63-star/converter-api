import sys
import os
import fitz  # pymupdf

def rotate_pdf(input_path, output_path, rotation, pages="all"):
    """
    Rotates PDF pages.
    rotation: Degrees to rotate (0, 90, 180, 270)
    pages: "all" or a comma-separated list of page numbers (1-indexed) or ranges (e.g., "1-3,5")
    """
    try:
        doc = fitz.open(input_path)
        
        target_pages = []
        if pages == "all":
            target_pages = range(len(doc))
        else:
            # Parse page selection (e.g., "1,2,5-8")
            for part in pages.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    target_pages.extend(range(start - 1, end))
                else:
                    target_pages.append(int(part) - 1)
        
        for pno in target_pages:
            if 0 <= pno < len(doc):
                page = doc[pno]
                # set_rotation adds to existing rotation. 
                # We want to set it relative to 0 or add? 
                # Usually users mean "rotate 90 degrees more".
                current_rotation = page.rotation
                page.set_rotation((current_rotation + int(rotation)) % 360)
        
        doc.save(output_path)
        doc.close()
        print(f"SUCCESS: Rotated pages {pages} by {rotation} degrees.")
        return True
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python rotate_pdf.py <input_pdf> <output_pdf> <rotation_degrees> [pages_selection]")
        sys.exit(1)
        
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    rotation = sys.argv[3]
    pages = sys.argv[4] if len(sys.argv) > 4 else "all"
    
    if rotate_pdf(input_pdf, output_pdf, rotation, pages):
        sys.exit(0)
    else:
        sys.exit(1)

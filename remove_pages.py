import sys
import os
import fitz  # pymupdf

def remove_pages(input_path, output_path, pages):
    """
    pages: Comma-separated list of page numbers to remove (1-indexed) or ranges (e.g., "1-3,5")
    """
    try:
        doc = fitz.open(input_path)
        
        # Parse pages to remove
        to_remove = []
        for part in pages.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                to_remove.extend(range(start - 1, end))
            else:
                to_remove.append(int(part) - 1)
        
        # Sort in reverse to avoid index shifting during deletion
        to_remove = sorted(list(set(to_remove)), reverse=True)
        
        for pno in to_remove:
            if 0 <= pno < len(doc):
                doc.delete_page(pno)
        
        if len(doc) == 0:
            print("ERROR: Cannot remove all pages from PDF.", file=sys.stderr)
            doc.close()
            return False
            
        doc.save(output_path)
        doc.close()
        print(f"SUCCESS: Removed pages {pages}.")
        return True
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python remove_pages.py <input_pdf> <output_pdf> <pages_to_remove>")
        sys.exit(1)
        
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    pages = sys.argv[3]
    
    if remove_pages(input_pdf, output_pdf, pages):
        sys.exit(0)
    else:
        sys.exit(1)

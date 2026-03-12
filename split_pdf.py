import sys
import os
import fitz  # PyMuPDF

def parse_range(range_str, max_pages):
    """
    Parses a range string like "1-5, 8, 11-13" into a list of 0-based page indices.
    """
    pages = set()
    parts = range_str.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                # Adjust for 0-based index
                start = max(1, start) - 1
                end = min(max_pages, end) - 1
                if start <= end:
                    for i in range(start, end + 1):
                        pages.add(i)
            except ValueError:
                continue
        else:
            try:
                page = int(part) - 1
                if 0 <= page < max_pages:
                    pages.add(page)
            except ValueError:
                continue
    return sorted(list(pages))

def split_pdf(input_pdf, output_dir, range_str=None):
    try:
        doc = fitz.open(input_pdf)
        max_pages = len(doc)
        generated_files = []

        if range_str:
            # Mode 1: Extract specific pages into ONE new PDF
            selected_pages = parse_range(range_str, max_pages)
            
            if not selected_pages:
                print("Error: No valid pages selected.")
                return False

            out_doc = fitz.open()
            for page_num in selected_pages:
                out_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
            
            # Filename based on original + range
            input_basename = os.path.splitext(os.path.basename(input_pdf))[0]
            # Sanitize range string for filename
            safe_range = "".join(c for c in range_str if c.isalnum() or c in ('-', '_')).strip()[:20]
            output_filename = f"{input_basename}_split_{safe_range}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            out_doc.save(output_path)
            out_doc.close()
            generated_files.append(output_filename)

        else:
            # Mode 2: Burst all pages (Default behavior)
            input_basename = os.path.splitext(os.path.basename(input_pdf))[0]
            
            for i in range(max_pages):
                out_doc = fitz.open()
                out_doc.insert_pdf(doc, from_page=i, to_page=i)
                output_filename = f"{input_basename}_page_{i+1}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                out_doc.save(output_path)
                out_doc.close()
                generated_files.append(output_filename)

        doc.close()
        
        # Print generated files for PHP to capture
        print("GENERATED_FILES:" + "|".join(generated_files))
        return True

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python split_pdf.py <input_pdf> <output_dir> [range_string]")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_dir = sys.argv[2]
    # Check if range is provided as 3rd arg (actually 4th arg in sys.argv index logic if checking length)
    # sys.argv is [script, input, output, (range)]
    range_str = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.exists(input_pdf):
        print(f"Error: Input file not found: {input_pdf}", file=sys.stderr)
        sys.exit(1)

    if split_pdf(input_pdf, output_dir, range_str):
        sys.exit(0)
    else:
        sys.exit(1)

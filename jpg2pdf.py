import sys
import os
import img2pdf

def convert_jpg_to_pdf(image_files, output_pdf):
    try:
        # Convert images to PDF
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert(image_files))
        print(f"Conversion successful: {output_pdf}")
        return True
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python jpg2pdf.py <output_pdf> <input_jpg1> [input_jpg2 ...]")
        sys.exit(1)

    output_pdf = sys.argv[1]
    input_jpgs = sys.argv[2:]

    # Validate input files
    for jpg in input_jpgs:
        if not os.path.exists(jpg):
            print(f"Error: Input file not found: {jpg}", file=sys.stderr)
            sys.exit(1)

    success = convert_jpg_to_pdf(input_jpgs, output_pdf)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

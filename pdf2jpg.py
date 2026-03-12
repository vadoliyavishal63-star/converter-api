import sys
import os
import fitz  # pymupdf

def convert_pdf_to_jpg(pdf_path, output_dir):
    try:
        doc = fitz.open(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        generated_files = []
        
        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap(dpi=150)
            
            # Naming convention: filename_page_1.jpg
            # If only 1 page, maybe just filename.jpg? 
            # Let's keep consistent numbering for now to avoid overwriting if user converts same file twice (though PHP handles unique dirs usually)
            # Actually, PHP creates unique output filenames usually.
            # Let's use: base_name_page_X.jpg
            
            img_name = f"{base_name}_page_{i+1}.jpg"
            img_path = os.path.join(output_dir, img_name)
            
            # If single page, we might want cleaner name, but PHP renaming handles the download name.
            
            pix.save(img_path)
            generated_files.append(img_name)
                
        doc.close()
        
        # Print list of files for PHP to capture
        print("GENERATED_FILES:" + "|".join(generated_files))
        return True
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf2jpg.py <input_pdf> <output_dir>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(input_pdf):
        print(f"Error: Input file not found: {input_pdf}", file=sys.stderr)
        sys.exit(1)
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    success = convert_pdf_to_jpg(input_pdf, output_dir)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

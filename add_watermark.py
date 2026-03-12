import sys
import os
import fitz  # pymupdf

def add_watermark(input_path, output_path, text, opacity=0.3, fontsize=50):
    try:
        doc = fitz.open(input_path)
        
        # Color: Light Gray (0.7, 0.7, 0.7)
        color = (0.7, 0.7, 0.7)
        
        for page in doc:
            # Calculate center
            rect = page.rect
            width = rect.width
            height = rect.height
            
            # Use insert_template or insert_text
            # insert_text with rotation and opacity
            # For a "diagonal" watermark, we rotate the text
            
            # Simple centered watermark
            # Note: PyMuPDF doesn't have a direct "watermark" method in high level, 
            # but we can insert text with transparency.
            
            # Using insert_text with overlay=True
            # To get transparency, we can use a Shape or just lighter color.
            # PyMuPDF 1.18+ supports opacity in insert_text via 'fill_opacity'
            
            page.insert_text(
                (width/4, height/2), 
                text,
                fontsize=fontsize,
                color=color,
                rotate=45,
                fill_opacity=opacity
            )
            
        doc.save(output_path)
        doc.close()
        print(f"SUCCESS: Added watermark '{text}' to all pages.")
        return True
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python add_watermark.py <input_pdf> <output_pdf> <text> [opacity] [fontsize]")
        sys.exit(1)
        
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    text = sys.argv[3]
    opacity = float(sys.argv[4]) if len(sys.argv) > 4 else 0.3
    fontsize = int(sys.argv[5]) if len(sys.argv) > 5 else 50
    
    if add_watermark(input_pdf, output_pdf, text, opacity, fontsize):
        sys.exit(0)
    else:
        sys.exit(1)

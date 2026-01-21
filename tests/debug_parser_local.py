import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from app.services.resume_parser import resume_parser

def debug_parser():
    file_path = "sample_resume.docx"
    if not os.path.exists(file_path):
        print("File not found")
        return

    print("--- Extracting Text ---")
    raw_text = resume_parser.extract_text(file_path, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    print(repr(raw_text))
    
    print("\n--- extracting sections ---")
    sections = resume_parser._extract_sections(raw_text)
    print("Sections found:", sections.keys())
    for k, v in sections.items():
        print(f"{k}: {len(v)} items")
        if v:
            print(f"Sample {k}: {v[0]}")

if __name__ == "__main__":
    debug_parser()

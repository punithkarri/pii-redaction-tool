import os
import sys

# Ensure the project root is in the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.main import main

if __name__ == "__main__":
    input_file = os.path.join(project_root, "input", "Red Herring Prospectus.docx")
    output_file = os.path.join(project_root, "output", "Redacted_Red_Herring_Prospectus.docx")
    
    # Run main pipeline
    result = main(input_file, output_file)
    
    # Copy to public folder for static Vercel download
    import shutil
    public_file = os.path.join(project_root, "public", "Redacted_Red_Herring_Prospectus.docx")
    os.makedirs(os.path.dirname(public_file), exist_ok=True)
    shutil.copy(output_file, public_file)
    print(f"Copied redacted document to static website: {public_file}")


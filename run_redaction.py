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
    main(input_file, output_file)

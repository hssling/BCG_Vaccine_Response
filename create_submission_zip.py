
import zipfile
import os
from pathlib import Path
import shutil

# Config
BASE_DIR = Path("d:/research-automation/TB multiomics/TB Chromatin Priming Multiomics/BCG_Vaccine_Response")
MANUSCRIPT_DIR = BASE_DIR / "4_manuscript"
FIGURES_DIR = BASE_DIR / "3_results/figures"
ARTIFACTS_DIR = Path("C:/Users/hssli/.gemini/antigravity/brain/b402a181-faf0-426a-9375-226adfc1b53a")

OUTPUT_ZIP = MANUSCRIPT_DIR / "BCG_Submission_Package_Pathogens_Immunity.zip"

def create_zip():
    print(f"Creating submission package at {OUTPUT_ZIP}...")
    
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 1. Main Manuscript
        manuscript = MANUSCRIPT_DIR / "Manuscript_BCG_Systematic_Review_EXPANDED.docx"
        if manuscript.exists():
            zipf.write(manuscript, arcname="Manuscript_Main.docx")
            print(f"Added: {manuscript.name}")
        else:
            print(f"ERROR: Manuscript not found at {manuscript}")

        # 2. Cover Letter
        cover_letter = MANUSCRIPT_DIR / "Cover_Letter_BCG_Systematic_Review.docx"
        if cover_letter.exists():
            zipf.write(cover_letter, arcname="Cover_Letter.docx")
            print(f"Added: {cover_letter.name}")
        
        # 3. Figures (Optional but good practice to include separately)
        if FIGURES_DIR.exists():
            for fig in FIGURES_DIR.glob("*.png"):
                zipf.write(fig, arcname=f"Figures/{fig.name}")
                print(f"Added Figure: {fig.name}")

        # 4. Verification Certificate (as Supplement)
        cert = ARTIFACTS_DIR / "Data_Verification_Certificate.md"
        if cert.exists():
            zipf.write(cert, arcname="Supplementary_Data_Verification.md")
            print(f"Added: {cert.name}")

    print("ZIP creation complete.")

if __name__ == "__main__":
    create_zip()

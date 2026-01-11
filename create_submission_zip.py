
import zipfile
import os
from pathlib import Path

def create_submission_zip():
    base_dir = Path("d:/research-automation/TB multiomics/TB Chromatin Priming Multiomics/BCG_Vaccine_Response")
    output_zip = base_dir / "BCG_Submission_Package_Pathogens_Immunity.zip"
    
    files_to_include = [
        base_dir / "4_manuscript/Manuscript_BCG_Systematic_Review_FINAL_SUBMISSION_v2.docx",
        base_dir / "4_manuscript/Cover_Letter_PathogensImmunity.docx",
        base_dir / "4_manuscript/TitlePage_PathogensImmunity.docx",
        base_dir / "4_manuscript/Supplementary_Materials.docx",
        base_dir / "3_results/figures/Graphical_Abstract.png",
        base_dir / "3_results/figures/Fig1_Heterogeneity_Distribution.png",
        base_dir / "3_results/figures/Fig2_IL1B_Meta_Analysis_ForestPlot.png",
        base_dir / "3_results/tables/Table1_Included_Studies.csv",
        base_dir / "3_results/tables/Table2_IL1B_MetaAnalysis_Summary.csv",
        base_dir / "3_results/figures/FigS1_PRISMA_Flow_Diagram.png"
    ]
    
    with zipfile.ZipFile(output_zip, 'w') as zf:
        print(f"Creating submission package at {output_zip}...")
        for file_path in files_to_include:
            if file_path.exists():
                # Add file to root of zip
                zf.write(file_path, arcname=file_path.name)
                print(f"  Added: {file_path.name}")
            else:
                print(f"  WARNING: Missing file {file_path}")
    
    print("\nSubmission package created successfully.")

if __name__ == "__main__":
    create_submission_zip()

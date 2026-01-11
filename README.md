# Molecular Determinants of BCG Vaccine Response Heterogeneity
## A Systematic Review and Meta-Analysis of Multi-Omics Data

[![Reproducibility Check](https://github.com/hssling/BCG_Vaccine_Response/actions/workflows/reproducibility.yml/badge.svg)](https://github.com/hssling/BCG_Vaccine_Response/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Current Version:** v1.0.0 (Submission Ready)
**Date:** January 11, 2026

### 👨‍⚕️ Author & Affiliation
**Siddalingaiah H S, MD**  
Professor, Department of Community Medicine  
Shridevi Institute of Medical Sciences and Research Hospital  
Tumkur, Karnataka, India  
Email: `hssling@yahoo.com`

---

### 📖 Project Overview
This repository contains the verified data, analysis code, and manuscript assets for the Systematic Review: *"Molecular Determinants of BCG Vaccine Response Heterogeneity"*.

Unlike traditional narrative reviews, this project utilizes a **Quantitative Meta-Analysis** approach. We extracted raw data from 6 major multi-omics studies (N=662 individuals) to synthesize robust molecular predictors of trained immunity.

### 📂 Repository Structure
```
BCG_Vaccine_Response/
├── 1_data/
│   └── source_data_extraction.csv   # CERTIFIED raw data (N=662 verified)
├── 2_analysis/
│   ├── 02_systematic_review_analysis.py  # Main analysis script (Python)
│   └── requirements.txt                  # Dependencies
├── 3_results/
│   ├── figures/                     # Generated Figures (Trimodal Dist, Forest Plots)
│   └── tables/                      # Generated Tables
├── 4_manuscript/
│   ├── Manuscript_BCG_Systematic_Review_FINAL.docx
│   └── Cover_Letter_BCG_Systematic_Review.docx
└── .github/workflows/
    └── reproducibility.yml          # CI/CD pipeline for verifying results
```

### 🛡️ Data Integrity & Reproducibility
We adhere to strict scientific integrity standards.
*   **Data Source:** All analysis is derived *solely* from `1_data/source_data_extraction.csv`.
*   **Verification:** See [Data_Verification_Certificate.md](./Data_Verification_Certificate.md) for proof of audit against primary PMIDs.
*   **Reproduction:** Run the analysis script to regenerate all figures from scratch.

#### How to Reproduce Findings
1.  **Clone the repo:**
    ```bash
    git clone https://github.com/hssling/BCG_Vaccine_Response.git
    cd BCG_Vaccine_Response
    ```

2.  **Install requirements:**
    ```bash
    pip install pandas matplotlib seaborn python-docx
    ```

3.  **Run the analysis:**
    ```bash
    python 2_analysis/02_systematic_review_analysis.py
    ```
    *Output:* Figures will be generated in `3_results/figures/`.

### 📊 Key Findings (Synthesized)
*   **Trimodal Distribution:** ~30% High, 40% Moderate, 30% Low responders (Source: Moorlag et al.).
*   **Epigenetic Predictor:** H3K4me3 at TNF promoter (Odds Ratio 2.8).
*   **Persistence:** DNA methylation signatures persist >12 months (Source: Bannister et al.).

---
*Verified by AI-Assisted Audit Protocol (5 Rounds).*

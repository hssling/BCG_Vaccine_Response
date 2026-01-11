
"""
BCG Systematic Review Analysis - VALID IL-1β META-ANALYSIS
Reads RAW extracted data from source_data_extraction.csv
Generates CORRECT meta-analysis outputs:
- Focused on IL-1β fold-change (common outcome across 3 studies)
- Pooled effect size with 95% CI
- Forest plot with study weights
- Heterogeneity statistics (I², Q)

Studies included in IL-1β meta-analysis:
1. Moorlag 2024 (N=323) - OR 2.1
2. Arts 2018 (N=18) - 1.8x fold-change
3. Kleinnijenhuis 2012 (N=20) - 2.0x fold-change
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
from scipy import stats

# Config
BASE_DIR = Path("d:/research-automation/TB multiomics/TB Chromatin Priming Multiomics/BCG_Vaccine_Response")
DATA_FILE = BASE_DIR / "1_data/source_data_extraction.csv"
RESULTS_DIR = BASE_DIR / "3_results"
FIG_DIR = RESULTS_DIR / "figures"
TBL_DIR = RESULTS_DIR / "tables"

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TBL_DIR, exist_ok=True)

def load_data():
    print(f"Loading data from {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    return df

def compute_log_effect_se(effect_val, p_val):
    """Compute log effect size and SE from effect and p-value."""
    log_effect = np.log(effect_val)
    z = stats.norm.ppf(1 - p_val / 2)
    se = abs(log_effect / z) if z != 0 else 0.3
    return log_effect, se

def dersimonian_laird_meta(log_effects, ses):
    """DerSimonian-Laird random effects meta-analysis."""
    k = len(log_effects)
    if k < 2:
        return log_effects[0], ses[0], 0, 0, 0, 1.0
    
    weights = 1 / (ses ** 2)
    Q = np.sum(weights * (log_effects - np.sum(weights * log_effects) / np.sum(weights)) ** 2)
    df = k - 1
    Q_pval = 1 - stats.chi2.cdf(Q, df)
    I2 = max(0, (Q - df) / Q * 100) if Q > 0 else 0
    C = np.sum(weights) - np.sum(weights ** 2) / np.sum(weights)
    tau2 = max(0, (Q - df) / C) if C > 0 else 0
    re_weights = 1 / (ses ** 2 + tau2)
    pooled_log = np.sum(re_weights * log_effects) / np.sum(re_weights)
    pooled_se = np.sqrt(1 / np.sum(re_weights))
    
    return pooled_log, pooled_se, tau2, I2, Q, Q_pval

def generate_table_1_studies(df):
    """Generate Table 1: All Included Studies"""
    print("Generating Table 1...")
    studies = df[['Author', 'Year', 'Journal', 'N_Total', 'Platform', 'Key_Finding', 'Include_IL1B_Meta']].drop_duplicates()
    output_path = TBL_DIR / "Table1_Included_Studies.csv"
    studies.to_csv(output_path, index=False)
    print(f"Saved Table 1 to {output_path}")
    return studies

def generate_figure_1_heterogeneity(df):
    """Generate Figure 1: Response Heterogeneity (from Moorlag)"""
    print("Generating Figure 1 (Response Heterogeneity)...")
    
    moorlag = df[df['Author'].str.contains("Moorlag")].iloc[0]
    if pd.isna(moorlag['High_Responders_N']):
        print("No responder data in Moorlag row, skipping Figure 1.")
        return
    
    categories = ['High Responders', 'Moderate Responders', 'Low Responders']
    counts = [moorlag['High_Responders_N'], moorlag['Moderate_Responders_N'], moorlag['Low_Responders_N']]
    total = sum(counts)
    percentages = [c/total*100 for c in counts]
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(categories, counts, color=['#2ca02c', '#ff7f0e', '#d62728'], edgecolor='black')
    # Adjusted title y-position and layout to prevent overflow
    plt.title(f"BCG Response Heterogeneity\n(Data Source: {moorlag['Author']} {moorlag['Year']}, N={int(total)})", fontsize=14, y=1.05)
    plt.ylabel("Number of Individuals")
    
    for bar, count, pct in zip(bars, counts, percentages):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                 f'{int(count)}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    # Explicitly adjust top margin to accommodate title
    plt.subplots_adjust(top=0.90)
    output_path = FIG_DIR / "Fig1_Heterogeneity_Distribution.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    plt.close()
    print(f"Saved Figure 1 to {output_path}")

def generate_figure_s1_prisma():
    """Generate Figure S1: PRISMA Flow Diagram"""
    print("Generating Figure S1 (PRISMA Flow Diagram)...")
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.axis('off')
    
    # Define box coordinates and text
    boxes = [
        {'text': "Identification of studies via databases\n(PubMed/MEDLINE)\n(n = 487)", 'xy': (0.5, 0.9), 'box_color': '#E0E0E0'},
        {'text': "Records removed before screening:\nDuplicate records removed (n = 175)", 'xy': (0.8, 0.8), 'box_color': '#FFCDD2'},
        {'text': "Records screened\n(n = 312)", 'xy': (0.5, 0.7), 'box_color': '#E0E0E0'},
        {'text': "Records excluded\n(n = 267)", 'xy': (0.8, 0.7), 'box_color': '#FFCDD2'},
        {'text': "Reports sought for retrieval\n(n = 45)", 'xy': (0.5, 0.5), 'box_color': '#E0E0E0'},
        {'text': "Reports assessed for eligibility\n(n = 45)", 'xy': (0.5, 0.35), 'box_color': '#E0E0E0'},
        {'text': "Reports excluded:\nNo multi-omics (n=8)\nAdaptive immunity only (n=6)\nNo heterogeneity (n=5)\nInsufficient data (n=3)\nNon-English (n=1)", 'xy': (0.8, 0.35), 'box_color': '#FFCDD2'},
        {'text': "Studies included in review\n(n = 22)", 'xy': (0.5, 0.1), 'box_color': '#C8E6C9'}
    ]
    
    # Draw boxes
    for box in boxes:
        ax.text(box['xy'][0], box['xy'][1], box['text'], ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', fc=box['box_color'], ec="black"), fontsize=10)
        
    # Draw arrows
    ax.annotate('', xy=(0.5, 0.82), xytext=(0.5, 0.86), arrowprops=dict(arrowstyle='->', lw=1.5)) # ID to Screening
    ax.annotate('', xy=(0.5, 0.62), xytext=(0.5, 0.66), arrowprops=dict(arrowstyle='->', lw=1.5)) # Screening to Retrieval
    ax.annotate('', xy=(0.5, 0.42), xytext=(0.5, 0.46), arrowprops=dict(arrowstyle='->', lw=1.5)) # Retrieval to Eligibility
    ax.annotate('', xy=(0.5, 0.15), xytext=(0.5, 0.28), arrowprops=dict(arrowstyle='->', lw=1.5)) # Eligibility to Included
    
    # Exclusion arrows
    ax.annotate('', xy=(0.65, 0.7), xytext=(0.58, 0.7), arrowprops=dict(arrowstyle='->', lw=1.5)) # Screened to Excluded
    ax.annotate('', xy=(0.65, 0.35), xytext=(0.58, 0.35), arrowprops=dict(arrowstyle='->', lw=1.5)) # Eligibility to Excluded Reasons

    plt.tight_layout()
    output_path = FIG_DIR / "FigS1_PRISMA_Flow_Diagram.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved Figure S1 to {output_path}")

def generate_figure_2_il1b_forest_plot(df):
    """Generate Figure 2: IL-1β-SPECIFIC Forest Plot (Valid Meta-Analysis)"""
    print("Generating Figure 2 (IL-1β Meta-Analysis Forest Plot)...")
    
    # Filter to studies included in IL-1β meta-analysis
    il1b_studies = df[df['Include_IL1B_Meta'] == 'YES'].copy()
    
    if len(il1b_studies) < 2:
        print("ERROR: Insufficient IL-1β studies for meta-analysis.")
        return None
    
    # Compute effect sizes
    log_effects = []
    ses = []
    for _, row in il1b_studies.iterrows():
        effect = row['IL1B_FoldChange']
        p = row['Predictor_Pval']
        log_e, se = compute_log_effect_se(effect, p)
        log_effects.append(log_e)
        ses.append(se)
    
    il1b_studies['log_effect'] = log_effects
    il1b_studies['SE'] = ses
    il1b_studies['CI_lower'] = np.exp(il1b_studies['log_effect'] - 1.96 * il1b_studies['SE'])
    il1b_studies['CI_upper'] = np.exp(il1b_studies['log_effect'] + 1.96 * il1b_studies['SE'])
    
    # Compute pooled estimate
    pooled_log, pooled_se, tau2, I2, Q, Q_pval = dersimonian_laird_meta(
        np.array(log_effects), np.array(ses)
    )
    pooled_effect = np.exp(pooled_log)
    pooled_ci_lower = np.exp(pooled_log - 1.96 * pooled_se)
    pooled_ci_upper = np.exp(pooled_log + 1.96 * pooled_se)
    
    # Create forest plot - WIDER figure to prevent text overflow
    fig, ax = plt.subplots(figsize=(14, 6))
    
    y_positions = list(range(len(il1b_studies), 0, -1))
    
    # Plot individual studies
    for i, (_, row) in enumerate(il1b_studies.iterrows()):
        y = y_positions[i]
        effect = row['IL1B_FoldChange']
        ci_low = row['CI_lower']
        ci_high = row['CI_upper']
        n = row['N_Total']
        
        # Weight proportional to 1/SE²
        weight = 1 / (row['SE'] ** 2)
        marker_size = max(80, min(400, weight * 30))
        ax.scatter(effect, y, s=marker_size, color='#1f77b4', zorder=3, marker='s')
        ax.plot([ci_low, ci_high], [y, y], color='#1f77b4', linewidth=2, zorder=2)
        
        # Study label (left side)
        label = f"{row['Author']} ({row['Year']}) [N={int(n)}]"
        ax.text(0.55, y, label, ha='left', va='center', fontsize=10)
        
        # Effect size on right - moved left to fit in box
        txt = f"{effect:.2f} [{ci_low:.2f}, {ci_high:.2f}]"
        ax.text(3.5, y, txt, ha='left', va='center', fontsize=9, family='monospace')
    
    # Pooled estimate (diamond)
    diamond_y = 0
    diamond_half_height = 0.25
    diamond_x = [pooled_ci_lower, pooled_effect, pooled_ci_upper, pooled_effect]
    diamond_y_coords = [diamond_y, diamond_y + diamond_half_height, diamond_y, diamond_y - diamond_half_height]
    ax.fill(diamond_x, diamond_y_coords, color='#d62728', zorder=3)
    ax.text(0.55, diamond_y, "Pooled (Random Effects)", ha='left', va='center', fontsize=10, fontweight='bold')
    txt = f"{pooled_effect:.2f} [{pooled_ci_lower:.2f}, {pooled_ci_upper:.2f}]"
    ax.text(3.5, diamond_y, txt, ha='left', va='center', fontsize=9, family='monospace', fontweight='bold')
    
    # Reference line at effect=1
    ax.axvline(x=1, color='black', linestyle='--', linewidth=1, zorder=1)
    
    # Formatting
    ax.set_xlim(0.4, 6)
    ax.set_xscale('log')
    ax.set_xlabel("IL-1β Fold-Change / Odds Ratio (95% CI)", fontsize=12)
    ax.set_ylim(-0.8, len(il1b_studies) + 1)
    ax.set_yticks([])
    
    # Title with heterogeneity
    total_n = il1b_studies['N_Total'].sum()
    title = f"Forest Plot: IL-1β Response as Predictor of BCG Trained Immunity\n"
    title += f"3 Studies, N={int(total_n)} | I² = {I2:.1f}%, Q = {Q:.2f} (p = {Q_pval:.3f})"
    ax.set_title(title, fontsize=13)
    
    # Header labels - aligned with data columns
    ax.text(0.55, len(il1b_studies) + 0.6, "Study", ha='left', va='center', fontsize=11, fontweight='bold')
    ax.text(3.5, len(il1b_studies) + 0.6, "Effect [95% CI]", ha='left', va='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    output_path = FIG_DIR / "Fig2_IL1B_Meta_Analysis_ForestPlot.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved Figure 2 (IL-1β Forest Plot) to {output_path}")
    
    return {
        'pooled_effect': pooled_effect,
        'pooled_ci_lower': pooled_ci_lower,
        'pooled_ci_upper': pooled_ci_upper,
        'I2': I2,
        'Q': Q,
        'Q_pval': Q_pval,
        'tau2': tau2,
        'n_studies': len(il1b_studies),
        'total_n': int(total_n)
    }

def generate_table_2_meta_results(meta_results):
    """Generate Table 2: IL-1β Meta-Analysis Summary"""
    print("Generating Table 2 (Meta-Analysis Summary)...")
    
    if meta_results is None:
        return
    
    summary = pd.DataFrame([{
        'Metric': 'Pooled IL-1β Effect',
        'Value': f"{meta_results['pooled_effect']:.2f}",
        '95% CI': f"[{meta_results['pooled_ci_lower']:.2f}, {meta_results['pooled_ci_upper']:.2f}]"
    }, {
        'Metric': 'Heterogeneity (I²)',
        'Value': f"{meta_results['I2']:.1f}%",
        '95% CI': 'N/A'
    }, {
        'Metric': "Cochran's Q",
        'Value': f"{meta_results['Q']:.2f}",
        '95% CI': f"p = {meta_results['Q_pval']:.3f}"
    }, {
        'Metric': 'Between-study variance (τ²)',
        'Value': f"{meta_results['tau2']:.4f}",
        '95% CI': 'N/A'
    }, {
        'Metric': 'Studies included',
        'Value': str(meta_results['n_studies']),
        '95% CI': f"Total N = {meta_results['total_n']}"
    }])
    
    output_path = TBL_DIR / "Table2_IL1B_MetaAnalysis_Summary.csv"
    summary.to_csv(output_path, index=False)
    print(f"Saved Table 2 to {output_path}")

def main():
    df = load_data()
    
    # 1. Table of all studies
    studies = generate_table_1_studies(df)
    total_n = studies['N_Total'].sum()
    print(f"Total N across all {len(studies)} studies: {total_n}")
    
    # 2. Response heterogeneity figure
    generate_figure_1_heterogeneity(df)
    
    # 2. PRISMA Flow Diagram
    generate_figure_s1_prisma()

    # 3. IL-1β-SPECIFIC Meta-Analysis (VALID)
    meta_results = generate_figure_2_il1b_forest_plot(df)
    
    # 4. Meta-analysis summary table
    generate_table_2_meta_results(meta_results)
    
    print("\n" + "="*70)
    print("VALID IL-1β META-ANALYSIS COMPLETE")
    print("="*70)
    if meta_results:
        print(f"Outcome: IL-1β fold-change/OR as predictor of trained immunity")
        print(f"Studies: {meta_results['n_studies']} (N = {meta_results['total_n']})")
        print(f"Pooled Effect: {meta_results['pooled_effect']:.2f} (95% CI: {meta_results['pooled_ci_lower']:.2f}-{meta_results['pooled_ci_upper']:.2f})")
        print(f"Heterogeneity I²: {meta_results['I2']:.1f}%")
        print(f"Cochran's Q: {meta_results['Q']:.2f} (p={meta_results['Q_pval']:.3f})")
    print("="*70)

if __name__ == "__main__":
    main()

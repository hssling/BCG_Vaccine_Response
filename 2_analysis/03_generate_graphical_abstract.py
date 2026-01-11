
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

BASE_DIR = Path("d:/research-automation/TB multiomics/TB Chromatin Priming Multiomics/BCG_Vaccine_Response")
OUTPUT_DIR = BASE_DIR / "3_results" / "figures"

def create_graphical_abstract():
    # Setup figure
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    # Colors
    c_bcg = '#1f77b4'
    c_high = '#2ca02c'
    c_mod = '#ff7f0e'
    c_low = '#d62728'
    c_pred = '#9467bd'
    
    # 1. Panel 1: BCG Vaccination
    # Draw Syringe/Vial schematic (simplified as Box)
    rect_vax = patches.FancyBboxPatch((0.05, 0.4), 0.2, 0.4, boxstyle="round,pad=0.05", 
                                      linewidth=2, edgecolor=c_bcg, facecolor='white')
    ax.add_patch(rect_vax)
    ax.text(0.15, 0.65, "BCG\nVaccine", ha='center', va='center', fontsize=16, fontweight='bold', color=c_bcg)
    
    # Arrow to heterogeneity
    ax.arrow(0.27, 0.6, 0.08, 0, head_width=0.03, head_length=0.03, fc='black', ec='black')
    
    # 2. Panel 2: Response Heterogeneity (Pie Chart in center)
    # Draw "Population" box
    # We'll use a pie chart inset
    ax_pie = fig.add_axes([0.35, 0.4, 0.25, 0.4]) # [left, bottom, width, height]
    sizes = [30, 40, 30]
    labels = ['High\n(30%)', 'Moderate\n(40%)', 'Low\n(30%)']
    colors = [c_high, c_mod, c_low]
    wedges, texts = ax_pie.pie(sizes, labels=labels, colors=colors, startangle=90, 
                               wedgeprops={'edgecolor': 'white', 'linewidth': 2},
                               textprops={'fontsize': 10, 'weight': 'bold'})
    ax_pie.set_title("Response Heterogeneity", fontsize=12, fontweight='bold', pad=10)
    
    # 3. Panel 3: Predictor Discovery
    # Arrow from pie
    ax.arrow(0.62, 0.6, 0.08, 0, head_width=0.03, head_length=0.03, fc='black', ec='black')
    
    # Result Box
    rect_res = patches.FancyBboxPatch((0.72, 0.35), 0.23, 0.5, boxstyle="round,pad=0.05", 
                                      linewidth=2, edgecolor=c_pred, facecolor='#f0f0f5')
    ax.add_patch(rect_res)
    
    ax.text(0.835, 0.75, "Key Predictor", ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(0.835, 0.65, "IL-1β Production", ha='center', va='center', fontsize=16, fontweight='bold', color='#d62728')
    ax.text(0.835, 0.55, "Meta-Analysis:\nOR = 1.96\n(I² = 0%)", ha='center', va='center', fontsize=12)
    
    # 4. Implications (Bottom Banner)
    rect_imp = patches.FancyBboxPatch((0.2, 0.05), 0.6, 0.15, boxstyle="round,pad=0.02", 
                                      linewidth=0, facecolor='#e6ffe6')
    ax.add_patch(rect_imp)
    ax.text(0.5, 0.125, "Implication: Personalized Vaccination Stratification", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='darkgreen')
            
    # Connecting arrows to implications
    ax.annotate('', xy=(0.5, 0.22), xytext=(0.48, 0.38), arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-0.2", color='gray', lw=2))
    ax.annotate('', xy=(0.6, 0.22), xytext=(0.8, 0.33), arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=0.2", color='gray', lw=2))

    # Save
    output_path = OUTPUT_DIR / "Graphical_Abstract.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Graphical Abstract saved to {output_path}")

if __name__ == "__main__":
    create_graphical_abstract()

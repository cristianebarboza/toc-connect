from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def save_connectivity_report(matrix: pd.DataFrame, output_dir: str | Path) -> None:
    """Salva matriz e figura de calor em arquivos simples e compartilháveis."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    matrix.to_csv(out / "connectivity_fisher_z.csv", index_label="roi")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(matrix, cmap="vlag", center=0, square=True, annot=True, fmt=".2f", ax=ax,
                cbar_kws={"label": "Conectividade (z de Fisher)"})
    ax.set_title("Conectividade funcional entre ROIs")
    fig.tight_layout()
    fig.savefig(out / "connectivity_heatmap.png", dpi=180)
    plt.close(fig)

"""Gera uma demonstração sem dados humanos ou clínicos."""
from pathlib import Path
import numpy as np
import pandas as pd
from toc_connect.core import fisher_z_connectivity
from toc_connect.report import save_connectivity_report

rng = np.random.default_rng(42)
base = rng.normal(size=180)
timeseries = pd.DataFrame({
    "OFC": base + rng.normal(scale=.35, size=180),
    "caudado": .55 * base + rng.normal(scale=.70, size=180),
    "putamen": -.25 * base + rng.normal(scale=.85, size=180),
    "talamo": .35 * base + rng.normal(scale=.75, size=180),
    "ACC": .45 * base + rng.normal(scale=.70, size=180),
})
out = Path("results/demo_synthetic")
save_connectivity_report(fisher_z_connectivity(timeseries), out)
print(f"Demonstração criada em: {out.resolve()}")

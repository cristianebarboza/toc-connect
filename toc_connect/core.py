from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd


def _nilearn():
    """Importa Nilearn somente quando imagens NIfTI forem processadas."""
    try:
        from nilearn.maskers import NiftiMasker
        from nilearn import image
        return NiftiMasker, image
    except ImportError as error:
        raise ImportError("Para processar NIfTI, instale as dependências: pip install -e .") from error



def discover_bold(bids_dir: str | Path) -> list[Path]:
    """Encontra imagens BOLD NIfTI recursivamente em uma pasta BIDS."""
    root = Path(bids_dir)
    files = sorted(root.rglob("*_bold.nii")) + sorted(root.rglob("*_bold.nii.gz"))
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo *_bold.nii[.gz] encontrado em {root}")
    return files


def load_masks(masks_dir: str | Path) -> dict[str, Path]:
    """Carrega máscaras NIfTI; o nome do arquivo torna-se o nome da ROI."""
    masks = {}
    for path in sorted(Path(masks_dir).glob("*.nii*")):
        name = path.name.replace(".nii.gz", "").replace(".nii", "")
        masks[name] = path
    if len(masks) < 2:
        raise ValueError("Forneça ao menos duas máscaras NIfTI de regiões de interesse.")
    return masks


def extract_roi_timeseries(bold_path: str | Path, masks: dict[str, Path], tr: float) -> pd.DataFrame:
    """Extrai a média temporal de cada ROI, reamostrando máscara quando necessário."""
    NiftiMasker, image = _nilearn()
    bold = image.load_img(bold_path)
    signals = {}
    for name, mask_path in masks.items():
        mask = image.resample_to_img(mask_path, bold, interpolation="nearest", force_resample=True)
        masker = NiftiMasker(mask_img=mask, standardize="zscore_sample", t_r=tr)
        values = masker.fit_transform(bold)
        if values.shape[1] == 0:
            raise ValueError(f"Máscara vazia após reamostragem: {name}")
        signals[name] = values.mean(axis=1)
    return pd.DataFrame(signals)


def fisher_z_connectivity(timeseries: pd.DataFrame) -> pd.DataFrame:
    """Calcula correlações ROI-a-ROI e a transformação z de Fisher."""
    corr = timeseries.corr(method="pearson").clip(-0.999999, 0.999999)

    z = pd.DataFrame(
        np.arctanh(corr.to_numpy()),
        index=corr.index,
        columns=corr.columns,
    )

    for roi in z.index:
        z.loc[roi, roi] = 0.0

    return z
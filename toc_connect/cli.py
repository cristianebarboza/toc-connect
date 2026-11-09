from __future__ import annotations
import argparse, json
from pathlib import Path
from .core import discover_bold, load_masks, extract_roi_timeseries, fisher_z_connectivity
from .report import save_connectivity_report


def run(args: argparse.Namespace) -> None:
    bold_files = discover_bold(args.bids_dir)
    masks = load_masks(args.masks_dir)
    output = Path(args.output_dir)
    subjects = []
    for bold in bold_files:
        subject = next((part for part in bold.parts if part.startswith("sub-")), bold.stem.split("_")[0])
        subject_dir = output / subject
        ts = extract_roi_timeseries(bold, masks, args.tr)
        matrix = fisher_z_connectivity(ts)
        save_connectivity_report(matrix, subject_dir)
        subjects.append({"subject": subject, "bold_file": str(bold), "n_volumes": len(ts)})
        print(f"OK: {subject} → {subject_dir}")
    summary = {"tr_seconds": args.tr, "rois": list(masks), "processed": subjects}
    output.mkdir(parents=True, exist_ok=True)
    (output / "run_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Conectividade funcional de ROIs no TOC.")
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("run", help="processa imagens BOLD em uma pasta BIDS")
    command.add_argument("--bids-dir", required=True, help="pasta-raiz BIDS")
    command.add_argument("--masks-dir", required=True, help="pasta com máscaras ROI NIfTI")
    command.add_argument("--output-dir", default="results", help="pasta de saída")
    command.add_argument("--tr", type=float, required=True, help="tempo de repetição em segundos")
    command.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

"""Run the PISCES public-preview model on normalized 60-step windows."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

FEATURE_COLUMNS = ["bx", "by", "bz", "bt", "density", "speed", "temperature"]
REQUIRED_COLUMNS = ["window_id", "step", *FEATURE_COLUMNS]
METADATA_COLUMNS = ["start_utc", "source"]
WINDOW_SIZE = 60
DEFAULT_MODEL = Path(__file__).resolve().parents[1] / "model" / "pisces_preview.pt"


def _load_windows(path: Path) -> tuple[pd.DataFrame, np.ndarray]:
    df = pd.read_csv(path, dtype={"window_id": "string", "start_utc": "string", "source": "string"})
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")
    if df[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError("required columns must not contain blank or NaN values")

    metadata_rows: list[dict[str, str]] = []
    windows: list[np.ndarray] = []

    for window_id, group in df.groupby("window_id", sort=False, dropna=False):
        group = group.sort_values("step")
        if len(group) != WINDOW_SIZE:
            raise ValueError(f"window {window_id!r} has {len(group)} rows; expected {WINDOW_SIZE}")
        steps = group["step"].to_numpy()
        if not np.array_equal(steps, np.arange(WINDOW_SIZE)):
            raise ValueError(f"window {window_id!r} step values must be 0..{WINDOW_SIZE - 1}")
        feature_values = group[FEATURE_COLUMNS].astype(np.float32).to_numpy()
        if not np.isfinite(feature_values).all():
            raise ValueError(f"window {window_id!r} contains non-finite values")

        row = {"window_id": str(window_id)}
        for column in METADATA_COLUMNS:
            if column in group.columns:
                non_null = group[column].dropna()
                metadata_values = non_null.astype(str).unique()
                if len(metadata_values) == 0:
                    continue
                if len(metadata_values) > 1 or len(non_null) != len(group):
                    raise ValueError(f"window {window_id!r} metadata column {column!r} must be constant or blank")
                row[column] = metadata_values[0]
        metadata_rows.append(row)
        windows.append(feature_values)

    if not windows:
        raise ValueError("input file contains no windows")

    return pd.DataFrame(metadata_rows), np.stack(windows, axis=0)


def run(model_path: Path, input_path: Path, output_path: Path) -> None:
    metadata, windows = _load_windows(input_path)
    if not model_path.exists():
        raise FileNotFoundError(f"model file not found: {model_path}")

    model = torch.jit.load(str(model_path), map_location="cpu")
    model.eval()

    x = torch.from_numpy(windows).permute(0, 2, 1).contiguous()
    with torch.no_grad():
        recon = model(x).permute(0, 2, 1).cpu().numpy()

    if recon.shape != windows.shape:
        raise RuntimeError(f"model output shape {recon.shape} does not match input shape {windows.shape}")

    output = metadata.copy()
    output["reconstruction_error"] = ((recon - windows) ** 2).mean(axis=(1, 2))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the PISCES public-preview model.")
    parser.add_argument("input_csv", type=Path, help="CSV of normalized 60-step windows")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--out", type=Path, default=Path("preview_output.csv"))
    args = parser.parse_args()

    try:
        run(args.model, args.input_csv, args.out)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

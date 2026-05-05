# PISCES model card

## Artifact

- Model: `model/pisces_preview.pt`
- Runner: `pisces_preview/run_preview.py`

## Input

Normalized 60-step windows with seven channels:

```text
bx, by, bz, bt, density, speed, temperature
```

Optional `start_utc` and `source` metadata columns are allowed.

## Output

```text
window_id,reconstruction_error
```

If `start_utc` or `source` is present in the input, it is copied to the output. `reconstruction_error` is unweighted mean squared reconstruction error in normalized input space.

## Examples

Synthetic example:

```bash
python -m pisces_preview.run_preview examples/example_normalized_windows.csv --out preview_output.csv
```

NASA OMNI preview windows:

```bash
python -m pisces_preview.run_preview examples/omni_may2024_preview_windows.csv --out omni_preview_output.csv
```

Expected OMNI output is in `examples/expected_preview_output.csv`.

## Scope

This preview includes the initial model, small normalized inputs, and supporting materials. Full preprocessing, scoring, thresholds, event evaluation, training, and baselines are planned for the full release.

## Citation

```bibtex
@inproceedings{march2026pisces,
  title={{PISCES}: Physics-Informed Convolutional Autoencoder for Solar Wind Anomaly
         Detection and Space Weather Early Warning},
  author={March, Alison J. and Lee, Kevin},
  booktitle={NASA 5th Eddy Cross-Disciplinary Symposium},
  year={2026},
  address={Boulder, Colorado}
}
```

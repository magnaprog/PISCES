# Example inputs

## Synthetic example input

`example_normalized_windows.csv` contains synthetic normalized windows for checking that the runner works.

## NASA OMNI preview windows

`omni_may2024_preview_windows.csv` contains two normalized windows derived from NASA OMNI high-resolution 1-minute data:

- `omni_001_quiet_20240508_1633`
- `omni_002_gannon_20240511_1759`

Expected output is in `expected_preview_output.csv`.

## Schema

Required columns:

```text
window_id,step,bx,by,bz,bt,density,speed,temperature
```

Each `window_id` must have exactly 60 rows, with `step` values from 0 to 59. Optional `start_utc` and `source` values must be constant within a window and are copied to the output.

Values are normalized model inputs, not raw solar-wind measurements.

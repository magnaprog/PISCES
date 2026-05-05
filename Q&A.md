# Q&A

## What is PISCES?

PISCES is a physics-informed convolutional autoencoder for detecting anomal 60-minute solar-wind patterns near L1 point. The broader project studies near-Earth solar-wind anomaly detection and physical interpretation.

## What is included in this preview?

- `model/pisces_preview.pt` — exported preview model
- `pisces_preview/run_preview.py` — runner for normalized 60-step windows
- `examples/example_normalized_windows.csv` — small synthetic example input
- `examples/omni_may2024_preview_windows.csv` — two normalized NASA OMNI-derived windows
- `examples/expected_preview_output.csv` — expected output for the OMNI example
- `presentation/Poster.pdf` and `presentation/Presentation.pdf`

Full preprocessing, scoring, thresholds, event evaluation, training, and baselines are planned for the full release.

## What can I run from this repo?

You can run the exported model on normalized 60-minute windows and get one reconstruction error per window.

Synthetic example:

```bash
python -m pisces_preview.run_preview examples/example_normalized_windows.csv --out preview_output.csv
```

NASA OMNI preview windows:

```bash
python -m pisces_preview.run_preview examples/omni_may2024_preview_windows.csv --out omni_preview_output.csv
```

Expected OMNI output is in `examples/expected_preview_output.csv`.

## Is there a real NASA OMNI example?

Yes. `examples/omni_may2024_preview_windows.csv` includes two normalized windows derived from NASA OMNI data:

- quiet baseline: 2024-05-08 16:33 UTC
- May 2024 Gannon storm interval: 2024-05-11 17:59 UTC

These rows are not raw OMNI measurements. They are normalized inputs prepared for the preview model.

## Can I run this on raw OMNI files?

No. This preview starts from normalized windows. Raw OMNI download, preprocessing, scoring, and event evaluation are planned for the full code release.

## What input format is required?

See `examples/README.md`. Required columns are:

```text
window_id,step,bx,by,bz,bt,density,speed,temperature
```

Each `window_id` must have exactly 60 rows with `step` values `0..59`. Optional `start_utc` and `source` values must be constant within a window and are copied to the output.

## What does `reconstruction_error` mean?

`reconstruction_error` is the unweighted mean squared reconstruction error in normalized input space. It is not a probability, event label, or operational alert threshold. Compare values only within the same normalized-input setup.

## Does the preview output the full PISCES anomaly score?

No. The preview runner outputs only `reconstruction_error`. The full project uses additional scoring components and thresholds that are not included in this preview.

## Does PISCES classify ICMEs, shocks, or high-speed streams?

No. PISCES is not a supervised event classifier. The broader project uses anomaly scores and physical diagnostic components to help interpret unusual intervals, but those diagnostics are not class labels.

## Is this operational space-weather forecasting?

No. PISCES works with near-Earth/L1 solar-wind measurements. It is relevant to near-Earth monitoring, but it is not a Sun-to-Earth CME forecast model and is not operationally validated.

## What does physics-informed mean here?

The broader research model uses physically motivated solar-wind consistency checks and empirical relationships in training and scoring. These are soft constraints and diagnostics, not a full plasma-physics solver.

## Are those physics terms exact laws?

No. Some are algebraic consistency checks; others are empirical relationships or smoothness expectations. Real transients can legitimately violate them. In short: physics-informed, not physics-enforcing.

## Does this reproduce the poster metrics?

No. This preview only checks the exported model on small example inputs. It does not include the full scoring pipeline, thresholds, event matching, baselines, or figure generation needed to reproduce the poster table.

## How should I read the poster comparison?

Read the poster table metric by metric. It reports PISCES as strongest on PR-AUC and precision, with the lowest false-alarm ratio among the six listed methods, while OC-SVM is stronger on POD and Heidke Skill Score at the selected threshold. Do not summarize the result as “PISCES is best on every metric.”

## Does PR-AUC measure lead time?

No. PR-AUC measures ranking quality against catalog-based labels across thresholds. Lead time and operational warning performance are separate questions.

## Are catalog labels perfect ground truth?

No. Catalogs can miss events or have uncertain boundaries. An unmatched window may still be physically interesting. This is one reason the full paper separates model ranking, fixed-threshold behavior, and physical interpretation.

## Is the poster context map a model output?

No. Any ballistic back-mapping or heliospheric context map in the poster is a visualization, not a PISCES model output, not an MHD reconstruction, and not a direct measurement inside 1 AU.

## Why 60-minute windows?

The preview model expects a 60-step solar-wind window with seven channels. Multi-scale inputs and longer-context analysis are outside this preview.

## Why are the values normalized?

The model was exported to run on normalized inputs. Normalization keeps variables with different units and scales in the numerical range expected by the trained model. The normalization and raw-data preprocessing scripts are planned for the full release.

## How do I verify files after download?

```bash
sha256sum -c CHECKSUMS.txt
```

## Where is the citation?

Use `CITATION.cff` or the BibTeX block in `README.md`.

OSMOREGULATION — SINGLE-GRAPH EDITION

One animated graph with four axes:
X: Plasma osmolarity (mOsm/L)
Left Y: ADH concentration (ng/L), blue
Right Y: Urine osmolarity (mOsm/L), orange
Further-right Y: Thirst (relative intensity), purple

No explanatory captions, body-water box, or audio. A live plasma osmolarity
readout accompanies a shared vertical cursor. All three curves draw together
as the cursor moves right. The urine curve reaches a plateau while ADH
continues to rise. The cursor then moves left along the retained curves.
Each curve uses its own colored vertical axis; heights are not comparable
across different physiological quantities.

The curves are schematic, not fitted experimental data. Thirst is shown on
an arbitrary relative scale. Thresholds vary and can overlap; the classic
separation shown here is illustrative. The horizontal axis represents
osmolarity, not elapsed time. The leftward sweep demonstrates decreasing
osmolarity; no clinical intervention or response timing is implied.

Terminology follows the requested axes: osmolarity in mOsm/L. Osmolality
would instead be expressed in mOsm/kg H2O. Numeric illustration functions
are not patient measurements or conversions between these quantities.

Files
osmoregulation.mp4 — 1920 × 1080, 30 fps, silent
preview.png — frame at the end of the rightward sweep
osmoregulation.py — editable Manim Community scene
chapter-times.json — rendered timing information
render-report.json — video properties and verification
requirements.txt — pinned Manim dependency
versions/v1/ — preserved earlier version with stacked graphs and water box

Reproduce, from this directory:
uv run --with manim==0.22.1 manim -r 1920,1080 --fps 30 --media_dir /tmp/osmoregulation-v2-render osmoregulation.py Osmoregulation -o osmoregulation.mp4

Physiological references
https://www.ncbi.nlm.nih.gov/books/NBK279157/figure/neurohypophys-endo.F6/
https://journals.physiology.org/doi/full/10.1152/ajpendo.00033.2004
https://www.ncbi.nlm.nih.gov/books/NBK231119/?report=classic

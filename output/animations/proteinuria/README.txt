THREE ROUTES TO PROTEINURIA

A captioned, silent animation comparing the predominant proteinuria
mechanisms in the three clinical examples from the teaching question.

Files
proteinuria.mp4 — 1080p, 30 fps animation
preview.png — representative overflow frame
comparison.png — closing three-mechanism comparison
proteinuria.py — editable Manim Community scene
chapter-times.json — timings produced by the full render
render-report.json — video details and verification
requirements.txt — pinned animation dependency
narration.txt — optional voice-over outline; no audio is included in the MP4

Sequence
Normal handling: most albumin remains on the blood side; filtered small
proteins enter proximal tubular cells, leaving very little protein in urine.
Glomerular leakage: greater barrier permeability increases albumin delivery
to the tubule and urinary albumin despite some continued cellular uptake.
Tubular failure: reduced uptake allows filtered low-molecular-weight
proteins to remain in the lumen and reach urine.
Overflow: excess circulating free light chains increase the filtered load.
Uptake continues, but the load exceeds capacity and excess reaches urine.
Comparison: barrier leak, uptake failure and excessive filtered load are
linked to the corresponding protein patterns and clinical examples.

Visual design
Matches renal-pressure, urine-concentration and micturition: dark #10151F
background, Avenir Next, white captions, muted anatomical labels and sparse
text. Coral particles represent albumin. Gold particles represent small
proteins; in the overflow scene these specifically represent free light
chains. Teal arrows denote uptake into tubular cells. Mechanism and output
labels sit beside their respective structures. No course, week, learning-
objective or exam-answer labels appear in the animation.

Interpretation and limits
The diagram unrolls filtration and proximal tubular handling into one
left-to-right schematic. It is not a full nephron or a renal circulation
map. Retained albumin particles turn back as a visual cue for retention;
this does not represent reversal of blood flow.
The mesh symbolises glomerular selectivity. Its changing gaps are not
literal anatomical holes or a model of the multiple barrier layers.
Normal albumin restriction is not absolute; some filtered albumin uptake
is shown. The proximal tubule also handles albumin, so albuminuria alone
does not establish a uniquely glomerular mechanism in every patient.
Upward protein movement ends inside tubular cells, where filtered proteins
are processed. The diagram does not depict intact protein moving directly
back to blood. Receptor and lysosome details are omitted.
Tubular uptake is reduced, not completely eliminated, in the injury scene.
The red crosses mark impaired uptake rather than absent cells or complete
necrosis. In overflow, the uptake process remains active as more substrate
passes through the barrier. A primary glomerular leak is not required.
Free light chains can also injure tubules or be associated with glomerular
disease; the overflow example isolates the predominant mechanism asked
about in this question. Mechanisms may coexist clinically.
Particle number, speed, size, uptake thresholds and mesh spacing are
qualitative visual controls. They are not measured filtration fractions,
protein excretion rates, molecular sizes or a kinetic model. Small numbers
of residual urine particles illustrate that normal excretion is low rather
than literally zero. The clinical examples are illustrative, not diagnostic
rules or a complete classification of proteinuria.

Sources
Hall AM. Protein handling in kidney tubules. Nature Reviews Nephrology.
2025;21:241–252. doi:10.1038/s41581-024-00914-1.
https://www.nature.com/articles/s41581-024-00914-1
Proximal tubular protein uptake and processing; uptake defects and proteinuria.

Sirac C, Batuman V, Sanders PW. The Proximal Tubule Toxicity of Immunoglobulin
Light Chains. Kidney International Reports. 2021;6(5):1225–1231.
doi:10.1016/j.ekir.2021.02.026.
https://pmc.ncbi.nlm.nih.gov/articles/PMC8116766/
Free-light-chain filtration, uptake saturation and multiple renal injury mechanisms.

NIDDK. Diabetic Kidney Disease.
https://www.niddk.nih.gov/health-information/diabetes/overview/preventing-problems/diabetic-kidney-disease
Diabetes-related kidney damage and urinary albumin.

Reproduce
With Python 3.13 and the pinned Manim dependency installed:
manim -r 1920,1080 --fps 30 --media_dir /tmp/proteinuria-render proteinuria.py Proteinuria -o proteinuria.mp4

For quick frame review, set PROTEINURIA_REVIEW=normal, glomerular, tubular
or overflow and use Manim's -s option. Without this variable, the animation
also renders the closing comparison and writes chapter-times.json.

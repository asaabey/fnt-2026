MEDICINES AND GLOMERULAR PRESSURE

A general renal-haemodynamics animation, independent of any course or exam.
The video is captioned and silent. Manim Community 0.22.1 is used to render
an editable, vector-based scene as an MP4.

Included comparisons
• Angiotensin II: preferential efferent constriction at moderate activation.
• ACE inhibitors: reduced angiotensin II formation and efferent relaxation.
• ARBs: AT1 blockade and reduced efferent constrictor tone.
• Prostaglandins: support for afferent dilation when perfusion is low.
• NSAIDs: COX inhibition removes that vasodilator support.
• SGLT2 inhibitors: restored tubuloglomerular feedback in the classic
  hyperfiltration model, plus context-dependent post-glomerular effects.
• Low perfusion/volume depletion combined with an NSAID and an ACEi OR ARB.

Medicine labels are placed above the vessel affected in that scene: afferent
on the left and efferent on the right. Unchanged vessels have no medicine
label. The combination scene labels both sides; the closing summary also
keeps the classes on their respective sides. Repeated headings, unchanged-
vessel labels, boilerplate notes and the footer have been removed.

Each comparison resets to its own stated reference condition. Except for
the final combination scene, the drugs are not being added sequentially.
The afferent vessel is the inlet; the efferent vessel is the outlet.
Arteriolar resistance changes influence glomerular capillary pressure:
the video does not imply that drugs simply target an independent
"afferent pressure" or "efferent pressure" measurement.

Clinical interpretation
The direction of the initial haemodynamic effect is not a verdict on
long-term kidney benefit. ACE inhibitors, ARBs and SGLT2 inhibitors can
reduce intraglomerular pressure and benefit appropriately selected patients.
Perfusion dependence and interacting medicines matter. The NSAID/low-volume
combination is distinct from the expected initial dip with protective
therapies. This is a mechanism illustration, not an instruction to start,
stop or combine medicines.

SGLT2 nuance
Restored macula-densa signalling and increased afferent tone are a useful
classic hyperfiltration model, supported by mechanistic work. Human type 2
diabetes studies such as the RED trial support a post-glomerular dilation
interpretation in some settings. The video shows these separately. Neither
is presented as an invariant mechanism in every patient. The type 1
diabetes mechanistic study is cited as physiology evidence, not as a
clinical recommendation for SGLT2 inhibitor use in that population.

Model limits
Bar levels, particle velocities and vessel dimensions are qualitative,
not calibrated predictions or patient measurements. Only selected vascular
mechanisms are depicted. Changes in systemic pressure, filtration
coefficient, oncotic pressure, tubular effects and structural injury can
alter the actual response. Red blood cells remain on the vascular path;
gold particles represent filtrate. Afferent and efferent vessel geometry
is schematic rather than anatomically scaled.

Re-render
Install Python, uv, Cairo, Pango and FFmpeg as required for your platform.
From this directory:
  uv venv .venv
  uv pip install --python .venv/bin/python -r requirements.txt
  .venv/bin/manim -r 1920,1080 --fps 30 renal_pressure.py RenalPressure

The source reads storyboard.json from the same directory. It writes
chapter-times.json with the actual scene timing. The requirements are
pinned in requirements.txt. The rendered file is renal-pressure.mp4.

Sources and evidence details
See mechanisms-and-sources.txt. No branding, weekly headings, objective
numbers or assessment-answer labels are included in the animation.

Revision — 11 November 2026
Calcineurin inhibitors removed from the comparisons and closing summary.
ACE inhibitor, ARB and both SGLT2 inhibitor scenes include the qualitative
clinical outcome “Can reduce albuminuria”. This is a treatment outcome in
relevant clinical settings, not a calculated consequence of the GFR bar.
No albumin-particle count or quantitative protein-excretion model is implied.
Kidney protection involves mechanisms beyond the displayed vascular effects.
The previous export and source files are preserved in versions/v1/.

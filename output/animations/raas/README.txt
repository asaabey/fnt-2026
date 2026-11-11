RENIN → ANGIOTENSIN II → ALDOSTERONE

Silent, sparse-label Manim animation. Dark background, Avenir Next and the
same palette as the existing renal animations. Anatomy and particle movement
are schematic. No question numbers or answer labels appear.

Sequence
1. Reduced renal perfusion, reduced NaCl transport at the macula densa and
   increased beta-1 sympathetic signalling stimulate JG granular-cell renin.
2. Liver-derived angiotensinogen is cleaved by renin to angiotensin I.
   Endothelial ACE, illustrated at the lungs, forms angiotensin II.
3. Angiotensin II causes vasoconstriction, increases proximal sodium
   reabsorption and stimulates aldosterone from the adrenal zona glomerulosa.
4. A principal-cell view places tubular lumen on the left and blood on the
   right. Increased apical ENaC and basolateral Na/K-ATPase activity promote
   sodium reabsorption and potassium secretion through an apical K channel.
   Gold marks sodium; teal marks potassium. The minus symbol indicates a
   relatively negative lumen. K enters via the pump before exiting to urine.
5. Volume and BP restoration reduce renin, angiotensin II and aldosterone.
   A separate K-to-adrenal arrow shows direct stimulation by elevated K.
6. Autonomous aldosterone remains elevated despite suppressed renin and
   angiotensin II. The resulting phenotype is hypertension with low plasma K.

Limits
Renin and ACE are enzymes above reaction arrows, not intermediate substrates.
Pulmonary endothelium is an important ACE site, not its exclusive location.
The blood compartment beside the principal cell includes interstitium and
peritubular circulation. Ion counts, speeds, dimensions and sequence timings
are qualitative; this is not a stoichiometric or mass-conserving model.
ENaC and pump symbols indicate transport activity, not literal protein counts.
Aldosterone has additional effects, including regulation of K channels;
secretion also depends on distal delivery, flow and potassium availability.
The vessels and organs are simplified teaching illustrations.
The direct potassium stimulus is a parallel regulatory route, not a claim
that plasma potassium must be elevated during gastrointestinal bleeding.
Angiotensin II effects on efferent resistance, thirst and AVP are omitted
in this focused account of sodium conservation and potassium secretion.
The last scene is a separate autonomous-secretion state, not progression
from blood loss to primary aldosteronism. Hypokalaemia is not universal in
primary aldosteronism.

Sources
https://www.ncbi.nlm.nih.gov/books/NBK470410/
https://pmc.ncbi.nlm.nih.gov/articles/PMC4137912/
https://www.endocrine.org/clinical-practice-guidelines/primary-aldosteronism-2

Reproduce
uv run --with manim==0.22.1 manim -r 1920,1080 --fps 30 --media_dir /tmp/raas-render raas.py RAAS -o raas.mp4

Files
raas.mp4 — 1080p, 30 fps, no audio
raas.py — editable Manim scene
preview.png — principal-cell frame
chapter-times.json — generated chapter timings
render-report.json — video metadata and verification

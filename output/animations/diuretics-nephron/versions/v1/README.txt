DIURETICS: ONE NEPHRON, DIFFERENT TARGETS

A single persistent nephron with eight sequential mechanism insets.
Silent 1920 × 1080, 30 fps Manim animation matching the renal teaching set.
Anatomical segment names are primary; small Site I–IV labels provide the
traditional teaching cross-reference. There are no course or exam labels.

Sequence
1. Mannitol: luminal osmoles oppose water reabsorption in water-permeable
   segments, illustrated in the proximal tubule and descending limb.
2. Acetazolamide: carbonic anhydrase inhibition reduces NaHCO3 reabsorption.
3. SGLT2 inhibitors: proximal sodium–glucose cotransport inhibition produces
   glycosuria and osmotic diuresis, with context-dependent natriuresis.
4. Loop diuretics: apical NKCC2 inhibition in the thick ascending limb causes
   natriuresis and weakens the medullary gradient. The limb remains relatively
   water-impermeable; maximum concentrating capacity falls.
5. Thiazides/thiazide-like drugs: apical NCC inhibition in the distal
   convoluted tubule reduces NaCl reabsorption.
6. Spironolactone/eplerenone: intracellular mineralocorticoid receptor
   antagonism reduces aldosterone-dependent sodium transport.
7. Amiloride/triamterene: direct apical ENaC blockade reduces sodium entry.
   Both potassium-sparing groups reduce a driving force for K secretion.
8. Tolvaptan: basolateral V2 antagonism reduces signalling for apical AQP2
   insertion. AQP2 is retrieved into a schematic intracellular vesicle.
9. Summary: targets beside the same nephron; natriuresis versus aquaresis.

Interpretation and limits
The nephron is a continuous schematic. A thin ascending portion is shown
separately below the thick ascending limb; NKCC2 highlighting is confined to
the latter. DCT, connecting tubule and collecting system are distinguished
spatially, without attempting to map every cell subtype. Site IV is a broad
teaching grouping, not a uniform transporter distribution. The MR and ENaC
scenes highlight the aldosterone-sensitive distal nephron schematically.
The collecting duct is shown as the downstream drainage system of one
nephron; convergence from other nephrons is omitted.

Every inset has tubular fluid/apical membrane on the left and interstitium/
basolateral membrane on the right. MR is intracellular, ENaC apical and V2
basolateral. Target inhibition is shown by a coral mark. Fading transport
arrows indicate reduced flux, not zero transport. These are separate drug
comparisons, not a sequence of drugs being administered together.

Mannitol acts across water-permeable segments, not at a unique numbered site.
Its diagram focuses on luminal osmosis and does not model systemic fluid
shifts. Carbonic anhydrase has luminal and intracellular roles; the enzyme
icon is not a full reaction map. Sodium-pump, potassium-channel and other
basolateral transporter detail is omitted from the insets. The Na and K
arrows in the potassium-sparing scenes show distinct fluxes, not a direct
one-for-one Na/K exchanger through ENaC. Potassium handling also depends on
delivery, flow, renal function and potassium availability.

Tolvaptan blocks V2 signalling, not AQP2 directly. The AQP2 vesicle and
retrieval animation are schematic. Residual water pathways are omitted;
water permeability need not fall to zero. Aquaretic action means increased
water excretion relatively independently of electrolyte excretion, rather
than literally solute-free urine. SGLT2 inhibitors are included because of
their renal transport and diuretic effects; their kidney and cardiovascular
benefits extend beyond diuresis. Natriuresis may attenuate over time.

Geometry, highlighting, particle counts and transition times are qualitative,
not calibrated anatomical, pharmacokinetic or mass-conserving simulations.
No dose, indication, treatment selection or comparative potency is implied.
The scope is the major drug groups in the revised lesson, not every agent
with a secondary diuretic effect.

Files
 diuretics-nephron.mp4 — complete silent animation
 diuretics_nephron.py — editable vector source
 preview.png — representative mechanism frame
 comparison.png — contact sheet of the eight mechanisms and summary
 nephron-summary.png — standalone final summary frame
 chapter-times.json — actual render timings
 render-report.json — metadata, hashes and checks
 mechanisms-and-sources.txt — physiology sources and terminology discussion
 narration.txt — optional voice-over outline; no audio in the MP4
 youtube-upload.txt — suggested title and description
 requirements.txt — pinned Manim dependency

Reproduce
/tmp/fnt-renal-manim-env/bin/manim -r 1920,1080 --fps 30 --media_dir /tmp/diuretics-nephron-render diuretics_nephron.py DiureticsNephron -o diuretics-nephron.mp4
Or install requirements.txt into an appropriate Manim environment.
Static layout review: set DIURETIC_REVIEW to osmotic, carbonic-anhydrase,
sglt2, loop, thiazide, mineralocorticoid, enac or v2, and use Manim -s.

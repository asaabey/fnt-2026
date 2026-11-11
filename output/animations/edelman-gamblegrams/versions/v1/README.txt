EDELMAN–ROSE GAMBLEGRAMS: SODIUM CONTENT, WATER AND CONCENTRATION

A Manim teaching prototype for the sodium-concentration questions, including
sodium retention, hypotonic hyponatraemia and diabetes insipidus (DI).
It uses original diagrams informed by Rondon-Berrios's 2024 teaching paper.

Teaching purpose
Animation helps by holding a reference fixed, changing body amounts and
showing the resulting concentration. It directly supports Q11's normal
plasma sodium despite sodium/fluid retention, and Q15's oedematous
hyponatraemia with reduced effective arterial filling. The water-gain scene
also supports the concentration/content distinction in Q3. The DI extension
shows how unreplaced water loss can reverse the direction of concentration
change, followed by a separate drinking-compensation step.

Files
edelman-gamblegrams.mp4 — silent captioned 1080p, 30 fps prototype
preview.png — representative oedematous hyponatraemia frame
comparison.png — five-situation overview
normal-retention.png — sodium and water retention with normal plasma sodium
water-gain.png — water-predominant hypotonic hyponatraemia
sodium-loss.png — sodium depletion with hypotonic hyponatraemia
di-water-loss.png — unreplaced water loss in DI
di-compensated.png — normal model sodium when drinking replaces DI losses
edelman_gamblegrams.py — editable Manim scene
cases.json — illustrative model inputs, captions and clinical scenario labels
model-checks.json — arithmetic and relative-water checks
chapter-times.json — chapter timings from the full render
render-report.json — export details and verification
narration.txt — optional voice-over outline; no audio is included in the MP4
requirements.txt — pinned animation dependency

Model and display
The simplified Edelman–Rose relation is displayed with an approximation sign:
plasma sodium ≈ (exchangeable sodium + exchangeable potassium) / total body water.
The empirical Edelman relation has additional slope/intercept terms; the
prototype uses Rose's simplified relation rather than fitting patient data.

Gold represents exchangeable sodium, grey represents exchangeable potassium
and teal represents water. Potassium is included and held fixed throughout.
This preserves the combined cation numerator while letting the viewer focus
on sodium and water. Gold sodium amounts are not silently substituted for
the entire numerator.

Each total bar is normalised to its OWN baseline amount. Equal bar heights
mean the ratio equals the reference ratio, not that millimoles equal litres.
The sodium and potassium segments share the cation-total scale. Grey K stays
fixed while the gold Na segment changes. These are body-amount bars, not
measurements of plasma concentration or drawings of ECF/ICF compartments.

The model reference is Na_e = 2800 mmol, K_e = 2800 mmol and TBW = 40 L,
which gives 140 mmol/L under the simplified relation. These are illustrative
starting values. All displayed concentration readouts are calculated from
the inputs; the numbers are not predictions for the question's patients.

Examples
Normal-concentration retention: sodium increases with sufficient water to
preserve the cation/water ratio, giving a model sodium of 140 mmol/L.
Three different low-sodium situations all give 128 mmol/L: water gain with
unchanged sodium, sodium depletion with a smaller relative cation-matched
water loss, and sodium plus water retention with disproportionate water gain.
The DI water-loss example gives 160 mmol/L when losses are not replaced.
The follow-on compensation step restores the reference water amount and
model sodium of 140 mmol/L, while explicitly retaining dilute polyuria as
a possible ongoing feature.

Hatching denotes water excess or deficit relative to the water matched to
the cation amount at the reference concentration. It is a graphical ratio
comparison, not a physically separate water compartment. A relative excess
can therefore appear even when total body water is below baseline. The
calculated differences in model-checks.json are not replacement prescriptions.

Clinical interpretation
The low-sodium examples represent hypotonic hyponatraemia. Glucose-related
translocational hyponatraemia, pseudohyponatraemia, solute intake, urine
composition and ongoing losses are outside the depicted model.
Sodium content helps frame ECF volume, but oedema, vascular filling and
haemodynamics require clinical context. The bars do not measure intravascular
versus interstitial volume or independently diagnose heart failure or SIAD.
A near-unchanged sodium amount with water gain is a conceptual example, not
a claim that every SIAD case has exactly unchanged sodium stores.
DI produces hypotonic polyuria through AVP deficiency (central DI) or renal
AVP resistance (nephrogenic DI). A high sodium occurs if water losses exceed
replacement. Thirst and drinking often preserve sodium; normal sodium does
not exclude DI. The body-amount bars cannot distinguish the two mechanisms.
The DI step idealises electrolyte-poor water loss while holding cations
fixed. Actual urine contains solutes. Replacement shows a balance concept,
not a water-deprivation test or a prescribed treatment.

Evidence and attribution
Rondon-Berrios H. Edelman Gamblegrams: a tool to teach and learn disorders of
water/plasma tonicity homeostasis. Advances in Physiology Education.
2024;48:200–204. doi:10.1152/advan.00253.2023.
https://journals.physiology.org/doi/full/10.1152/advan.00253.2023
The paper introduces the teaching approach; the prototype uses newly drawn
bars, a retained fixed K segment and original numerical examples. The paper
reports teaching experience; this prototype has not undergone a formal
learning-outcome evaluation. Publisher direct-page access was restricted,
but the search-indexed article text and figure captions were available.

Edelman IS, Leibman J, O'Meara MP, Birkenfeld LW. Interrelations Between Serum
Sodium Concentration, Serum Osmolarity and Total Exchangeable Sodium, Total
Exchangeable Potassium and Total Body Water. J Clin Invest. 1958;37:1236–1256.
https://www.jci.org/articles/view/103712

Rose BD. New approach to disturbances in the plasma sodium concentration.
Am J Med. 1986;81:1033–1040.
https://pubmed.ncbi.nlm.nih.gov/3799631/

Workeneh BT, Meena P, Christ-Crain M, Rondon-Berrios H. Hyponatremia Demystified:
Integrating Physiology to Shape Clinical Practice. Adv Kidney Dis Health.
2023;30:85–101.
https://pmc.ncbi.nlm.nih.gov/articles/PMC9993811/

NIDDK. Diabetes Insipidus.
https://www.niddk.nih.gov/health-information/kidney-disease/diabetes-insipidus

Gubbi S, Shahid M, Koch CA, Verbalis JG. Diagnostic Tests for Diabetes Insipidus.
Endotext. Updated 23 November 2025.
https://www.ncbi.nlm.nih.gov/sites/books/NBK537591/

Reproduce
With Python 3.13 and the pinned Manim dependency installed:
manim -r 1920,1080 --fps 30 --media_dir /tmp/gamblegrams-render edelman_gamblegrams.py EdelmanGamblegrams -o edelman-gamblegrams.mp4

Quick frame review: set GAMBLEGRAM_REVIEW=baseline, balanced-retention,
water-gain, sodium-loss, hypotonic-retention, di-water-loss or di-compensated
and use -s. The full render also creates the comparison and chapter timings.

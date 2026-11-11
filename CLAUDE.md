# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Teaching materials for a Year 2 medical-student renal/urology revision session (FNT 2026). It is primarily a teaching-content repository, with Manim animation and asset-hosting scripts. Generated artefacts are excluded by `.gitignore`. The two root PDFs (`Revised - 2026 Year 2 Semester 2 Practice Exam 1 Paper.pdf` and the `Bonus Questions` PDF) are the source exam papers. Everything derived from them lives in `output/`. `tmp/` holds scratch PDF/figure extractions.

Content is clinical and educational, so accuracy matters more than polish. Each deliverable carries its own caveats (what is qualitative, which mechanism is simplified, sources). Keep those caveats and source citations up to date whenever you change content.

## Layout of `output/`

- `markdown/`: the exam PDFs converted to `.md`/`.txt` (figures in `assets/`), plus the urology/nephrology question selections. `urology-nephrology-selection-index.md` and `urology-nephrology-selection.json` hold the selection: 44 of 163 questions, with source question number and PDF page. The selection index describes topics only and must not reveal answers.
- `fimbria/`: lessons for the Fimbria teaching app. The current lesson is `renal-weeks-1-4/renal-weeks-1-4-lesson.json` (id `fnt-2026-renal-weeks-1-4-v1`), with `teacher-notes.txt`, `learning-objective-map.json` and `validation-report.json` alongside it.
- `animations/<topic>/`: one Manim animation per folder (renal-pressure, proteinuria, diuretics-nephron, urine-concentration, water-load, osmoregulation, raas, micturition, nephritic-nephrotic, edelman-gamblegrams). `youtube-titles-and-descriptions.txt` collects the YouTube copy for all current videos.
- `hosting/lattice-1-assets/`: CC BY microscopy figures served from a Cloudflare R2 bucket (`fimbria-teaching-assets`, public at `assets.lattice-1.com`). The lesson JSON uses these figures for Q12 (IgA) and Q15 (ANCA).

## Fimbria lesson JSON

- Every step is a `slide`, a `question` (`options`, `correctOptionId`, `explanation`) or a `video` (YouTube). `lesson.schema.json` is an old snapshot of the app's schema: it has no `video` type, and `validation-report.json` records `schemaSnapshotMatchesApp: false`. Validation is actually done with the Fimbria application's own parser, not with this file. The size limit is 262144 bytes.
- Explanation text is markdown-ish: `**bold**`, `==highlight==`, ↑/↓ arrows, and images given as markdown image links to `assets.lattice-1.com` URLs.
- Questions display in topic order (Q1–Q19), but **step IDs stay stable** (e.g. `q01-week1-lo4`). Never renumber the IDs when you reorder. Keep answer keys, existing distractor misconceptions and the YouTube inserts unless the user asks to change them.
- Before an edit that changes structure, copy the current files into `versions/before-<change>/`. Afterwards, update `validation-report.json` (sha256, counts, scope of the change, `previousVersion`).

## Animations (Manim Community 0.22.1)

Every animation folder follows the same pattern: `<name>.py` (Scene class), pinned `requirements.txt`, `<name>.mp4`, `preview.png`/`comparison.png`, `chapter-times.json` (written by a full render), `render-report.json` (sha256 of the video and source, duration, review notes, `changes`, `previousVersion`), `README.txt` (scope, limits, sources, re-render command), `narration.txt` and `youtube-upload.txt`. Some folders also read their scene text from `storyboard.json` or `cases.json`.

Render (from the animation folder):
```
uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/manim -r 1920,1080 --fps 30 renal_pressure.py RenalPressure
```
Use the `-s` flag to render a single frame. Some scenes support review env vars for jumping to one section (e.g. `PROTEINURIA_REVIEW=normal|glomerular|tubular|overflow`). Check each README for its exact class name and flags.

Shared visual style: background `#10151F`, Avenir Next font, white captions, muted labels, sparse text. Coral = albumin, gold = filtrate/small proteins, teal = uptake or drug labels. The videos are silent and captioned. They must not contain course or week names, learning-objective numbers or exam-answer labels.

When you revise an animation, move the previous `.py`/README/export into `versions/vN/`. Then update `render-report.json`, the README's "Revision" section, `youtube-upload.txt` and the matching entry in `animations/youtube-titles-and-descriptions.txt`.

## Asset hosting

From `output/hosting/lattice-1-assets/`, run `python upload-assets.py` to upload through Wrangler (it checks sha256 against `assets.json` first) and `python verify-assets.py` to check over HTTP. File names are versioned with a hash and served with immutable caching, so publish a changed file under a new name instead of overwriting the old one. Wrangler holds the credentials; do not store them here.

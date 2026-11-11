# FNT 2026

Renal physiology and urology teaching materials, Fimbria lesson sources, and editable Manim animations for a Year 2 medical revision session.

## Contents

- `output/animations/`: Manim scenes, requirements, storyboards, teaching notes, and video publishing copy. Topics include RAAS, osmoregulation, diuretics, renal pressure, urine concentration, proteinuria, and micturition.
- `output/fimbria/`: lesson JSON, schemas, question sets, and teacher notes.
- `output/markdown/`: exam-paper transcriptions and selected renal/urology questions.
- `output/hosting/`: asset manifests and upload/verification scripts.

Individual animation `README.txt` files describe physiological scope, simplifications, references, and render commands. Earlier source revisions are retained in `versions/` subdirectories.

## Render an animation

Requires Python, FFmpeg, Manim's system dependencies, and the Avenir Next font used by these scenes. With [uv](https://docs.astral.sh/uv/) installed:

```sh
cd output/animations/raas
uv run --with manim==0.22.1 manim -r 1920,1080 --fps 30 --media_dir media raas.py RAAS -o raas.mp4
```

See each animation's README for its scene class and any additional dependencies.

## Files kept outside Git

The repository tracks editable text and source files. `.gitignore` excludes video renders, image assets/previews, PDF and Office binaries, generated render/validation reports, scratch files, caches, environments, and local credentials. These files remain available locally; they are not uploaded with the repository. Some lesson images refer to externally hosted assets documented in their manifests.

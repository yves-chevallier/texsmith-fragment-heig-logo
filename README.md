# TeXSmith Fragment - HEIG-VD Logo

A [TeXSmith](https://github.com/HEIG-VD/texsmith) fragment that drops the
HEIG-VD letterhead logo on the first page of a document.

## Install

```bash
uv add texsmith-fragment-heig-logo
# or
pip install texsmith-fragment-heig-logo
```

The package registers a `heiglogo` fragment via the
`texsmith.fragments` entry-point group, so TeXSmith picks it up
automatically — no path configuration needed.

## Usage

In your document's YAML front matter (or in `texsmith.yaml`), append the
fragment to the rendering pipeline:

```yaml
fragments:
  append:
    - heiglogo
heiglogo:
  color: false   # set to true for the red HEIG-VD logo
  year: auto     # auto | 1998 | 2004 | 2009 | 2020
```

The logo is positioned 1 cm from the top-left of the page on every page of
the document.

### Logo vintages

The bundled package supports the historical HEIG-VD logos (its *vintages*):
`1998`, `2004`, `2009` and `2020` (the current letterhead). Pick one in two
ways:

- **Explicitly** — set `heiglogo.year` to a vintage:

  ```yaml
  heiglogo:
    year: 2004
  ```

- **Automatically from the document date** (the default, `year: auto`) — the
  vintage in force when the document was written is selected from the front
  matter `date`. Each vintage applies from its introduction year up to the
  next one:

  | Document `date`      | Logo vintage |
  |----------------------|--------------|
  | before 2004          | `1998`       |
  | 2004 – 2008          | `2004`       |
  | 2009 – 2019          | `2009`       |
  | 2020 and later       | `2020`       |

  When no usable date is available, the current logo (`2020`) is used.

### Attributes

| Attribute        | Default  | Description                            |
|------------------|----------|----------------------------------------|
| `heiglogo.color` | `false`  | Render the logo in HEIG-VD red (`e1251b`) instead of black. |
| `heiglogo.year`  | `auto`   | Logo vintage: `auto` (from the document `date`), or one of `1998`, `2004`, `2009`, `2020`. |

### Demo

`demo/demo.sh` renders the same document across several dates and explicit
vintages, then compiles a PDF for each so you can compare the logos:

```bash
./demo/demo.sh              # render + build PDFs with xelatex
NO_BUILD=1 ./demo/demo.sh   # LaTeX only, no PDF
```

Output (one folder per scenario) lands under `demo/output/`.

## Requirements

- TeXSmith ≥ 0.3.0
- A LaTeX engine with `xelatex` or `lualatex` (the bundled `heiglogo.sty`
  uses `fontspec` and refuses `pdflatex`).
- The `TeX Gyre Heros` font family (already present in standard TeX Live
  distributions).

## How it works

The package ships these files under
`src/texsmith_fragment_heig_logo/fragment/`:

- `heiglogo.sty` — the docstrip-generated LaTeX package (now multi-vintage).
- `heiglogo.jinja.tex` — a one-line Jinja template that calls
  `\AddToShipoutPictureBG*{\logo[..., year=NNNN]}`.
- `fragment.toml` — a declarative description of the fragment, kept in sync
  for documentation and as a static fallback.

Choosing the vintage from the document date needs a little Python, so the
fragment is registered as an **object** rather than a bare directory.
`_fragment.py` defines `HeigLogoFragment`, a TeXSmith `BaseFragment` whose
`build_config()` reads the `date` from the render context and resolves the
vintage (the pure logic lives in `_vintage.py`). The entry point is a lazy
factory:

```toml
[project.entry-points."texsmith.fragments"]
heiglogo = "texsmith_fragment_heig_logo:load_fragment"
```

When TeXSmith starts, its `FragmentRegistry._discover_entry_points()` scans
the `texsmith.fragments` group, calls `load_fragment()`, and registers the
returned fragment as if it were built-in. The factory is lazy (and the
package avoids importing TeXSmith at module load) to sidestep a circular
import: TeXSmith builds its registry *while it is itself being imported*.

## Regenerating `heiglogo.sty` from upstream

`heiglogo.sty` is a generated artefact; the canonical sources live at
[HEIG-VD/logos](https://github.com/HEIG-VD/logos) as a `.dtx` file. To
refresh the bundled copy:

```bash
git clone https://github.com/HEIG-VD/logos
cd logos/heig-vd/latex
latex heiglogo.ins          # docstrip: heiglogo.dtx -> heiglogo.sty
cp heiglogo.sty <this-repo>/src/texsmith_fragment_heig_logo/fragment/heiglogo.sty
```

Then make the copy **self-contained**: upstream's `\ProvidesPackage` line
expands `\HeigGitDate` / `\HeigGitTag`, which are CI-generated into
`version.tex` (only the documentation driver defines fallbacks). Insert
matching `\providecommand` lines just after `\NeedsTeXFormat`, using the
vendored commit's date and short hash, e.g.:

```latex
\providecommand\HeigGitDate{2026/06/04}
\providecommand\HeigGitTag{34e9c6e}
```

Bump the package version and commit.

## Licence

- The wrapper code (Python module, manifest, Jinja template, build
  configuration) is released under the **MIT license** — see
  [`LICENSE`](LICENSE).
- The bundled `heiglogo.sty` file is distributed under the **LaTeX Project
  Public License (LPPL) 1.3c or later** — see [`LICENSE-LPPL`](LICENSE-LPPL)
  and the upstream repository.

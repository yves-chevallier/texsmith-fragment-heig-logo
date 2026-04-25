# TeXSmith Fragment - HEIG-VD Logo

A [TeXSmith](https://github.com/HEIG-VD/texsmith) fragment that drops the
HEIG-VD letterhead logo on the first page of a document.

## Install

```bash
uv add texsmith-fragment-heig-logo
# or
pip install texsmith-fragment-heig-logo
```

The package registers a `ts-heiglogo` fragment via the
`texsmith.fragments` entry-point group, so TeXSmith picks it up
automatically — no path configuration needed.

## Usage

In your document's YAML front matter (or in `texsmith.yaml`), append the
fragment to the rendering pipeline:

```yaml
fragments:
  append:
    - ts-heiglogo
heiglogo:
  color: false   # set to true for the red HEIG-VD logo
```

The logo is positioned 1 cm from the top-left of the page on every page of
the document.

### Attributes

| Attribute        | Default | Description                            |
|------------------|---------|----------------------------------------|
| `heiglogo.color` | `false` | Render the logo in HEIG-VD red (`e1251b`) instead of black. |

## Requirements

- TeXSmith ≥ 0.3.0
- A LaTeX engine with `xelatex` or `lualatex` (the bundled `heiglogo.sty`
  uses `fontspec` and refuses `pdflatex`).
- The `TeX Gyre Heros` font family (already present in standard TeX Live
  distributions).

## How it works

The package ships three files under
`src/texsmith_fragment_heig_logo/fragment/`:

- `fragment.toml` — declares the fragment to TeXSmith and exposes the
  `heiglogo_color` attribute.
- `heiglogo.sty` — the docstrip-generated LaTeX package.
- `ts-heiglogo.jinja.tex` — a one-line Jinja template that calls
  `\AddToShipoutPictureBG*{\logo[...]}`.

The package's `__init__.py` exports a `FRAGMENT_PATH` constant. The
`pyproject.toml` declares it as the entry point:

```toml
[project.entry-points."texsmith.fragments"]
ts-heiglogo = "texsmith_fragment_heig_logo:FRAGMENT_PATH"
```

When TeXSmith starts, its `FragmentRegistry._discover_entry_points()`
scans the `texsmith.fragments` group, loads each entry, and registers the
fragment directory as if it were built-in.

## Regenerating `heiglogo.sty` from upstream

`heiglogo.sty` is a generated artefact; the canonical sources live at
[HEIG-VD/logos](https://github.com/HEIG-VD/logos) as a `.dtx` file. To
refresh the bundled copy:

```bash
git clone https://github.com/HEIG-VD/logos
cd logos/heig-vd/latex
latex heiglogo.dtx
cp heiglogo.sty <this-repo>/src/texsmith_fragment_heig_logo/fragment/heiglogo.sty
```

Bump the package version and commit.

## Licence

- The wrapper code (Python module, manifest, Jinja template, build
  configuration) is released under the **MIT license** — see
  [`LICENSE`](LICENSE).
- The bundled `heiglogo.sty` file is distributed under the **LaTeX Project
  Public License (LPPL) 1.3c or later** — see [`LICENSE-LPPL`](LICENSE-LPPL)
  and the upstream repository.

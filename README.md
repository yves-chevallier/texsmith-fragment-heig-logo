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
press:
  template: article
  fragments:
    append:
      - heiglogo
heiglogo:
  color: false   # set to true for the red HEIG-VD logo
  year: auto     # auto | 1998 | 2004 | 2009 | 2020
  left: 1cm      # distance from the left edge of the sheet
  top: 1cm       # distance from the top edge of the sheet
  group: iict    # optional: institute or centre logo (bar and text)
```

(The legacy top-level `fragments:` key is still honoured.)

The logo is positioned 1 cm from the top-left of the page by default; `left`
and `top` move it, for instance `left: 17mm` to leave room for a binding
gutter.

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

### Institute and centre logos

Set `heiglogo.group` to draw the full logo of one of the twelve institutes and
centres of the 2020 graphic charter (*Logothèque*): the mark, a vertical bar
and the group's name. Without it, the logo is drawn without text.

```yaml
heiglogo:
  color: true
  group: reds
```

| `group`                     | Text                                                       |
|-----------------------------|------------------------------------------------------------|
| `comatec`                   | **COMATEC** Institut de Conception mécanique et Technologies des matériaux |
| `iai`                       | **IAI** Institut d’Automatisation industrielle             |
| `ie`                        | **IE** Institut des Énergies                               |
| `iict`                      | **IICT** Institut des Technologies de l’information et de la communication |
| `iide`                      | **IIDE** Institut interdisciplinaire du Développement de l’entreprise |
| `insit`                     | **INSIT** Institut d’Ingénierie du territoire              |
| `mei`                       | **MEI** Media Engineering Institute                        |
| `reds`                      | **REDS** Institut Reconfigurable and Embedded Digital Systems |
| `formation-continue`        | **Centre Formation continue**                              |
| `formation-base`            | **Centre Formation de base**                               |
| `rad`                       | **Centre Ra&D**                                            |
| `relations-internationales` | **Centre Relations internationales**                       |

As in the charter, an institute shows its acronym in bold at the top and its
name flush with the bottom of the mark; a centre shows its whole name in bold.
The line breaks are the charter's. The charter's typeface, Circular, is not
freely available, so the text is set in **Arial**, falling back to its metric
clones Arimo or Liberation Sans, then to TeX Gyre Heros.

### Attributes

| Attribute        | Default  | Description                            |
|------------------|----------|----------------------------------------|
| `heiglogo.color` | `false`  | Render the logo in HEIG-VD red (`e1251b`) instead of black. |
| `heiglogo.year`  | `auto`   | Logo vintage: `auto` (from the document `date`), or one of `1998`, `2004`, `2009`, `2020`. |
| `heiglogo.left`  | `1cm`    | Distance from the left edge of the sheet, as a TeX length (`17mm`, `0.8cm`, …). |
| `heiglogo.top`   | `1cm`    | Distance from the top edge of the sheet, as a TeX length. |
| `heiglogo.group` | —        | Institute or centre whose full logo (bar and text) is drawn, see above. Case-insensitive; `_` and spaces stand for `-`. |

### Demo

`demo/demo.sh` renders the same document across several dates and explicit
vintages, then compiles a PDF for each so you can compare the logos:

```bash
./demo/demo.sh              # render + build PDFs with xelatex
NO_BUILD=1 ./demo/demo.sh   # LaTeX only, no PDF
```

Output (one folder per scenario) lands under `demo/output/`.

## Typst

The same front matter places the logo in a Typst render (`--format typst`),
with the same options — `color`, `year`, `left`, `top` and `group`:

```bash
texsmith rapport.md -t article --format typst -o build --build
```

The fragment's Typst pieces write `heiglogo.typ` next to the `.typ` and put
the logo in the first page's background; the content is moved below the logo
when the template would start it underneath. TeXSmith renders a fragment's
Typst pieces since 0.9.4.

`heiglogo.typ` is a Typst port of `heiglogo.sty`: the outlines of the four
vintages are translated from the package's TikZ paths by
`scripts/generate_typst_outlines.py` (rerun it after refreshing the `.sty`; a
test fails when they drift), with the same geometry and text metrics. It can
also be imported by hand:

```typst
#import "heiglogo.typ": heiglogo, heiglogo-page

// First page only, 1 cm from the top-left corner (left/top adjustable).
#set page(background: heiglogo-page(group: "iict", color: true))

// Or inline, anywhere.
#heiglogo(year: "2009", height: 18mm)
#heiglogo(group: "rad")
```

Typst warns once per missing family of the font fallback list (`Arial`,
`Arimo`, `Liberation Sans`, `TeX Gyre Heros`); the first one installed is used.

## Requirements

- TeXSmith ≥ 0.9.4, < 1.0
- A LaTeX engine with `xelatex` or `lualatex` (the bundled `heiglogo.sty`
  uses `fontspec` and refuses `pdflatex`).
- The `TeX Gyre Heros` font family (already present in standard TeX Live
  distributions); for `heiglogo.group`, preferably Arial (or Arimo /
  Liberation Sans).

## How it works

The package ships these files under
`src/texsmith_fragment_heig_logo/fragment/`:

- `heiglogo.sty` — the docstrip-generated LaTeX package (now multi-vintage).
- `heiglogo.jinja.tex` — a short Jinja template that calls
  `\AddToShipoutPictureBG*{\logo[left=…, top=…, year=NNNN]}`, adding the
  group's title and subtitle arguments (and the Arial font) when
  `heiglogo.group` is set.
- `heiglogo.typ` — the Typst port of the logos and the groups, written next
  to the `.typ` by a Typst render.
- `heiglogo.jinja.typ` — the Typst counterpart of `heiglogo.jinja.tex`: the
  `#set page(background: heiglogo-page(…))` call.
- `fragment.toml` — the manifest TeXSmith reads when the fragment is
  resolved *by path*; it names the same `entrypoint` as the
  `texsmith.fragments` entry point, so both routes yield the same object.

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

Regenerate the Typst outlines from the new drawings with
`python scripts/generate_typst_outlines.py`, then bump the package version and
commit.

## Licence

- The wrapper code (Python module, manifest, Jinja template, build
  configuration) is released under the **MIT license** — see
  [`LICENSE`](LICENSE).
- The bundled `heiglogo.sty` file is distributed under the **LaTeX Project
  Public License (LPPL) 1.3c or later** — see [`LICENSE-LPPL`](LICENSE-LPPL)
  and the upstream repository.

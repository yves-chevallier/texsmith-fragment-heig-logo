#!/usr/bin/env bash
#
# Demonstrates the heiglogo fragment's logo-vintage selection.
#
# It renders the same letter-headed document several times:
#   * four "auto" runs whose date alone picks the vintage (1998/2004/2009/2020);
#   * one run that pins the vintage explicitly via `heiglogo.year`;
#   * one run in HEIG-VD red (`heiglogo.color`);
#   * two runs with an institute/centre logo (`heiglogo.group`).
#
# Each scenario lands in its own demo/output/<name>/ folder, holding the source
# Markdown, the generated LaTeX (so you can read the chosen `\logo[... year=NNNN]`)
# and, unless NO_BUILD is set, the compiled PDF. With FORMAT=typst, the Typst
# source (`heiglogo-page(...)`) and its PDF are written under <name>/typst/.
#
# Usage:
#   ./demo/demo.sh              # render + build PDFs with xelatex
#   ENGINE=lualatex ./demo/demo.sh
#   NO_BUILD=1 ./demo/demo.sh   # emit LaTeX only, skip PDF compilation
#   FORMAT=typst ./demo/demo.sh # also render and build the Typst output
#   TEXSMITH=~/texsmith ./demo/demo.sh  # use a TeXSmith checkout
#
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
OUT="$HERE/output"
ENGINE="${ENGINE:-xelatex}"

# Always use the project's environment so the local heiglogo fragment is found,
# regardless of the current working directory.
# TEXSMITH points at a TeXSmith checkout to use instead of the locked release.
ts() {
  if [[ -n "${TEXSMITH:-}" ]]; then
    uv run -q --project "$ROOT" --with-editable "$TEXSMITH" texsmith "$@"
  else
    uv run -q --project "$ROOT" texsmith "$@"
  fi
}

rm -rf "$OUT"
mkdir -p "$OUT"

# render <name> <extra-front-matter>
render() {
  local name="$1" front="$2"
  local dest="$OUT/$name"
  local src="$dest/$name.md"
  mkdir -p "$dest"
  {
    printf -- '---\n'
    printf -- 'title: Rapport de démonstration\n'
    printf -- 'author: Ada Lovelace\n'
    printf -- 'language: french\n'
    printf -- 'fragments:\n  append:\n    - heiglogo\n'
    printf -- '%s\n' "$front"
    printf -- '---\n\n'
    printf -- '# %s\n\nLogo HEIG-VD en haut à gauche.\n' "$name"
  } >"$src"

  echo ">>> $name"
  # 1) Render to LaTeX so the chosen vintage is visible in the .tex.
  ts "$src" -t article -o "$dest" >/dev/null
  grep -h 'logo\[' "$dest"/*.tex | sed 's/^/    chosen: /'

  # 2) Compile the PDF (in $dest, since --build writes the PDF to the cwd).
  if [[ -z "${NO_BUILD:-}" ]]; then
    (cd "$dest" && ts "$src" -t article -e "$ENGINE" --build >/dev/null)
    echo "    pdf:    $dest/$name.pdf"
  fi

  # 3) The same document in Typst.
  if [[ "${FORMAT:-}" == "typst" ]]; then
    local build=()
    [[ -z "${NO_BUILD:-}" ]] && build=(--build)
    ts "$src" -t article --format typst -o "$dest/typst" "${build[@]}" >/dev/null
    grep -h 'heiglogo-page' "$dest/typst/$name.typ" | sed 's/^/    typst:  /'
  fi
}

# --- Automatic selection: the date alone decides the vintage. ---------------
render "auto-2001-vintage-1998" $'date: 2001-09-01'
render "auto-2006-vintage-2004" $'date: 2006-05-01'
render "auto-2015-vintage-2009" $'date: 2015-03-12'
render "auto-2024-vintage-2020" $'date: 2024-11-20'

# --- Explicit selection via front matter (overrides the date). --------------
render "explicit-1998" $'date: 2024-01-01\nheiglogo:\n  year: 1998'

# --- Colour variant. --------------------------------------------------------
render "color-2020" $'date: 2024-01-01\nheiglogo:\n  color: true'

# --- Institute and centre logos (bar and text). -----------------------------
render "group-iict" $'date: 2024-01-01\nheiglogo:\n  color: true\n  group: iict'
render "group-rad" $'date: 2024-01-01\nheiglogo:\n  group: rad'

echo
echo "Done. Output under: $OUT"

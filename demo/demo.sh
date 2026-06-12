#!/usr/bin/env bash
#
# Demonstrates the heiglogo fragment's logo-vintage selection.
#
# It renders the same letter-headed document several times:
#   * four "auto" runs whose date alone picks the vintage (1998/2004/2009/2020);
#   * one run that pins the vintage explicitly via `heiglogo.year`;
#   * one run in HEIG-VD red (`heiglogo.color`).
#
# Each scenario lands in its own demo/output/<name>/ folder, holding the source
# Markdown, the generated LaTeX (so you can read the chosen `\logo[... year=NNNN]`)
# and, unless NO_BUILD is set, the compiled PDF.
#
# Usage:
#   ./demo/demo.sh              # render + build PDFs with xelatex
#   ENGINE=lualatex ./demo/demo.sh
#   NO_BUILD=1 ./demo/demo.sh   # emit LaTeX only, skip PDF compilation
#
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
OUT="$HERE/output"
ENGINE="${ENGINE:-xelatex}"

# Always use the project's environment so the local heiglogo fragment is found,
# regardless of the current working directory.
ts() { uv run --project "$ROOT" texsmith "$@"; }

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

echo
echo "Done. Output under: $OUT"

// HEIG-VD logo for Typst, with the institute and centre variants.
//
// A port of heiglogo.sty (https://github.com/HEIG-VD/logos): the outlines of
// the four vintages (1998, 2004, 2009, 2020) are translated from the package's
// TikZ paths by scripts/generate_typst_outlines.py, in the same native units,
// with the same separator and text anchors and the same text metrics. The
// institute and centre texts follow the 2020 graphic charter (Logothèque,
// pages 17-18), set in Arial instead of the charter's Circular, which is not
// freely available.
//
//   #import "heiglogo.typ": heiglogo, heiglogo-page
//   #heiglogo(group: "iict", color: true)                // inline box
//   #set page(background: heiglogo-page(group: "reds"))  // first page, 1 cm in
//
// The group table mirrors GROUPS in _groups.py; a test keeps them in step.

#let heiglogo-groups = (
  // Instituts: acronym in bold on top, name flush with the bottom of the mark.
  "comatec": (title: ("COMATEC",), subtitle: ("Institut de Conception", "mécanique et", "Technologies des", "matériaux")),
  "iai": (title: ("IAI",), subtitle: ("Institut", "d’Automatisation", "industrielle")),
  "ie": (title: ("IE",), subtitle: ("Institut", "des Énergies")),
  "iict": (title: ("IICT",), subtitle: ("Institut des", "Technologies de", "l’information et de", "la communication")),
  "iide": (title: ("IIDE",), subtitle: ("Institut", "interdisciplinaire", "du Développement", "de l’entreprise")),
  "insit": (title: ("INSIT",), subtitle: ("Institut", "d’Ingénierie", "du territoire")),
  "mei": (title: ("MEI",), subtitle: ("Media", "Engineering", "Institute")),
  "reds": (title: ("REDS",), subtitle: ("Institut", "Reconfigurable", "and Embedded", "Digital Systems")),
  // Centres: the whole name in bold, from the top.
  "formation-continue": (title: ("Centre", "Formation", "continue"), subtitle: ()),
  "formation-base": (title: ("Centre", "Formation", "de base"), subtitle: ()),
  "rad": (title: ("Centre", "Ra&D"), subtitle: ()),
  "relations-internationales": (title: ("Centre", "Relations", "internationales"), subtitle: ()),
)

#let heiglogo-fonts = ("Arial", "Arimo", "Liberation Sans", "TeX Gyre Heros")

// The colours of heiglogo.sty.
#let _red = rgb("#e1251b")
#let _vintage-colors = (
  "1998": (a: rgb("#00a651"), b: rgb("#ed1c29"), c: rgb("#231f20")),
  "2004": (logo: rgb("#ee3124")),
  "2009": (logo: rgb("#a63136")),
  "2020": (:),
)

// BEGIN GENERATED OUTLINES (scripts/generate_typst_outlines.py)
// Do not edit: translated from the \heiglogo@draw@<year> macros.
#let _vintages = (
  "2020": (
    width: 100, height: 75, separator: 114, text: 125,
    size: ("height", 18mm),
    fills: (
      (role: "ink", even-odd: false, path: (("M", 74, 18), ("L", 56, 18), ("L", 56, 12), ("L", 68, 12), ("L", 68, 12), ("C", 67, 7, 63, 5, 57, 5), ("C", 50, 5, 45, 10, 45, 17), ("C", 45, 24, 50, 30, 57, 30), ("C", 63, 30, 67, 27, 69, 23), ("L", 74, 25), ("C", 71, 32, 65, 35, 57, 35), ("C", 47, 35, 39, 27, 39, 17), ("C", 39, 7, 47, 0, 57, 0), ("C", 62, 0, 66, 2, 69, 5), ("L", 69, 1), ("L", 74, 1), ("L", 74, 17), ("Z",),)),
      (role: "ink", even-odd: false, path: (("M", 74, 47), ("L", 46, 47), ("L", 46, 56), ("L", 70, 56), ("L", 70, 61), ("L", 46, 61), ("L", 46, 70), ("L", 74, 70), ("L", 74, 75), ("L", 40, 75), ("L", 40, 42), ("L", 74, 42), ("Z",),)),
      (role: "ink", even-odd: false, path: (("M", 27, 61), ("L", 5, 61), ("L", 5, 75), ("L", 0, 75), ("L", 0, 42), ("L", 5, 42), ("L", 5, 56), ("L", 27, 56), ("L", 27, 42), ("L", 33, 42), ("L", 33, 75), ("L", 27, 75), ("Z",),)),
      (role: "ink", even-odd: false, path: (("M", 19, 6), ("L", 19, 29), ("L", 33, 29), ("L", 33, 34), ("L", 0, 34), ("L", 0, 29), ("L", 13, 29), ("L", 13, 6), ("L", 0, 6), ("L", 0, 1), ("L", 33, 1), ("L", 33, 6), ("Z",),)),
      (role: "ink", even-odd: false, path: (("M", 88, 75), ("L", 90, 75), ("L", 87, 65), ("L", 85, 65), ("L", 81, 75), ("L", 83, 75), ("L", 86, 68), ("Z",),)),
      (role: "ink", even-odd: false, path: (("M", 92, 65), ("L", 92, 75), ("L", 95, 75), ("C", 98, 75, 100, 73, 100, 70), ("C", 100, 67, 98, 65, 95, 65), ("Z",),)),
      (role: "white", even-odd: false, path: (("M", 95, 67), ("C", 97, 67, 98, 68, 98, 70), ("C", 98, 72, 97, 73, 95, 73), ("L", 94, 73), ("L", 94, 67), ("Z",),)),
    ),
  ),
  "1998": (
    width: 175.77, height: 89.27, separator: 179, text: 184,
    size: ("height", 18mm),
    fills: (
      (role: "a", even-odd: true, path: (("M", 91.22, 57.45), ("C", 98.92, 58.46, 104.47, 59.11, 112.89, 60.98), ("C", 115.91, 50.9, 116.63, 42.26, 117.21, 18.57), ("C", 131.68, 33.33, 134.78, 38.8, 134.78, 42.4), ("C", 134.78, 46.58, 128.66, 47.94, 128.66, 53.7), ("C", 128.66, 58.02, 132.84, 60.83, 136.15, 60.97), ("C", 140.04, 60.97, 144.93, 57.87, 144.93, 52.26), ("C", 144.93, 39.59, 128.23, 20.8, 104.47, 0.71), ("L", 100.87, 0.71), ("L", 101.45, 17.99), ("C", 101.59, 23.82, 101.74, 36.64, 99.51, 47.01), ("C", 97.93, 53.99, 96.27, 53.99, 91.23, 53.99), ("L", 91.23, 57.45), ("L", 91.23, 57.45), ("L", 91.22, 57.45), ("Z",),)),
      (role: "a", even-odd: true, path: (("M", 169.63, 11.3), ("C", 167.4, 8.06, 162.36, 0.86, 156.09, 0.86), ("C", 155.37, 0.86, 150.55, 0.86, 150.55, 5.83), ("C", 150.55, 7.27, 150.84, 8.64, 151.49, 11.3), ("L", 151.35, 11.16), ("C", 148.76, 7.13, 144.29, 0.72, 136.45, 0.72), ("C", 128.61, 0.72, 126.8, 7.56, 126.8, 11.16), ("C", 126.8, 24.12, 140.77, 40.03, 151.35, 40.03), ("C", 155.31, 40.03, 156.82, 38.52, 158.19, 37.37), ("C", 160.13, 44.21, 162.37, 51.34, 162.37, 52.56), ("C", 162.37, 54.65, 160.71, 55.08, 158.63, 55.08), ("L", 156.83, 55.08), ("L", 156.83, 57.31), ("C", 168.42, 58.17, 172.6, 59.11, 175.77, 59.69), ("L", 165.76, 26.07), ("C", 164.75, 23.19, 160.58, 9.08, 160.58, 7.78), ("C", 160.58, 7.42, 160.72, 6.7, 161.59, 6.7), ("C", 163.53, 6.7, 167.13, 11.88, 167.71, 12.53), ("L", 169.65, 11.31), ("L", 169.65, 11.31), ("L", 169.63, 11.3), ("Z",), ("M", 141.91, 6.69), ("C", 150.55, 6.69, 156.81, 29.87, 156.81, 32.18), ("C", 156.81, 32.76, 156.67, 36.57, 153.28, 36.57), ("C", 145.36, 36.57, 138.09, 17.27, 138.09, 11.59), ("C", 138.09, 11.16, 138.23, 6.69, 141.91, 6.69), ("L", 141.91, 6.69), ("L", 141.91, 6.69), ("Z",),)),
      (role: "b", even-odd: true, path: (("M", 83.3, 19.5), ("C", 80.49, 15.76, 75.74, 9.49, 72.43, 9.49), ("C", 71.57, 9.49, 70.34, 9.99, 70.34, 11.29), ("C", 70.34, 15.32, 78.84, 42.25, 84.24, 60.39), ("C", 74.81, 58.3, 61.7, 57.15, 56.09, 56.72), ("L", 56.09, 53.41), ("C", 60.12, 53.55, 64.3, 53.41, 64.3, 49.38), ("C", 63.65, 46.43, 62.5, 42.4, 61.28, 38.08), ("C", 60.85, 36.42, 60.13, 34.41, 59.62, 32.46), ("C", 57.6, 26.48, 55.3, 20.8, 52.78, 17.7), ("C", 50.12, 14.75, 45.22, 9.2, 37.01, 9.2), ("C", 23.76, 9.2, 20.67, 22.16, 20.23, 32.89), ("L", 55.37, 32.89), ("C", 55.01, 39.73, 53.14, 61.91, 28.87, 61.91), ("C", 12.74, 61.91, 0, 49.89, 0, 31.1), ("C", 0, 9.5, 14.4, 0, 28.51, 0), ("C", 38.81, 0, 46.37, 3.46, 54.14, 13.39), ("C", 53.71, 11.45, 53.42, 9.86, 53.42, 9.07), ("C", 53.42, 5.97, 55, 0.57, 63.07, 0.57), ("C", 73.37, 0.57, 79.27, 7.91, 86.4, 17.85), ("L", 87.34, 19.07), ("L", 84.17, 20.8), ("L", 83.31, 19.5), ("L", 83.31, 19.5), ("L", 83.3, 19.5), ("Z",), ("M", 29.45, 57.88), ("C", 34.35, 57.88, 36.15, 54.78, 37.01, 52.05), ("C", 38.09, 48.09, 38.09, 41.54, 38.23, 37.65), ("L", 19.58, 37.65), ("C", 19.58, 55.07, 24.26, 57.88, 29.44, 57.88), ("L", 29.44, 57.88), ("L", 29.45, 57.88), ("Z",),)),
      (role: "b", even-odd: true, path: (("M", 80.21, 89.27), ("C", 73.95, 89.27, 70.99, 83.8, 70.99, 80.92), ("C", 70.99, 77.54, 73.65, 72.21, 80.21, 72.21), ("C", 85.68, 72.21, 89.86, 76.03, 89.86, 80.63), ("C", 89.86, 85.23, 85.53, 89.27, 80.21, 89.27), ("L", 80.21, 89.27), ("Z",),)),
      (role: "c", even-odd: true, path: (("M", 89.85, 16.84), ("C", 95.83, 16.84, 100.58, 21.74, 100.58, 27.64), ("C", 100.58, 33.54, 95.83, 38.37, 89.85, 38.37), ("C", 83.87, 38.37, 79.27, 33.47, 79.27, 27.64), ("C", 79.27, 21.81, 84.02, 16.84, 89.85, 16.84), ("L", 89.85, 16.84), ("Z",),)),
    ),
  ),
  "2004": (
    width: 34, height: 70.9, separator: 39, text: 44,
    size: ("height", 26mm),
    fills: (
      (role: "logo", even-odd: false, path: (("M", 0, 0), ("L", 34, 0), ("L", 34, 70.9), ("L", 0, 70.9), ("Z",),)),
      (role: "white", even-odd: true, path: (("M", 26.2, 13.2), ("L", 18.8, 13.2), ("C", 17.2, 13.2, 15.4, 12.9, 15.4, 10.4), ("C", 15.4, 9.5, 15.7, 8.9, 16, 8.5), ("C", 16.7, 7.7, 17.9, 7.5, 18.7, 7.5), ("L", 26.1, 7.5), ("L", 26.1, 6.3), ("L", 10.7, 6.3), ("L", 10.7, 7.5), ("L", 16.2, 7.5), ("C", 15.6, 7.6, 14.3, 8.7, 14.3, 10.6), ("C", 14.3, 12.1, 14.9, 13.2, 15.6, 13.7), ("C", 16.4, 14.3, 17.4, 14.3, 18.7, 14.3), ("L", 26.1, 14.3), ("L", 26.1, 13.2), ("L", 26.2, 13.2), ("Z",),)),
      (role: "white", even-odd: true, path: (("M", 20.7, 17.5), ("C", 20.7, 17.5, 20.9, 17.5, 21.1, 17.5), ("C", 22.2, 17.6, 25.1, 17.9, 25.1, 21.6), ("C", 25.1, 23.9, 23.5, 25, 23.5, 25), ("L", 25, 24.8), ("C", 25, 24.8, 26.2, 23.6, 26.2, 21.5), ("C", 26.2, 16.6, 22.1, 16.2, 20.4, 16.2), ("C", 18.5, 16.2, 14.3, 16.7, 14.3, 20.9), ("C", 14.3, 25.1, 18.9, 25.3, 20.1, 25.3), ("C", 20.4, 25.3, 20.7, 25.3, 20.7, 25.3), ("L", 20.7, 17.5), ("L", 20.7, 17.5), ("Z",), ("M", 15.4, 21), ("C", 15.3, 17.7, 19.4, 17.6, 19.7, 17.6), ("L", 19.7, 24.1), ("C", 19.7, 24.1, 15.4, 24.2, 15.4, 21), ("Z",),)),
      (role: "white", even-odd: true, path: (("M", 21.3, 41), ("L", 20.1, 41), ("L", 20.1, 45.9), ("L", 21.3, 45.9), ("L", 21.3, 41), ("Z",),)),
      (role: "white", even-odd: true, path: (("M", 26.4, 60.3), ("C", 26.4, 57.2, 23.7, 55.9, 20.3, 55.9), ("C", 17.1, 55.9, 14.4, 57.7, 14.4, 60.4), ("C", 14.4, 62.3, 15.6, 63.2, 16.1, 63.4), ("L", 10.7, 63.4), ("L", 10.7, 64.6), ("C", 10.7, 64.6, 20.9, 64.6, 22, 64.6), ("C", 23.6, 64.6, 26.4, 63.6, 26.4, 60.3), ("Z",), ("M", 18.9, 63.4), ("C", 18.3, 63.4, 17, 63.3, 16.3, 62.6), ("C", 15.8, 62.2, 15.5, 61.4, 15.5, 60.4), ("C", 15.5, 58.3, 17.7, 57.1, 20.5, 57.1), ("C", 23.1, 57.1, 25.4, 58, 25.4, 60.4), ("C", 25.4, 62.3, 23.8, 63.3, 22.4, 63.3), ("L", 18.9, 63.3), ("L", 18.9, 63.4), ("Z",),)),
      (role: "white", even-odd: true, path: (("M", 14.6, 54.2), ("C", 14.6, 54.2, 24.6, 51.1, 24.7, 51), ("C", 24.9, 50.9, 24.9, 50.9, 24.7, 50.8), ("C", 24.6, 50.8, 14.6, 47.6, 14.6, 47.6), ("L", 14.6, 46.4), ("L", 25.4, 49.9), ("C", 26, 50.2, 26.3, 50.5, 26.3, 51), ("C", 26.3, 51.5, 26.1, 51.8, 25.4, 52.1), ("C", 25.4, 52.1, 14.6, 55.5, 14.6, 55.5), ("L", 14.6, 54.2), ("L", 14.6, 54.2), ("Z",),)),
      (role: "white", even-odd: true, path: (("M", 26.2, 27.4), ("L", 14.6, 27.4), ("L", 14.6, 28.6), ("L", 26.2, 28.6), ("L", 26.2, 27.4), ("Z",),)),
      (role: "white", even-odd: true, path: (("M", 12.8, 27.4), ("L", 11.5, 27.4), ("L", 11.5, 28.6), ("L", 12.8, 28.6), ("L", 12.8, 27.4), ("Z",),)),
      (role: "white", even-odd: true, path: (("M", 24, 35.4), ("C", 24, 34.3, 24.3, 32, 23.1, 32), ("C", 22.1, 32, 22.2, 33.6, 22.2, 35.2), ("C", 22.2, 37.7, 20.7, 39.3, 18.3, 39.3), ("C", 17, 39.3, 16, 38.9, 15.3, 38.1), ("L", 15.3, 39.5), ("L", 14.3, 39.5), ("L", 14.3, 35.2), ("L", 14.3, 35.2), ("C", 14.3, 35.2, 14.3, 35.1, 14.3, 35.1), ("C", 14.3, 33.3, 15.3, 31.3, 18.3, 31.3), ("C", 20.3, 31.3, 21.3, 32.6, 21.4, 33.1), ("C", 21.4, 32.6, 21.7, 30.8, 23.2, 30.9), ("C", 24.1, 30.9, 24.5, 31.4, 24.7, 32.4), ("C", 24.9, 31.8, 25.8, 30.9, 27.1, 30.9), ("C", 28.7, 30.9, 30.1, 32.4, 30.1, 35.4), ("C", 30.1, 37.9, 29, 39.7, 26.9, 39.8), ("C", 25, 39.7, 24, 38.4, 24, 35.4), ("Z",), ("M", 18.3, 32.4), ("C", 16.6, 32.4, 15.3, 33.2, 15.3, 35.2), ("C", 15.3, 37.4, 16.8, 38.1, 18.3, 38.1), ("C", 20.3, 38.1, 21.2, 36.9, 21.2, 35.1), ("C", 21.3, 33.6, 20.1, 32.4, 18.3, 32.4), ("Z",), ("M", 29.2, 35.3), ("C", 29.2, 33.1, 28.3, 31.9, 27.1, 31.9), ("C", 26.1, 31.9, 25.3, 32.7, 25.2, 33.4), ("C", 25.2, 33.4, 25.2, 34.4, 25.2, 35.3), ("C", 25.2, 37.8, 26.1, 38.5, 27.1, 38.5), ("C", 28.5, 38.5, 29.2, 36.8, 29.2, 35.3), ("Z",),)),
    ),
  ),
  "2009": (
    width: 224.29, height: 75, separator: 229.3, text: 235.3,
    size: ("width", 35mm),
    fills: (
      (role: "logo", even-odd: true, path: (("M", 43.19, 36.42), ("L", 43.19, 34.84), ("C", 43.43, 30.75, 44.61, 19.29, 58.82, 19.29), ("C", 67.52, 19.29, 71.93, 25.47, 71.93, 25.47), ("L", 71.34, 19.69), ("C", 71.34, 19.69, 66.89, 15, 58.66, 15), ("C", 39.69, 15, 38.27, 30.71, 38.27, 37.44), ("C", 38.27, 44.61, 40.31, 60.79, 56.26, 60.87), ("C", 72.56, 60.94, 73.35, 43.19, 73.35, 38.58), ("L", 73.35, 36.38), ("L", 43.19, 36.38), ("M", 56.42, 56.97), ("C", 43.58, 57.2, 43.43, 41.42, 43.43, 40.35), ("L", 68.58, 40.35), ("C", 68.58, 40.35, 68.9, 56.73, 56.42, 56.97),)),
      (role: "logo", even-odd: false, path: (("M", 133.31, 34.13), ("L", 152.17, 34.13), ("L", 152.17, 38.66), ("L", 133.31, 38.66), ("Z",),)),
      (role: "logo", even-odd: true, path: (("M", 184.21, 59.84), ("C", 184.21, 59.84, 172.13, 21.34, 171.97, 20.91), ("C", 171.69, 20.2, 171.61, 20.24, 171.38, 20.94), ("C", 171.22, 21.38, 159.17, 59.84, 159.17, 59.84), ("L", 154.41, 59.84), ("L", 167.64, 18.31), ("C", 168.62, 15.98, 169.8, 15, 171.69, 15), ("C", 173.58, 15, 174.8, 15.94, 175.79, 18.31), ("L", 188.98, 59.84), ("L", 184.21, 59.84),)),
      (role: "logo", even-odd: false, path: (("M", 81.14, 15.35), ("L", 85.83, 15.35), ("L", 85.83, 59.84), ("L", 81.14, 59.84), ("Z",),)),
      (role: "logo", even-odd: false, path: (("M", 81.14, 66.97), ("L", 85.87, 66.97), ("L", 85.87, 71.81), ("L", 81.14, 71.81), ("Z",),)),
      (role: "logo", even-odd: true, path: (("M", 111.93, 23.9), ("C", 107.64, 23.9, 98.78, 22.83, 98.78, 27.2), ("C", 98.78, 31.06, 105.12, 30.59, 111.3, 30.59), ("C", 121.06, 30.59, 127.01, 36.34, 127.01, 45.55), ("C", 127.01, 50.35, 125.31, 54.33, 122.28, 57.01), ("L", 127.52, 57.01), ("L", 127.52, 60.91), ("L", 110.98, 60.91), ("C", 110.98, 60.91, 110.79, 60.91, 110.67, 60.91), ("C", 103.66, 60.91, 95.94, 57.13, 95.94, 45.51), ("C", 95.94, 37.8, 101.06, 33.86, 102.91, 33.5), ("C", 101.02, 33.5, 94.21, 32.52, 94.37, 26.46), ("C", 94.45, 23.07, 96.26, 21.34, 100.04, 20.71), ("C", 97.91, 19.96, 94.13, 16.57, 94.13, 11.42), ("C", 94.13, 5.08, 99.88, 0, 111.5, 0), ("C", 120.94, 0, 128.11, 4.09, 128.27, 12.17), ("C", 128.43, 19.8, 123.35, 23.9, 112.01, 23.9), ("M", 100.35, 45.51), ("C", 100.35, 52.17, 103.54, 56.93, 111.3, 56.93), ("C", 119.61, 56.93, 122.56, 51.02, 122.56, 45.51), ("C", 122.56, 37.95, 117.8, 34.17, 110.94, 34.17), ("C", 104.96, 34.17, 100.35, 38.78, 100.35, 45.51), ("L", 100.35, 45.51), ("Z",), ("M", 111.42, 3.94), ("C", 103.03, 3.94, 98.43, 7.32, 98.43, 12.17), ("C", 98.43, 15.87, 101.65, 18.98, 104.13, 19.65), ("C", 104.13, 19.65, 108.07, 19.72, 111.61, 19.65), ("C", 121.06, 19.57, 123.78, 16.02, 123.78, 12.17), ("C", 123.78, 6.65, 117.44, 3.94, 111.46, 3.94),)),
      (role: "logo", even-odd: true, path: (("M", 26.57, 15.35), ("L", 26.57, 43.78), ("C", 26.57, 50.12, 25.59, 56.77, 15.94, 56.77), ("C", 12.32, 56.77, 10.2, 55.79, 8.54, 54.37), ("C", 5.35, 51.65, 4.69, 47.13, 4.69, 43.94), ("L", 4.69, 15.31), ("L", 0, 15.31), ("L", 0, 74.76), ("L", 4.69, 74.76), ("L", 4.69, 53.54), ("C", 5.2, 55.94, 9.13, 60.87, 16.77, 60.87), ("C", 22.68, 60.87, 26.89, 58.66, 28.78, 55.75), ("C", 30.94, 52.64, 31.26, 48.94, 31.26, 43.94), ("L", 31.26, 15.31), ("L", 26.57, 15.31),)),
      (role: "logo", even-odd: true, path: (("M", 207.83, 14.69), ("C", 195.98, 14.69, 190.98, 25.24, 190.98, 38.03), ("C", 190.98, 50.83, 197.72, 60.83, 208.15, 60.75), ("C", 215.63, 60.67, 219.09, 56.26, 219.57, 54.37), ("L", 219.57, 75), ("L", 224.29, 75), ("L", 224.29, 31.38), ("C", 224.29, 25.2, 220.63, 14.72, 207.83, 14.72), ("M", 219.57, 43.46), ("C", 219.57, 45.63, 219.17, 50.87, 216.69, 53.62), ("C", 215.04, 55.55, 212.2, 56.89, 208.39, 56.89), ("C", 200.24, 56.89, 195.67, 48.31, 195.75, 37.83), ("C", 195.83, 27.72, 199.41, 18.82, 208.39, 18.82), ("C", 215.83, 18.82, 219.57, 24.96, 219.57, 30.43), ("L", 219.57, 43.46),)),
    ),
  ),
)
// END GENERATED OUTLINES

// One fill, in native units with y pointing up as in TikZ: "M"/"L" take a
// point, "C" two control points and an end point, "Z" closes the subpath.
#let _shape(fill, u, top, paint) = {
  let pt(x, y) = (x * u, (top - y) * u)
  let parts = ()
  for seg in fill.path {
    let op = seg.at(0)
    if op == "M" {
      parts.push(curve.move(pt(seg.at(1), seg.at(2))))
    } else if op == "L" {
      parts.push(curve.line(pt(seg.at(1), seg.at(2))))
    } else if op == "C" {
      parts.push(curve.cubic(pt(seg.at(1), seg.at(2)), pt(seg.at(3), seg.at(4)), pt(seg.at(5), seg.at(6))))
    } else {
      parts.push(curve.close())
    }
  }
  curve(
    fill: paint,
    fill-rule: if fill.even-odd { "even-odd" } else { "non-zero" },
    stroke: none,
    ..parts,
  )
}

// The logo of `year` as a box. Its size is `height`, or `width`, or else the
// vintage's default (18 mm high; 26 mm high for 2004; 35 mm wide for 2009).
// `group` names an institute or a centre (a key of `heiglogo-groups`) whose
// bar and text follow the mark; `none` draws the mark alone.
#let heiglogo(year: "2020", height: auto, width: auto, color: false, group: none, lines: 5) = {
  let year = str(year)
  assert(year in _vintages,
    message: "unknown heiglogo year " + repr(year) + "; expected one of "
      + _vintages.keys().join(", "))
  let v = _vintages.at(year)
  let height = if height != auto {
    height
  } else if width != auto {
    width * v.height / v.width
  } else if v.size.at(0) == "width" {
    v.size.at(1) * v.height / v.width
  } else {
    v.size.at(1)
  }
  let u = height / v.height
  let ink = if color { _red } else { black }
  let colors = _vintage-colors.at(year)
  let paint(role) = if role == "white" { white } else if color and role in colors { colors.at(role) } else { ink }
  let mark = v.fills.map(f => place(top + left, _shape(f, u, v.height, paint(f.role)))).join()
  if group == none {
    return box(width: v.width * u, height: height, mark)
  }
  let key = lower(str(group)).replace("_", "-").replace(" ", "-")
  assert(key in heiglogo-groups,
    message: "unknown heiglogo group " + repr(group) + "; expected one of "
      + heiglogo-groups.keys().join(", "))
  let entry = heiglogo-groups.at(key)

  // The metrics of heiglogo.sty: `lines` baselines over the mark (plus 1 mm),
  // the font size 1/1.2 of the baseline skip.
  let skip = (height + 1mm) / lines
  let size = skip / 1.2
  let setting(rows, weight) = text(
    font: heiglogo-fonts, size: size, weight: weight, fill: ink,
    top-edge: "cap-height", bottom-edge: "baseline",
    rows.join(linebreak()),
  )
  context {
    let cap = measure(text(font: heiglogo-fonts, size: size, top-edge: "cap-height", bottom-edge: "baseline", "H")).height
    set par(leading: skip - cap, spacing: 0pt, justify: false)
    let title = setting(entry.title, "bold")
    let subtitle = if entry.subtitle.len() > 0 { setting(entry.subtitle, "regular") }
    let width = calc.max(measure(title).width, if subtitle != none { measure(subtitle).width } else { 0pt })
    box(width: v.text * u + width, height: height, {
      mark
      place(top + left, dx: v.separator * u, rect(width: u, height: height, fill: ink, stroke: none))
      place(top + left, dx: v.text * u, title)
      if subtitle != none {
        place(bottom + left, dx: v.text * u, dy: -2 * u, subtitle)
      }
    })
  }
}

// For `set page(background: ...)`: the logo `left`/`top` from the sheet's
// top-left corner, on the first page only.
#let heiglogo-page(left: 1cm, top: 1cm, ..args) = context {
  if here().page() == 1 {
    place(std.top + std.left, dx: left, dy: top, heiglogo(..args))
  }
}

// Vertical space that moves the flow below a logo placed `top` from the sheet
// edge (plus `gap`), when the page's content would otherwise start under it.
#let heiglogo-clearance(top: 1cm, gap: 5mm, ..args) = context {
  let bottom = top + measure(heiglogo(..args)).height + gap
  let y = here().position().y
  if y < bottom { v(bottom - y) }
}

---
title: Rapport de laboratoire
author: Ada Lovelace
date: 2006-05-01
language: french
fragments:
  append:
    - heiglogo
heiglogo:
  # year: 2004     # décommenter pour forcer un millésime précis
  # year: auto      # (défaut) déduit le millésime de la date du document
  color: false
---

# Introduction

Ce document montre le fragment `heiglogo`. Le logo apparaît en haut à
gauche de chaque page. Comme `heiglogo.year` vaut `auto` (la valeur par
défaut), le millésime du logo est choisi automatiquement à partir du
champ `date` de l'en-tête : un document daté de 2006 reçoit le logo 2004.

# Conclusion

Changez la `date` (ou fixez `heiglogo.year`) pour obtenir un autre
millésime — voir `demo.sh`.

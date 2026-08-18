#!/usr/bin/env python3
"""Leser kvartalstall fra en CSV-fil og skriver ut et sammendrag.

Sammendraget følger retningslinjene i CLAUDE.md:
- punktform på bokmål
- maksimalt tre punkter
- inkluderer alltid største og minste verdi fra dataene
"""

import csv
import sys


def les_data(filnavn):
    """Leser CSV-filen og returnerer (kvartaler, [(region, [tall])])."""
    rader = []
    with open(filnavn, newline="", encoding="utf-8") as f:
        leser = csv.DictReader(f)
        kvartaler = [k for k in leser.fieldnames if k != "region"]
        for rad in leser:
            tall = [float(rad[k]) for k in kvartaler]
            rader.append((rad["region"], tall))
    return kvartaler, rader


def finn_ytterpunkt(kvartaler, rader, velg):
    """Finner høyeste (velg=max) eller laveste (velg=min) enkeltverdi.

    Returnerer (region, kvartal, verdi)."""
    treff = None
    for region, tall in rader:
        for kvartal, verdi in zip(kvartaler, tall):
            if treff is None or velg(verdi, treff[2]) == verdi:
                treff = (region, kvartal, verdi)
    return treff


def lag_sammendrag(kvartaler, rader):
    """Bygger et sammendrag på maksimalt tre punkter."""
    alle_tall = [v for _, tall in rader for v in tall]
    snitt = sum(alle_tall) / len(alle_tall)

    hoy_region, hoy_kvartal, hoy_verdi = finn_ytterpunkt(kvartaler, rader, max)
    lav_region, lav_kvartal, lav_verdi = finn_ytterpunkt(kvartaler, rader, min)

    return [
        f"Gjennomsnittet på tvers av {len(rader)} regioner er {snitt:.1f}.",
        f"Største verdi er {hoy_verdi:.0f} ({hoy_region}, {hoy_kvartal}).",
        f"Minste verdi er {lav_verdi:.0f} ({lav_region}, {lav_kvartal}).",
    ]


def main():
    filnavn = sys.argv[1] if len(sys.argv) > 1 else "kvartalstall2.csv"
    kvartaler, rader = les_data(filnavn)

    print(f"Sammendrag (fil: {filnavn})")
    for punkt in lag_sammendrag(kvartaler, rader):
        print(f"- {punkt}")


if __name__ == "__main__":
    main()

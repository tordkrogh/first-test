#!/usr/bin/env python3
"""Leser kvartalstall fra en CSV-fil og skriver ut et kort sammendrag.

For hver region beregnes gjennomsnittet av de fire kvartalene og den
største endringen mellom to påfølgende kvartaler.
"""

import csv
import sys


def les_data(filnavn):
    """Leser CSV-filen og returnerer en liste med (region, [tall])."""
    rader = []
    with open(filnavn, newline="", encoding="utf-8") as f:
        leser = csv.DictReader(f)
        kvartaler = [k for k in leser.fieldnames if k != "region"]
        for rad in leser:
            tall = [float(rad[k]) for k in kvartaler]
            rader.append((rad["region"], tall))
    return kvartaler, rader


def storste_endring(tall):
    """Returnerer (endring, fra_indeks) for den største endringen i
    absoluttverdi mellom to påfølgende kvartaler."""
    endringer = [tall[i + 1] - tall[i] for i in range(len(tall) - 1)]
    beste = max(range(len(endringer)), key=lambda i: abs(endringer[i]))
    return endringer[beste], beste


def main():
    filnavn = sys.argv[1] if len(sys.argv) > 1 else "kvartalstall.csv"
    kvartaler, rader = les_data(filnavn)

    print(f"Sammendrag for {len(rader)} regioner (fil: {filnavn})")
    print("-" * 48)

    for region, tall in rader:
        snitt = sum(tall) / len(tall)
        endring, fra = storste_endring(tall)
        overgang = f"{kvartaler[fra]}->{kvartaler[fra + 1]}"
        fortegn = "+" if endring >= 0 else ""
        print(
            f"{region:<10} gjennomsnitt: {snitt:6.1f}   "
            f"største endring: {fortegn}{endring:.0f} ({overgang})"
        )


if __name__ == "__main__":
    main()

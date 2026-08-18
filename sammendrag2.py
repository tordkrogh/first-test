#!/usr/bin/env python3
"""Leser kvartalstall fra en CSV-fil og skriver ut et sammendrag.

Sammendraget følger retningslinjene i CLAUDE.md:
- punktform på bokmål
- maksimalt tre punkter
- inkluderer alltid største og minste verdi fra dataene

I tillegg lages en enkel linjediagram-figur av kvartalstallene, lagret
som en PNG-fil.
"""

import csv
import os
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


# FIN supplerende designprofil – fargepalett (primærfarger først).
# Linjediagram: maks fire linjer, mørkeblå er primær.
FIN_PALETTE = [
    "#181c62",  # mørkeblå
    "#4156a6",  # mellomblå
    "#5b91cc",  # lyseblå
    "#f15d61",  # rød
]


def lag_figur(kvartaler, rader, filnavn):
    """Lager et linjediagram av kvartalstallene etter FINs designprofil.

    Én linje per region (maks fire). Returnerer filnavnet ved suksess,
    ellers None (for eksempel hvis matplotlib ikke er installert)."""
    try:
        import logging
        import matplotlib
        matplotlib.use("Agg")  # headless-backend, krever ingen skjerm
        import matplotlib.pyplot as plt
        # Arial foretrekkes (FIN-profil), men mangler den, faller vi stille
        # tilbake til DejaVu Sans i stedet for å spamme advarsler.
        logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    except ImportError:
        print("(Hopper over figur: matplotlib er ikke installert – "
              "kjør 'pip install matplotlib')")
        return None

    # FIN-profil: Arial-font, hvit bakgrunn, tynne sorte akser, ingen grid.
    plt.rcParams.update({
        "font.family": ["Arial", "DejaVu Sans", "sans-serif"],
        "font.size": 10,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#000000",
        "axes.linewidth": 0.5,
        "axes.spines.top": False,
        "axes.spines.right": True,   # y-akse på begge sider
        "xtick.direction": "in",     # tickmarks peker inn mot figuren
        "ytick.direction": "in",
        "xtick.major.size": 0,       # ingen tickmarks på x-aksen
        "ytick.major.size": 3,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "lines.linewidth": 1.5,
        "lines.solid_capstyle": "round",
    })

    fig, ax = plt.subplots(figsize=(8, 5))
    for i, (region, tall) in enumerate(rader):
        farge = FIN_PALETTE[i % len(FIN_PALETTE)]
        ax.plot(kvartaler, tall, marker="o", color=farge, label=region)

    # Ingen tittel/kilde inne i figuren (FIN-konvensjon). Enheten står som
    # en liten merkelapp øverst ved y-aksen.
    ax.set_xlabel("Kvartal")
    ax.set_ylabel("Verdi")

    # Speil y-aksen til høyre side med innovervendte tickmarks.
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(ax.get_yticks())
    ax2.tick_params(axis="y", direction="in", length=3, colors="#000000")
    ax2.spines["top"].set_visible(False)

    # Tegnforklaring under diagrammet, full bredde.
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12),
              ncol=len(rader), frameon=False)

    fig.savefig(filnavn, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return filnavn


def main():
    filnavn = sys.argv[1] if len(sys.argv) > 1 else "kvartalstall2.csv"
    kvartaler, rader = les_data(filnavn)

    print(f"Sammendrag (fil: {filnavn})")
    for punkt in lag_sammendrag(kvartaler, rader):
        print(f"- {punkt}")

    figurfil = os.path.splitext(filnavn)[0] + ".png"
    lagret = lag_figur(kvartaler, rader, figurfil)
    if lagret:
        print(f"Figur lagret: {lagret}")


if __name__ == "__main__":
    main()

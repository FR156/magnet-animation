"""Scene 09 — Closing (20 d).

Narasi (rencana, disinkronkan ulang setelah voice-over final):
  0–14  "Dari kutub magnet sampai transformator, satu hal menyatukan semuanya: listrik dan magnet
         saling menghasilkan. Terima kasih sudah menonton."
  14–20 (hening, kredit tampil, fade ke hitam)

Titik sinkron (pad_to): 6.0 | 18.3 | 20.0
"""
import sys
import pathlib

# Agar `utils` dapat diimpor saat scene dirender langsung lewat `manim`.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    VGroup, FadeIn, FadeOut, Write, LaggedStart, DOWN, UR,
)
from utils import style as S  # noqa: E402
from utils.components import (  # noqa: E402
    BaseScene, txt, formula, u_s_badge, bar_magnet, magnet_field_lines, wire_cross_section, circular_field,
)

SCENE_ID = 9
MEMBERS = ["Daffina Anastasya", "Olivia Maria Sinaga", "Elvan Bastanta Barus", "Fazli Rasyad"]


def emblem(scale=0.55):
    """Lambang pembuka: magnet + garis medan  <->  kawat berarus + lingkaran medan (seperti Scene 1)."""
    magnet = bar_magnet()
    lines = magnet_field_lines(spread=(1.1, 2.0))
    left = VGroup(magnet, lines).move_to([0, 0, 0])
    wire = wire_cross_section("out")
    rings = VGroup(circular_field(0.85, ccw=True), circular_field(1.55, ccw=True))
    right = VGroup(rings, wire).move_to([0, 0, 0])
    left.scale(scale).move_to([-2.5, 0, 0])
    right.scale(scale).move_to([2.5, 0, 0])
    link = formula(r"\leftrightarrow", S.ACCENT, 72).move_to([0, 0, 0])
    return VGroup(left, link, right)


class Scene09Closing(BaseScene):
    def construct(self):
        badge = u_s_badge().to_corner(UR, buff=0.6)
        self.add(badge)
        em = emblem().move_to([0, 2.0, 0])
        title = txt("Magnet dan Elektromagnetik", 52, S.TEXT, "BOLD").move_to([0, -0.15, 0])
        self.play(FadeIn(em), run_time=1.2)
        self.play(Write(title), run_time=1.5)

        # kredit
        self.pad_to(6.0)
        head = txt("Kelompok 10", S.SZ_HEAD, S.ACCENT, "BOLD")
        names = VGroup(*[txt(n, S.SZ_BODY, S.TEXT_SOFT) for n in MEMBERS]).arrange(DOWN, buff=0.16)
        credits = VGroup(head, names).arrange(DOWN, buff=0.28).move_to([0, -2.2, 0])
        self.play(FadeIn(head), LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.35), run_time=2.2)

        # fade ke hitam
        self.pad_to(18.3)
        self.play(FadeOut(VGroup(em, title, credits, badge)), run_time=1.7)
        self.pad_to(S.SCENE_DURATIONS[SCENE_ID])

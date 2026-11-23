"""Scene 01 — Opening (12 d).

Narasi (0:00–0:12):
  "Magnet dan listrik tampak berbeda, tetapi ternyata keduanya saling berhubungan.
   Hubungan inilah yang menggerakkan motor, memutar generator, dan mengubah
   tegangan di transformator."

Alur visual:
  0.0–5.3  magnet batang + garis medan (U -> S), lalu kawat berarus + lingkaran medan
  5.3–8.3  keduanya bergeser ke tengah, tanda hubungan (<->) muncul
  8.3–10.9 judul + subjudul
  10.9–12  judul mengecil menjadi lencana [U | S] di pojok
"""
import sys
import pathlib

# Agar `utils` dapat diimpor saat scene dirender langsung lewat `manim`.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from manim import (  # noqa: E402
    VGroup, FadeIn, FadeOut, Create, Write, MathTex, LaggedStart,
    UP, DOWN, UR, LEFT, RIGHT,
)
from utils import style as S  # noqa: E402
from utils.components import (  # noqa: E402
    BaseScene, txt, formula, u_s_badge, bar_magnet, magnet_field_lines,
    wire_cross_section, circular_field,
)

SCENE_ID = 1


class Scene01Opening(BaseScene):
    def construct(self):
        # ---------- Kiri: magnet batang + garis medan (U -> S di luar magnet) ----------
        magnet = bar_magnet()
        lines = magnet_field_lines(spread=(1.1, 2.0))
        b_label = formula("B", S.FIELD, 48).move_to(UP * 2.35)
        left = VGroup(magnet, lines, b_label).move_to([-3.8, 0, 0])

        # ---------- Kanan: kawat berarus ⊙ + lingkaran medan (berlawanan arah jarum jam) ----------
        wire = wire_cross_section("out")
        rings = VGroup(circular_field(0.85, ccw=True), circular_field(1.55, ccw=True))
        i_label = formula("I", S.CURRENT, 48).move_to(UP * 0.56)
        b_label2 = formula("B", S.FIELD, 48).move_to(RIGHT * 1.9)
        right = VGroup(rings, wire, i_label, b_label2).move_to([3.8, 0, 0])

        # ---------- Adegan 1: magnet ----------
        self.play(FadeIn(magnet), run_time=0.6)
        self.play(Create(lines), FadeIn(b_label, run_time=0.8), run_time=1.8)
        self.wait(0.4)

        # ---------- Adegan 2: kawat berarus ----------
        self.play(FadeIn(wire), FadeIn(i_label), run_time=0.5)
        self.play(Create(rings), FadeIn(b_label2, run_time=0.8), run_time=1.6)
        self.wait(1.2)

        # ---------- Adegan 3: bertemu di tengah ----------
        link = MathTex(r"\leftrightarrow", color=S.ACCENT, font_size=72).move_to([0, 1.2, 0])
        self.play(
            left.animate.scale(0.55).move_to([-2.5, 1.2, 0]),
            right.animate.scale(0.55).move_to([2.5, 1.2, 0]),
            run_time=1.3,
        )
        self.play(FadeIn(link, scale=0.6), run_time=0.5)

        # ---------- Adegan 4: judul ----------
        title = txt("Magnet dan Elektromagnetik", 52, S.TEXT, "BOLD").move_to([0, -1.0, 0])
        sub = txt("Konsep, rumus, dan contoh soal", S.SZ_BODY, S.MUTED).next_to(title, DOWN, buff=0.35)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)

        # ---------- Transisi: judul mengecil menjadi lencana [U | S] ----------
        badge = u_s_badge().to_corner(UR, buff=0.6)
        self.play(
            title.animate.scale(0.15).move_to(badge).set_opacity(0),
            FadeIn(badge),
            FadeOut(sub), FadeOut(left), FadeOut(right), FadeOut(link),
            run_time=1.1,
        )
        self.pad_to(S.SCENE_DURATIONS[SCENE_ID])

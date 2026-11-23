"""Scene 08 — Rangkuman konsep dan latihan (25 d).

Narasi (rencana, disinkronkan ulang setelah voice-over final):
  0–15  "Mari rangkum. Oersted: arus menghasilkan medan magnet. Lorentz: medan magnet memberi
         gaya pada arus atau muatan. Faraday dan Lenz: perubahan fluks menghasilkan GGL yang
         melawan penyebabnya. Semuanya dipakai pada motor, generator, dan transformator."
  15–25 "Sekarang giliranmu. Jeda video, lalu coba kerjakan tiga soal latihan ini."
         (soal tetap di layar tanpa jawaban)

Titik sinkron (pad_to): 14.5 | 15.0 | 25.0

Isi mengikuti slide 11 (Rangkuman dan Latihan). Kunci jawaban TIDAK ditampilkan.
"""
import sys
import math
import pathlib

# Agar `utils` dapat diimpor saat scene dirender langsung lewat `manim`.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    VGroup, FadeIn, FadeOut, Create, Write, ReplacementTransform, LaggedStart, RoundedRectangle, Circle,
    Line, Arrow, UP, DOWN, LEFT, RIGHT, UL, UR, ORIGIN, PI,
)
from utils import style as S  # noqa: E402
from utils.components import (  # noqa: E402
    BaseScene, txt, formula, u_s_badge, bar_magnet, coil_side_view, wire_cross_section, circular_field,
)

SCENE_ID = 8


def icon_oersted():
    return VGroup(circular_field(0.62, ccw=True), wire_cross_section("out", radius=0.17))


def icon_lorentz():
    i = Arrow([-0.7, -0.25, 0], [0.7, -0.25, 0], buff=0, color=S.CURRENT, stroke_width=6,
              max_tip_length_to_length_ratio=0.25)
    f = Arrow([0, -0.25, 0], [0, 0.6, 0], buff=0, color=S.ACCENT, stroke_width=6, max_tip_length_to_length_ratio=0.3)
    return VGroup(i, f)


def icon_faraday():
    m = bar_magnet(0.9, 0.34, flipped=True, label_size=14).move_to([-0.65, 0, 0])
    c = coil_side_view(4, 0.9, 0.6).move_to([0.55, 0, 0])
    return VGroup(m, c)


def icon_apps():
    ring = Circle(radius=0.4, stroke_color=S.ACCENT, stroke_width=4)
    spokes = VGroup(*[Line(ORIGIN, 0.36 * np.array([math.cos(a), math.sin(a), 0]), stroke_color=S.ACCENT,
                           stroke_width=4) for a in (PI / 2, PI * 7 / 6, PI * 11 / 6)])
    return VGroup(ring, spokes)


def summary_card(name, color, icon, lines, cx, cy=0.75, w=3.15, h=3.5):
    box = RoundedRectangle(corner_radius=0.2, width=w, height=h, fill_color=S.CARD, fill_opacity=1,
                           stroke_color=color, stroke_width=3).move_to([cx, cy, 0])
    head = txt(name, 24, color, "BOLD").move_to([cx, cy + h / 2 - 0.45, 0])
    icon.move_to([cx, cy + 0.35, 0])
    body = VGroup(*[txt(l, 19, S.TEXT_SOFT) for l in lines]).arrange(DOWN, buff=0.06).move_to([cx, cy - h / 2 + 0.95, 0])
    return VGroup(box, head, icon, body)


def practice_card(num, stmt, dk, dt, cx, top=2.6, w=4.3, h=4.65):
    box = RoundedRectangle(corner_radius=0.2, width=w, height=h, fill_color=S.CARD, fill_opacity=1,
                           stroke_color=S.CARD_EDGE, stroke_width=2).move_to([cx, top - h / 2, 0])
    head = txt(f"Soal {num}", 28, S.ACCENT, "BOLD")
    st = VGroup(*[txt(l, 18, S.TEXT_SOFT) for l in stmt]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    dk_h = txt("Diketahui", 22, S.FIELD, "BOLD")
    dk_b = VGroup(*[formula(t, S.TEXT, 24) for t in dk]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    dt_h = txt("Ditanya", 22, S.NORTH, "BOLD")
    dt_b = formula(dt, S.TEXT, 26)
    stack = VGroup(head, st, dk_h, dk_b, dt_h, dt_b).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    stack.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.35)
    stack.align_to(box, UP).shift(DOWN * 0.3)
    return VGroup(box, stack)


class Scene08Summary(BaseScene):
    def construct(self):
        badge = u_s_badge().to_corner(UR, buff=0.6)
        self.add(badge)
        title = txt("Rangkuman", S.SZ_TITLE, S.TEXT, "BOLD").to_corner(UL, buff=0.6)
        self.play(Write(title), run_time=0.7)

        # ===================== 0–15 d : empat kartu rangkuman =====================
        xs = [-5.1, -1.7, 1.7, 5.1]
        cards = [
            summary_card("Oersted", S.CURRENT, icon_oersted(), ["Arus listrik", "menghasilkan", "medan magnet"], xs[0]),
            summary_card("Lorentz", S.ACCENT, icon_lorentz(), ["Medan magnet", "memberi gaya pada", "arus/muatan"], xs[1]),
            summary_card("Faraday–Lenz", S.FIELD, icon_faraday(), ["Perubahan fluks", "menghasilkan GGL"], xs[2]),
            summary_card("Penerapan", S.OK, icon_apps(), ["Motor, generator,", "transformator"], xs[3]),
        ]
        # diagram siklus: arus <-> medan
        n_i = RoundedRectangle(corner_radius=0.2, width=3.0, height=0.8, fill_color=S.CARD, fill_opacity=1,
                               stroke_color=S.CURRENT, stroke_width=3).move_to([-2.9, -2.65, 0])
        n_b = RoundedRectangle(corner_radius=0.2, width=3.0, height=0.8, fill_color=S.CARD, fill_opacity=1,
                               stroke_color=S.FIELD, stroke_width=3).move_to([2.9, -2.65, 0])
        t_i = txt("Arus listrik", S.SZ_BODY - 2, S.CURRENT, "BOLD").move_to(n_i)
        t_b = txt("Medan magnet", S.SZ_BODY - 2, S.FIELD, "BOLD").move_to(n_b)
        a_top = Arrow([-1.2, -2.45, 0], [1.2, -2.45, 0], buff=0, color=S.ACCENT, stroke_width=5,
                      max_tip_length_to_length_ratio=0.15)
        a_bot = Arrow([1.2, -2.85, 0], [-1.2, -2.85, 0], buff=0, color=S.ACCENT, stroke_width=5,
                      max_tip_length_to_length_ratio=0.15)
        l_top = txt("Oersted", S.SZ_LABEL + 2, S.ACCENT, "BOLD").move_to([0, -2.1, 0])
        l_bot = txt("Faraday–Lenz", S.SZ_LABEL + 2, S.ACCENT, "BOLD").move_to([0, -3.22, 0])
        cycle = VGroup(n_i, n_b, t_i, t_b, a_top, a_bot, l_top, l_bot)

        self.pad_to(1.2)
        self.play(FadeIn(cards[0]), run_time=0.8)
        self.pad_to(4.4)
        self.play(FadeIn(cards[1]), run_time=0.8)
        self.pad_to(7.8)
        self.play(FadeIn(cards[2]), run_time=0.8)
        self.pad_to(10.0)
        self.play(FadeIn(cycle), run_time=1.2)
        self.pad_to(11.8)
        self.play(FadeIn(cards[3]), run_time=0.8)
        self.pad_to(14.5)
        self.play(FadeOut(VGroup(*cards, cycle)), run_time=0.5)

        # ===================== 15–25 d : latihan =====================
        self.pad_to(15.0)
        new_title = txt("Latihan", S.SZ_TITLE, S.TEXT, "BOLD").to_corner(UL, buff=0.6)
        self.play(ReplacementTransform(title, new_title), run_time=0.6)
        p1 = practice_card(1, ["Hitung B pada jarak 2 cm", "dari kawat berarus 10 A."],
                           [r"I=10\ \mathrm{A}", r"a=2\ \mathrm{cm}=0{,}02\ \mathrm{m}"], r"B=\ ?", -4.7)
        p2 = practice_card(2, ["Kawat 0,2 m, I = 5 A,", "B = 0,4 T, θ = 30°. Hitung F."],
                           [r"L=0{,}2\ \mathrm{m}", r"I=5\ \mathrm{A}", r"B=0{,}4\ \mathrm{T}",
                            r"\theta=30^\circ"], r"F=\ ?", 0.0)
        p3 = practice_card(3, ["Trafo step-down 220 V", "menjadi 11 V, Np = 2000.", "Hitung Ns."],
                           [r"V_p=220\ \mathrm{V}", r"V_s=11\ \mathrm{V}", r"N_p=2000"], r"N_s=\ ?", 4.7)
        self.play(LaggedStart(FadeIn(p1), FadeIn(p2), FadeIn(p3), lag_ratio=0.35), run_time=1.6)
        hint = txt("Jeda video, lalu coba hitung sendiri.", S.SZ_BODY, S.MUTED).move_to([0, -3.35, 0])
        self.pad_to(17.4)
        self.play(FadeIn(hint), run_time=0.6)
        self.pad_to(S.SCENE_DURATIONS[SCENE_ID])

"""Scene 05 — Gaya Lorentz (35 d).

Narasi (rencana, disinkronkan ulang setelah voice-over final):
  0–12  "Sekarang sebaliknya: medan magnet memberi gaya pada kawat berarus atau muatan yang
         bergerak. Inilah gaya Lorentz. Besarnya F sama dengan B kali I kali L kali sin theta."
  12–23 "Arahnya ditentukan tangan kanan: ibu jari arah arus, empat jari arah medan, telapak
         tangan arah gaya. Gaya maksimum saat tegak lurus, dan nol saat sejajar."
  23–35 "Kawat 0,5 meter dengan arus 4 ampere di medan 0,2 tesla mengalami gaya 0,4 newton.
         Dua kawat sejajar searah tarik-menarik, berlawanan tolak-menolak. Penerapannya:
         motor listrik, speaker, galvanometer."

Titik sinkron (pad_to): 4.5 | 8.0 | 11.5 | 12.0 | ... | 23.0 | 35.0

Fisika:
  - I ke kanan (+x), B masuk layar (-z):  F = I L x B = x̂ x (-ẑ) = +ŷ  -> gaya ke ATAS.
  - Kaidah tangan kanan (PPT): ibu jari = I, empat jari = B, telapak = F  (palm = ibu jari x jari).
  - Dua kawat sejajar: arus searah -> tarik-menarik, berlawanan -> tolak-menolak.
"""
import sys
import math
import pathlib

# Agar `utils` dapat diimpor saat scene dirender langsung lewat `manim`.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    VGroup, FadeIn, FadeOut, Create, Write, ReplacementTransform, Transform, LaggedStart,
    ValueTracker, always_redraw, RoundedRectangle, SurroundingRectangle, Rectangle, Circle,
    Arc, Line, Arrow, DoubleArrow, Polygon, UP, DOWN, LEFT, RIGHT, UL, UR, ORIGIN, PI,
)
from utils import style as S  # noqa: E402
from utils import physics as P  # noqa: E402
from utils.components import (  # noqa: E402
    BaseScene, txt, formula, u_s_badge, labeled_arrow, field_cross, problem_card,
)

SCENE_ID = 5
FORCE = S.ACCENT

F_WIRE = P.f_wire(0.2, 4, 0.5)                       # 0,4 N
FM, FE = P.sci_notation(P.f_charge(1.6e-19, 2e6, 0.5), 1)  # ("1,6", -13)
FM = FM.replace(",", "{,}")
FW = f"{F_WIRE:.1f}".replace(".", "{,}")


def app_icon(kind):
    """Ikon geometris sederhana untuk penerapan."""
    if kind == "motor":
        ring = Circle(radius=0.22, stroke_color=S.ACCENT, stroke_width=3)
        spokes = VGroup(*[Line(ORIGIN, 0.2 * np.array([math.cos(a), math.sin(a), 0]),
                               stroke_color=S.ACCENT, stroke_width=3) for a in (PI / 2, PI * 7 / 6, PI * 11 / 6)])
        return VGroup(ring, spokes)
    if kind == "speaker":
        box = Rectangle(width=0.16, height=0.22, stroke_color=S.ACCENT, stroke_width=3).shift(LEFT * 0.14)
        cone = Polygon([-0.06, 0.11, 0], [0.2, 0.28, 0], [0.2, -0.28, 0], [-0.06, -0.11, 0],
                       stroke_color=S.ACCENT, stroke_width=3)
        return VGroup(box, cone)
    arc = Arc(radius=0.26, start_angle=0, angle=PI, stroke_color=S.ACCENT, stroke_width=3).shift(DOWN * 0.12)
    needle = Line([0, -0.12, 0], [0.13, 0.1, 0], stroke_color=S.ACCENT, stroke_width=3)
    base = Line([-0.26, -0.12, 0], [0.26, -0.12, 0], stroke_color=S.ACCENT, stroke_width=3)
    return VGroup(arc, needle, base)


class Scene05LorentzForce(BaseScene):
    def construct(self):
        badge = u_s_badge().to_corner(UR, buff=0.6)
        self.add(badge)
        title = txt("Gaya Lorentz", S.SZ_TITLE, S.TEXT, "BOLD").to_corner(UL, buff=0.6)
        self.play(Write(title), run_time=0.7)

        # ===================== 0–12 d : kawat berarus dalam medan B (masuk layar) =====================
        region = RoundedRectangle(corner_radius=0.2, width=9.4, height=4.6, fill_color=S.FIELD,
                                  fill_opacity=0.07, stroke_color=S.FIELD, stroke_width=2).move_to([0, -0.5, 0])
        crosses = VGroup(*[field_cross(0.13).move_to([x, y, 0])
                           for y in (1.3, 0.5, -0.3, -1.1, -1.9) for x in np.linspace(-4.0, 4.0, 9)])
        b_lab = VGroup(formula("B", S.FIELD, 38), txt("(masuk layar)", S.SZ_LABEL, S.FIELD)
                       ).arrange(RIGHT, buff=0.2).align_to([-4.6, 2.2, 0], UL)
        self.play(FadeIn(region), LaggedStart(*[FadeIn(c) for c in crosses], lag_ratio=0.02),
                  FadeIn(b_lab), run_time=1.8)

        y0 = -1.5
        wire = Arrow([-3.0, y0, 0], [3.0, y0, 0], buff=0, color=S.CURRENT, stroke_width=9,
                     max_tip_length_to_length_ratio=0.12)
        i_lab = formula("I", S.CURRENT, 44).move_to([-3.35, y0, 0])
        self.play(Create(wire), FadeIn(i_lab), run_time=1.0)
        self.pad_to(4.5)

        f_arrow = labeled_arrow([0, y0, 0], [0, y0 + 1.3, 0], "F", FORCE, label_dir=RIGHT, size=34)
        mover = VGroup(wire, i_lab, f_arrow)
        self.play(FadeIn(f_arrow), run_time=0.6)
        self.play(mover.animate.shift(UP * 1.0), run_time=1.4)
        self.pad_to(8.0)
        f_form = formula(r"F=B\,I\,L\sin\theta", S.TEXT, 44).move_to([2.2, 3.15, 0])
        self.play(Write(f_form), run_time=1.2)
        self.pad_to(11.5)
        self.play(FadeOut(VGroup(region, crosses, b_lab, mover)), run_time=0.5)

        # ===================== 12–23 d : tangan kanan + pengaruh sudut θ =====================
        self.pad_to(12.0)
        O = np.array([-4.2, -0.7, 0])
        bx = field_cross(0.3, S.FIELD, 3.5).move_to(O)
        arr_i = Arrow(O + RIGHT * 0.45, O + RIGHT * 2.7, buff=0, color=S.CURRENT, stroke_width=7)
        arr_f = Arrow(O + UP * 0.45, O + UP * 2.0, buff=0, color=FORCE, stroke_width=7)
        l_i = formula("I", S.CURRENT, 44).next_to(arr_i.get_end(), DOWN, buff=0.12)
        l_f = formula("F", FORCE, 44).next_to(arr_f.get_end(), LEFT, buff=0.15)
        l_b = formula("B", S.FIELD, 40).next_to(bx, DOWN + LEFT, buff=0.05)
        legend = VGroup(
            txt("ibu jari → arah arus (I)", S.SZ_LABEL + 2, S.CURRENT, "BOLD"),
            txt("empat jari → arah medan (B, masuk layar)", S.SZ_LABEL + 2, S.FIELD, "BOLD"),
            txt("telapak tangan → arah gaya (F)", S.SZ_LABEL + 2, FORCE, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).align_to([-6.8, -1.6, 0], UL)
        head_rule = txt("Kaidah tangan kanan", S.SZ_BODY, S.ACCENT, "BOLD").align_to([-6.8, 2.3, 0], UL)
        self.play(FadeIn(head_rule), FadeIn(bx), FadeIn(l_b), run_time=0.6)
        self.play(Create(arr_i), FadeIn(l_i), run_time=0.8)
        self.play(Create(arr_f), FadeIn(l_f), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(x) for x in legend], lag_ratio=0.6), run_time=1.8)

        # sudut θ: B di bidang layar (kanan), kawat berputar dari 90° ke 0°
        self.pad_to(16.5)
        pv = np.array([2.1, -0.9, 0])
        head_ang = txt("Pengaruh sudut θ", S.SZ_BODY, S.ACCENT, "BOLD").align_to([1.0, 2.3, 0], UL)
        tr = ValueTracker(90)
        rad = lambda: math.radians(tr.get_value())
        b_vec = Arrow(pv, pv + RIGHT * 3.0, buff=0, color=S.FIELD, stroke_width=6)
        b_vl = formula("B", S.FIELD, 40).next_to(b_vec.get_end(), UP, buff=0.1)
        w_vec = always_redraw(lambda: Arrow(pv, pv + 2.4 * np.array([math.cos(rad()), math.sin(rad()), 0]),
                                            buff=0, color=S.CURRENT, stroke_width=7))
        arc = always_redraw(lambda: Arc(radius=0.9, start_angle=0, angle=max(rad(), 1e-3), arc_center=pv,
                                        color=S.ACCENT, stroke_width=4))
        th_lab = always_redraw(lambda: formula(r"\theta", S.ACCENT, 34).move_to(
            pv + 1.3 * np.array([math.cos(max(rad(), 0.35) / 2), math.sin(max(rad(), 0.35) / 2), 0])))
        i_wl = always_redraw(lambda: formula("I", S.CURRENT, 40).move_to(
            pv + 2.85 * np.array([math.cos(rad()), math.sin(rad()), 0]) + np.array([-0.05, 0.0, 0])))
        bar_base = np.array([6.3, -2.0, 0])
        bar = always_redraw(lambda: Rectangle(width=0.5, height=max(0.03, 2.8 * math.sin(rad())),
                                              fill_color=FORCE, fill_opacity=1, stroke_width=0
                                              ).move_to(bar_base + UP * max(0.03, 2.8 * math.sin(rad())) / 2))
        bar_lab = formula("F", FORCE, 40).move_to(bar_base + DOWN * 0.4)
        self.play(FadeIn(head_ang), Create(b_vec), FadeIn(b_vl), FadeIn(w_vec), FadeIn(arc), FadeIn(th_lab),
                  FadeIn(i_wl), FadeIn(bar), FadeIn(bar_lab), run_time=1.0)
        cap1 = txt("θ = 90°: F maksimum", S.SZ_BODY, S.TEXT_SOFT, "BOLD").align_to([1.0, -2.8, 0], UL)
        self.play(FadeIn(cap1), run_time=0.5)
        self.pad_to(18.5)
        self.play(tr.animate.set_value(0), run_time=2.6)
        cap2 = txt("θ = 0°: F = 0 (sejajar)", S.SZ_BODY, S.TEXT_SOFT, "BOLD").align_to([1.0, -2.8, 0], UL)
        self.play(ReplacementTransform(cap1, cap2), run_time=0.5)
        self.pad_to(22.5)
        for m in (w_vec, arc, th_lab, i_wl, bar):
            m.clear_updaters()
        self.play(FadeOut(VGroup(head_rule, bx, l_b, arr_i, arr_f, l_i, l_f, legend, head_ang, b_vec, b_vl,
                                 w_vec, arc, th_lab, i_wl, bar, bar_lab, cap2, f_form)), run_time=0.5)

        # ===================== 23–35 d : contoh soal, kawat sejajar, penerapan =====================
        self.pad_to(23.0)
        top = 2.45
        card_w = 4.15
        # kartu 1: kawat berarus
        c1 = problem_card("Contoh: kawat", S.ACCENT, [
            formula(r"L=0{,}5\ \mathrm{m},\ \ I=4\ \mathrm{A}", S.TEXT, 26),
            formula(r"B=0{,}2\ \mathrm{T},\ \ \theta=90^\circ", S.TEXT, 26),
            formula(r"F=B\,I\,L\sin90^\circ", S.TEXT, 28),
            formula(r"F=0{,}2\times4\times0{,}5\times1", S.TEXT, 28),
            formula(rf"F={FW}\ \mathrm{{N}}", S.ACCENT, 38),
        ], card_w, 22).align_to([-6.9, top, 0], UL)
        # kartu 2: muatan bergerak (elektron)
        c2 = problem_card("Elektron bergerak", S.ACCENT, [
            formula(r"q=1{,}6\times10^{-19}\ \mathrm{C}", S.TEXT, 26),
            formula(r"v=2\times10^{6}\ \mathrm{m/s}", S.TEXT, 26),
            formula(r"B=0{,}5\ \mathrm{T},\ \ \theta=90^\circ", S.TEXT, 26),
            formula(r"F=q\,v\,B", S.TEXT, 28),
            formula(rf"F={FM}\times10^{{{FE}}}\ \mathrm{{N}}", S.ACCENT, 34),
        ], card_w, 22).align_to([-2.5, top, 0], UL)
        self.play(FadeIn(c1[0]), FadeIn(c1[1]), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(x) for x in c1[2]], lag_ratio=0.6), run_time=1.5)
        res1 = SurroundingRectangle(c1[2][4], color=S.ACCENT, buff=0.12, corner_radius=0.1, stroke_width=3)
        self.play(Create(res1), run_time=0.4)
        self.pad_to(25.5)
        self.play(FadeIn(c2[0]), FadeIn(c2[1]), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(x) for x in c2[2]], lag_ratio=0.5), run_time=1.3)
        res2 = SurroundingRectangle(c2[2][4], color=S.ACCENT, buff=0.12, corner_radius=0.1, stroke_width=3)
        self.play(Create(res2), run_time=0.4)

        # dua kawat sejajar
        self.pad_to(28.0)
        px = 4.4
        panel = RoundedRectangle(corner_radius=0.16, width=5.0, height=3.55, fill_color=S.CARD, fill_opacity=1,
                                 stroke_color=S.CARD_EDGE, stroke_width=2).move_to([px, top - 3.55 / 2, 0])
        x1, x2 = px - 0.9, px + 0.9
        w1 = Arrow([x1, 0.0, 0], [x1, 1.5, 0], buff=0, color=S.CURRENT, stroke_width=7)
        w2 = Arrow([x2, 0.0, 0], [x2, 1.5, 0], buff=0, color=S.CURRENT, stroke_width=7)
        i1 = formula("I_1", S.CURRENT, 30).next_to(w1, UP, buff=0.1)
        i2 = formula("I_2", S.CURRENT, 30).next_to(w2, UP, buff=0.1)
        f1 = labeled_arrow([x1 + 0.15, 0.75, 0], [x1 + 0.7, 0.75, 0], "F", FORCE, label_dir=UP, size=24)
        f2 = labeled_arrow([x2 - 0.15, 0.75, 0], [x2 - 0.7, 0.75, 0], "F", FORCE, label_dir=UP, size=24)
        dist = DoubleArrow([x1, -0.3, 0], [x2, -0.3, 0], buff=0, color=S.MUTED, stroke_width=2, tip_length=0.12)
        a_lab = formula("a", S.TEXT_SOFT, 26).next_to(dist, DOWN, buff=0.05)
        cap_a = txt("searah: tarik-menarik", S.SZ_LABEL, S.OK, "BOLD").move_to([px, -0.85, 0])
        self.play(FadeIn(panel), FadeIn(w1), FadeIn(w2), FadeIn(i1), FadeIn(i2), FadeIn(dist), FadeIn(a_lab),
                  run_time=0.8)
        self.play(FadeIn(f1), FadeIn(f2), FadeIn(cap_a), run_time=0.6)
        self.pad_to(30.4)
        # arus I2 dibalik -> tolak-menolak
        w2b = Arrow([x2, 1.5, 0], [x2, 0.0, 0], buff=0, color=S.CURRENT, stroke_width=7)
        f1b = labeled_arrow([x1 - 0.15, 0.75, 0], [x1 - 0.7, 0.75, 0], "F", FORCE, label_dir=UP, size=24)
        f2b = labeled_arrow([x2 + 0.15, 0.75, 0], [x2 + 0.7, 0.75, 0], "F", FORCE, label_dir=UP, size=24)
        cap_b = txt("berlawanan: tolak-menolak", S.SZ_LABEL, S.NORTH, "BOLD").move_to([px, -0.85, 0])
        self.play(ReplacementTransform(w2, w2b), ReplacementTransform(f1, f1b), ReplacementTransform(f2, f2b),
                  ReplacementTransform(cap_a, cap_b), run_time=1.0)
        f_par = formula(r"\frac{F}{L}=\frac{\mu_0 I_1 I_2}{2\pi a}", S.TEXT, 34).move_to([px, -1.95, 0])
        self.play(Write(f_par), run_time=0.9)

        # penerapan
        self.pad_to(32.6)
        pills = VGroup()
        for kind, name, cx in (("motor", "motor listrik", -4.5), ("speaker", "speaker", 0.0),
                               ("galvano", "galvanometer", 4.5)):
            box = RoundedRectangle(corner_radius=0.3, width=4.0, height=0.8, fill_color=S.CARD, fill_opacity=1,
                                   stroke_color=S.CARD_EDGE, stroke_width=2).move_to([cx, -3.2, 0])
            ic = app_icon(kind).move_to([cx - 1.55, -3.2, 0])
            lb = txt(name, S.SZ_BODY - 2, S.TEXT, "BOLD").move_to([cx + 0.45, -3.2, 0])
            pills.add(VGroup(box, ic, lb))
        self.play(LaggedStart(*[FadeIn(p) for p in pills], lag_ratio=0.5), run_time=1.6)
        self.pad_to(S.SCENE_DURATIONS[SCENE_ID])

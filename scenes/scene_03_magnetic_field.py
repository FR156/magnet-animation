"""Scene 03 — Medan magnet dan Oersted (35 d).

Narasi (rencana, disinkronkan ulang setelah voice-over final):
  0–12  "Ruang di sekitar magnet tempat gaya magnet terasa disebut medan magnet. Di luar
         magnet, garis gayanya keluar dari kutub utara dan masuk ke kutub selatan;
         makin rapat, makin kuat."
  12–24 "Tapi magnet bukan satu-satunya sumber medan. Oersted menemukan bahwa arus listrik
         juga menimbulkan medan magnet. Arahnya mengikuti kaidah tangan kanan: ibu jari arah
         arus, lipatan jari arah medan."
  24–35 "Besar induksi magnet bergantung pada bentuk penghantarnya: kawat lurus, lingkaran,
         atau solenoida, masing-masing dengan rumusnya sendiri."

Titik sinkron (pad_to): 12.0 | 24.0 | 35.0

Fisika yang divisualisasikan:
  - Di luar magnet garis medan: U -> S; di dalam magnet: S -> U (loop tertutup).
  - Arus ⊙ (keluar layar) -> B berlawanan arah jarum jam; ujung merah (U) jarum kompas
    searah B.
  - Kaidah tangan kanan (Oersted): ibu jari = arus, lipatan jari = B. Untuk arus ke atas,
    dilihat dari atas, B berlawanan arah jarum jam (busur depan ke kanan, busur belakang ke kiri).
"""
import sys
import math
import pathlib

# Agar `utils` dapat diimpor saat scene dirender langsung lewat `manim`.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from manim import (  # noqa: E402
    VGroup, FadeIn, FadeOut, Create, Write, Indicate, MoveAlongPath, ReplacementTransform,
    Transform, RoundedRectangle, Circle, Dot, Line, DashedLine, DoubleArrow, Arrow, Polygon,
    ParametricFunction, DashedVMobject, rate_functions,
    UP, DOWN, LEFT, RIGHT, UL, UR, PI,
)
import numpy as np  # noqa: E402
from utils import style as S  # noqa: E402
from utils.components import (  # noqa: E402
    BaseScene, txt, formula, u_s_badge, bar_magnet, magnet_field_lines,
    wire_cross_section, circular_field, coil_side_view, tip_on,
)

SCENE_ID = 3


def stacked(*lines, size=S.SZ_LABEL, color=S.TEXT_SOFT, weight="NORMAL"):
    """Beberapa baris teks rata kiri."""
    return VGroup(*[txt(l, size, color, weight) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)


def compass_needle(length=0.5, width=0.15):
    """Jarum kompas: ujung merah (U) = arah medan; ekor biru (S). Default menghadap +x."""
    h = length / 2
    red = Polygon([h, 0, 0], [0, width / 2, 0], [0, -width / 2, 0],
                  fill_color=S.NORTH, fill_opacity=1, stroke_width=0)
    blue = Polygon([-h, 0, 0], [0, width / 2, 0], [0, -width / 2, 0],
                   fill_color=S.SOUTH, fill_opacity=1, stroke_width=0)
    return VGroup(red, blue)


# ----------------------------- diagram mini untuk kartu rumus -----------------------------
def diagram_wire():
    wire = Arrow([0, -0.85, 0], [0, 0.85, 0], buff=0, color=S.CURRENT, stroke_width=S.STROKE,
                 max_tip_length_to_length_ratio=0.2)
    pt = Dot([1.15, 0, 0], radius=0.08, color=S.FIELD)
    link = DashedLine([0, 0, 0], [1.15, 0, 0], color=S.MUTED, stroke_width=2)
    a = formula("a", S.TEXT_SOFT, 26).move_to([0.58, 0.22, 0])
    i = formula("I", S.CURRENT, 28).move_to([-0.3, 0.7, 0])
    return VGroup(link, wire, pt, a, i)


def diagram_loop():
    ring = Circle(radius=0.72, stroke_color=S.CURRENT, stroke_width=S.STROKE)
    tip = tip_on(ring, 0.25, S.CURRENT, 0.15)  # tanda arah arus berlawanan jarum jam (di puncak)
    ctr = Dot([0, 0, 0], radius=0.08, color=S.FIELD)
    rad = Line([0, 0, 0], [0.72, 0, 0], color=S.MUTED, stroke_width=2)
    a = formula("a", S.TEXT_SOFT, 26).move_to([0.38, 0.2, 0])
    i = formula("I", S.CURRENT, 28).move_to([-0.95, 0.3, 0])
    return VGroup(ring, tip, rad, ctr, a, i)


def diagram_solenoid(point="center"):
    length = 2.0
    axis = DashedLine([-length / 2 - 0.25, 0, 0], [length / 2 + 0.25, 0, 0], color=S.FIELD, stroke_width=2.5)
    coil = coil_side_view(6, length, 0.9)
    x = 0 if point == "center" else length / 2
    pt = Dot([x, 0, 0], radius=0.09, color=S.ACCENT)
    span = DoubleArrow([-length / 2, -0.7, 0], [length / 2, -0.7, 0], buff=0, color=S.MUTED,
                       stroke_width=2, tip_length=0.12)
    lab = formula("L", S.TEXT_SOFT, 26).move_to([0, -0.95, 0])
    return VGroup(axis, coil, pt, span, lab)


def formula_card(name, tex, diagram, center):
    box = RoundedRectangle(corner_radius=0.18, width=6.4, height=2.4, fill_color=S.CARD,
                           fill_opacity=1, stroke_color=S.CARD_EDGE, stroke_width=2).move_to(center)
    nm = txt(name, S.SZ_LABEL + 2, S.ACCENT, "BOLD")
    nm.move_to(center).align_to(box, LEFT).shift(RIGHT * 0.35)
    nm.set_y(center[1] + 0.9)
    diagram.move_to([center[0] - 1.55, center[1] - 0.2, 0])
    f = formula(tex, S.TEXT, 38).move_to([center[0] + 1.7, center[1] - 0.25, 0])
    return VGroup(box, nm), diagram, f


class Scene03MagneticField(BaseScene):
    def construct(self):
        badge = u_s_badge().to_corner(UR, buff=0.6)
        self.add(badge)  # kontinuitas dari scene sebelumnya
        title = txt("Medan Magnet", S.SZ_TITLE, S.TEXT, "BOLD").to_corner(UL, buff=0.6)

        # ===================== 0–12 d : garis medan magnet batang =====================
        self.play(Write(title), run_time=0.7)
        mc = np.array([0, -0.1, 0])
        magnet = bar_magnet().move_to(mc)
        lines = magnet_field_lines().move_to(mc)
        self.play(FadeIn(magnet), run_time=0.5)
        self.play(Create(lines), run_time=3.5)
        self.pad_to(5.5)

        # titik bergerak: di luar U -> S, di dalam S -> U
        outer, inner = lines[4], lines[12]  # kurva luar (atas) dan garis dalam (y>0)
        dot = Dot(outer.point_from_proportion(0), radius=0.1, color=S.TEXT)
        self.play(FadeIn(dot), run_time=0.2)
        self.play(MoveAlongPath(dot, outer), run_time=2.4, rate_func=rate_functions.linear)
        self.play(dot.animate.move_to(inner.get_start()), run_time=0.3)
        self.play(MoveAlongPath(dot, inner), run_time=0.8, rate_func=rate_functions.linear)
        self.play(FadeOut(dot), run_time=0.2)

        # rapat = kuat (dekat kutub), renggang = lemah (jauh)
        ring_strong = DashedVMobject(Circle(radius=0.55, stroke_color=S.ACCENT, stroke_width=3)
                                     .move_to([-1.75, -0.1, 0]), num_dashes=16)
        t_strong = stacked("garis rapat:", "medan kuat", size=S.SZ_BODY, color=S.ACCENT, weight="BOLD")
        t_strong.move_to([-4.7, -0.1, 0])
        c_strong = Line([-3.55, -0.1, 0], [-2.35, -0.1, 0], color=S.ACCENT, stroke_width=2)
        weak_pt = (outer.point_from_proportion(0.8) + lines[8].point_from_proportion(0.8)) / 2
        ring_weak = DashedVMobject(Circle(radius=0.42, stroke_color=S.ACCENT, stroke_width=3)
                                   .move_to(weak_pt), num_dashes=14)
        t_weak = stacked("garis renggang:", "medan lemah", size=S.SZ_BODY, color=S.ACCENT, weight="BOLD")
        t_weak.move_to([5.2, 1.9, 0])
        c_weak = Line(weak_pt + RIGHT * 0.42, t_weak.get_left() + LEFT * 0.12, color=S.ACCENT, stroke_width=2)
        callouts = VGroup(ring_strong, t_strong, c_strong, ring_weak, t_weak, c_weak)
        self.play(FadeIn(callouts), run_time=0.7)
        self.pad_to(11.5)
        self.play(FadeOut(VGroup(magnet, lines, callouts)), run_time=0.5)

        # ===================== 12–24 d : percobaan Oersted + tangan kanan =====================
        self.pad_to(12.0)
        C = np.array([-3.6, -0.1, 0])
        R = 1.15   # radius jarum kompas
        RR = 1.85  # radius garis medan
        head_l = txt("Percobaan Oersted", S.SZ_BODY, S.ACCENT, "BOLD").move_to([C[0], 2.55, 0])
        wire = wire_cross_section("out").move_to(C)
        angles = [math.radians(22.5 + 45 * k) for k in range(8)]
        needles = []
        for th in angles:
            n = compass_needle()
            n.rotate(PI / 2)  # arus mati: semua jarum menunjuk ke atas
            n.move_to(C + R * np.array([math.cos(th), math.sin(th), 0]))
            needles.append(n)
        status = txt("arus mati", S.SZ_BODY, S.MUTED).move_to([C[0], -2.45, 0])
        self.play(FadeIn(head_l), FadeIn(wire), *[FadeIn(n) for n in needles], FadeIn(status), run_time=0.8)
        self.pad_to(14.0)

        # arus dinyalakan: jarum berputar mengikuti garis medan (berlawanan arah jarum jam)
        ring = circular_field(RR, ccw=True).move_to(C)
        status_on = txt("arus mengalir (keluar layar)", S.SZ_BODY, S.CURRENT, "BOLD").move_to([C[0], -2.45, 0])
        rot = []
        for n, th in zip(needles, angles):
            d = (math.degrees(th) + 180) % 360 - 180  # putaran terpendek dari "atas" ke garis singgung
            rot.append(n.animate.rotate(math.radians(d)))
        self.play(Indicate(wire, color=S.CURRENT, scale_factor=1.3), ReplacementTransform(status, status_on),
                  run_time=0.8)
        self.play(*rot, Create(ring), run_time=1.6)
        b_lab = formula("B", S.FIELD, 44).move_to(C + np.array([RR + 0.5, 0.6, 0]))
        i_lab = formula("I", S.CURRENT, 44).move_to(C + np.array([0, 0.62, 0]))
        legend = txt("ujung merah jarum = arah medan B", S.SZ_LABEL - 2, S.MUTED).move_to([C[0], -2.95, 0])
        self.play(FadeIn(b_lab), FadeIn(i_lab), FadeIn(legend), run_time=0.5)
        self.pad_to(17.5)

        # kaidah tangan kanan (skema): ibu jari = arus, lipatan jari = B
        cx, cy, r, sq = 3.0, -0.1, 1.25, 0.32
        head_r = txt("Kaidah tangan kanan", S.SZ_BODY, S.ACCENT, "BOLD").move_to([cx + 0.7, 2.55, 0])

        def ell(t_a, t_b):
            return ParametricFunction(
                lambda t: np.array([cx + r * math.cos(t), cy + r * sq * math.sin(t), 0]),
                t_range=[t_a, t_b], color=S.FIELD, stroke_width=S.STROKE)

        back = ell(0, PI)        # setengah belakang: kanan -> kiri (putus-putus)
        front = ell(PI, 2 * PI)  # setengah depan: kiri -> kanan (utuh)
        back_dashed = DashedVMobject(back, num_dashes=14)
        tip_back = tip_on(back, 0.5, S.FIELD, 0.17)
        tip_front = tip_on(front, 0.5, S.FIELD, 0.17)
        thumb = Arrow([cx, cy - 1.5, 0], [cx, cy + 1.7, 0], buff=0, color=S.CURRENT, stroke_width=7,
                      max_tip_length_to_length_ratio=0.12)
        i_lab2 = formula("I", S.CURRENT, 44).move_to([cx - 0.4, cy + 1.55, 0])
        b_lab2 = formula("B", S.FIELD, 44).move_to([cx + r + 0.35, cy - 0.45, 0])
        cap_i = stacked("ibu jari:", "arah arus (I)", size=S.SZ_LABEL, color=S.CURRENT, weight="BOLD")
        cap_i.move_to([cx + 1.75, cy + 1.35, 0])
        cap_b = stacked("lipatan jari:", "arah medan (B)", size=S.SZ_LABEL, color=S.FIELD, weight="BOLD")
        cap_b.move_to([cx + 2.3, cy - 1.1, 0])

        self.play(FadeIn(head_r), run_time=0.5)
        self.play(Create(back_dashed), FadeIn(tip_back), Create(thumb), run_time=0.8)
        self.play(Create(front), FadeIn(tip_front), run_time=0.8)
        self.play(FadeIn(i_lab2), FadeIn(b_lab2), FadeIn(cap_i), FadeIn(cap_b), run_time=0.7)
        self.pad_to(23.5)
        right_hand = VGroup(head_r, back_dashed, tip_back, thumb, front, tip_front, i_lab2, b_lab2, cap_i, cap_b)
        left_all = VGroup(head_l, wire, *needles, status_on, ring, b_lab, i_lab, legend)
        self.play(FadeOut(right_hand), FadeOut(left_all), run_time=0.5)

        # ===================== 24–35 d : rumus induksi magnet =====================
        self.pad_to(24.0)
        new_title = txt("Induksi Magnet", S.SZ_TITLE, S.TEXT, "BOLD").to_corner(UL, buff=0.6)
        self.play(ReplacementTransform(title, new_title), run_time=0.6)

        specs = [
            ("Kawat lurus", r"B=\frac{\mu_0 I}{2\pi a}", diagram_wire(), [-3.7, 1.45, 0], 24.8),
            ("Pusat lingkaran", r"B=\frac{\mu_0 I N}{2a}", diagram_loop(), [3.7, 1.45, 0], 26.6),
            ("Solenoida (tengah)", r"B=\frac{\mu_0 I N}{L}", diagram_solenoid("center"), [-3.7, -1.25, 0], 28.4),
            ("Solenoida (ujung)", r"B=\frac{\mu_0 I N}{2L}", diagram_solenoid("end"), [3.7, -1.25, 0], 30.2),
        ]
        for name, tex, dg, ctr, t0 in specs:
            self.pad_to(t0)
            head, dg, f = formula_card(name, tex, dg, np.array(ctr))
            self.play(FadeIn(head), FadeIn(dg), run_time=0.6)
            self.play(Write(f), run_time=0.8)

        # kartu kecil toroida di akhir
        self.pad_to(32.2)
        pill = RoundedRectangle(corner_radius=0.25, width=5.6, height=0.85, fill_color=S.CARD,
                                fill_opacity=1, stroke_color=S.CARD_EDGE, stroke_width=2).move_to([0, -3.2, 0])
        t_name = txt("Toroida", S.SZ_LABEL, S.ACCENT, "BOLD").move_to(pill).shift(LEFT * 1.6)
        t_form = formula(r"B=\frac{\mu_0 I N}{2\pi r}", S.TEXT, 26).move_to(pill).shift(RIGHT * 0.9)
        self.play(FadeIn(VGroup(pill, t_name, t_form)), run_time=0.7)
        self.pad_to(S.SCENE_DURATIONS[SCENE_ID])

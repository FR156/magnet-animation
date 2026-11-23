"""Scene 04 — Perhitungan induksi magnet (30 d).

Narasi (rencana, disinkronkan ulang setelah voice-over final):
  0–17  "Coba hitung. Kawat lurus dialiri arus 5 ampere; berapa induksi magnetnya pada jarak
         10 sentimeter, atau 0,1 meter? Dengan rumus mu nol I per dua pi a, pi-nya saling
         habis, hasilnya satu kali sepuluh pangkat min lima tesla."
  17–30 "Pada solenoida dengan 500 lilitan, panjang 25 sentimeter, dan arus 2 ampere, medan di
         tengahnya mu nol I N per L, yaitu sekitar lima kali sepuluh pangkat min tiga tesla."

Titik sinkron (pad_to): 8.0 | 10.0 | 12.5 | 14.0 | 17.0 | 22.5 | 24.5 | 27.0 | 30.0

Semua angka berasal dari utils/physics.py (dicek oleh tests/test_physics.py).

Fisika diagram:
  - Soal 1 (tampak atas): arus ⊙ (keluar layar) -> B berlawanan arah jarum jam; di titik P
    (sisi kanan kawat) B menunjuk ke atas.
  - Soal 2: arus ke bawah di sisi depan lilitan -> (tangan kanan) B menuju kanan.
"""
import sys
import pathlib

# Agar `utils` dapat diimpor saat scene dirender langsung lewat `manim`.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    VGroup, FadeIn, FadeOut, Create, Write, Indicate, ReplacementTransform, LaggedStart,
    RoundedRectangle, SurroundingRectangle, Dot, Line, DashedLine, DoubleArrow, Arrow,
    UP, DOWN, LEFT, RIGHT, UL, UR, DL,
)
from utils import style as S  # noqa: E402
from utils import physics as P  # noqa: E402
from utils.components import (  # noqa: E402
    BaseScene, txt, formula, u_s_badge, wire_cross_section, circular_field,
    labeled_arrow, solenoid_front,
)

SCENE_ID = 4

# ---- data soal (sesuai slide 4) ----
I1, A1 = 5, 0.1                  # soal 1: kawat lurus
N2, L2, I2 = 500, 0.25, 2        # soal 2: solenoida
B1 = P.b_wire(I1, A1)
B2 = P.b_solenoid_center(I2, N2, L2)
M1, E1 = P.sci_notation(B1, 0)   # ("1", -5)
M2, E2 = P.sci_notation(B2, 1)   # ("5,0", -3)
# Koma desimal di mode matematika LaTeX harus ditulis {,} agar tidak diberi spasi.
M1, M2 = M1.replace(",", "{,}"), M2.replace(",", "{,}")


def make_card(title, color, items, width, title_size=24):
    """Kartu bergaya PPT: judul berwarna + daftar baris (mobject)."""
    head = txt(title, title_size, color, "BOLD")
    body = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    box = RoundedRectangle(corner_radius=0.16, width=width, height=content.height + 0.5,
                           fill_color=S.CARD, fill_opacity=1, stroke_color=S.CARD_EDGE, stroke_width=2)
    content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.3)
    return box, head, body


def solution_card(center, width, height):
    box = RoundedRectangle(corner_radius=0.16, width=width, height=height, fill_color=S.CARD,
                           fill_opacity=1, stroke_color=S.CARD_EDGE, stroke_width=2).move_to(center)
    head = txt("Penyelesaian", 24, S.OK, "BOLD")
    head.align_to(box, UL).shift(RIGHT * 0.3 + DOWN * 0.22)
    return box, head


def pi_glyphs(mathtex, size):
    """Cari glyph π di dalam rumus dengan mencocokkan bentuknya terhadap π tunggal."""
    ref = formula(r"\pi", S.TEXT, size)[0][0]
    return [g for g in mathtex[0]
            if len(g.points) == len(ref.points) and abs(g.width - ref.width) < 0.02]


def strike(glyph):
    """Garis coret diagonal (merah) melintasi sebuah glyph."""
    return Line(glyph.get_corner(DL) + DL * 0.07, glyph.get_corner(UR) + UR * 0.07,
                color=S.NORTH, stroke_width=5)


class Scene04MagneticInduction(BaseScene):
    def construct(self):
        badge = u_s_badge().to_corner(UR, buff=0.6)
        self.add(badge)
        title = txt("Contoh Soal: Induksi Magnet", S.SZ_TITLE, S.TEXT, "BOLD").to_corner(UL, buff=0.6)
        self.play(Write(title), run_time=0.7)

        # ====================== SOAL 1 : kawat lurus (tata letak layar penuh) ======================
        h1 = txt("Contoh Soal 1", 30, S.ACCENT, "BOLD").align_to([-6.6, 2.6, 0], UL)
        q1 = txt("Kawat lurus dialiri arus 5 A. Hitung induksi magnet pada jarak 10 cm dari kawat.",
                 S.SZ_LABEL, S.TEXT_SOFT).align_to([-6.6, 2.0, 0], UL)
        self.play(FadeIn(h1), FadeIn(q1), run_time=0.8)

        dk_items = [formula(r"I=5\ \mathrm{A}", S.TEXT, 26),
                    formula(r"a=10\ \mathrm{cm}=0{,}1\ \mathrm{m}", S.TEXT, 26),
                    formula(r"\mu_0=4\pi\times10^{-7}\ \mathrm{Wb/A{\cdot}m}", S.TEXT, 26)]
        dk_box, dk_head, dk_body = make_card("Diketahui", S.FIELD, dk_items, 4.6)
        dk1 = VGroup(dk_box, dk_head, dk_body).align_to([-6.9, 1.6, 0], UL)
        dt_box, dt_head, dt_body = make_card("Ditanya", S.NORTH, [formula(r"B=\ ?", S.TEXT, 30)], 4.6)
        dt1 = VGroup(dt_box, dt_head, dt_body).align_to([-6.9, dk1.get_bottom()[1] - 0.2, 0], UL)

        # diagram tampak atas: kawat ⊙, lingkaran medan, titik P berjarak a
        D = np.array([2.45, 0.55, 0])
        R = 1.15
        wire = wire_cross_section("out", radius=0.22).move_to(D)
        ring = circular_field(R, ccw=True).move_to(D)
        P_pt = D + np.array([R, 0, 0])
        dot_p = Dot(P_pt, radius=0.08, color=S.TEXT)
        lab_p = txt("P", S.SZ_LABEL, S.TEXT, "BOLD").next_to(dot_p, DOWN, buff=0.12).shift(RIGHT * 0.12)
        radius_ln = DashedLine(D + RIGHT * 0.22, P_pt, color=S.MUTED, stroke_width=2)
        a_lab = formula(r"a=0{,}1\ \mathrm{m}", S.TEXT_SOFT, 22).move_to(D + np.array([0.5, -0.42, 0]))
        i_lab = formula(r"I=5\ \mathrm{A}", S.CURRENT, 28).move_to(D + np.array([-1.95, 0.0, 0]))
        b_arrow = labeled_arrow(P_pt, P_pt + UP * 0.8, "B", S.FIELD, label_dir=RIGHT)
        cap = txt("tampak atas, arus keluar layar", 18, S.MUTED).move_to(D + np.array([0, -1.5, 0]))
        diagram1 = VGroup(ring, radius_ln, wire, dot_p, lab_p, a_lab, i_lab, b_arrow, cap)

        # kartu penyelesaian
        sc = np.array([2.45, -2.5, 0])
        sol_box, sol_head = solution_card(sc, 8.9, 2.4)
        fc = sc + np.array([0.2, -0.2, 0])

        self.play(FadeIn(dk_box), FadeIn(dk_head), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(x) for x in dk_body], lag_ratio=0.7), run_time=1.6)
        self.play(FadeIn(dt1), run_time=0.6)
        self.play(Create(ring), FadeIn(wire), FadeIn(radius_ln), run_time=1.0)
        self.play(FadeIn(dot_p), FadeIn(lab_p), FadeIn(a_lab), FadeIn(i_lab), FadeIn(b_arrow), FadeIn(cap),
                  run_time=0.8)
        self.pad_to(6.5)
        self.play(FadeIn(sol_box), FadeIn(sol_head), run_time=0.5)

        # rumus -> substitusi -> coret π -> hasil
        f_a = formula(r"B=\frac{\mu_0 I}{2\pi a}", S.TEXT, 46).move_to(fc)
        self.pad_to(8.0)
        self.play(Write(f_a), run_time=1.0)
        self.pad_to(10.0)
        f_b = formula(r"B=\frac{4\pi\times10^{-7}\times5}{2\pi\times0{,}1}", S.TEXT, 40).move_to(fc)
        self.play(ReplacementTransform(f_a, f_b), Indicate(i_lab, color=S.ACCENT), Indicate(a_lab, color=S.ACCENT),
                  run_time=1.2)
        self.pad_to(12.5)
        slashes = VGroup(*[strike(g) for g in pi_glyphs(f_b, 40)])
        self.play(Create(slashes), run_time=0.7)
        self.pad_to(14.0)
        f_res = formula(rf"B={M1}\times10^{{{E1}}}\ \mathrm{{T}}", S.ACCENT, 48).move_to(fc)
        res_box = SurroundingRectangle(f_res, color=S.ACCENT, buff=0.2, corner_radius=0.12, stroke_width=3)
        self.play(ReplacementTransform(f_b, f_res), FadeOut(slashes), run_time=1.0)
        self.play(Create(res_box), run_time=0.5)

        # ====================== transisi: Soal 1 mengecil ke kiri ======================
        self.pad_to(17.0)
        s1 = VGroup(h1, q1, dk1, dt1, diagram1, sol_box, sol_head, f_res, res_box)
        self.play(s1.animate.scale(0.48).move_to([-3.6, 0.7, 0]), run_time=1.0)

        # ====================== SOAL 2 : solenoida (separuh layar kanan) ======================
        h2 = txt("Contoh Soal 2", 26, S.ACCENT, "BOLD").align_to([0.5, 2.6, 0], UL)
        q2 = VGroup(txt("Solenoida 500 lilitan, panjang 25 cm,", 18, S.TEXT_SOFT),
                    txt("dialiri arus 2 A. Hitung B di tengah solenoida.", 18, S.TEXT_SOFT)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).align_to([0.5, 2.1, 0], UL)
        self.play(FadeIn(h2), FadeIn(q2), run_time=0.6)

        dk2_items = [formula(r"N=500\ \text{lilitan}", S.TEXT, 22),
                     formula(r"L=25\ \mathrm{cm}=0{,}25\ \mathrm{m}", S.TEXT, 22),
                     formula(r"I=2\ \mathrm{A}", S.TEXT, 22),
                     formula(r"\mu_0=4\pi\times10^{-7}\ \mathrm{Wb/A{\cdot}m}", S.TEXT, 20)]
        dk2_box, dk2_head, dk2_body = make_card("Diketahui", S.FIELD, dk2_items, 3.7, 22)
        dk2 = VGroup(dk2_box, dk2_head, dk2_body).align_to([0.4, 1.55, 0], UL)
        dt2_box, dt2_head, dt2_body = make_card("Ditanya", S.NORTH,
                                                [formula(r"B\ \text{di tengah}=\ ?", S.TEXT, 22)], 3.7, 22)
        dt2 = VGroup(dt2_box, dt2_head, dt2_body).align_to([0.4, dk2.get_bottom()[1] - 0.2, 0], UL)

        # diagram solenoida: B ke kanan (arus ke bawah di sisi depan)
        C2 = np.array([5.55, 0.25, 0])
        coil = solenoid_front(6, 2.2, 1.2).move_to(C2)
        axis = Arrow(C2 + LEFT * 1.3, C2 + RIGHT * 1.3, buff=0, color=S.FIELD, stroke_width=4,
                     max_tip_length_to_length_ratio=0.12)
        b2_lab = formula("B", S.FIELD, 36).move_to(axis.get_end() + np.array([-0.1, 0.42, 0]))
        mid = Dot(C2, radius=0.09, color=S.ACCENT)
        span = DoubleArrow(C2 + np.array([-1.1, -0.9, 0]), C2 + np.array([1.1, -0.9, 0]), buff=0,
                           color=S.MUTED, stroke_width=2, tip_length=0.12)
        l_lab = formula(r"L=0{,}25\ \mathrm{m}", S.TEXT_SOFT, 22).move_to(C2 + np.array([0, -1.22, 0]))
        n_lab = formula(r"N=500", S.TEXT_SOFT, 22).move_to(C2 + np.array([-0.6, 1.1, 0]))
        i2_lab = formula(r"I=2\ \mathrm{A}", S.CURRENT, 22).move_to(C2 + np.array([0.75, 1.1, 0]))
        diagram2 = VGroup(axis, coil, mid, span, l_lab, n_lab, i2_lab, b2_lab)

        sc2 = np.array([3.65, -3.0, 0])
        sol2_box, sol2_head = solution_card(sc2, 6.5, 1.55)
        fc2 = sc2 + np.array([0.3, -0.18, 0])

        self.play(FadeIn(dk2_box), FadeIn(dk2_head), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(x) for x in dk2_body], lag_ratio=0.7), Create(axis), run_time=1.5)
        self.play(FadeIn(coil), FadeIn(mid), FadeIn(span), FadeIn(l_lab), FadeIn(n_lab), FadeIn(i2_lab),
                  FadeIn(b2_lab), run_time=0.8)
        self.play(FadeIn(dt2), run_time=0.4)
        self.play(FadeIn(sol2_box), FadeIn(sol2_head), run_time=0.4)

        f2_a = formula(r"B=\frac{\mu_0 I N}{L}", S.TEXT, 38).move_to(fc2)
        self.pad_to(22.5)
        self.play(Write(f2_a), run_time=0.9)
        self.pad_to(24.5)
        f2_b = formula(r"B=\frac{4\pi\times10^{-7}\times2\times500}{0{,}25}", S.TEXT, 34).move_to(fc2)
        self.play(ReplacementTransform(f2_a, f2_b), Indicate(i2_lab, color=S.ACCENT),
                  Indicate(n_lab, color=S.ACCENT), Indicate(l_lab, color=S.ACCENT), run_time=1.2)
        self.pad_to(27.0)
        f2_res = formula(rf"B\approx{M2}\times10^{{{E2}}}\ \mathrm{{T}}", S.ACCENT, 42).move_to(fc2)
        res2_box = SurroundingRectangle(f2_res, color=S.ACCENT, buff=0.18, corner_radius=0.12, stroke_width=3)
        self.play(ReplacementTransform(f2_b, f2_res), run_time=1.0)
        self.play(Create(res2_box), run_time=0.5)
        self.pad_to(S.SCENE_DURATIONS[SCENE_ID])

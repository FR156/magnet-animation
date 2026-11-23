"""Scene 06 — Induksi elektromagnetik (48 d).

Narasi (rencana, disinkronkan ulang setelah voice-over final):
  0–12  "Jika arus dapat menimbulkan medan magnet, bisakah medan magnet menimbulkan arus?
         Bisa, lewat induksi elektromagnetik. Kuncinya fluks magnetik, yaitu B kali A kali cos theta."
  12–25 "Saat magnet digerakkan mendekati kumparan, fluksnya berubah dan muncul GGL induksi;
         magnet diam tidak menghasilkan apa-apa. Makin banyak lilitan dan makin cepat perubahan
         fluks, makin besar GGL."
  25–36 "Arahnya ditentukan hukum Lenz: arus induksi selalu melawan penyebabnya. Itulah tanda
         minus di rumus. Magnet mendekat ditolak, magnet menjauh ditarik."
  36–48 "Pada kawat yang digerakkan dalam medan, GGL sama dengan B kali L kali v. Dengan 0,4 tesla,
         0,5 meter, dan 10 meter per sekon, hasilnya 2 volt."

Titik sinkron (pad_to): 5.0 | 7.5 | 12.0 | 14.0 | 17.5 | 22.0 | 25.0 | 30.5 | 36.0 | 48.0

Fisika:
  - Φ = B A cosθ, θ = sudut B terhadap GARIS NORMAL bidang. Garis yang menembus ~ cosθ.
  - Magnet dengan kutub U menuju kumparan: fluks (ke kanan) bertambah -> B induksi ke KIRI
    (menentang pertambahan) -> ujung kiri kumparan jadi U -> menolak.
    Magnet menjauh: fluks berkurang -> B induksi ke KANAN -> ujung kiri jadi S -> menarik.
  - Arus induksi: B ke kiri -> arus ke atas di sisi depan; B ke kanan -> arus ke bawah.
  - Kawat bergerak: ε = B L v sinθ, θ = sudut v terhadap B (di sini 90°).
"""
import sys
import math
import pathlib

# Agar `utils` dapat diimpor saat scene dirender langsung lewat `manim`.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    VGroup, VMobject, FadeIn, FadeOut, Create, Write, ReplacementTransform, LaggedStart,
    ValueTracker, always_redraw, MathTex, Rotate, RoundedRectangle, SurroundingRectangle,
    Rectangle, Circle, Dot, Arc, Line, Arrow, DoubleArrow, UP, DOWN, LEFT, RIGHT, UL, UR, ORIGIN, PI,
)
from utils import style as S  # noqa: E402
from utils import physics as P  # noqa: E402
from utils.components import (  # noqa: E402
    BaseScene, SANS_TEX, txt, formula, u_s_badge, bar_magnet, solenoid_front, labeled_arrow,
    field_cross, problem_card,
)

SCENE_ID = 6
EMF = P.emf_motional(0.4, 0.5, 10)  # 2 V
EMF_S = f"{EMF:g}"


def galvanometer(center):
    """Galvanometer: kotak + busur skala + jarum merah. Kembalikan (grup, jarum, pivot)."""
    c = np.array(center, dtype=float)
    box = RoundedRectangle(corner_radius=0.15, width=2.2, height=1.5, fill_color=S.CARD, fill_opacity=1,
                           stroke_color=S.CARD_EDGE, stroke_width=2).move_to(c)
    pivot = c + DOWN * 0.45
    scale = Arc(radius=0.85, start_angle=PI * 0.2, angle=PI * 0.6, arc_center=pivot, stroke_color=S.MUTED,
                stroke_width=2)
    ticks = VGroup(*[Line(pivot + 0.85 * np.array([math.cos(a), math.sin(a), 0]),
                          pivot + 0.75 * np.array([math.cos(a), math.sin(a), 0]),
                          stroke_color=S.MUTED, stroke_width=2) for a in np.linspace(PI * 0.2, PI * 0.8, 7)])
    needle = Line(pivot, pivot + UP * 0.8, stroke_color=S.NORTH, stroke_width=4)
    hub = Dot(pivot, radius=0.06, color=S.TEXT)
    lab = txt("G", S.SZ_LABEL, S.TEXT_SOFT, "BOLD").move_to(c + np.array([0.8, -0.45, 0]))
    return VGroup(box, scale, ticks, needle, hub, lab), needle, pivot


def polyline(points, color=S.MUTED, width=3):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners([np.array(p, dtype=float) for p in points])
    return m


class Scene06ElectromagneticInduction(BaseScene):
    def construct(self):
        badge = u_s_badge().to_corner(UR, buff=0.6)
        self.add(badge)
        title = txt("Induksi Elektromagnetik", S.SZ_TITLE, S.TEXT, "BOLD").to_corner(UL, buff=0.6)
        self.play(Write(title), run_time=0.7)

        # ===================== 0–12 d : pertanyaan + fluks magnetik =====================
        t1 = txt("Arus listrik  →  medan magnet", 38, S.TEXT, "BOLD").move_to([0, 0.7, 0])
        t2 = txt("Medan magnet  →  arus listrik ?", 38, S.ACCENT, "BOLD").move_to([0, -0.5, 0])
        self.play(FadeIn(t1), run_time=0.8)
        self.pad_to(2.4)
        self.play(FadeIn(t2), run_time=0.8)
        self.pad_to(4.5)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.5)

        # diagram fluks tampak samping: garis B mendatar, bidang kumparan berputar
        self.pad_to(5.0)
        C = np.array([-2.5, -0.5, 0])
        ys = np.arange(-1.5, 1.51, 0.5)
        tr = ValueTracker(0)
        rad = lambda: math.radians(tr.get_value())
        half = 1.2  # setengah panjang bidang

        def b_lines():
            g = VGroup()
            for y in ys:
                crossing = abs(y) < half * abs(math.cos(rad())) - 1e-3
                g.add(Arrow([-5.7, C[1] + y, 0], [0.4, C[1] + y, 0], buff=0, stroke_width=3,
                            color=S.FIELD, stroke_opacity=1.0 if crossing else 0.22,
                            max_tip_length_to_length_ratio=0.05, max_stroke_width_to_length_ratio=20))
            return g

        lines_b = always_redraw(b_lines)
        plane = always_redraw(lambda: Line(C + half * np.array([-math.sin(rad()), math.cos(rad()), 0]),
                                           C - half * np.array([-math.sin(rad()), math.cos(rad()), 0]),
                                           stroke_color=S.TEXT, stroke_width=8))
        normal = always_redraw(lambda: Arrow(C, C + 1.2 * np.array([math.cos(rad()), math.sin(rad()), 0]),
                                             buff=0, color=S.ACCENT, stroke_width=5,
                                             max_tip_length_to_length_ratio=0.25))
        n_lab = always_redraw(lambda: formula("n", S.ACCENT, 34).move_to(
            C + 1.55 * np.array([math.cos(rad()), math.sin(rad()), 0]) + np.array([0.05, 0.1, 0])))
        arc = always_redraw(lambda: Arc(radius=0.75, start_angle=0, angle=max(rad(), 1e-3), arc_center=C,
                                        color=S.ACCENT, stroke_width=3))
        th = always_redraw(lambda: formula(r"\theta", S.ACCENT, 30).move_to(
            C + 1.0 * np.array([math.cos(max(rad(), 0.3) / 2), math.sin(max(rad(), 0.3) / 2), 0])))
        b_lab = formula("B", S.FIELD, 40).move_to([-5.9, C[1] + 1.7, 0])
        a_lab = formula("A", S.TEXT, 34).move_to(C + np.array([0.0, -1.55, 0]))
        self.play(FadeIn(lines_b), FadeIn(plane), FadeIn(normal), FadeIn(n_lab), FadeIn(arc), FadeIn(th),
                  FadeIn(b_lab), FadeIn(a_lab), run_time=1.0)
        f_phi = formula(r"\Phi=B\,A\cos\theta", S.TEXT, 56).move_to([3.7, 1.4, 0])
        cap_th = VGroup(txt("θ = sudut B terhadap", S.SZ_LABEL + 2, S.TEXT_SOFT),
                        txt("garis normal bidang", S.SZ_LABEL + 2, S.TEXT_SOFT)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.7, 0.2, 0])
        self.play(Write(f_phi), FadeIn(cap_th), run_time=1.2)
        self.pad_to(7.5)
        self.play(tr.animate.set_value(90), run_time=3.0)
        cap0 = txt("θ = 90°: tidak ada garis menembus, Φ = 0", S.SZ_LABEL + 2, S.ACCENT, "BOLD").move_to([3.4, -1.3, 0])
        self.play(FadeIn(cap0), run_time=0.5)
        self.pad_to(11.5)
        for m in (lines_b, plane, normal, n_lab, arc, th):
            m.clear_updaters()
        self.play(FadeOut(VGroup(lines_b, plane, normal, n_lab, arc, th, b_lab, a_lab, f_phi, cap_th, cap0)),
                  run_time=0.5)

        # ===================== 12–25 d : magnet digerakkan mendekati kumparan =====================
        self.pad_to(12.0)
        COIL = np.array([0.3, 0.5, 0])
        coil_plain = solenoid_front(6, 2.4, 1.4, show_current=False).move_to(COIL)
        lx, rx = COIL[0] - 1.2, COIL[0] + 1.2
        G_c = np.array([4.5, 0.5, 0])
        galv, needle, pivot = galvanometer(G_c)
        wire_a = polyline([[lx, COIL[1] - 0.7, 0], [lx, -1.9, 0], [G_c[0] + 0.5, -1.9, 0],
                           [G_c[0] + 0.5, G_c[1] - 0.75, 0]])
        wire_b = polyline([[rx, COIL[1] - 0.7, 0], [rx, -0.9, 0], [G_c[0] - 0.5, -0.9, 0],
                           [G_c[0] - 0.5, G_c[1] - 0.75, 0]])
        mag = bar_magnet(1.8, 0.6, flipped=True, label_size=22).move_to([-4.4, COIL[1], 0])  # U di kanan
        n_coil = VGroup(formula("N", S.TEXT_SOFT, 30), txt("lilitan", S.SZ_LABEL, S.TEXT_SOFT)
                        ).arrange(RIGHT, buff=0.12).move_to(COIL + np.array([0, 1.25, 0]))
        flux = VGroup(*[Arrow(COIL + np.array([-0.95, dy, 0]), COIL + np.array([0.95, dy, 0]), buff=0,
                              color=S.FIELD, stroke_width=3, max_tip_length_to_length_ratio=0.12)
                        for dy in (-0.3, 0.0, 0.3)]).set_stroke(opacity=0.0)
        self.play(FadeIn(coil_plain), FadeIn(wire_a), FadeIn(wire_b), FadeIn(galv), FadeIn(mag), FadeIn(n_coil),
                  run_time=0.9)
        cap = txt("magnet diam: jarum nol", S.SZ_BODY, S.TEXT_SOFT, "BOLD").move_to([-0.3, -2.9, 0])
        self.play(FadeIn(cap), run_time=0.4)
        self.pad_to(14.0)
        cap_m = txt("magnet mendekat: fluks bertambah, jarum menyimpang", S.SZ_BODY, S.ACCENT, "BOLD").move_to(cap)
        self.add(flux)
        self.play(mag.animate.shift(RIGHT * 2.3), Rotate(needle, angle=-PI / 6, about_point=pivot),
                  flux.animate.set_stroke(opacity=1.0), ReplacementTransform(cap, cap_m), run_time=1.8)
        cap_s = txt("magnet diam: jarum nol", S.SZ_BODY, S.TEXT_SOFT, "BOLD").move_to(cap_m)
        self.play(Rotate(needle, angle=PI / 6, about_point=pivot), ReplacementTransform(cap_m, cap_s),
                  run_time=0.6)
        self.pad_to(17.5)

        eps_parts = MathTex(r"\varepsilon=", "-", r"N\frac{\Delta\Phi}{\Delta t}", font_size=46,
                            tex_template=SANS_TEX, color=S.TEXT)
        eps_parts.move_to([3.6, 2.2, 0])
        self.play(Write(eps_parts), run_time=1.2)
        e1 = VGroup(txt("makin banyak lilitan (N),", S.SZ_LABEL, S.TEXT_SOFT),
                    txt("makin besar GGL", S.SZ_LABEL, S.TEXT_SOFT)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        e2 = VGroup(txt("makin cepat berubah (Δt kecil),", S.SZ_LABEL, S.TEXT_SOFT),
                    txt("makin besar GGL", S.SZ_LABEL, S.TEXT_SOFT)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        e1.move_to([-3.6, 2.2, 0]).align_to([-6.8, 2.2, 0], LEFT)
        e2.move_to([-3.6, 1.4, 0]).align_to([-6.8, 1.4, 0], LEFT)
        self.pad_to(19.0)
        self.play(FadeIn(e1), FadeIn(e2), run_time=0.8)
        self.pad_to(22.0)
        chips = VGroup()
        for i, name in enumerate(["gerak magnet", "perubahan B", "perubahan A", "perubahan θ"]):
            box = RoundedRectangle(corner_radius=0.25, width=3.0, height=0.62, fill_color=S.CARD, fill_opacity=1,
                                   stroke_color=S.CARD_EDGE, stroke_width=2)
            lb = txt(name, S.SZ_LABEL + 2, S.TEXT, "BOLD").move_to(box)
            chips.add(VGroup(box, lb))
        chips.arrange(RIGHT, buff=0.3).move_to([0, -3.55, 0])
        chips_head = txt("Penyebab perubahan fluks:", S.SZ_LABEL, S.MUTED).move_to([-5.2, -2.75, 0])
        self.play(FadeIn(chips_head), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.4), run_time=2.0)
        self.pad_to(24.5)
        self.play(FadeOut(VGroup(chips, chips_head, e1, e2, galv, wire_a, wire_b, flux, cap_s)), run_time=0.5)

        # ===================== 25–36 d : hukum Lenz =====================
        self.pad_to(25.0)
        # tanda minus ditandai merah
        self.play(eps_parts[1].animate.set_color(S.NORTH), run_time=0.4)
        minus_note = VGroup(txt("tanda minus:", S.SZ_LABEL + 2, S.NORTH, "BOLD"),
                            txt("melawan perubahan fluks", S.SZ_LABEL + 2, S.NORTH, "BOLD")
                            ).arrange(DOWN, buff=0.06).move_to([3.6, 1.35, 0])
        self.play(FadeIn(minus_note), run_time=0.5)

        coil_in = solenoid_front(6, 2.4, 1.4, direction="left").move_to(COIL)   # B induksi ke kiri
        coil_out = solenoid_front(6, 2.4, 1.4, direction="right").move_to(COIL)  # B induksi ke kanan
        ind_u = Rectangle(width=0.4, height=1.0, fill_color=S.NORTH, fill_opacity=1, stroke_width=0
                          ).move_to([lx - 0.25, COIL[1], 0])
        ind_u_l = txt("U", S.SZ_BODY, S.BG, "BOLD").move_to(ind_u)
        ind_s = Rectangle(width=0.4, height=1.0, fill_color=S.SOUTH, fill_opacity=1, stroke_width=0
                          ).move_to([lx - 0.25, COIL[1], 0])
        ind_s_l = txt("S", S.SZ_BODY, S.BG, "BOLD").move_to(ind_s)
        b_ind_l = labeled_arrow(COIL + np.array([0.8, -1.05, 0]), COIL + np.array([-0.8, -1.05, 0]), "B induksi", S.FIELD, label_dir=DOWN, size=S.SZ_LABEL)
        b_ind_r = labeled_arrow(COIL + np.array([-0.8, -1.05, 0]), COIL + np.array([0.8, -1.05, 0]), "B induksi", S.FIELD, label_dir=DOWN, size=S.SZ_LABEL)
        v_r = labeled_arrow([-3.9, 1.7, 0], [-2.7, 1.7, 0], "v", S.TEXT, label_dir=UP, size=S.SZ_LABEL + 4)
        v_l = labeled_arrow([-2.7, 1.7, 0], [-3.9, 1.7, 0], "v", S.TEXT, label_dir=UP, size=S.SZ_LABEL + 4)
        mag.move_to([-4.4, COIL[1], 0])
        cap_a = txt("mendekat → ditolak", S.SZ_BODY + 2, S.NORTH, "BOLD").move_to([-0.3, -2.6, 0])
        self.play(FadeOut(coil_plain), FadeIn(coil_in), FadeIn(ind_u), FadeIn(ind_u_l), FadeIn(b_ind_l),
                  FadeIn(v_r), FadeIn(cap_a), run_time=0.8)
        self.play(mag.animate.shift(RIGHT * 2.3), run_time=2.2)
        self.pad_to(30.5)
        cap_b = txt("menjauh → ditarik", S.SZ_BODY + 2, S.FIELD, "BOLD").move_to(cap_a)
        self.play(ReplacementTransform(coil_in, coil_out), ReplacementTransform(ind_u, ind_s),
                  ReplacementTransform(ind_u_l, ind_s_l), ReplacementTransform(b_ind_l, b_ind_r),
                  ReplacementTransform(v_r, v_l), ReplacementTransform(cap_a, cap_b), run_time=0.8)
        self.play(mag.animate.shift(LEFT * 2.3), run_time=2.2)
        self.pad_to(35.5)
        self.play(FadeOut(VGroup(coil_out, ind_s, ind_s_l, b_ind_r, v_l, cap_b, mag, n_coil, minus_note,
                                 eps_parts)), run_time=0.5)

        # ===================== 36–48 d : penghantar bergerak, ε = B L v =====================
        self.pad_to(36.0)
        region = RoundedRectangle(corner_radius=0.2, width=6.9, height=4.3, fill_color=S.FIELD,
                                  fill_opacity=0.07, stroke_color=S.FIELD, stroke_width=2).move_to([-3.4, -0.6, 0])
        crosses = VGroup(*[field_cross(0.12).move_to([x, y, 0])
                           for y in (0.1, -0.7, -1.5) for x in np.linspace(-6.3, -0.5, 8)])
        rail_t = Line([-6.4, 0.9, 0], [-0.4, 0.9, 0], stroke_color=S.MUTED, stroke_width=5)
        rail_b = Line([-6.4, -2.3, 0], [-0.4, -2.3, 0], stroke_color=S.MUTED, stroke_width=5)
        rod = Line([-4.6, 0.9, 0], [-4.6, -2.3, 0], stroke_color=S.CURRENT, stroke_width=9)
        l_lab = VGroup(Rectangle(width=0.5, height=0.5, fill_color=S.BG, fill_opacity=0.9, stroke_width=0),
                       formula("L", S.TEXT_SOFT, 34)).move_to([-5.05, -0.7, 0])
        b_tag = VGroup(formula("B", S.FIELD, 36), txt("(masuk layar)", S.SZ_LABEL, S.FIELD)
                       ).arrange(RIGHT, buff=0.15).move_to([-4.1, 1.75, 0])
        self.play(FadeIn(region), FadeIn(crosses), FadeIn(rail_t), FadeIn(rail_b),
                  FadeIn(rod), FadeIn(l_lab), FadeIn(b_tag), run_time=1.0)
        v_arr = labeled_arrow([-4.4, -0.7, 0], [-2.9, -0.7, 0], "v", S.TEXT, label_dir=UP, size=S.SZ_LABEL + 6)
        mover = VGroup(rod, l_lab, v_arr)
        self.play(FadeIn(v_arr), run_time=0.4)
        self.play(mover.animate.shift(RIGHT * 2.0), run_time=2.2)

        card = problem_card("Contoh soal", S.ACCENT, [
            formula(r"L=0{,}5\ \mathrm{m},\ \ v=10\ \mathrm{m/s}", S.TEXT, 28),
            formula(r"B=0{,}4\ \mathrm{T},\ \ \theta=90^\circ", S.TEXT, 28),
        ], 5.6, 26).align_to([1.1, 2.7, 0], UL)
        self.play(FadeIn(card), run_time=0.7)
        self.pad_to(41.0)
        f_a = formula(r"\varepsilon=B\,L\,v", S.TEXT, 54).move_to([3.9, 0.0, 0])
        self.play(Write(f_a), run_time=1.0)
        self.pad_to(43.0)
        f_b = formula(r"\varepsilon=0{,}4\times0{,}5\times10", S.TEXT, 50).move_to([3.9, 0.0, 0])
        self.play(ReplacementTransform(f_a, f_b), run_time=1.0)
        self.pad_to(45.0)
        f_c = formula(rf"\varepsilon={EMF_S}\ \mathrm{{V}}", S.ACCENT, 60).move_to([3.9, -1.3, 0])
        box = SurroundingRectangle(f_c, color=S.ACCENT, buff=0.2, corner_radius=0.12, stroke_width=3)
        self.play(FadeIn(f_c), Create(box), run_time=0.9)
        self.pad_to(S.SCENE_DURATIONS[SCENE_ID])

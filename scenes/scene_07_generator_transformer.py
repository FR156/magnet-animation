"""Scene 07 — Generator dan transformator (45 d).

Narasi (rencana, disinkronkan ulang setelah voice-over final):
  0–13  "Generator mengubah energi gerak menjadi energi listrik. Kumparan diputar dalam medan
         magnet sehingga fluksnya berubah, menghasilkan GGL N kali B kali A kali omega kali sin omega t."
  13–24 "Transformator memakai prinsip serupa, tetapi hanya bekerja pada arus bolak-balik, sebab
         fluks di inti harus terus berubah."
  24–36 "Tegangan sebanding dengan lilitan. Bila Ns lebih besar dari Np, tegangan naik; bila lebih
         kecil, turun. Contoh: Np seribu, Ns dua ratus, Vp 220 volt, maka Vs 44 volt, step-down."
  36–45 "Daya primer 110 watt, daya sekunder 88 watt, jadi efisiensi 80 persen. Kurang dari 100
         persen karena panas dan arus eddy."

Titik sinkron (pad_to): 13.0 | 24.0 | 36.0 | 45.0

Fisika:
  - Kumparan berputar: θ = ωt (sudut B terhadap normal). Φ = NBA cosθ -> ε = -dΦ/dt = NBAω sin ωt.
  - Trafo: Vp/Vs = Np/Ns = Is/Ip; hanya bekerja pada AC (fluks inti harus berubah).
  - Efisiensi η = Ps/Pp x 100%.
"""
import sys
import math
import pathlib

# Agar `utils` dapat diimpor saat scene dirender langsung lewat `manim`.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    VGroup, VMobject, FadeIn, FadeOut, Create, Write, ReplacementTransform, LaggedStart, Rotate,
    ValueTracker, always_redraw, Axes, RoundedRectangle, SurroundingRectangle, Rectangle, Circle, Ellipse,
    Dot, Arc, Line, Arrow, rate_functions, UP, DOWN, LEFT, RIGHT, UL, UR, ORIGIN, PI,
)
from utils import style as S  # noqa: E402
from utils import physics as P  # noqa: E402
from utils.components import (  # noqa: E402
    BaseScene, txt, formula, u_s_badge, problem_card,
)

SCENE_ID = 7
VS = P.trafo_vs(220, 1000, 200)            # 44 V
PP, PS = P.power(220, 0.5), P.power(VS, 2)  # 110 W, 88 W
ETA = P.efficiency(PS, PP)                  # 80 %


def polyline(points, color=S.MUTED, width=3):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners([np.array(p, dtype=float) for p in points])
    return m


def transformer(n_p, n_s, w=3.6, h=2.6, leg=0.55):
    """Inti besi berbentuk persegi + kumparan primer (kiri) dan sekunder (kanan).
    Kembalikan (grup, info) dengan info = posisi pelat kumparan untuk menyambung kabel."""
    outer = Rectangle(width=w, height=h, fill_color=S.MUTED, fill_opacity=0.45, stroke_color=S.TEXT_SOFT,
                      stroke_width=2)
    hole = Rectangle(width=w - 2 * leg, height=h - 2 * leg, fill_color=S.BG, fill_opacity=1,
                     stroke_color=S.TEXT_SOFT, stroke_width=2)
    xl, xr = -(w / 2 - leg / 2), (w / 2 - leg / 2)
    span = h / 2 - 0.3

    def coil(n, x):
        ys = np.linspace(span, -span, n) if n > 1 else [0.0]
        return VGroup(*[Ellipse(width=leg + 0.42, height=0.16, stroke_color=S.CURRENT, stroke_width=3,
                                fill_color=S.BG, fill_opacity=0.0).move_to([x, y, 0]) for y in ys])

    prim, sec = coil(n_p, xl), coil(n_s, xr)
    info = {"xl": xl, "xr": xr, "top_p": span if n_p > 1 else 0.0, "bot_p": -span if n_p > 1 else 0.0,
            "top_s": span if n_s > 1 else 0.0, "bot_s": -span if n_s > 1 else 0.0,
            "half_w": (leg + 0.42) / 2, "w": w, "h": h, "leg": leg}
    return VGroup(outer, hole, prim, sec), info


class Scene07GeneratorTransformer(BaseScene):
    def construct(self):
        badge = u_s_badge().to_corner(UR, buff=0.6)
        self.add(badge)
        title = txt("Generator dan Transformator", S.SZ_TITLE, S.TEXT, "BOLD").to_corner(UL, buff=0.6)
        self.play(Write(title), run_time=0.7)

        # ===================== 0–13 d : generator =====================
        GC = np.array([-3.4, -0.2, 0])
        u_blk = Rectangle(width=0.8, height=2.8, fill_color=S.NORTH, fill_opacity=1, stroke_width=0).move_to(GC + LEFT * 2.5)
        s_blk = Rectangle(width=0.8, height=2.8, fill_color=S.SOUTH, fill_opacity=1, stroke_width=0).move_to(GC + RIGHT * 2.5)
        u_l = txt("U", S.SZ_HEAD, S.BG, "BOLD").move_to(u_blk)
        s_l = txt("S", S.SZ_HEAD, S.BG, "BOLD").move_to(s_blk)
        b_arrows = VGroup(*[Arrow(GC + np.array([-2.0, dy, 0]), GC + np.array([2.0, dy, 0]), buff=0, color=S.FIELD,
                                  stroke_width=3, max_tip_length_to_length_ratio=0.08, stroke_opacity=0.7)
                            for dy in (-1.1, -0.55, 0.55, 1.1)])
        b_lab = formula("B", S.FIELD, 40).move_to(GC + np.array([0.0, 1.75, 0]))
        tr = ValueTracker(0.0)   # θ = ωt (rad)
        th = lambda: tr.get_value()
        half = 0.95
        loop = always_redraw(lambda: Line(GC + half * np.array([-math.sin(th()), math.cos(th()), 0]),
                                          GC - half * np.array([-math.sin(th()), math.cos(th()), 0]),
                                          stroke_color=S.CURRENT, stroke_width=8))
        ends = always_redraw(lambda: VGroup(*[Dot(GC + sg * half * np.array([-math.sin(th()), math.cos(th()), 0]),
                                                  radius=0.1, color=S.CURRENT) for sg in (1, -1)]))
        normal = always_redraw(lambda: Arrow(GC, GC + 0.8 * np.array([math.cos(th()), math.sin(th()), 0]), buff=0,
                                             color=S.ACCENT, stroke_width=4, max_tip_length_to_length_ratio=0.3))
        arc = always_redraw(lambda: Arc(radius=0.45, start_angle=0, angle=max(th() % (2 * PI), 1e-3), arc_center=GC,
                                        color=S.ACCENT, stroke_width=3))
        cap_g = txt("kumparan berputar, θ = ωt", S.SZ_LABEL + 2, S.TEXT_SOFT).move_to(GC + np.array([0, -1.95, 0]))
        self.play(FadeIn(VGroup(u_blk, s_blk, u_l, s_l, b_arrows, b_lab)), FadeIn(loop), FadeIn(ends),
                  FadeIn(normal), FadeIn(arc), FadeIn(cap_g), run_time=0.9)

        axes = Axes(x_range=[0, 4 * PI, PI], y_range=[-1.2, 1.2, 1], x_length=5.8, y_length=2.6,
                    axis_config={"color": S.MUTED, "include_ticks": False, "include_tip": True, "tip_width": 0.15,
                                 "tip_height": 0.15, "stroke_width": 2}).move_to([3.5, -0.4, 0])
        eps_l = formula(r"\varepsilon", S.TEXT_SOFT, 34).next_to(axes.y_axis.get_end(), LEFT, buff=0.1)
        t_l = formula("t", S.TEXT_SOFT, 34).next_to(axes.x_axis.get_end(), DOWN, buff=0.1)
        curve = always_redraw(lambda: axes.plot(lambda x: math.sin(x), x_range=[0, max(th(), 0.02)],
                                                color=S.ACCENT, stroke_width=5))
        dot = always_redraw(lambda: Dot(axes.c2p(th() if th() > 0.02 else 0.02, math.sin(max(th(), 0.02))),
                                        radius=0.09, color=S.TEXT))
        f_gen = formula(r"\varepsilon=N\,B\,A\,\omega\sin\omega t", S.TEXT, 42).move_to([3.4, 2.2, 0])
        self.play(Create(axes), FadeIn(eps_l), FadeIn(t_l), run_time=0.8)
        self.play(Write(f_gen), run_time=1.0)
        self.add(curve, dot)
        self.pad_to(3.5)
        self.play(tr.animate.set_value(4 * PI), run_time=7.0, rate_func=rate_functions.linear)
        for m in (loop, ends, normal, arc, curve, dot):
            m.clear_updaters()
        self.pad_to(10.8)
        pills = VGroup()
        for name, cx in (("dinamo", -2.4), ("PLTA", 0.4), ("PLTU", 3.2)):
            box = RoundedRectangle(corner_radius=0.28, width=2.4, height=0.7, fill_color=S.CARD, fill_opacity=1,
                                   stroke_color=S.CARD_EDGE, stroke_width=2).move_to([cx + 0.8, -3.4, 0])
            pills.add(VGroup(box, txt(name, S.SZ_BODY, S.TEXT, "BOLD").move_to(box)))
        pills_head = txt("Contoh generator:", S.SZ_LABEL + 2, S.MUTED).move_to([-5.3, -3.4, 0])
        self.play(FadeIn(pills_head), LaggedStart(*[FadeIn(p) for p in pills], lag_ratio=0.4), run_time=1.5)
        self.pad_to(12.5)
        self.play(FadeOut(VGroup(u_blk, s_blk, u_l, s_l, b_arrows, b_lab, loop, ends, normal, arc, cap_g, axes,
                                 eps_l, t_l, curve, dot, f_gen, pills, pills_head)), run_time=0.5)

        # ===================== 13–24 d : prinsip transformator, hanya AC =====================
        self.pad_to(13.0)
        T, inf = transformer(10, 2, w=3.8, h=2.8)
        T.move_to([0.4, -0.1, 0])
        c = np.array([0.4, -0.1, 0])
        xl, xr, hw = c[0] + inf["xl"], c[0] + inf["xr"], inf["half_w"]
        top_p, bot_p = c[1] + inf["top_p"], c[1] + inf["bot_p"]
        top_s, bot_s = c[1] + inf["top_s"], c[1] + inf["bot_s"]
        src_c, load_c = np.array([-4.2, c[1], 0]), np.array([5.0, c[1], 0])
        src = Circle(radius=0.5, stroke_color=S.TEXT, stroke_width=3, fill_color=S.CARD, fill_opacity=1).move_to(src_c)
        src_s = formula(r"\sim", S.TEXT, 52).move_to(src_c)
        src_t = txt("AC", S.SZ_LABEL + 2, S.TEXT_SOFT, "BOLD").next_to(src, DOWN, buff=0.15)
        load = Circle(radius=0.45, stroke_color=S.ACCENT, stroke_width=3, fill_color=S.CARD, fill_opacity=1).move_to(load_c)
        load_x = VGroup(Line(load_c + np.array([-0.3, -0.3, 0]), load_c + np.array([0.3, 0.3, 0]), stroke_color=S.ACCENT, stroke_width=3),
                        Line(load_c + np.array([-0.3, 0.3, 0]), load_c + np.array([0.3, -0.3, 0]), stroke_color=S.ACCENT, stroke_width=3))
        load_t = txt("beban", S.SZ_LABEL + 2, S.TEXT_SOFT, "BOLD").next_to(load, DOWN, buff=0.15)
        w_p1 = polyline([[xl - hw, top_p, 0], [src_c[0], top_p, 0], [src_c[0], src_c[1] + 0.5, 0]])
        w_p2 = polyline([[xl - hw, bot_p, 0], [src_c[0], bot_p, 0], [src_c[0], src_c[1] - 0.5, 0]])
        w_s1 = polyline([[xr + hw, top_s, 0], [load_c[0], top_s, 0], [load_c[0], load_c[1] + 0.45, 0]])
        w_s2 = polyline([[xr + hw, bot_s, 0], [load_c[0], bot_s, 0], [load_c[0], load_c[1] - 0.45, 0]])
        lab_p = formula(r"N_p", S.TEXT_SOFT, 34).move_to([xl - hw - 0.55, c[1], 0])
        lab_s = formula(r"N_s", S.TEXT_SOFT, 34).move_to([xr + hw + 0.55, c[1], 0])
        core_lab = txt("inti besi", S.SZ_LABEL, S.MUTED).move_to([c[0], c[1] + 1.8, 0])
        self.play(FadeIn(T), FadeIn(VGroup(src, src_s, src_t, load, load_x, load_t, w_p1, w_p2, w_s1, w_s2)),
                  FadeIn(lab_p), FadeIn(lab_s), FadeIn(core_lab), run_time=1.2)
        # fluks bolak-balik di inti
        a, b = (inf["w"] - inf["leg"]) / 2, (inf["h"] - inf["leg"]) / 2
        mk = lambda p, q: Arrow(c + np.array(p), c + np.array(q), buff=0, color=S.FIELD, stroke_width=6,
                                max_tip_length_to_length_ratio=0.35)
        flux = VGroup(mk([-0.4, b, 0], [0.4, b, 0]), mk([a, 0.4, 0], [a, -0.4, 0]),
                      mk([0.4, -b, 0], [-0.4, -b, 0]), mk([-a, -0.4, 0], [-a, 0.4, 0]))
        flux_lab = formula(r"\Phi", S.FIELD, 44).move_to(c + np.array([0.0, 0.0, 0]))
        self.play(FadeIn(flux), FadeIn(flux_lab), run_time=0.6)
        cap_f = txt("fluks inti berubah terus (bolak-balik)", S.SZ_BODY, S.FIELD, "BOLD").move_to([0.4, -2.65, 0])
        self.play(FadeIn(cap_f), run_time=0.5)
        for _ in range(3):
            self.play(*[Rotate(x, PI) for x in flux], run_time=0.9)
        self.pad_to(21.0)
        dc = txt("DC", S.SZ_HEAD + 4, S.TEXT, "BOLD").move_to([-4.2, 2.3, 0])
        dc_x = Line(dc.get_corner(np.array([-1, -1, 0])) + DOWN * 0.05, dc.get_corner(np.array([1, 1, 0])) + UP * 0.05,
                    stroke_color=S.NORTH, stroke_width=6)
        only = txt("hanya AC: fluks harus berubah", S.SZ_BODY, S.ACCENT, "BOLD").move_to([-2.0, 2.3, 0]).align_to([-3.4, 2.3, 0], LEFT)
        self.play(FadeIn(dc), Create(dc_x), FadeIn(only), run_time=0.9)
        self.pad_to(23.5)
        self.play(FadeOut(VGroup(T, src, src_s, src_t, load, load_x, load_t, w_p1, w_p2, w_s1, w_s2, lab_p, lab_s,
                                 core_lab, flux, flux_lab, cap_f, dc, dc_x, only)), run_time=0.5)

        # ===================== 24–36 d : rumus trafo + contoh Vs =====================
        self.pad_to(24.0)
        f_t = formula(r"\frac{V_p}{V_s}=\frac{N_p}{N_s}=\frac{I_s}{I_p}", S.TEXT, 46).move_to([-2.5, 1.85, 0])
        self.play(Write(f_t), run_time=1.2)
        up, up_i = transformer(2, 6, w=2.4, h=1.8, leg=0.4)
        dn, dn_i = transformer(6, 2, w=2.4, h=1.8, leg=0.4)
        up.move_to([-5.3, -0.3, 0])
        dn.move_to([-2.0, -0.3, 0])
        up_t = VGroup(txt("step-up", S.SZ_BODY, S.OK, "BOLD"), formula(r"N_s>N_p", S.TEXT, 30),
                      txt("tegangan naik", S.SZ_LABEL, S.TEXT_SOFT)).arrange(DOWN, buff=0.1).move_to([-5.3, -2.15, 0])
        dn_t = VGroup(txt("step-down", S.SZ_BODY, S.NORTH, "BOLD"), formula(r"N_s<N_p", S.TEXT, 30),
                      txt("tegangan turun", S.SZ_LABEL, S.TEXT_SOFT)).arrange(DOWN, buff=0.1).move_to([-2.0, -2.15, 0])
        self.play(FadeIn(up), FadeIn(up_t), run_time=0.7)
        self.play(FadeIn(dn), FadeIn(dn_t), run_time=0.7)
        self.pad_to(29.5)
        ex = problem_card("Contoh soal", S.ACCENT, [
            formula(r"N_p=1000,\ \ N_s=200", S.TEXT, 28),
            formula(r"V_p=220\ \mathrm{V}", S.TEXT, 28),
            formula(r"V_s=V_p\times\frac{N_s}{N_p}", S.TEXT, 30),
            formula(r"V_s=220\times\frac{200}{1000}", S.TEXT, 30),
            VGroup(formula(rf"V_s={VS:g}\ \mathrm{{V}}", S.ACCENT, 36),
                   txt("step-down", S.SZ_LABEL, S.NORTH, "BOLD")).arrange(RIGHT, buff=0.3),
        ], 4.3, 24).align_to([2.6, 2.65, 0], UL)
        self.play(FadeIn(ex[0]), FadeIn(ex[1]), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(x) for x in ex[2]], lag_ratio=0.6), run_time=3.0)
        res = SurroundingRectangle(ex[2][4][0], color=S.ACCENT, buff=0.12, corner_radius=0.1, stroke_width=3)
        self.play(Create(res), run_time=0.6)
        self.pad_to(35.5)
        self.play(FadeOut(VGroup(f_t, up, dn, up_t, dn_t, ex, res)), run_time=0.5)

        # ===================== 36–45 d : daya dan efisiensi =====================
        self.pad_to(36.0)
        pcard = problem_card("Daya primer dan sekunder", S.ACCENT, [
            formula(r"P_p=V_p\,I_p=220\times0{,}5=110\ \mathrm{W}", S.TEXT, 28),
            formula(rf"P_s=V_s\,I_s={VS:g}\times2={PS:g}\ \mathrm{{W}}", S.TEXT, 28),
        ], 7.2, 24).align_to([-6.8, 2.7, 0], UL)
        self.play(FadeIn(pcard[0]), FadeIn(pcard[1]), LaggedStart(*[FadeIn(x) for x in pcard[2]], lag_ratio=0.8),
                  run_time=2.2)
        # diagram batang: daya masuk vs keluar
        base_y, k = -3.4, 0.022
        bar_p = Rectangle(width=1.1, height=PP * k * 1.0, fill_color=S.CURRENT, fill_opacity=1, stroke_width=0
                          ).move_to([-5.4, base_y + PP * k / 2, 0])
        bar_s = Rectangle(width=1.1, height=PS * k, fill_color=S.OK, fill_opacity=1, stroke_width=0
                          ).move_to([-3.8, base_y + PS * k / 2, 0])
        lost = Rectangle(width=1.1, height=(PP - PS) * k, fill_color=S.NORTH, fill_opacity=0.55, stroke_color=S.NORTH,
                         stroke_width=2).move_to([-3.8, base_y + PS * k + (PP - PS) * k / 2, 0])
        lb_p = formula(r"P_p", S.TEXT, 34).next_to(bar_p, DOWN, buff=0.1)
        lb_s = formula(r"P_s", S.TEXT, 34).next_to(bar_s, DOWN, buff=0.1)
        v_p = formula(r"110\ \mathrm{W}", S.TEXT, 28).next_to(bar_p, UP, buff=0.08)
        v_s = formula(rf"{PS:g}\ \mathrm{{W}}", S.TEXT, 28).next_to(bar_s, UP, buff=0.08).shift(UP * (PP - PS) * k)
        heat = VGroup(txt("hilang menjadi", S.SZ_LABEL, S.NORTH, "BOLD"), txt("panas & arus eddy", S.SZ_LABEL, S.NORTH, "BOLD")
                      ).arrange(DOWN, buff=0.05).move_to([-1.35, base_y + PS * k + (PP - PS) * k / 2 + 0.1, 0])
        self.pad_to(39.0)
        self.play(FadeIn(bar_p), FadeIn(lb_p), FadeIn(v_p), run_time=0.6)
        self.play(FadeIn(bar_s), FadeIn(lb_s), run_time=0.6)
        self.play(FadeIn(lost), FadeIn(v_s), FadeIn(heat), run_time=0.7)
        self.pad_to(42.0)
        f_eta = formula(rf"\eta=\frac{{P_s}}{{P_p}}\times100\%=\frac{{{PS:g}}}{{{PP:g}}}\times100\%", S.TEXT, 40
                        ).move_to([3.0, -0.6, 0])
        f_res = formula(rf"\eta={ETA:g}\%", S.ACCENT, 60).move_to([2.9, -2.2, 0])
        box = SurroundingRectangle(f_res, color=S.ACCENT, buff=0.2, corner_radius=0.12, stroke_width=3)
        self.play(Write(f_eta), run_time=1.2)
        self.pad_to(43.8)
        self.play(FadeIn(f_res), Create(box), run_time=0.9)
        self.pad_to(S.SCENE_DURATIONS[SCENE_ID])

"""Scene 02 — Kemagnetan dan jenis bahan (30 d).

Narasi (rencana, disinkronkan ulang setelah voice-over final):
  0–10  "Magnet menarik besi, baja, nikel, dan kobalt. Ia selalu punya dua kutub,
         utara dan selatan. Kutub senama saling menolak, tidak senama saling menarik."
  10–18 "Kutub ini tak bisa dipisahkan. Dipotong sekecil apa pun, magnet tetap punya dua kutub."
  18–30 "Bahan dibagi tiga. Feromagnetik ... ditarik kuat. Paramagnetik ... ditarik lemah.
         Diamagnetik ... ditolak lemah."

Titik sinkron (pad_to): 10.0 | 18.0 | 30.0
"""
import sys
import pathlib

# Agar `utils` dapat diimpor saat scene dirender langsung lewat `manim`.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from manim import (  # noqa: E402
    VGroup, FadeIn, FadeOut, Create, Write, RoundedRectangle, Circle, DashedLine,
    LaggedStart, Succession, rate_functions,
    UP, DOWN, LEFT, RIGHT, UL, UR,
)
from utils import style as S  # noqa: E402
from utils.components import (  # noqa: E402
    BaseScene, txt, u_s_badge, bar_magnet, labeled_arrow,
)

SCENE_ID = 2
FORCE = S.ACCENT  # gaya pada magnet/bahan digambar emas, selalu berlabel "F"


def chip(name):
    """Benda logam kecil berlabel (besi, baja, ...)."""
    box = RoundedRectangle(corner_radius=0.1, width=1.0, height=0.46, fill_color=S.CARD_EDGE,
                           fill_opacity=1, stroke_color=S.MUTED, stroke_width=1.5)
    return VGroup(box, txt(name, 18, S.TEXT)).move_to(box)


class Scene02Magnetism(BaseScene):
    def construct(self):
        badge = u_s_badge().to_corner(UR, buff=0.6)
        self.add(badge)  # sudah ada di akhir Scene 1 (kontinuitas)
        title = txt("Kemagnetan", S.SZ_TITLE, S.TEXT, "BOLD").to_corner(UL, buff=0.6)
        self.play(Write(title), run_time=0.7)

        # ================= 0–10 d : tarik benda logam + kutub senama/tidak senama =================
        magnet = bar_magnet().move_to([0, -0.2, 0])
        self.play(FadeIn(magnet), run_time=0.5)

        names = ["besi", "baja", "nikel", "kobalt"]
        chips = [chip(n) for n in names]
        starts = [[-5.6, 2.0, 0], [-5.6, -2.6, 0], [5.6, 2.0, 0], [5.6, -2.6, 0]]
        stops = [[-2.25, 0.05, 0], [-2.25, -0.45, 0], [2.25, 0.05, 0], [2.25, -0.45, 0]]
        for c, p in zip(chips, starts):
            c.move_to(p)
        self.play(*[FadeIn(c) for c in chips], run_time=0.5)
        self.play(
            *[c.animate(rate_func=rate_functions.ease_in_quad).move_to(p) for c, p in zip(chips, stops)],
            run_time=1.6,
        )
        self.pad_to(3.8)
        self.play(FadeOut(magnet), *[FadeOut(c) for c in chips], run_time=0.6)

        # dua baris magnet: baris 1 senama (U–U), baris 2 tidak senama (U–S)
        W, H = 2.4, 0.7
        far, near, touch = 3.7, 1.65, 1.2
        y1, y2 = 1.3, -1.3
        a1 = bar_magnet(W, H, flipped=True, label_size=26).move_to([-far, y1, 0])   # [S|U]
        b1 = bar_magnet(W, H, label_size=26).move_to([far, y1, 0])                  # [U|S]
        a2 = bar_magnet(W, H, label_size=26).move_to([-far, y2, 0])                 # [U|S]
        b2 = bar_magnet(W, H, label_size=26).move_to([far, y2, 0])                  # [U|S]
        lab1 = txt("Kutub senama: tolak-menolak", S.SZ_BODY, S.TEXT_SOFT).move_to([0, y1 - 0.85, 0])
        lab2 = txt("Kutub tidak senama: tarik-menarik", S.SZ_BODY, S.TEXT_SOFT).move_to([0, y2 - 0.85, 0])
        self.play(FadeIn(VGroup(a1, b1, a2, b2)), FadeIn(lab1), FadeIn(lab2), run_time=0.6)

        # mendekat
        self.play(
            a1.animate.move_to([-near, y1, 0]), b1.animate.move_to([near, y1, 0]),
            a2.animate.move_to([-near, y2, 0]), b2.animate.move_to([near, y2, 0]),
            run_time=1.2,
        )
        # panah gaya (berlabel F): baris 1 saling menjauh, baris 2 saling mendekat
        dy = 0.68
        f_a1 = labeled_arrow([-near, y1 + dy, 0], [-near - 0.9, y1 + dy, 0], "F", FORCE)
        f_b1 = labeled_arrow([near, y1 + dy, 0], [near + 0.9, y1 + dy, 0], "F", FORCE)
        f_a2 = labeled_arrow([-near, y2 + dy, 0], [-near + 0.9, y2 + dy, 0], "F", FORCE)
        f_b2 = labeled_arrow([near, y2 + dy, 0], [near - 0.9, y2 + dy, 0], "F", FORCE)
        forces = VGroup(f_a1, f_b1, f_a2, f_b2)
        self.play(FadeIn(forces), run_time=0.5)
        self.wait(0.6)
        # baris 1 saling menjauh, baris 2 menempel
        self.play(
            FadeOut(forces),
            a1.animate.move_to([-far, y1, 0]), b1.animate.move_to([far, y1, 0]),
            a2.animate.move_to([-touch, y2, 0]), b2.animate.move_to([touch, y2, 0]),
            run_time=1.1,
        )
        self.pad_to(9.5)
        self.play(FadeOut(VGroup(a1, b1, a2, b2, lab1, lab2)), run_time=0.5)

        # ================= 10–18 d : kutub tidak dapat dipisahkan =================
        self.pad_to(10.0)
        big = bar_magnet(4.8, 1.0).move_to([0, 0.5, 0])
        self.play(FadeIn(big), run_time=0.5)
        cut1 = DashedLine([0, 1.3, 0], [0, -0.3, 0], color=S.TEXT, stroke_width=3)
        self.play(Create(cut1), run_time=0.5)
        p1 = bar_magnet(2.4, 1.0).move_to([-1.2, 0.5, 0])
        p2 = bar_magnet(2.4, 1.0).move_to([1.2, 0.5, 0])
        self.play(FadeOut(big), FadeOut(cut1), FadeIn(p1), FadeIn(p2), run_time=0.4)
        self.play(p1.animate.shift(LEFT * 0.9), p2.animate.shift(RIGHT * 0.9), run_time=0.8)
        cap = txt("Kutub magnet tak dapat dipisahkan", S.SZ_HEAD, S.TEXT_SOFT).move_to([0, -1.5, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(0.5)

        # potong lagi: tiap potongan dipotong menjadi dua
        cut2a = DashedLine([-2.1, 1.3, 0], [-2.1, -0.3, 0], color=S.TEXT, stroke_width=3)
        cut2b = DashedLine([2.1, 1.3, 0], [2.1, -0.3, 0], color=S.TEXT, stroke_width=3)
        self.play(Create(cut2a), Create(cut2b), run_time=0.5)
        xs = [-3.15, -1.05, 1.05, 3.15]
        q = [bar_magnet(1.2, 1.0, label_size=26).move_to([x, 0.5, 0]) for x in xs]
        # posisi awal: dua pasang berdempetan di bekas potongan, lalu merenggang
        start_x = [-2.7, -1.5, 1.5, 2.7]
        for m, x0 in zip(q, start_x):
            m.move_to([x0, 0.5, 0])
        self.play(FadeOut(p1), FadeOut(p2), FadeOut(cut2a), FadeOut(cut2b),
                  *[FadeIn(m) for m in q], run_time=0.4)
        self.play(*[m.animate.move_to([x, 0.5, 0]) for m, x in zip(q, xs)], run_time=0.8)
        self.pad_to(17.4)
        self.play(FadeOut(VGroup(*q)), FadeOut(cap), run_time=0.6)

        # ================= 18–30 d : tiga jenis bahan =================
        self.pad_to(18.0)
        specs = [
            ("F", "Feromagnetik", "ditarik kuat", "besi, nikel, kobalt", "strong"),
            ("P", "Paramagnetik", "ditarik lemah", "aluminium, platina", "weak_in"),
            ("D", "Diamagnetik", "ditolak lemah", "tembaga, emas, air", "weak_out"),
        ]
        xs_card = [-4.7, 0.0, 4.7]
        cards, anims = [], []
        for (letter, name, desc, ex, kind), cx in zip(specs, xs_card):
            box = RoundedRectangle(corner_radius=0.2, width=4.2, height=4.4, fill_color=S.CARD,
                                   fill_opacity=1, stroke_color=S.CARD_EDGE, stroke_width=2)
            box.move_to([cx, -0.1, 0])
            dot = Circle(radius=0.26, fill_color=S.ACCENT, fill_opacity=1, stroke_width=0)
            dot.move_to([cx - 1.65, 1.6, 0])
            let = txt(letter, 24, S.BG, "BOLD").move_to(dot)
            nm = txt(name, 26, S.TEXT, "BOLD").next_to(dot, RIGHT, buff=0.2)
            ds = txt(desc, S.SZ_BODY, S.ACCENT, "BOLD").move_to([cx, 0.85, 0])
            exs = txt(ex, S.SZ_LABEL, S.TEXT_SOFT).move_to([cx, 0.3, 0])

            # animasi mini: magnet kecil (kiri) dan benda uji (kanan)
            mag = bar_magnet(1.4, 0.46, label_size=18).move_to([cx - 0.9, -1.0, 0])
            item_x0 = cx + 1.25
            item = Circle(radius=0.2, fill_color=S.MUTED, fill_opacity=1, stroke_width=0)
            item.move_to([item_x0, -1.0, 0])
            if kind == "strong":
                item_x1, arr_len, arr_dir = cx - 0.9 + 0.7 + 0.2, 1.0, -1   # menempel di kutub S
            elif kind == "weak_in":
                item_x1, arr_len, arr_dir = item_x0 - 0.18, 0.4, -1
            else:
                item_x1, arr_len, arr_dir = item_x0 + 0.18, 0.4, +1
            ay = -1.75
            f = labeled_arrow([item_x0 if arr_dir < 0 else item_x0 - 0.3, ay, 0],
                              [(item_x0 if arr_dir < 0 else item_x0 - 0.3) + arr_dir * arr_len, ay, 0],
                              "F", FORCE)
            static = VGroup(box, dot, let, nm, ds, exs, mag, item)
            cards.append((static, f, item, item_x1))

        for k, (static, f, item, x1) in enumerate(cards):
            self.play(FadeIn(static), run_time=0.6)
            self.play(FadeIn(f), run_time=0.3)
            self.play(item.animate.set_x(x1), run_time=1.2 if k == 0 else 1.0)
            if k < 2:
                self.pad_to([21.8, 25.0][k])
        self.pad_to(S.SCENE_DURATIONS[SCENE_ID])

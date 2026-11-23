"""Komponen visual reusable."""
import numpy as np
from manim import (
    VGroup, Rectangle, RoundedRectangle, Circle, Ellipse, Dot, Line, Text, Triangle,
    CubicBezier, Arrow, DashedLine, MathTex, Scene, TexTemplate, DOWN, UP, LEFT, RIGHT,
    angle_of_vector, config,
)
from . import style as S

# Template LaTeX: font matematika sans-serif agar serasi dengan teks.
SANS_TEX = TexTemplate()
SANS_TEX.add_to_preamble(r"\usepackage{sansmath}\sansmath")


class BaseScene(Scene):
    """Dasar semua scene: terapkan tema dan sediakan pengatur durasi."""

    def setup(self):
        S.apply_theme(self)

    def pad_to(self, seconds: float):
        """Tahan layar hingga scene mencapai waktu `seconds` (sesuai storyboard).
        Dihitung dalam satuan frame agar tidak ada selisih pembulatan.
        Jika animasi sudah melewati target, beri peringatan di konsol."""
        fps = config.frame_rate
        frames = round((seconds - self.renderer.time) * fps)
        if frames > 0:
            # Jeda statis di Manim dibulatkan ke BAWAH (int(durasi * fps)), jadi tambahkan
            # 1/4 frame agar hasilnya tepat `frames` dan tahan terhadap derau floating-point.
            # (renderer.time dihitung per frame, jadi pembacaan waktu tetap akurat.)
            self.wait((frames + 0.25) / fps)
        elif frames < 0:
            print(f"[PERINGATAN] {type(self).__name__} melebihi target "
                  f"{seconds:.1f} d (aktual {self.renderer.time:.1f} d)")


def txt(s, size=S.SZ_BODY, color=S.TEXT, weight="NORMAL", **kw):
    return Text(s, font=S.FONT, font_size=size, color=color, weight=weight, **kw)


def formula(tex, color=S.TEXT, size=S.SZ_FORMULA):
    return MathTex(tex, color=color, font_size=size, tex_template=SANS_TEX)


def u_s_badge(w=0.9, h=0.4):
    """Lencana [U | S] seperti di pojok slide PPT."""
    u = Rectangle(width=w, height=h, fill_color=S.NORTH, fill_opacity=1, stroke_width=0)
    s = Rectangle(width=w, height=h, fill_color=S.SOUTH, fill_opacity=1, stroke_width=0)
    s.next_to(u, RIGHT, buff=0)
    lu = txt("U", 20, S.BG, "BOLD").move_to(u)
    ls = txt("S", 20, S.BG, "BOLD").move_to(s)
    return VGroup(u, s, lu, ls)


def bar_magnet(width=S.MAGNET_W, height=S.MAGNET_H, flipped=False, label_size=S.SZ_HEAD):
    """Magnet batang: U (merah) di kiri, S (biru) di kanan.
    flipped=True menukar sisi (S di kiri, U di kanan) tanpa membalik huruf."""
    half = width / 2
    left_c, right_c = (S.SOUTH, S.NORTH) if flipped else (S.NORTH, S.SOUTH)
    left_l, right_l = ("S", "U") if flipped else ("U", "S")
    a = Rectangle(width=half, height=height, fill_color=left_c, fill_opacity=1, stroke_width=0)
    b = Rectangle(width=half, height=height, fill_color=right_c, fill_opacity=1, stroke_width=0)
    a.move_to(LEFT * half / 2)
    b.move_to(RIGHT * half / 2)
    la = txt(left_l, label_size, S.BG, "BOLD").move_to(a)
    lb = txt(right_l, label_size, S.BG, "BOLD").move_to(b)
    return VGroup(a, b, la, lb)


def _tip_on(curve, alpha, color, size=0.16):
    """Kepala panah kecil pada posisi alpha (0..1) sepanjang kurva."""
    p = curve.point_from_proportion(alpha)
    q = curve.point_from_proportion(min(alpha + 0.01, 1))
    tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(size)
    tip.rotate(angle_of_vector(q - p) - np.pi / 2)  # Triangle default menghadap atas
    tip.move_to(p)
    return tip


tip_on = _tip_on  # alias publik


def magnet_field_lines(width=S.MAGNET_W, spread=(0.9, 1.7, 2.5)):
    """Garis medan: di luar magnet dari U (kiri) ke S (kanan); di dalam dari S ke U.
    Garis tidak berpotongan."""
    half = width / 2
    group = VGroup()
    for k in spread:
        for sign in (+1, -1):
            c = CubicBezier(
                np.array([-half, 0, 0]),
                np.array([-half - k * 0.9, sign * k * 1.3, 0]),
                np.array([half + k * 0.9, sign * k * 1.3, 0]),
                np.array([half, 0, 0]),
                stroke_color=S.FIELD, stroke_width=S.STROKE_THIN,
            )
            group.add(c, _tip_on(c, 0.5, S.FIELD))
    for y in (0.27, -0.27):  # putih agar terlihat di atas warna magnet
        ln = Line([half * 0.9, y, 0], [-half * 0.9, y, 0],
                  stroke_color=S.TEXT, stroke_width=S.STROKE_THIN)
        group.add(ln, _tip_on(ln, 0.5, S.TEXT, 0.14))
    return group


def wire_cross_section(direction="out", radius=0.28):
    """Penampang kawat: ⊙ (arus keluar layar) atau ⊗ (masuk layar)."""
    ring = Circle(radius=radius, stroke_color=S.CURRENT, stroke_width=S.STROKE,
                  fill_color=S.CARD, fill_opacity=1)
    if direction == "out":
        mark = Dot(radius=radius * 0.3, color=S.CURRENT)
    else:
        d = radius * 0.45
        mark = VGroup(
            Line([-d, -d, 0], [d, d, 0], stroke_color=S.CURRENT, stroke_width=S.STROKE),
            Line([-d, d, 0], [d, -d, 0], stroke_color=S.CURRENT, stroke_width=S.STROKE),
        )
    return VGroup(ring, mark)


def circular_field(radius=1.4, ccw=True, color=S.FIELD):
    """Lingkaran medan di sekitar kawat (ccw=True untuk arus ⊙, False untuk ⊗)."""
    c = Circle(radius=radius, stroke_color=color, stroke_width=S.STROKE_THIN)
    tips = VGroup()
    for alpha in (0.0, 0.25, 0.5, 0.75):
        p = c.point_from_proportion(alpha)
        q = c.point_from_proportion((alpha + 0.01) % 1)
        v = (q - p) if ccw else (p - q)
        tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.14)
        tip.rotate(angle_of_vector(v) - np.pi / 2).move_to(p)
        tips.add(tip)
    return VGroup(c, tips)


def labeled_arrow(start, end, label, color=S.FIELD, label_dir=UP, size=S.SZ_LABEL):
    """Panah vektor berlabel (semua vektor wajib berlabel)."""
    a = Arrow(start, end, buff=0, color=color, stroke_width=S.STROKE,
              max_tip_length_to_length_ratio=0.25)
    t = txt(label, size, color, "BOLD").next_to(a, label_dir, buff=0.12)
    return VGroup(a, t)


def info_card(title, lines, accent=S.ACCENT, width=5.6, line_size=S.SZ_LABEL):
    """Kartu bergaya PPT: judul berwarna + baris keterangan."""
    head = txt(title, S.SZ_BODY, accent, "BOLD")
    body = VGroup(*[txt(l, line_size, S.TEXT_SOFT) for l in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.14)
    content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    box = RoundedRectangle(corner_radius=0.18, width=max(width, content.width + 0.6),
                           height=content.height + 0.6, fill_color=S.CARD, fill_opacity=1,
                           stroke_color=S.CARD_EDGE, stroke_width=2)
    content.move_to(box)
    return VGroup(box, content)


def coil_side_view(n_loops=6, length=2.4, height=0.9, color=S.CURRENT):
    """Kumparan/solenoida tampak samping: deretan lilitan (elips) berwarna arus."""
    loops = VGroup()
    for i in range(n_loops):
        x = -length / 2 + length * i / (n_loops - 1)
        e = Ellipse(width=0.28, height=height, stroke_color=color,
                    stroke_width=S.STROKE_THIN + 0.5, fill_opacity=0)
        e.move_to([x, 0, 0])
        loops.add(e)
    return loops


def solenoid_front(n_turns=6, length=2.4, height=1.2, color=S.CURRENT, direction="right", show_current=True):
    """Solenoida tampak samping dengan arah arus.
    Lilitan depan (utuh) dan lilitan belakang (putus-putus, samar).
    direction="right": arus ke BAWAH di sisi depan  =>  (tangan kanan) B menuju KANAN (+x).
    direction="left" : arus ke ATAS di sisi depan   =>  B menuju KIRI (-x).
    show_current=False: tanpa tanda panah arus (kumparan tanpa arus)."""
    dx = length / n_turns
    slant = dx * 0.5
    group = VGroup()
    xs = [-length / 2 + dx * (i + 0.5) for i in range(n_turns)]
    for i, x in enumerate(xs):
        if i + 1 < n_turns:  # lilitan belakang: dari dasar lilitan i ke puncak lilitan i+1
            group.add(DashedLine([x + slant / 2, -height / 2, 0], [xs[i + 1] - slant / 2, height / 2, 0],
                                 color=color, stroke_width=2, stroke_opacity=0.35))
    for x in xs:  # lilitan depan
        top, bot = np.array([x - slant / 2, height / 2, 0]), np.array([x + slant / 2, -height / 2, 0])
        ln = Line(top, bot, stroke_color=color, stroke_width=S.STROKE)
        group.add(ln)
        if show_current:
            tip_line = Line(top, bot) if direction == "right" else Line(bot, top)
            group.add(tip_on(tip_line, 0.5, color, 0.12))
    return group


def field_cross(radius=0.14, color=S.FIELD, width=2.2):
    """Simbol ⊗: vektor menuju masuk ke bidang layar (dipakai untuk B masuk layar)."""
    d = radius * 0.62
    ring = Circle(radius=radius, stroke_color=color, stroke_width=width, fill_opacity=0)
    a = Line([-d, -d, 0], [d, d, 0], stroke_color=color, stroke_width=width)
    b = Line([-d, d, 0], [d, -d, 0], stroke_color=color, stroke_width=width)
    return VGroup(ring, a, b)


def problem_card(title, color, items, width, title_size=24):
    """Kartu gaya PPT (Diketahui/Ditanya/Penyelesaian): kembalikan VGroup(box, head, body).
    `items` = daftar mobject baris; body dapat dimunculkan bertahap (LaggedStart)."""
    head = txt(title, title_size, color, "BOLD")
    body = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    box = RoundedRectangle(corner_radius=0.16, width=width, height=content.height + 0.5,
                           fill_color=S.CARD, fill_opacity=1, stroke_color=S.CARD_EDGE, stroke_width=2)
    content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.3)
    return VGroup(box, head, body)

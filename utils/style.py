"""Satu-satunya tempat konfigurasi warna, font, ukuran, dan durasi scene."""
from manim import config, ManimColor

# ---- Warna (diambil dari PPT agar konsisten) ----
BG        = "#0B1530"   # latar navy
CARD      = "#13224A"   # panel/kartu
CARD_EDGE = "#2A4580"   # tepi kartu
TEXT      = "#FFFFFF"   # teks utama
TEXT_SOFT = "#DCE6F7"   # teks sekunder
MUTED     = "#9FB2D6"   # label redup

FIELD     = "#3DA5FF"   # medan magnet / kutub S
CURRENT   = "#FF9F43"   # arus listrik
NORTH     = "#FF4D5A"   # kutub U / arah penting
SOUTH     = FIELD
ACCENT    = "#FFC857"   # judul / hasil akhir
OK        = "#2EC4B6"   # "Penyelesaian"
METAL     = "#B8C2D6"   # logam / benda uji (paku, sampel)
FORCE     = ACCENT      # panah gaya (F)

# ---- Font ----
FONT_PREFERRED = ["Inter", "Segoe UI", "Calibri", "Helvetica Neue", "Arial", "DejaVu Sans"]

def pick_font() -> str:
    """Pilih font pertama yang tersedia di sistem."""
    try:
        import manimpango
        available = set(manimpango.list_fonts())
        for f in FONT_PREFERRED:
            if f in available:
                return f
    except Exception:
        pass
    return "sans-serif"

FONT = pick_font()

# ---- Ukuran teks (skala 1080p) ----
SZ_TITLE, SZ_HEAD, SZ_BODY, SZ_LABEL, SZ_FORMULA = 44, 32, 26, 22, 44

# ---- Garis & objek ----
STROKE, STROKE_THIN = 4, 2.5
MAGNET_W, MAGNET_H = 3.2, 0.9

# ---- Durasi target tiap scene (detik), sesuai storyboard Phase 2 (revisi) ----
SCENE_DURATIONS = {
    1: 12, 2: 30, 3: 35, 4: 30, 5: 35, 6: 48, 7: 45, 8: 25, 9: 20,
}  # total 280 d = 4:40

# Latar diterapkan saat modul diimpor (sebelum renderer dibuat).
config.background_color = ManimColor(BG)

def apply_theme(scene=None):
    """Pastikan kamera memakai latar navy (dipanggil dari BaseScene.setup)."""
    if scene is not None:
        scene.camera.background_color = ManimColor(BG)

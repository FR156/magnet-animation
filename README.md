# Magnet dan Elektromagnetik — Video Animasi (Manim Community Edition)

Video edukasi Fisika Dasar, target durasi 4:40, 1920×1080, 30 FPS.
Sumber materi: `Magnet_dan_Elektromagnetik.pptx` (Kelompok 10).

Diuji dengan: Python 3.12.3, Manim CE 0.22.1, ManimPango 0.7.1, FFmpeg, TeX Live.

## 1. Instalasi

### Dependensi sistem
Manim CE membutuhkan: **FFmpeg**, **Pango/Cairo**, dan **LaTeX** (untuk rumus).
Paket LaTeX yang dipakai project ini: `standalone`, `amsmath`, `sansmath` (bagian dari
`latex-extra`), serta `dvisvgm`.

| Sistem | Perintah |
|---|---|
| Ubuntu/Debian | `sudo apt install ffmpeg libpango1.0-dev libcairo2-dev pkg-config python3-dev texlive texlive-latex-extra texlive-fonts-recommended dvisvgm` |
| macOS (Homebrew) | `brew install ffmpeg pango pkg-config cairo` lalu pasang MacTeX (`brew install --cask mactex-no-gui`) |
| Windows | Pasang FFmpeg dan MiKTeX (izinkan pemasangan paket otomatis). Pango biasanya sudah tercakup roda (wheel) Manim. |

Panduan resmi: https://docs.manim.community/en/stable/installation.html

### Dependensi Python
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Font (opsional)
Teks memakai font pertama yang tersedia dari: Inter, Segoe UI, Calibri, Helvetica Neue,
Arial, DejaVu Sans. Pasang **Inter** (gratis) untuk tampilan terbaik.

## 2. Perintah render

Semua perintah dijalankan dari folder project.

```bash
python main.py list                 # daftar scene
python main.py test                 # tes perhitungan fisika (semua contoh soal PPT)

python main.py render 3             # preview scene 3 (854x480, 15 FPS)
python main.py render 3 -q medium   # 1280x720, 30 FPS
python main.py render 3 -q final    # 1920x1080, 30 FPS

python main.py all -q final         # semua scene, satu per satu
python main.py concat -q final      # gabung hasil render (tanpa audio)
```

Hasil: `renders/videos/<nama_scene>/<resolusi><fps>/<Kelas>.mp4`;
gabungan: `renders/magnet_<kualitas>_tanpa_audio.mp4`.

> **Catatan FPS:** flag `-qh` bawaan Manim merender 1080p **60 FPS**. Karena target kita
> 30 FPS, kualitas `final` memakai `-r 1920,1080 --fps 30`.

### Render langsung dengan manim (tanpa main.py)
```bash
manim -ql scenes/scene_03_magnetic_field.py Scene03MagneticField
manim -r 1920,1080 --fps 30 scenes/scene_03_magnetic_field.py Scene03MagneticField
```

## 3. Struktur

```
magnet-animation/
├── assets/audio, assets/images     # voice-over dan gambar (isi di Phase 6)
├── scenes/                         # 9 scene, masing-masing dapat dirender mandiri
├── utils/
│   ├── style.py                    # warna, font, ukuran, DURASI TARGET tiap scene
│   ├── components.py               # komponen reusable + BaseScene
│   └── physics.py                  # perhitungan fisika (tanpa Manim)
├── tests/test_physics.py           # tes semua contoh soal PPT
├── renders/                        # hasil render (tidak masuk git)
├── main.py                         # pengelola render
└── requirements.txt
```

## 4. Konvensi

- Warna/font/ukuran hanya diubah di `utils/style.py`.
- Durasi tiap scene di `SCENE_DURATIONS` (`style.py`); tiap scene memanggil
  `self.pad_to(...)` di akhir agar durasinya sesuai storyboard.
- Setiap scene memulai dengan `sys.path.insert(...)` agar `utils` dapat diimpor
  saat dirender langsung.
- Warna: biru = medan magnet / kutub S, oranye = arus, merah = kutub U / arah penting,
  emas = hasil akhir.

## 5. Status

| Phase | Status |
|---|---|
| 1–3 Analisis, storyboard, design system | Selesai |
| 4 Setup project | Selesai |
| 5 Pengembangan scene 1–9 | Selesai (semua dirender 1920×1080, 30 FPS; total 280 d = 4:40) |
| 6 Perakitan akhir | Video gabungan tanpa audio tersedia. Voice-over dan subtitle menunggu persetujuan naskah (`narration/naskah_narasi.md`) |

## 6. Catatan teknis

- Render **berurutan**, jangan paralel: cache LaTeX/teks di `renders/` dipakai bersama dan dapat rusak
  (muncul `ParseError: no element found`). Jika terjadi, hapus file `*.svg` berukuran 0 di `renders/`.
- `main.py` memakai `--disable_caching` agar jumlah frame tiap scene selalu tepat.
- Durasi tiap scene tepat sesuai `SCENE_DURATIONS` (frame: 360, 900, 1050, 900, 1050, 1440, 1350, 750, 600).

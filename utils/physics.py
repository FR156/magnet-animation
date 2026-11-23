"""Perhitungan fisika murni (tanpa Manim). Semua rumus sesuai PPT."""
import math

MU0 = 4 * math.pi * 1e-7  # Wb/A.m

# --- Induksi magnet (slide 3) ---
def b_wire(i, a):               return MU0 * i / (2 * math.pi * a)
def b_loop_center(i, n, a):     return MU0 * i * n / (2 * a)
def b_solenoid_center(i, n, l): return MU0 * i * n / l
def b_solenoid_end(i, n, l):    return MU0 * i * n / (2 * l)
def b_toroid(i, n, r):          return MU0 * i * n / (2 * math.pi * r)

# --- Gaya Lorentz (slide 5) ---
def f_wire(b, i, l, theta_deg=90):
    return b * i * l * math.sin(math.radians(theta_deg))
def f_charge(q, v, b, theta_deg=90):
    return q * v * b * math.sin(math.radians(theta_deg))
def f_per_length_parallel(i1, i2, a):
    return MU0 * i1 * i2 / (2 * math.pi * a)
def radius_circular(m, v, q, b):
    return m * v / (q * b)

# --- Induksi elektromagnetik (slide 7) ---
def flux(b, area, theta_deg=0):
    return b * area * math.cos(math.radians(theta_deg))
def emf_faraday(n, d_phi, dt):
    return -n * d_phi / dt
def emf_motional(b, l, v, theta_deg=90):
    return b * l * v * math.sin(math.radians(theta_deg))

# --- Generator & transformator (slide 9) ---
def emf_generator(n, b, area, omega, t):
    return n * b * area * omega * math.sin(omega * t)
def trafo_vs(vp, np_, ns):  return vp * ns / np_
def trafo_ns(vp, vs, np_):  return np_ * vs / vp
def power(v, i):            return v * i
def efficiency(ps, pp):     return ps / pp * 100


# --- Format tampilan ---
def sci_notation(value, decimals=0):
    """Pecah angka menjadi (mantissa, eksponen) dengan koma desimal gaya Indonesia.
    sci_notation(1e-5, 0) -> ("1", -5);  sci_notation(5.0265e-3, 1) -> ("5,0", -3)."""
    exp = math.floor(math.log10(abs(value)))
    mant = value / 10 ** exp
    return f"{mant:.{decimals}f}".replace(".", ","), exp

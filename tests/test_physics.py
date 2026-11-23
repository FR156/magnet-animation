"""Cek semua contoh soal PPT. Jalankan: python -m unittest discover tests"""
import unittest
from utils import physics as P


class TestPPTExamples(unittest.TestCase):
    def test_b_wire(self):       self.assertAlmostEqual(P.b_wire(5, 0.1), 1e-5, places=12)
    def test_b_solenoid(self):   self.assertAlmostEqual(P.b_solenoid_center(2, 500, 0.25), 5.0265e-3, places=6)
    def test_f_wire(self):       self.assertAlmostEqual(P.f_wire(0.2, 4, 0.5), 0.4)
    def test_f_electron(self):   self.assertAlmostEqual(P.f_charge(1.6e-19, 2e6, 0.5), 1.6e-13, places=20)
    def test_emf_motional(self): self.assertAlmostEqual(P.emf_motional(0.4, 0.5, 10), 2.0)
    def test_trafo_vs(self):     self.assertAlmostEqual(P.trafo_vs(220, 1000, 200), 44.0)

    def test_efficiency(self):
        pp, ps = P.power(220, 0.5), P.power(44, 2)
        self.assertAlmostEqual(pp, 110.0)
        self.assertAlmostEqual(ps, 88.0)
        self.assertAlmostEqual(P.efficiency(ps, pp), 80.0)

    # Soal latihan (slide 11): kunci jawaban hitungan sendiri, bukan dari PPT
    def test_latihan_1(self):    self.assertAlmostEqual(P.b_wire(10, 0.02), 1e-4, places=12)
    def test_latihan_2(self):    self.assertAlmostEqual(P.f_wire(0.4, 5, 0.2, 30), 0.2)
    def test_latihan_3(self):    self.assertAlmostEqual(P.trafo_ns(220, 11, 2000), 100.0)

    def test_sci_notation(self):
        self.assertEqual(P.sci_notation(P.b_wire(5, 0.1), 0), ("1", -5))
        self.assertEqual(P.sci_notation(P.b_solenoid_center(2, 500, 0.25), 1), ("5,0", -3))


if __name__ == "__main__":
    unittest.main()

import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)
        self.varasto2 = Varasto(-15, -3)  # Tilavuus ja saldo virheelliset
        self.varasto3 = Varasto(8, 10)  # Saldoa enemmän kuin tilavuus

    def test_konstruktori_nollaa_virheellisen_tilavuuden(self):
        self.assertAlmostEqual(self.varasto2.tilavuus, 0)

    def test_konstruktori_nollaa_virheellisen_saldon(self):
        self.assertAlmostEqual(self.varasto2.saldo, 0)

    def test_konstruktori_rajoittaa_saldon_tilavuuteen(self):
        self.assertAlmostEqual(self.varasto3.tilavuus, 8)
        # Tilavuus täyteen, loput saldosta hukkaan
        self.assertAlmostEqual(self.varasto3.saldo, 8)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisaysta_ei_tehda_jos_maara_on_virheellinen(self):
        self.varasto.lisaa_varastoon(-5)  # Yritetään lisätä negatiivinen määrä
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_saldoa_vain_tayteen_asti(self):
        # Yritetään lisätä varastoon enemmän kuin siellä on tilaa
        # Lisätään 15, kun tilavuun on vain 10
        self.varasto.lisaa_varastoon(15)
        self.assertAlmostEqual(self.varasto.saldo, 10)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_negatiivista_maaraa_ei_voida_ottaa(self):
        self.varasto.lisaa_varastoon(8)
        self.varasto.ota_varastosta(-10)
        self.assertAlmostEqual(self.varasto.saldo, 8)  # Edelleen 8

    def test_voidaan_ottaa_korkeintaan_saldon_verran(self):
        self.varasto.lisaa_varastoon(8)
        saatu_maara = self.varasto.ota_varastosta(15)

        self.assertAlmostEqual(saatu_maara, 8)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_str(self):
        self.varasto.lisaa_varastoon(7)
        varasto_str = self.varasto.__str__()
        self.assertEqual(varasto_str, "saldo = 7, vielä tilaa 3")

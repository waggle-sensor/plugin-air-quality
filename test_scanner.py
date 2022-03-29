import unittest
from scanner import Scanner, compute_checksum
from io import BytesIO
from random import uniform, randint


class DataGenerator:

    def readline(self):
        self.conc = uniform(0, 100)
        self.flow = uniform(0, 10)
        self.temp = uniform(-40, 120)
        rh = randint(0, 999)
        self.rh = rh/100
        self.bp = uniform(900, 1100)
        self.status = randint(0, 99)
        line = f"{self.conc},{self.flow},{self.temp},{rh},{self.bp},{self.status},".encode()
        checksum = compute_checksum(line)
        line += f"*{checksum:04d}\n".encode()
        return line


class TestParse(unittest.TestCase):
    
    def test_read(self):
        test_cases = [
            {
                "data": b"000.000,2.0,+20.9,029,0980.1,00,*01541",
                "values": {
                    "conc": 0.0,
                    "flow": 2.0,
                    "temp": 20.9,
                    "rh": 0.29,
                    "bp": 980.1,
                    "status": 0,
                }
            },
            {
                "data": b"""Conc(mg/m3),Flow(lpm),Temp(C),RH(%),BP(mbar),Status
000.000,2.0,+20.9,029,0980.1,00,*01541
""",
                "values": {
                    "conc": 0.0,
                    "flow": 2.0,
                    "temp": 20.9,
                    "rh": 0.29,
                    "bp": 980.1,
                    "status": 0,
                }
            },
            {
                "data": b"""
000.000,2.0,+20.9,029,0980.1,00,*01541
""",
                "values": {
                    "conc": 0.0,
                    "flow": 2.0,
                    "temp": 20.9,
                    "rh": 0.29,
                    "bp": 980.1,
                    "status": 0,
                }
            },
            {
                "data": b"""
001.000,3.0,+22.9,030,0980.1,00,*01541
000.000,2.0,+20.9,029,0980.1,00,*01541
""",
                "values": {
                    "conc": 0.0,
                    "flow": 2.0,
                    "temp": 20.9,
                    "rh": 0.29,
                    "bp": 980.1,
                    "status": 0,
                }
            },
        ]

        for tc in test_cases:
            scanner = Scanner(BytesIO(tc["data"]))
            self.assertTrue(scanner.scan())

            self.assertAlmostEqual(scanner.conc, tc["values"]["conc"])
            self.assertAlmostEqual(scanner.flow, tc["values"]["flow"])
            self.assertAlmostEqual(scanner.temp, tc["values"]["temp"])
            self.assertAlmostEqual(scanner.rh, tc["values"]["rh"])
            self.assertAlmostEqual(scanner.bp, tc["values"]["bp"])
            self.assertAlmostEqual(scanner.status, tc["values"]["status"])

    def test_eof(self):
        test_cases = [
            b"",
            b"\n",
            b"\n\n\n",
            b"Conc(mg/m3),Flow(lpm),Temp(C),RH(%),BP(mbar),Status", # bad line
            b"000.000,2.0,+20.9,029,0980.1,00,*01542", # bad checksum
        ]

        for tc in test_cases:
            scanner = Scanner(BytesIO(tc))
            self.assertFalse(scanner.scan())
    
    def test_fuzz(self):
        for _ in range(10000):
            gen = DataGenerator()
            scanner = Scanner(gen)
            
            self.assertTrue(scanner.scan())

            self.assertAlmostEqual(scanner.conc, gen.conc)
            self.assertAlmostEqual(scanner.flow, gen.flow)
            self.assertAlmostEqual(scanner.temp, gen.temp)
            self.assertAlmostEqual(scanner.rh, gen.rh)
            self.assertAlmostEqual(scanner.bp, gen.bp)
            self.assertAlmostEqual(scanner.status, gen.status)


if __name__ == "__main__":
    unittest.main()

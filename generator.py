from random import uniform, randint
from scanner import compute_checksum


class Generator:
    """
    Generator implements a reader which generates and stores random values and
    lines of data for testing.
    """

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

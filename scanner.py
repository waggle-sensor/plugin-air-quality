class Scanner:

    conc: float
    flow: float
    temp: float
    rh: float
    bp: float
    status: int

    def __init__(self, reader):
        self.reader = reader
    
    def scan(self) -> bool:
        while True:
            line = self.reader.readline()
            if line == b"":
                return False

            if not valid_checksum(line):
                continue

            fields = line.split(b",", maxsplit=6)
            if len(fields) != 7:
                continue

            try:
                self.conc = float(fields[0])
                self.flow = float(fields[1])
                self.temp = float(fields[2])
                self.rh = float(fields[3])/100.0
                self.bp = float(fields[4])
                self.status = int(fields[5])
            except ValueError:
                continue

            return True


def valid_checksum(data: bytes) -> bool:
    fields = data.split(b"*", maxsplit=2)

    if len(fields) != 2:
        return False

    try:
        checksum = int(fields[1])
    except ValueError:
        return False

    return compute_checksum(fields[0]) == checksum


def compute_checksum(data: bytes) -> int:
    return sum(data)

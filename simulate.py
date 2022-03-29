import argparse
from generator import Generator
from scanner import Scanner
import time
import logging
from waggle.plugin import Plugin
from main import scan_and_publish


class SlowGenerator:

    def __init__(self):
        self.gen = Generator()

    def readline(self):
        time.sleep(0.2)
        return self.gen.readline()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="enable debug logs")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    with Plugin() as plugin:
        scanner = Scanner(SlowGenerator())
        scan_and_publish(scanner, plugin)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

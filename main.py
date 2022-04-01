import argparse
from waggle.plugin import Plugin, get_timestamp
from scanner import Scanner
from serial import Serial
import logging
import time


def scan_and_publish(scanner, plugin):
    while scanner.scan():
        timestamp = get_timestamp()

        logging.info("publishing conc=%0.3f flow=%0.1f temp=%0.2f rh=%0.2f bp=%0.1f status=%d",
            scanner.conc,
            scanner.flow,
            scanner.temp,
            scanner.rh,
            scanner.bp,
            scanner.status)

        # TODO(sean) use standard ontology where it makes sense or standardize on one
        plugin.publish("env.air_quality.conc", scanner.conc, timestamp=timestamp)
        plugin.publish("env.air_quality.flow", scanner.flow, timestamp=timestamp)
        plugin.publish("env.air_quality.temp", scanner.temp, timestamp=timestamp)
        plugin.publish("env.air_quality.rh", scanner.rh, timestamp=timestamp)
        plugin.publish("env.air_quality.bp", scanner.bp, timestamp=timestamp)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="enable debug logs")
    parser.add_argument("--device", default="/dev/ttyUSB0", help="serial device to use")
    parser.add_argument("--baudrate", default=9600, type=int, help="baudrate to use")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    with Plugin() as plugin:
        while True:
            logging.info("opening serial device %s @ %s", args.device, args.baudrate)
            with Serial(args.device, baudrate=args.baudrate, timeout=3.0) as dev:
                scanner = Scanner(dev)
                logging.info("started scanning")
                scan_and_publish(scanner, plugin)
                logging.info("stopped scanning")
            time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

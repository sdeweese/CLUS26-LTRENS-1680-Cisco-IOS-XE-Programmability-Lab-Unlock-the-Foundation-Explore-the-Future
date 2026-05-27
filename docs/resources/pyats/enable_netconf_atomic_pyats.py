#!/usr/bin/env python3
"""Enable NETCONF candidate datastore and atomic config on IOS XE via pyATS."""

import argparse
import sys

from pyats.topology import loader


CONFIG_LINES = [
    "netconf-yang",
    "netconf-yang feature candidate-datastore",
    "yang-interfaces feature atomic-config",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Configure NETCONF candidate and atomic config features using pyATS"
    )
    parser.add_argument(
        "--testbed",
        required=True,
        help="Path to testbed YAML file",
    )
    parser.add_argument(
        "--device",
        default="c9300x-lab",
        help="Device name in testbed YAML (default: c9300x-lab)",
    )
    parser.add_argument(
        "--write-memory",
        action="store_true",
        help="Save running-config to startup-config after applying changes",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    testbed = loader.load(args.testbed)
    if args.device not in testbed.devices:
        print(f"ERROR: Device '{args.device}' not found in testbed file {args.testbed}")
        return 2

    device = testbed.devices[args.device]

    print(f"Connecting to {args.device}...")
    device.connect(log_stdout=False)

    try:
        print("Applying configuration...")
        result = device.configure(CONFIG_LINES)
        print(result)

        if args.write_memory:
            print("Saving configuration (write memory)...")
            print(device.execute("write memory"))

        print("Verifying running config...")
        print(device.execute("show running-config | section netconf-yang"))
        print(device.execute("show running-config | include atomic-config"))

    finally:
        device.disconnect()
        print("Disconnected.")

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Ensure NETCONF candidate datastore and atomic config are enabled on IOS XE via pyATS.

Default behavior (idempotent APPLY):
- If any required lines are missing, apply the missing ones.
- If all required lines are already present, make no changes.

Destructive opt-in:
- Pass --remove to unconfigure all feature lines. Use with care: this disables
  NETCONF and will break Terraform, Ansible ACR, gNMI, and other tools that rely
  on it.
"""

import argparse
import sys

from pyats.topology import loader


CONFIG_LINES = [
    "netconf-yang",
    "netconf-yang feature candidate-datastore",
    "yang-interfaces feature atomic-config",
]

REMOVE_LINES = [
    "no yang-interfaces feature atomic-config",
    "no netconf-yang feature candidate-datastore",
    "no netconf-yang",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ensure NETCONF candidate and atomic config features are enabled (idempotent APPLY by default)"
    )
    parser.add_argument(
        "--testbed",
        required=True,
        help="Path to testbed YAML file",
    )
    parser.add_argument(
        "--device",
        default="c9300-lab",
        help="Device name in testbed YAML (default: c9300-lab)",
    )
    parser.add_argument(
        "--write-memory",
        action="store_true",
        help="Save running-config to startup-config after applying changes",
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Destructive: unconfigure all feature lines (disables NETCONF; breaks Terraform/Ansible/gNMI)",
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
        print("Collecting current device state...")
        netconf_section = device.execute("show running-config | section netconf-yang")
        atomic_line = device.execute("show running-config | include atomic-config")
        current_output = f"{netconf_section}\n{atomic_line}".lower()

        line_state = {line: (line in current_output) for line in CONFIG_LINES}
        for line, present in line_state.items():
            status = "PRESENT" if present else "MISSING"
            print(f"[STATE] {status}: {line}")

        all_present = all(line_state.values())

        if args.remove:
            if not all_present:
                print("[OPERATION] SKIP: --remove requested but not all lines are present; nothing to remove.")
                result = ""
            else:
                print("[OPERATION] UNCONFIGURE (--remove): removing all feature lines.")
                print("[WARNING] This disables NETCONF and will break Terraform/Ansible/gNMI workflows.")
                result = device.configure(REMOVE_LINES)
        elif all_present:
            print("[OPERATION] NOOP: all required lines already present. No changes made.")
            print("           (Pass --remove to explicitly unconfigure.)")
            result = ""
        else:
            missing_lines = [line for line, present in line_state.items() if not present]
            print("[OPERATION] APPLY: one or more required lines are missing.")
            print(f"[OPERATION] Applying {len(missing_lines)} line(s).")
            result = device.configure(missing_lines)

        if result:
            print(result)

        if args.write_memory:
            print("Saving configuration (write memory)...")
            print(device.execute("write memory"))

        print("Verifying running config after operation...")
        print(device.execute("show running-config | section netconf-yang"))
        print(device.execute("show running-config | include atomic-config"))

    finally:
        device.disconnect()
        print("Disconnected.")

    return 0


if __name__ == "__main__":
    sys.exit(main())

# PyATS Testing

## Automated Testing with Cisco PyATS

Use this section to apply required Day 1 platform features with a single PyATS script.

## Goal

Configure the following on the C9300X lab switch (`10.1.1.5`):

```text
netconf-yang
netconf-yang feature candidate-datastore
yang-interfaces feature atomic-config
```

## Prerequisites

1. PyATS/Unicon installed in your active Python environment.
2. SSH reachability to `10.1.1.5`.
3. Credentials for `c9300x-lab` (default lab values: `admin` / `Cisco123`).

## Testbed Example

Create `testbed.yaml`:

```yaml
testbed:
  name: iosxe-lab

devices:
  c9300x-lab:
	os: iosxe
	type: switch
	connections:
	  cli:
		protocol: ssh
		ip: 10.1.1.5
	credentials:
	  default:
		username: admin
		password: Cisco123
```

## Single PyATS Script

Save as `enable_netconf_atomic_pyats.py`:

```python
#!/usr/bin/env python3
"""Enable NETCONF candidate datastore + atomic config on IOS XE via pyATS."""

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
		description="Configure NETCONF candidate + atomic config features using pyATS"
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
```

## Run It

```bash
python3 enable_netconf_atomic_pyats.py --testbed testbed.yaml --device c9300x-lab --write-memory
```

## Validation Commands on Device

```text
show running-config | section netconf-yang
show running-config | include atomic-config
```

Expected lines present:

```text
netconf-yang
netconf-yang feature candidate-datastore
yang-interfaces feature atomic-config
```

---

## Next Steps

✅ Completed: Day 1 - PyATS Testing

**Ready for Day 2?**

➡️ [Day 2: Device Monitoring Overview](../day-2/index.md) - Learn OpenTelemetry and gNXI

**Or return to:**
- [Day 1 Overview](index.md)
- [Atomic Config Replace](atomic-operations.md)

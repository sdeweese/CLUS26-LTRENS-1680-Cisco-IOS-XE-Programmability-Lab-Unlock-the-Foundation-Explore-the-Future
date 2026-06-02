# Ansible + gNMI

# Tooling Module

## Configuration Management with Ansible and gNMI

This module uses the CiscoDevNet `ansible-gnmi` examples to demonstrate model-driven read and write workflows on IOS XE.

This in-lab section is intentionally concise. For deep feature exploration, use the optional references at the end.

Repository reference:

- [CiscoDevNet/ansible-gnmi](https://github.com/CiscoDevNet/ansible-gnmi)

## Why Ansible + gNMI?

Ansible + gNMI gives you a structured, model-driven path for both state retrieval and configuration updates.

- **Model-driven operations**: Read and write data using YANG paths instead of CLI scraping
- **Automatable workflows**: Repeatable execution with inventory, vars, and playbooks
- **Validation-first approach**: Query first, change second, then verify
- **Scales to many devices**: Standard Ansible inventory and host/group vars

## Prerequisites

1. Access to the same lab switch used in Day 1 (`c9300x-lab`, `10.1.1.15`).
2. gNMI enabled and reachable on the target device.
3. Valid credentials (lab defaults: `admin` / `Cisco123`).
4. The `ansible-gnmi` repository already present on the lab VM.

> **Lab note**: Do not run `git clone` in this module. The repository is expected to be pre-staged before students start.

## Lab Setup

### Step 1: Change to the pre-staged repository directory

Use the repository path your lab prep provided. Common locations:

```bash
cd ~/ansible-gnmi
# or
cd ~/CiscoDevNet/ansible-gnmi
```

If needed, locate it:

```bash
find ~ -maxdepth 4 -type d -name ansible-gnmi
```

### Step 2: Install dependencies

From inside the repository:

```bash
python3 -m pip install --user -r requirements.txt
ansible-galaxy collection install -r requirements.yml
```

### Step 3: Review inventory and variables

The repo examples include inventory and variable patterns under `examples/`, including:

- `examples/group_vars/iosxe_devices.yml`
- `examples/host_vars/router1.yml`

Update host, username, and password values for your pod before running playbooks.

## Quick Lab Path

Use this sequence for class/lab execution:

1. Review inventory and variables in `examples/`.
2. Run GET example to confirm connectivity and baseline state.
3. Run SET example for one controlled change.
4. Re-run GET (or CLI) to verify expected state.
5. Optionally run SUBSCRIBE example to observe streaming updates.

## Demo 1: Read Device State with gNMI GET

This demo parallels Terraform `validate/plan` behavior: read current state first and confirm target data before any change.

### Objective

Use the repo GET examples to retrieve model-driven operational/configuration data from IOS XE.

### Steps

1. Review the GET example playbook:

```bash
cat examples/get_operations.yml
```

2. Run the GET example:

```bash
ansible-playbook -i examples/inventory.ini examples/get_operations.yml
```

3. If your pod uses certificate-based inventory, run with the cert inventory example:

```bash
ansible-playbook -i examples/inventory_with_certs.ini examples/playbook_with_inventory_vars.yml
```

### Verify

Confirm the play output returns expected YANG-path data (interfaces, system values, or other model content requested in the playbook) and that tasks complete with `ok`/`changed` as expected.

### Key Takeaway

GET operations are your pre-change safety step, similar to reviewing Terraform plan output before apply.

---

## Demo 2: Push a Controlled Change with gNMI SET

This demo parallels Terraform `apply`: make one explicit change, then immediately verify resulting state.

### Objective

Use repo SET examples to push a small configuration update via gNMI.

### Steps

1. Review the SET example playbook:

```bash
cat examples/set_operations.yml
```

2. Run the SET example:

```bash
ansible-playbook -i examples/inventory.ini examples/set_operations.yml
```

3. For focused hostname-style testing, use the sample playbook under `examples/playbooks/`:

```bash
ansible-playbook -i examples/inventory.ini examples/playbooks/test_set_hostname.yml
```

### Verify

Run a GET readback (Demo 1) or device CLI checks to confirm the intended value is present and only expected fields changed.

Suggested CLI validation on the switch:

```bash
ssh admin@10.1.1.15
show running-config | include hostname
```

### Key Takeaway

SET + GET verification gives you an apply-and-confirm loop similar to Terraform state convergence checks.

---

## Demo 3: Telemetry Stream with SUBSCRIBE

### Objective

Run the repository subscribe example to observe streaming data updates.

### Steps

1. Review the subscribe example:

```bash
cat examples/subscribe_operations.yml
```

2. Run the subscribe playbook:

```bash
ansible-playbook -i examples/inventory.ini examples/subscribe_operations.yml
```

### Verify

Confirm periodic telemetry/event updates are received for the subscribed paths and that the playbook exits cleanly (or as designed for streaming duration).

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| gNMI connection fails | Device gNMI service enabled, correct port/reachability, credentials valid |
| TLS or cert errors | Inventory cert paths in `examples/inventory_with_certs.ini` and related vars |
| Playbook cannot find vars | Host/group naming alignment between inventory, `group_vars`, and `host_vars` |
| Module import/dependency errors | Re-run `pip install -r requirements.txt` and collection install |

## Lab Mapping to Terraform Module

To keep student flow consistent with Terraform + NETCONF:

1. **Inspect inputs first**: inventory/vars (like Terraform provider and variables).
2. **Read current state**: gNMI GET (like Terraform plan-style visibility).
3. **Apply one change**: gNMI SET (like Terraform apply).
4. **Read back and verify**: GET/CLI confirmation of final state.

This keeps workflow sequencing familiar across both Day 1 modules.

## Optional Deep Dive

If you want to explore gNMI beyond this lab path:

1. Review additional playbooks under `examples/playbooks/` in the repo.
2. Explore certificate-based inventory patterns in `examples/inventory_with_certs.ini`.
3. Compare OpenConfig versus native model payloads in the included examples.

---

## Lab Transition

Before moving to PyATS or Day 2:

1. Exit any active SSH session and return to the lab VM terminal.
2. Keep the repo path noted for future replay of examples.
3. Stop or detach any long-running subscribe command output.

## Next Steps

✅ Completed: Day 1 - Ansible + gNMI

**Continue with Day 1:**

➡️ [PyATS Testing](pyats-testing.md) - Learn automated testing

**Or navigate to:**
- [Day 1 Overview](index.md)
- [Day 2: Device Monitoring](../day-2/index.md)

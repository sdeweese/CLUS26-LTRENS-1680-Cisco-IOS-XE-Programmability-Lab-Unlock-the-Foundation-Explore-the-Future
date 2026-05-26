# Atomic Config Replace (ACR) with Ansible

## Introduction

Atomic Config Replace (ACR) is a powerful configuration management approach that replaces the entire device configuration in a single atomic transaction. This lab uses an **Ansible-based framework** that runs over NETCONF to provide safe, repeatable, and auditable configuration management for Cisco IOS XE devices.

### Why Ansible + NETCONF?

Unlike traditional CLI-based configuration methods that apply changes line-by-line, this framework provides:

- **Atomic operations**: All changes succeed together or fail together (no partial configs)
- **Safe preview**: Stage changes to candidate datastore, review diffs, then commit or discard
- **Automated backups**: Before/after configs captured automatically
- **Idempotent workflows**: Safe to run multiple times without side effects
- **Version control ready**: Configuration files tracked in Git
- **No SSH/CLI required**: All operations use NETCONF for structured, reliable communication

### Two Parallel Workflows

This framework supports two approaches (both over NETCONF):

1. **CLI-RPC workflow** (recommended) — Work with familiar IOS CLI text, delivered via the `Cisco-IOS-XE-cli-rpc` YANG model
2. **YANG/XML workflow** — Use native YANG/XML payloads with standard NETCONF `edit-config`

Both workflows use the **candidate datastore** and **atomic commit** for safe, all-or-nothing configuration replacement.

---

> **📦 Lab Framework Source**
> 
> This lab follows the **IOS XE Atomic Config Replace — Ansible Framework** developed by Jeremy Cohoe.
> 
> **GitHub Repository**: [jeremycohoe/iosxe-atomic-netconf-ansible](https://github.com/jeremycohoe/iosxe-atomic-netconf-ansible)
> 
> The repository provides production-ready Ansible playbooks, inventory templates, and comprehensive documentation for atomic configuration management on Cisco IOS XE devices. We'll clone this repository and use its playbooks throughout this lab module.

---

## Architecture Overview

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        Your Lab Pod VM                          │
│                                                                 │
│  configs/desired/           Ansible            NETCONF (830)    │
│  ┌──────────────┐      ┌────────────┐      ┌────────────────┐  │
│  │ hostname.cfg  │─────▶│  Playbook  │─────▶│  IOS XE Device │  │
│  │ (CLI text)    │      │  (06/07)   │  SSH │  26.1.1+       │  │
│  └──────────────┘      └────────────┘      └────────────────┘  │
│                              │                     │            │
│  configs/baseline/           │              ┌──────┴──────┐     │
│  ┌──────────────┐            │              │  Candidate  │     │
│  │ baseline.cfg  │           │              │  Datastore  │     │
│  │ (reference)   │           │              └──────┬──────┘     │
│  └──────────────┘            │                     │            │
│                              │               commit (atomic)    │
│  configs/backups/            │                     │            │
│  ┌──────────────┐            │              ┌──────┴──────┐     │
│  │ pre_atomic_*.cfg │◀───────┘              │   Running   │     │
│  │ (auto backup) │                          │   Config    │     │
│  └──────────────┘                           └─────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

### Atomic Workflow — Step by Step

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Precheck │────▶│ Baseline │────▶│   Edit   │────▶│ Preview  │────▶│   Push   │
│          │     │ Capture  │     │ Desired  │     │  (diff)  │     │  (atomic)│
│ 01       │     │ 05       │     │ .cfg     │     │ 07       │     │ 06       │
└──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
  Verify           Pull              Make            Stage to         Stage to
  NETCONF,         running           your            candidate,       candidate,
  candidate,       config as         changes         diff vs          diff, then
  atomic-cfg       CLI text                          running,         COMMIT +
                                                     discard          save
                                                     (safe)           (atomic)
```

### What Happens on the Device

1. **Stage** — Desired config is pushed to the candidate datastore using `config-ios-cli-trans` with `<do-commit>false</do-commit>`. Running config is untouched.
2. **Diff** — Candidate is compared against running using `get-modelled-config-clis` on both datastores. You see exactly what will change.
3. **Commit** (live push only) — Candidate is atomically committed to running. All-or-nothing — if any part fails, the entire transaction rolls back.
4. **Save** — Running config is written to startup.

> **Dry run (default)**: Steps 1–2 only, then discard. The device is never modified.

---

## Prerequisites

### IOS XE Device Requirements

| Requirement | Value |
|-------------|-------|
| IOS XE version | 26.1.1 or later |
| NETCONF | Enabled and reachable on port 830 |
| Candidate datastore | Explicitly enabled (not on by default) |
| Atomic config | Feature flag enabled |
| Credentials | Local user with privilege 15 |

**Enable on the lab switch:**

```cisco
conf t
  netconf-yang
  netconf-yang feature candidate-datastore
  yang-interfaces feature atomic-config
end
write memory
```

> **Note**: After enabling candidate datastore, NETCONF restarts automatically (~60 seconds). Wait before testing connectivity.

### Workstation Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.10+ | Runtime |
| Ansible | 2.15+ | Automation framework |
| ncclient | 0.6.13+ | NETCONF client (used by Ansible netconf plugin) |
| lxml | any | XML parsing (ncclient dependency) |
| paramiko | any | SSH transport for NETCONF |
| xmltodict | any | XML parsing helpers |

### Lab Environment

The lab pod VM is pre-configured to access:

- **Lab switch**: `10.1.1.5:830` (hostname: `c9300x-lab`)
- **Credentials**: `admin` / `Cisco123`

These values are already set in the inventory files—no changes needed.

---

## Installation

### Step 1: Change to the ACR Lab Directory

From your SSH session on the lab pod VM:

```bash
cd ~
cd iosxe-atomic-netconf-ansible/atomic-netconf-ansible
```

### Step 2: Verify Ansible

Lab pods typically ship with Ansible pre-installed:

```bash
ansible --version
```

Expected output: Ansible 2.15 or later

### Step 3: Install Required Ansible Collections

```bash
ansible-galaxy collection install -r requirements.yml
```

This installs:

- `ansible.netcommon`
- `ansible.utils`
- `community.general`

### Step 4: Verify Python Dependencies

If you encounter errors about missing Python libraries, install them:

```bash
python3 -m pip install --user ansible ncclient lxml xmltodict paramiko
```

---

## Project Structure

```
atomic-netconf-ansible/
├── ansible.cfg                              # Ansible settings (YAML output, timeouts)
├── requirements.yml                         # Ansible Galaxy dependencies
├── README.md                                # GitHub repository documentation
│
├── inventory/
│   ├── hosts.yml                            # Pre-configured: c9300x-lab @ 10.1.1.5
│   └── group_vars/
│       ├── all/
│       │   ├── vars.yml                     # Connection settings, config paths
│       │   └── vault.yml                    # Credentials (admin/Cisco123)
│       └── access_switches/
│           └── vars.yml                     # Group-specific overrides
│
├── playbooks/
│   ├── 01_precheck.yml                      # Verify device readiness
│   ├── 02_baseline_capture.yml              # Capture running config (YANG/XML)
│   ├── 03_atomic_push.yml                   # Atomic push (YANG/XML)
│   ├── 04_diff_preview.yml                  # Diff preview (YANG/XML)
│   ├── 05_baseline_capture_cli.yml          # Capture running config (CLI-RPC)
│   ├── 06_atomic_push_cli.yml               # Atomic push (CLI-RPC) — includes before/after
│   └── 07_diff_preview_cli.yml              # Diff preview (CLI-RPC)
│
├── configs/
│   ├── baseline/<hostname>/baseline.cfg     # Reference configs (auto-generated)
│   ├── desired/<hostname>.cfg               # Desired configs (EDIT THESE)
│   └── backups/<hostname>/                  # Pre/post-commit backups
│       ├── pre_atomic_*.cfg                 #   Before commit snapshot
│       └── post_atomic_*.cfg                #   After commit snapshot
│
└── docs/
    └── quickstart.md                        # Detailed step-by-step walkthrough
```

---

## Quick Start Guide

All commands are run from inside the `atomic-netconf-ansible/` directory.

### Step 1: Verify Device Readiness

Run the precheck playbook to verify NETCONF connectivity, candidate datastore support, and atomic config capability:

```bash
ansible-playbook -i inventory/hosts.yml playbooks/01_precheck.yml
```

**What it checks:**
- NETCONF connectivity on port 830
- Candidate datastore enabled
- Atomic config feature enabled
- IOS XE version 26.1.1+

Expected output: All checks passed (green)

### Step 2: Capture Baseline Configuration

Pull the current running configuration from the device and save it as your baseline:

```bash
ansible-playbook -i inventory/hosts.yml playbooks/05_baseline_capture_cli.yml
```

**What it creates:**
- `configs/baseline/c9300x-lab/baseline.cfg` — Reference copy (don't edit)
- `configs/desired/c9300x-lab.cfg` — Your working copy (edit this)

Both files contain the complete device configuration in IOS CLI format.

### Step 3: Edit Desired Configuration

Open the desired configuration file and make your changes:

```bash
nano configs/desired/c9300x-lab.cfg
```

**Example changes:**

```diff
 interface TenGigabitEthernet1/0/1
- description Uplink Port
+ description UPLINK-TO-DIST-SW
  shutdown
  switchport access vlan 30
 exit
 
+interface TenGigabitEthernet1/0/2
+ description TEST-PORT-FOR-DEMO
+ switchport access vlan 100
+ no shutdown
+exit
```

> **Important**: This file contains the **complete** device configuration. Atomic config replace performs a full replace — anything you remove from this file will be removed from the device. Keep all physical interfaces defined.

Save and exit (Ctrl+X, Y, Enter).

### Step 4: Preview Changes (Safe Dry Run)

Stage your desired config to the candidate datastore, generate a diff against running config, then discard. The device is never modified:

```bash
ansible-playbook -i inventory/hosts.yml playbooks/07_diff_preview_cli.yml
```

**What you'll see:**

```diff
DIFF: c9300x-lab

- description Uplink Port
+ description UPLINK-TO-DIST-SW

+interface TenGigabitEthernet1/0/2
+ description TEST-PORT-FOR-DEMO
+ switchport access vlan 100
+ no shutdown
+exit

Lines added: 5
Lines removed: 1
```

**Diff symbols:**
- `+` = Lines being added
- `-` = Lines being removed
- ` ` = Unchanged context

If the diff looks incorrect or you see unexpected changes, **do not proceed to Step 5**. Go back to Step 3 and fix your desired config file.

### Step 5: Test Push with Dry Run

Perform a complete dry run that stages the config, shows the diff, and creates a backup — but does **not** commit to running:

```bash
ansible-playbook -i inventory/hosts.yml playbooks/06_atomic_push_cli.yml
```

**What happens:**
1. Captures current running config (pre-backup)
2. Stages desired config to candidate datastore
3. Shows diff (same as Step 4)
4. **Discards** candidate (device unchanged)
5. Saves pre-backup to `configs/backups/c9300x-lab/pre_atomic_<timestamp>.cfg`

This is your final safety check before the live push.

### Step 6: Live Push (Commit Changes)

When you're confident the changes are correct, run the live push:

```bash
ansible-playbook -i inventory/hosts.yml playbooks/06_atomic_push_cli.yml -e dry_run=false
```

**What happens:**
1. Captures BEFORE snapshot
2. Stages config to candidate
3. Shows diff
4. **Commits atomically** to running config
5. Saves running config to startup
6. Captures AFTER snapshot
7. Saves both snapshots to `configs/backups/c9300x-lab/`

**Atomic guarantee**: If any part of the commit fails (syntax error, dependency issue, etc.), the **entire transaction rolls back** automatically. Running config is never left in a partial state.

### Step 7: Verify Changes

Re-run the preview playbook to confirm no diff remains:

```bash
ansible-playbook -i inventory/hosts.yml playbooks/07_diff_preview_cli.yml
```

Expected output: `Desired matches running (no diff)`

You can also verify from the device CLI:

```bash
# SSH to the switch
ssh admin@10.1.1.5

# Check the changes
show run interface TenGigabitEthernet1/0/1
show run interface TenGigabitEthernet1/0/2
```

---

## Playbook Reference

### CLI-RPC Workflow (Recommended)

Work with familiar IOS CLI text—but the payload is delivered over NETCONF using the `Cisco-IOS-XE-cli-rpc` YANG model. No SSH/CLI session is opened.

| Order | Playbook | Purpose | Device Modified? |
|-------|----------|---------|------------------|
| 01 | `01_precheck.yml` | Verify NETCONF, candidate, atomic support | No |
| 05 | `05_baseline_capture_cli.yml` | Pull running config as CLI text via CLI-RPC | No |
| 07 | `07_diff_preview_cli.yml` | Stage to candidate, diff, discard | No |
| 06 | `06_atomic_push_cli.yml` | Full config replace via CLI-RPC | Dry run: No<br>Live: Yes |

**Usage examples:**

```bash
# Precheck
ansible-playbook -i inventory/hosts.yml playbooks/01_precheck.yml

# Capture baseline
ansible-playbook -i inventory/hosts.yml playbooks/05_baseline_capture_cli.yml

# Preview (safe dry run)
ansible-playbook -i inventory/hosts.yml playbooks/07_diff_preview_cli.yml

# Push (dry run - default)
ansible-playbook -i inventory/hosts.yml playbooks/06_atomic_push_cli.yml

# Push (live commit)
ansible-playbook -i inventory/hosts.yml playbooks/06_atomic_push_cli.yml -e dry_run=false
```

### YANG/XML Workflow

Work with native YANG/XML config payloads using standard NETCONF `edit-config` with `operation="replace"`. No CLI-RPC involvement.

| Order | Playbook | Purpose | Device Modified? |
|-------|----------|---------|------------------|
| 01 | `01_precheck.yml` | Verify NETCONF, candidate, atomic support | No |
| 02 | `02_baseline_capture.yml` | Pull running config as XML | No |
| 04 | `04_diff_preview.yml` | Stage to candidate, preview, discard | No |
| 03 | `03_atomic_push.yml` | Full config replace via edit-config | Dry run: No<br>Live: Yes |

**Usage examples:**

```bash
# Precheck
ansible-playbook -i inventory/hosts.yml playbooks/01_precheck.yml

# Capture baseline (XML)
ansible-playbook -i inventory/hosts.yml playbooks/02_baseline_capture.yml

# Preview (safe dry run)
ansible-playbook -i inventory/hosts.yml playbooks/04_diff_preview.yml

# Push (dry run - default)
ansible-playbook -i inventory/hosts.yml playbooks/03_atomic_push.yml

# Push (live commit)
ansible-playbook -i inventory/hosts.yml playbooks/03_atomic_push.yml -e dry_run=false
```

---

## Multi-Device Usage

The default lab pod inventory contains a single switch (`c9300x-lab`), so playbooks automatically run against that host. If you extend the inventory with additional devices, target a subset with `--limit`:

```bash
# Single device
ansible-playbook -i inventory/hosts.yml playbooks/06_atomic_push_cli.yml --limit c9300x-lab

# Device group
ansible-playbook -i inventory/hosts.yml playbooks/06_atomic_push_cli.yml --limit access_switches

# Multiple specific devices
ansible-playbook -i inventory/hosts.yml playbooks/06_atomic_push_cli.yml --limit "c9300x-lab,switch-02"
```

Without `--limit`, playbooks run against all devices in the `iosxe` group.

---

## Technical Details

### How config-ios-cli-trans Works

The `config-ios-cli-trans` RPC from the `Cisco-IOS-XE-cli-rpc` YANG model accepts a `<do-commit>` leaf that controls whether the RPC auto-commits to running:

| `<do-commit>` Value | Candidate Datastore | Running Config | Use Case |
|---------------------|---------------------|----------------|----------|
| `true` (default if omitted) | Written | Also written | Quick one-shot apply |
| `false` | Written | Untouched | Safe stage → diff → commit pattern |

All playbooks in this toolkit use `<do-commit>false</do-commit>` so that:

- Preview and dry-run can safely stage → diff → discard
- Live push explicitly commits only after showing the diff

### IOS XE 26.1.1+ Benefits

- **Crypto certificates abstracted** — No filtering or special handling needed during baseline capture
- **Candidate datastore** — Enables safe stage-then-commit workflows
- **Atomic config** — Ensures all-or-nothing config replacement with automatic rollback on failure

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| NETCONF connection refused | Verify `netconf-yang` is enabled; check port 830 reachability |
| NETCONF connection timeout | Increase `command_timeout` in ansible.cfg; verify network path to the switch |
| Precheck fails on candidate | Run `netconf-yang feature candidate-datastore` on device; wait 60s for NETCONF restart |
| Precheck fails on atomic config | Run `yang-interfaces feature atomic-config` on device |
| "Sync is in progress" error | Device busy with previous RPC — wait 30s and retry |
| `get-modelled-config-clis` slow | Normal — this RPC is heavy. Allow 30–60s per device |
| Diff shows unexpected reordering | YANG normalization reorders some CLI — focus on +/- lines |
| Diff shows no changes | Desired config already matches running |
| Push commit fails | Running config is untouched (atomic rollback). Check error message and fix desired config |

---

## Additional Exercises

### Exercise 1: Multi-Interface Configuration

Edit your desired config to add descriptions and VLANs to multiple interfaces, then preview and push the changes.

### Exercise 2: VLAN Management

Add new VLANs (e.g., VLAN 200, 300) to the desired config. Preview to see them staged, then commit.

### Exercise 3: Rollback Test

1. Capture a baseline
2. Make and commit changes
3. Restore the baseline by copying `baseline.cfg` over `desired/<hostname>.cfg`
4. Preview and push to roll back

### Exercise 4: Error Handling

Intentionally create an invalid configuration (e.g., reference a non-existent VLAN in an interface config). Attempt to push and observe the atomic rollback behavior.

---

## Reference Links

### Official Documentation

- [Cisco IOS XE Programmability Guide — Atomic Config Replace](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/xe-26/prog-xe-26-book.html)
- YANG model: `Cisco-IOS-XE-cli-rpc` (revision 2026-02-01, v1.3.0)

### GitHub Repositories

- **This Ansible framework**: [jeremycohoe/iosxe-atomic-netconf-ansible](https://github.com/jeremycohoe/iosxe-atomic-netconf-ansible)
- **Detailed walkthrough**: [docs/quickstart.md](https://github.com/jeremycohoe/iosxe-atomic-netconf-ansible/blob/main/atomic-netconf-ansible/docs/quickstart.md)
- **Python-based ACR examples**: [jeremycohoe/cisco-ios-xe-atomic-config-replace](https://github.com/jeremycohoe/cisco-ios-xe-atomic-config-replace)

### Alternative Approaches

If you prefer Python-based workflows, see the older Python ACR examples preserved in this repository:

- [atomic-operations/old-python-based-content/](../../atomic-operations/old-python-based-content/)

---

## Summary

In this module, you've learned how to:

✅ Use Ansible + NETCONF for atomic configuration replacement  
✅ Stage configurations to candidate datastore for safe preview  
✅ Generate diffs to see exactly what will change before committing  
✅ Perform atomic commits with automatic rollback on failure  
✅ Capture before/after snapshots for audit trails  
✅ Work with both CLI-RPC and YANG/XML workflows  

This Ansible-based approach provides a production-ready framework for managing IOS XE device configurations at scale with safety, auditability, and repeatability.

---

## Next Steps

✅ Completed: Day 1 - Atomic Config Replace

**Continue with Day 1:**

➡️ [Terraform + NETCONF](terraform-netconf.md) - Learn Infrastructure as Code

**Or explore:**

- [Ansible + gNMI](ansible-gnmi.md)
- [PyATS Testing](pyats-testing.md)
- [Day 1 Overview](index.md)
- [Day 2: Device Monitoring](../day-2/index.md)

# The Atomic Shift: Modernizing Your Network Management using Atomic Configuration Replace (ACR)

This workshop is designed for the Cisco Live Las Vegas 2026 DEVWKS-2810 workshop!

To learn more about Atomic Configuration replace and for the device credentials to access this lab environment, please see your instructor.

Ansible playbooks for performing **atomic config replace** on Cisco IOS XE devices running **26.1.1+**. Supports two parallel workflows that both run over NETCONF:

- **CLI-RPC workflow** (recommended): send IOS CLI text via the `Cisco-IOS-XE-cli-rpc` YANG model (`config-ios-cli-trans` / `get-modelled-config-clis`).
- **YANG/XML workflow**: send native YANG/XML via standard NETCONF `edit-config` with `operation="replace"`.

Both workflows use the candidate datastore and atomic commit, with no SSH/CLI pushes involved. This lab focuses on the first (CLI RPC). For full details, see the GitHub Repository for this project: <https://github.com/jeremycohoe/iosxe-atomic-netconf-ansible>

This toolkit (`atomic-netconf-ansible`) replaces the entire device configuration atomically. It either fully succeeds or keeps the current config on the device. No partial config states. No risk of half-applied changes.

## Why ACR? (Context from TECOPS-2314)

The Cisco Live TECOPS-2314 deck frames Atomic Config Replace as the answer to
three long-standing pain points of CLI-driven change management:

| Pillar | What CLI-only gives you | What ACR adds |
|---|---|---|
| Creating configs that just work | Line-by-line execution, partial state on failure | Declarative config + **two-phase commit** (validate before apply) |
| Error handling & rollback | No native rollback — you script it yourself | **Atomic transaction**: all changes succeed or none do, plus instant and post-deployment rollback options |
| Scalability & operational efficiency | Vendor- and version-specific syntax | Programmable interfaces (NETCONF/RESTCONF) on standard YANG models, ready for IaC |

The ACR transaction itself is the **Validate → Stage → Apply → (auto-)Rollback**
loop diagrammed in the deck: IOSd validates the candidate in a staging
environment, only writes to running config on commit, and reverts cleanly if
anything in the transaction fails. That is exactly what the playbooks in this
lab drive over NETCONF — you're just operating the deck slide.

## How It Works

### Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                        Your Workstation                         │
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
│  │ pre_atomic_*.cfg │◀──────────┘              │   Running   │     │
│  │ (auto backup) │                          │   Config    │     │
│  └──────────────┘                           └─────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

### Atomic Workflow Step by Step

```text
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Precheck │────▶│ Baseline │────▶│   Edit   │────▶│ Preview  │────▶│   Push   │
│          │     │ Capture  │     │ Desired  │     │  (diff)  │     │  (atomic)   │
│ 01       │     │ 05       │     │ .cfg     │     │ 07       │     │ 06       │
└──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
  Verify           Pull              Make            Stage to         Stage to
  NETCONF,         running           your            candidate,       candidate,
  candidate,       config as         changes          diff vs         diff, then
  atomic-cfg       CLI text                          running,         COMMIT +
                                                     discard          save
                                                     (safe)           (atomic)
```

### What Happens on the Device

1. **Stage**: Desired config is pushed to the **candidate datastore** using `config-ios-cli-trans` with `<do-commit>false</do-commit>`. Running config is untouched.
2. **Diff**: Candidate is compared against running using `get-modelled-config-clis` on both datastores. You see exactly what will change.
3. **Commit** (live push only): Candidate is atomically committed to running. All-or-nothing behavior applies. If any part fails, the entire transaction rolls back.
4. **Save**: Running config is written to startup.

> **Dry run** (default): Steps 1 and 2 only, then discard. The device is never modified.

## Prerequisites

### IOS XE Device Requirements

| Requirement | Detail |
|---|---|
| **IOS XE version** | 26.1.1 or later |
| **NETCONF** | Enabled and reachable on port 830 |
| **Candidate datastore** | Explicitly enabled (not on by default) |
| **Atomic config** | Feature flag enabled |
| **Credentials** | Local user with privilege 15 |

Enable on each device:

```
conf t
  netconf-yang
  netconf-yang feature candidate-datastore
  yang-interfaces feature atomic-config
end
write memory
```

After enabling candidate datastore, NETCONF restarts automatically (~60 seconds). Wait before testing connectivity.

### Workstation Requirements

| Component | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Runtime |
| Ansible | 2.15+ | Automation framework |
| ncclient | 0.6.13+ | NETCONF client (used by Ansible netconf plugin) |
| lxml | any | XML parsing (ncclient dependency) |
| paramiko | any | SSH transport for NETCONF |
| xmltodict | any | XML parsing helpers |

### Lab Environment Setup

<!-- for DevNet Workshop only

Note: Your instructor will give you a unique pod number, IP, and credentials to complete this lab.

1. On the laptop provided, use password 'cisco' to login.

2. Open Visual Studio Code. Open a new Terminal Window.
Type

`ssh –p 443 auto@pod##-xelab.cisco.com`

Relace ## is pod number on your desk.
Ex) Pod 5 will be: `ssh –p 443 auto@pod05-xelab.cisco.com`
If asked about adding a fingerprint, type yes
Password for your pod is
`pandalab2026!`

-->

SSH to your unique pod using the credentials provided by your instructor. Open a new terminal tab (pro tip, split the terminal window within Visual Studio Code to see the Cisco IOS XE device on one side and the workspace for running scripts on the other side using

```
ssh admin@10.1.1.5
```

and password:

```
Cisco123
```

Recommended: once you're connected to your switch, type `terminal monitor` to see real-time logs.

<!-- ![Connect to your switch](../images/acr-split-screen.png) -->

Navigate to the `DEVWKS-2810-The-Atomic-Shift-Modernizing-Your-Network-Management-using-Atomic-Configuration-Replace` directory.

```bash
# 1. Clone the repository (this has already been done for you in the lab pod)
#git clone https://github.com/jeremycohoe/iosxe-atomic-netconf-ansible.git

cd DEVWKS-2810-The-Atomic-Shift-Modernizing-Your-Network-Management-using-Atomic-Configuration-Replace/atomic-netconf-ansible

# 2. Confirm Ansible is available (lab pods normally ship with it)
ansible --version

# 3. Install the required Ansible collections (this has already been done for you in the lab pod)
#ansible-galaxy collection install -r requirements.yml
```

### Network Connectivity

The workstation (your pod VM) must reach the lab switch on **TCP port 830** (NETCONF over SSH). In the standard lab pod environment the switch is directly reachable at `10.1.1.5`, and the inventory is already configured for this.

| Scenario | Setup |
|---|---|
| **In-pod (default)** | Inventory already points at `10.1.1.5:830`, so no changes are needed |
| **Direct access (other)** | Edit `inventory/hosts.yml` and set `ansible_host` to the device management IP |
| **Via VPN** | No special config is required; ensure port 830 is reachable |

---

## Project Structure

```text
atomic-netconf-ansible/
├── ansible.cfg                              # Ansible settings (YAML output, timeouts)
├── requirements.yml                         # Ansible Galaxy dependencies
├── README.md                                # This file
│
├── inventory/
│   ├── hosts.yml                            # Pre-configured: c9300x-lab @ 10.1.1.5
│   └── group_vars/
│       ├── all/
│       │   ├── vars.yml                     # Connection settings, config paths
│       │   └── vault.yml                    # Credentials (admin/Cisco123 by default)
│       └── access_switches/
│           └── vars.yml                     # Group-specific overrides
│
├── playbooks/
│   ├── 01_precheck.yml                      # Verify device readiness
│   ├── 02_baseline_capture.yml              # Capture running config (YANG/XML)
│   ├── 03_atomic_push.yml                   # atomic push (YANG/XML)
│   ├── 04_diff_preview.yml                  # Diff preview (YANG/XML)
│   ├── 05_baseline_capture_cli.yml          # Capture running config (CLI-RPC: get-modelled-config-clis)
│   ├── 06_atomic_push_cli.yml               # Atomic push (CLI-RPC: config-ios-cli-trans), includes before/after capture
│   └── 07_diff_preview_cli.yml              # Diff preview (CLI-RPC)
│
├── configs/
│   ├── baseline/<hostname>/baseline.cfg     # Reference configs (auto-generated, don't edit)
│   ├── desired/<hostname>.cfg               # Desired configs (EDIT THESE)
│   └── backups/<hostname>/                  # Pre/post-commit backups (auto-generated)
│       ├── pre_atomic_*.cfg                 #   Running config before commit
│       └── post_atomic_*.cfg                #   Running config after commit
│
└── docs/
    └── quickstart.md                        # Detailed step-by-step walkthrough
```

---

## Quick Start

All commands are run from inside the extracted `DEVWKS-2810-The-Atomic-Shift-Modernizing-Your-Network-Management-using-Atomic-Configuration-Replace/atomic-netconf-ansible/` directory.

## Day 0 → Day 1 → Day 2 → Day 0 Cycle with `apply-config-day.sh`

Once your baseline is captured and you're comfortable with the preview/push flow, the lab includes a helper that rotates the active desired config between three checkpoint files and runs the live atomic push for you:

- `configs/desired/POD-<id>-day0.cfg` — clean baseline (starting state). Hostname `cat9300x-pod<id>a-sztp`, single user VLAN (pod# + 20).
- `configs/desired/POD-<id>-day1.cfg` — access-layer additions. Hostname becomes `cat9300x-pod<id>-day1`; adds VLANs `311` and `700` to the VLAN list; moves a block of access ports to `switchport access vlan 311` with `switchport mode access`; adds two `description setting for vlan ...` comments on selected interfaces.
- `configs/desired/POD-<id>-day2.cfg` — routing + time additions on top of day1. Hostname becomes `cat9300x-pod<id>-day2`; adds `router ospf 1` with `network 10.10.10.0 0.0.0.255 area 0`; sets `ntp source Vlan<pod#+20>`; adds NTP servers `10.1.7.2` and `10.11.13.10`.

Each pod has slightly different configs (the pod VLAN = pod# + 20) to support the lab flow. Your POD id comes from `cat ~/PODID` (e.g. `POD-13`). The script:

1. Repoints the symlink `configs/desired/c9300x-lab.cfg` → `POD-<id>-day<N>.cfg`
2. Runs `ansible-playbook -i inventory/hosts.yml playbooks/06_atomic_push_cli.yml -e dry_run=false`

Run `apply-config-day.sh --help` for full options (`--list`, `--no-run`).

### One-time setup

Ensure you are in the correct directory and make the script executable.

```bash
cd ~/DEVWKS-2810-The-Atomic-Shift-Modernizing-Your-Network-Management-using-Atomic-Configuration-Replace/atomic-netconf-ansible/
# Make the script executable
chmod +x apply-config-day.sh
```

### What you'll see when you run it

The script prints the symlink update, then streams the full `ansible-playbook` output (the same output you'd see running the playbook by hand):

```text
./apply-config-day.sh
```

You should see an output similar to this

```text
Detected PODID: POD-13
Which day would you like to rotate to? (Simply type the number and then press ENTER)
For Day0, type 0
For Day1, type 1
For Day2, type 2
Please Enter 0, 1, or 2: 1

Starting config replace for Day 1...
```

<!-- Updated: c9300x-lab.cfg -> POD-13-day1.cfg
Running Ansible full-replace playbook...
Command: ansible-playbook -i inventory/hosts.yml playbooks/06_atomic_push_cli.yml -e dry_run=false

PLAY [Atomic config push (CLI-RPC)] ********************************************
TASK [Gathering Facts] *********************************************************
...
TASK [Show diff] ***************************************************************
...
TASK [Commit candidate to running] *********************************************
changed: [c9300x-lab]

PLAY RECAP *********************************************************************
c9300x-lab : ok=12   changed=1    unreachable=0    failed=0    skipped=0
-->

If you face an error, check the Ansible output for the specific error message. Common issues include syntax errors in the desired config or missing required configuration elements. Use the error message to debug the issue.

If the `PLAY RECAP` line shows `failed=0`, the atomic commit succeeded and the device's running config now matches `POD-13-day1.cfg`.

### Walk the lifecycle

Run the script once per stage and pick the day at the prompt. After each commit, optionally re-run the diff preview to confirm the device matches the new desired state.

**Stage 1 — Apply Day 0 (baseline)**

```bash
./apply-config-day.sh
# When prompted, enter: 0
```

Result: device is reset to the clean POD baseline. Hostname becomes `cat9300x-pod<id>a-sztp`.

**Stage 2 — Apply Day 1 (access-layer VLAN/interface adds)**

```bash
./apply-config-day.sh
# When prompted, enter: 1
```

Watch the `PLAY RECAP`. If it shows `failed=0`, the day-1 deltas committed cleanly:
hostname is now `cat9300x-pod<id>-day1`, VLANs `311` and `700` are in the VLAN database, and
a block of access ports moved to `switchport access vlan 311` /
`switchport mode access`. Verify on the device:

```
show vlan brief | include 311|700
show running-config | section interface TenGigabit
```

#### If Stage 2 fails

If the `PLAY RECAP` instead shows `failed=1`, **the device did not change** — that is
the atomic guarantee. The candidate config was validated, IOS XE rejected one of the
lines, and the entire transaction was rolled back before anything touched the running
config.

Prove it for yourself:

```
show running-config | include hostname
```

The hostname is still the day-0 hostname (`cat9300x-pod<id>a-sztp`), not
`cat9300x-pod<id>-day1`. No VLANs were added, no ports were moved. Nothing landed.

**Read the Ansible failure output** — the error message will quote the exact CLI line
the device refused, typically with an `% Invalid input` marker or a parser error
pointing at the bad keyword.

**Fix the desired config:** open `configs/pod-targets/POD-<id>-day1.cfg` (or follow
the symlink at `configs/desired/c9300x-lab.cfg`), locate the offending line, correct
or remove it, and save.

> Tip: a quick way to spot what changed in day-1 is to diff against day-0:
> `diff configs/pod-targets/POD-<id>-day0.cfg configs/pod-targets/POD-<id>-day1.cfg`.
> One of the new lines is the culprit.

Re-run the push:

```bash
./apply-config-day.sh
# When prompted, enter: 1
```

This time `PLAY RECAP` should show `failed=0`. Re-run the verify commands above to
confirm the day-1 state is live.

**Stage 3 — Apply Day 2 (add OSPF routing + NTP)**

```bash
./apply-config-day.sh
# When prompted, enter: 2
```

Result: a single atomic transaction layers the day-2 deltas on top of day-1:

- Hostname changes to `cat9300x-pod<id>-day2`.
- `router ospf 1` is enabled
- NTP sourcing is pinned to the pod SVI: `ntp source Vlan<pod#+20>` (e.g. `Vlan33` for POD-13, `Vlan27` for POD-7).

Verify on the device after the commit:

```
sh run | s ospf
```

Should return

```
router ospf 1
 network 10.10.10.0 0.0.0.255 area 0
```

**Stage 4 — Roll back to Day 0**

```bash
./apply-config-day.sh
# When prompted, enter: 0
```

Result: full atomic replace back to the clean baseline. Day-1 (access-port/VLAN) and Day-2 (OSPF + NTP) additions are removed in a single transaction — no partial state, no reboot. Hostname returns to `cat9300x-pod<id>a-sztp` and `show ip protocols` no longer lists OSPF.

### Useful flags

```bash
./apply-config-day.sh --list      # show all available POD-*-day*.cfg targets
./apply-config-day.sh --no-run    # repoint the symlink only; skip the Ansible push
```

### Verify between stages (optional but recommended)

```bash
ansible-playbook -i inventory/hosts.yml playbooks/07_diff_preview_cli.yml
```

Expected after each `apply-config-day.sh` run: `Desired matches running (no diff)`.

### If something goes wrong

Ansible reports the failure in its standard `PLAY RECAP` (`failed=1`) and the script exits non-zero. Because this is an **atomic** replace, a failed push leaves the device on its previous running config — you'll never end up in a half-applied state.

Troubleshooting checklist:

1. Confirm POD id: `cat ~/PODID`
2. Confirm target exists: `ls configs/desired/POD-*-day*.cfg`
3. Check device reachability: `ansible-playbook -i inventory/hosts.yml playbooks/01_precheck.yml`
4. Preview the diff: `ansible-playbook -i inventory/hosts.yml playbooks/07_diff_preview_cli.yml`
5. Re-run verbosely: `ansible-playbook -vvv -i inventory/hosts.yml playbooks/06_atomic_push_cli.yml -e dry_run=false`
6. Common payload issues in `configs/desired/POD-*-dayN.cfg`:
    - close blocks with `exit`, **not** `end`
    - do **not** include `netconf-yang` or `restconf` (those are day-0 bootstrap, already on the device)

### Tips

- Payload files (`POD-*-dayN.cfg`) must use `exit` to close every config block. `end` is rejected by the NETCONF CLI-RPC parser.
- Do **not** put `netconf-yang` or `restconf` inside these payloads. Those are day-0 bootstrap commands and are already enabled on the device.
- Each run produces `pre_atomic_*.cfg` and `post_atomic_*.cfg` snapshots under `configs/backups/c9300x-lab/` for audit.
- If the device ever drifts, just `./apply-config-day.sh` → `0` to snap it back to baseline in a single transaction.

## Playbook Reference

### CLI-RPC Workflow (Recommended)

Work with familiar IOS CLI text. The payload is delivered over NETCONF using the `Cisco-IOS-XE-cli-rpc` YANG model (`config-ios-cli-trans` to push, `get-modelled-config-clis` to read). No SSH/CLI session is opened against the device.

| # | Playbook | Purpose | Modifies Device? |
|---|---|---|---|
| 01 | `01_precheck.yml` | Verify NETCONF, candidate, atomic support | No |
| 05 | `05_baseline_capture_cli.yml` | Pull running config as CLI text via CLI-RPC | No |
| 07 | `07_diff_preview_cli.yml` | Stage to candidate via CLI-RPC, diff, discard | No |
| 06 | `06_atomic_push_cli.yml` | Full config replace via CLI-RPC | **Dry run: No** / Live: **Yes** |

## Troubleshooting

| Problem | Solution |
|---|---|
| NETCONF connection refused | Verify `netconf-yang` is enabled; check port 830 reachability |
| NETCONF connection timeout | Increase `command_timeout` in `ansible.cfg`; verify network path to the switch |
| Precheck fails on candidate | Run `netconf-yang feature candidate-datastore` on device; wait 60s for NETCONF restart |
| Precheck fails on atomic config | Run `yang-interfaces feature atomic-config` on device |
| "Sync is in progress" error | Device busy with previous RPC. Wait 30s and retry |
| `get-modelled-config-clis` slow | Normal. This RPC is heavy. Allow 30-60s per device |
| Diff shows unexpected reordering | YANG normalization reorders some CLI. Focus on `+`/`-` lines |
| Diff shows no changes | Desired config already matches running |
| Push commit fails | Running config is untouched (atomic rollback). Check error message and fix desired config |

## Reference

- [Cisco IOS XE 26.1 Programmability Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/26x/26x-programmability-cg.html)
- YANG model: `Cisco-IOS-XE-cli-rpc` (revision 2026-02-01, v1.3.0)
- Supporting YANG models surfaced in TECOPS-2314 (used by these workflows under the hood):
    - `Cisco-IOS-XE-cli-preview-rpc` — `candidate-preview` RPC for the **config diff/preview** shown in playbook `07_diff_preview_cli.yml`.
    - `tail-f.com/ns/netconf/rollback` — `<rollback-comment>` on `edit-config` so every atomic change is auditable.
    - `Cisco-IOS-XE-rescue-config-rpc` — `<rescue-config-save/>` to mark a known-good config plus rollback-by-ID for post-deployment recovery.
- TECOPS-2314 Cisco Live deck — *Programmability and Automation with Cisco IOS XE* (ACR rationale, Validate/Stage/Apply/Rollback architecture, comment + rescue + diff RPCs): [TECOPS-2314 slides (PDF)](../resources/slides/TECOPS-2314-Programmability-and-Automation-with-Cisco-IOS-XE.pdf)
- Detailed walkthrough: `docs/quickstart.md` (in the lab repo)
- Jinja pod generation workflow: `docs/jinja-pod-workflow.md` (in the lab repo)

Congrats! You've completed the Atomic Config Replace Workshop!

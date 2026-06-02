# Guide Review Tracker

Last updated: 2026-05-29

## How This Tracker Works

- Status values:
	- ✅ `done`
	- 🚧 `in-progress`
	- ❌ `todo`
	- ⛔ `blocked`
	- 🟣 `story-pending` (pending item that is explicitly in Story's TODO list)
- I will implement items in order, without inventing missing details.
- Items that are unclear are marked `blocked` with explicit questions.

## Completed Recently

- Day 2 OTel + Splunk is focused on Splunk (TIG/Grafana removed).
- Splunk port-forwarding steps added with image.
- Splunk vs HEC vs TA terminology clarified.
- Day 1 PyATS guide expanded with helper scripts and verification flow.
- Day N App Hosting page drafted from slide deck content with Day N slide images.
- Day N App Hosting slide section now includes 1-2 sentence explanation per slide.
- Day 1 gNMI page tightened with concise quick-lab path and optional deep-dive section.
- Day 1 Terraform page now includes a student quick path and pre-installed Terraform note.
- Day 2 telemetry subscription-to-dashboard mapping section added.
- Day N App Hosting architecture workflow diagram added.

## Meeting Summary Traceability (Actionable Only)

| Item | Status | Scope | Next Action | Blocker / Question |
|---|---|---|---|---|
| Finalize App Hosting student command block with real values | ⛔ `blocked` | Day N docs | Replace placeholders in `app-hosting.md` with final app ID/package and exact command sequence | Need app ID, package filename, and script names/expected output |
| Add PyATS disable/remove workflow with validation | ✅ `done` | Day 1 docs + resources | Implemented one combined script that applies or unconfigures based on detected device state | No blocker |
| Telemetry innovations mapping (authoritative sub-ID to dashboard mapping) | 🚧 `in-progress` | Day 2 docs | Keep current practical mapping and upgrade once canonical mapping doc is provided | Need telemetry innovations doc/source with subscription ID to dashboard mapping |
| Blog/supporting resource link integration before Cisco Live | 🟣 `story-pending` | Intro/resources docs | Add final blog URL and short context once published | Need final publish URL and go-live timing |
| App hosting pod bake/deployment workflow validation (source VM -> pod rollout) | 🟣 `story-pending` | Lab environment + docs note | Add concise ops note once workflow is finalized by team | Need confirmed final operational runbook steps |
| Add GNMI 26.1 context slide/link without deep dive | ❌ `todo` | Day 1 gNMI docs | Add short context callout and optional link/reference | Need preferred slide/link artifact to reference |
| Atomic full-replace bundle: 3 complete config files | 🟣 `story-pending` | Day 1 Atomic docs + resources | Add exactly 3 CLI-only full-config examples when provided | Waiting for Story to provide the 3 config files |

## AI List Intake and Verification (May 28)

This section captures the AI action list you shared and whether each item is confirmed in the guide.

### Cross-Guide Items

| AI Item | Status | Verification Notes |
|---|---|---|
| Show how to connect using VS Code | ✅ `done` | Added general VS Code pod connection workflow in the intro guide. |
| Link to TechSem slides | ✅ `done` | Slides are linked in intro/resources and Day N includes embedded slide images. |
| Embed relevant TechSem slides inline | 🚧 `in-progress` | Day 0 and Day N have inline slide images; Day 1/Day 2 still mostly text-first with limited inline slides. |
| Add transitions between sections (switch -> VM -> next lab) | ✅ `done` | Transition callouts were added to Day 0/Day 1/Day 2/Day N module pages. |

### Day 0 (SZTP)

| AI Item | Status | Verification Notes |
|---|---|---|
| Vouchers for all pods (9300X context) | ⛔ `blocked` | Content references voucher workflows, but "all pods" readiness is environment-dependent and not fully verifiable from docs alone. |
| For one pod, get vouchers for all 3 switches | 🟣 `story-pending` | Requires exact 3-switch pod workflow confirmation and current inventory details. |
| Document MASA API script voucher flow | ✅ `done` | Day 0 SZTP guide references MASA flow and links to SZTP script README/resources. |
| Show scripts that are run | ✅ `done` | Added explicit "Scripts Run in This Lab (Day 0)" block with ordered execution list. |
| Better intro (OV, SUDI, scripts, DHCP option 67/143) | ✅ `done` | Day 0 content includes secure-first flow, MASA/SUDI context, and DHCP option 67/143 references. |
| Use C9350 since vouchers exist for those | ✅ `done` | Day 0 SZTP wording and runbook references were updated to C9350. |

### Day 1 (Atomic / Terraform / gNMI / PyATS)

| AI Item | Status | Verification Notes |
|---|---|---|
| Atomic: 3 complete configs (full replace) | ❌ `todo` | Atomic page is robust but does not yet present a clearly labeled "3 complete config" bundle set. |
| Atomic focus CLI-only for full replace examples | ✅ `done` | Atomic guide explicitly centers CLI-RPC workflow for this lab. |
| Add config update examples from slides (feature changes) | 🚧 `in-progress` | Some diff examples exist; can add 1-2 more explicit feature-based examples. |
| Add needed files to source VM | 🟣 `story-pending` | Environment rollout task, not fully solvable from docs only. |
| XML two-feature example (not full replace) | ❌ `todo` | Not explicitly added in Atomic section yet. |
| NaC Terraform examples from slides/PPT | 🚧 `in-progress` | Added NetasCode intent-to-provider examples (VLAN, ACL/interface, and a Day 1 copy/paste starter with exact pod values). Slide-tight examples/screenshots are still pending. |
| Terraform: use all 3 devices | ✅ `done` | Requirement changed by Story to focus on one device first. |
| Terraform: add screenshots per example | ❌ `todo` | Screenshots not yet embedded for Terraform walkthrough steps. |
| Ansible gNMI from CiscoDevNet repo in pod | ✅ `done` | Day 1 gNMI uses pre-staged CiscoDevNet repo and no-clone lab path. |
| PyATS: do installs/create venv + activate/deactivate guidance | ✅ `done` | PyATS flow now explicitly creates venv, activates before scripts, deactivates after. |
| PyATS: document pod reset method (use PnP service reset, avoid write erase) | ✅ `done` | Per latest direction, this guidance was intentionally not included; PyATS section keeps the original/current flow. |
| PyATS: include RESTCONF payload validation note with Day 1 flow | ✅ `done` | Added a RESTCONF verification note and sample read command in the PyATS guide. |
| PyATS: combine script or support add/remove scripts | ✅ `done` | Combined script now auto-selects APPLY or UNCONFIGURE based on current device state with explicit operation output. |
| PyATS: use 9300 + 10.1.1.55 consistently | 🚧 `in-progress` | Day 1 PyATS page updated to C9300 + `10.1.1.55`; remaining Day 1 naming consistency still pending. |
| PyATS: add NETCONF operational verification | ✅ `done` | Added service/session checks and proof-oriented validation sections. |
| PyATS: real NETCONF `<ok/>` proof test | ✅ `done` | Added lock/unlock RPC proof snippet expecting `<ok/>`. |

### Day 2 (OTel + Splunk)

| AI Item | Status | Verification Notes |
|---|---|---|
| OTel YANG gRPC receiver links and config refs | ✅ `done` | Added receiver repo, README/config, and implementation PR links. |
| Focus on Splunk TA | ✅ `done` | TA focus and terminology section are present. |
| Remove TIG/Grafana references from this flow | ✅ `done` | OTel+Splunk guide is now Splunk-focused. |
| Port forwarding instructions for Splunk | ✅ `done` | Detailed PORTS tab workflow and image are included. |
| Show script for subscriptions (already done for students) | ✅ `done` | Guide references script and notes pre-applied status. |
| Validate OTel + Splunk running / data flow / dashboards | ✅ `done` | Explicit container checks, data-flow verification, and dashboard steps included. |
| Add short Day 2 feature-history intro context | ✅ `done` | Added a concise feature-context section at the top of the OTel + Splunk guide. |
| Add model-innovations to dashboard mapping context | 🚧 `in-progress` | Mapping table added; needs authoritative source mapping confirmation for final version. |

### Day N (App Hosting)

| AI Item | Status | Verification Notes |
|---|---|---|
| App hosting aligned to session demo in pods | 🚧 `in-progress` | Day N is now lecture-aligned with slide context, diagram, and validation flow; final command block still placeholder-based pending app IDs/package names. |

## Questions Added from AI List

1. For Day 2 mapping, can you provide the telemetry innovations source doc/link with canonical subscription-ID-to-dashboard mapping so I can finalize the table?
2. For Day 1 naming consistency, should I run a full normalization pass for host/device labels across Atomic, Terraform, gNMI, and PyATS now?
3. For general VS Code connection guidance, should this be a new shared page under resources, or a short reusable snippet at the top of each day module?

## Remaining Work (Can Change Now)

1. Add Terraform screenshots per key example (provider/init, plan, apply/verification).

## Needs Input

1. Exact App Hosting deploy/activate script names and expected output.
2. Authoritative telemetry subscription-ID to dashboard mapping source.
3. Final naming convention to use across Day 1 (c9300-lab vs historical names).
4. Final blog URL for Cisco Live companion link.
5. Exact app ID to use in Day N examples (replace `<your-app-id>`).
6. Exact app package filename to use in Day N examples (replace `<your-app-package>.tar`).
7. Whether to include one final copy/paste command block for students only, with generic examples moved to instructor notes.
8. Three full CLI config-replace example files for Day 1 Atomic section (to be provided by Story).

## Blocked Until Input Arrives

1. Replace generic App Hosting placeholders with final student command block using real app ID/package values.

## Questions To Resolve

1. Should App Hosting include only pre-baked app usage, or also optional build-from-scratch appendix?
2. For telemetry mapping, table only or table plus diagram?
3. Should gNMI details stay brief with one external deep-dive link section?
4. For App Hosting final docs, should we include one required app only, or two examples (primary + optional)?

# OpenTelemetry + Splunk (OTel-Only Guide)

## Day 2 Device Monitoring with OpenTelemetry and Splunk

This guide is intentionally focused on one pipeline:

Cisco IOS XE -> OpenTelemetry Collector (`cisco_telemetry` receiver) -> Splunk HEC -> Splunk dashboards

It does not cover alternate collectors or time-series stacks.

## Lab Values Used in This Guide

- IOS XE device IP: `10.1.1.15`
- OTel collector host IP: `10.1.1.3`
- Telemetry receiver port: `57500`
- Splunk Web: `http://localhost:8000`
- Splunk HEC: `https://localhost:8088`

## TA Quick Path (What to Show First)

Use this sequence during demos to prove switch-to-Splunk telemetry quickly:

1. Turn on all subscriptions (use the full subscription config/script from the upstream repo).
2. Validate OTel collector and Splunk are both running.
3. Focus on Splunk as the source of truth for indexed metrics.
4. Confirm end-to-end data flow from `10.1.1.15` to Splunk.
5. Open Splunk dashboards and verify live updates.

## What You Will Build

By the end of this lab you will:

1. Run Splunk and an OTel collector that can ingest Cisco IOS XE gRPC dial-out telemetry.
2. Configure IOS XE telemetry subscriptions to send `encode-kvgpb` data to the collector.
3. Validate end-to-end flow from switch to Splunk.
4. Import and use prebuilt Splunk dashboards for telemetry analysis.

## Architecture

```text
Cisco IOS XE switch --gRPC dial-out (kvGPB)--> OTel Collector (cisco_telemetry)
                                                     |
                                                     +--> Splunk HEC (metrics index)
```

## Upstream Reference Implementation

This Day 2 workflow aligns with Jeremy Cohoe's receiver project:

- https://github.com/jeremycohoe/otel-grpc-cisco-receiver

Key files in that repo used by this guide:

- `docker-compose.yaml`
- `docker-collector-config.yaml`
- `collector-config.yaml`
- `start-splunk.sh`
- `start-otel.sh`
- `scripts/import-dashboards.sh`
- `c9300x-mdt-subscriptions.cfg`
- `configure-mdt.py`
- `scripts/fetch-yang-models.sh`

## Prerequisites

1. Docker and Docker Compose available on the host.
2. Reachability between IOS XE device and OTel collector host on telemetry port `57500`.
3. IOS XE device with telemetry support (17.x+ recommended).
4. Lab access to the switch console/CLI.

## Step 1: Change to the OTel Lab Directory

```bash
cd otel-grpc-cisco-receiver
```

## Step 2: Start Splunk + OTel Collector

Use either helper scripts or Compose.

### Option A (helper scripts)

```bash
./start-splunk.sh
./start-otel.sh
./scripts/import-dashboards.sh
```

### Option B (Compose)

```bash
docker compose up -d
```

With the default Compose setup, you should have:

1. OTel collector listening on `57500` for telemetry.
2. OTel self-metrics endpoint on `8888`.
3. Splunk Web on `8000`.
4. Splunk HEC on `8088`.

Default lab credentials and HEC values (as documented in the upstream repo):

- Splunk user: `admin`
- Splunk password: `Cisco123`
- HEC token: `cisco-mdt-token`
- Metrics index: `cisco_mdt`

## Step 2a: Verify Containers with `docker ps`

After startup, verify both Splunk and OTel containers are running:

```bash
docker ps
```

Look for:

1. A Splunk container in `Up` state.
2. Port mapping that includes `8000->8000/tcp` (Splunk Web).
3. Port mapping that includes `8088->8088/tcp` (Splunk HEC).
4. OTel collector container in `Up` state.

![docker ps output showing Splunk and mapped ports](../images/day2/day2-docker-ps.png)

### Access Splunk Web on Port 8000

Once `docker ps` shows Splunk mapped to port `8000`, open Splunk Web:

- On the same host: `http://localhost:8000`
- From another machine: `http://<docker-host-ip>:8000`

Login with the default lab credentials from above (`admin` / `Cisco123`), then proceed to dashboard validation.

## Step 3: (Optional but Recommended) Pull IOS XE YANG Models

The receiver works without downloaded models, but model files improve metadata quality and key propagation for broader path coverage.

```bash
./scripts/fetch-yang-models.sh
```

To target a specific IOS XE release, use the script argument shown in the upstream README.

## Step 4: Configure IOS XE Telemetry to OTel Collector

Set subscriptions to push to collector `10.1.1.3:57500` using `grpc-tcp` (or `grpc-tls` if TLS is enabled in collector config).

### Minimal example subscription

```text
telemetry ietf subscription 101
 encoding encode-kvgpb
 filter xpath /interfaces-ios-xe-oper:interfaces/interface/statistics
 source-address 10.1.1.15
 stream yang-push
 update-policy periodic 30000
 receiver ip address 10.1.1.3 57500 protocol grpc-tcp
```

### Use full subscription set

For richer dashboards, apply the predefined subscription bundle:

- `c9300x-mdt-subscriptions.cfg`

You can also push subscriptions programmatically:

```bash
pip install netmiko
python3 configure-mdt.py --host 10.1.1.15 --collector 10.1.1.3
```

To enable the complete telemetry set for this lab quickly, use:

- `c9300x-mdt-subscriptions.cfg`
- `configure-mdt.py`

## Step 5: Verify Data Flow

## On the switch

```text
show telemetry ietf subscription all
show telemetry ietf subscription 101 detail
show telemetry ietf subscription 101 receiver
```

Confirm subscriptions are valid and receiver state is healthy.

## On the collector host

Check collector self-metrics for receiver activity:

```bash
curl -s http://localhost:8888/metrics | grep cisco_telemetry
```

You should see counters increasing (messages/bytes/connections).

## Against Splunk search API

```bash
curl -sk -u admin:Cisco123 \
  'https://localhost:8089/services/search/jobs' \
  -d 'search=| mcatalog values(metric_name) WHERE index=cisco_mdt | stats count' \
  -d output_mode=json -d exec_mode=oneshot
```

A non-zero count indicates metrics are indexed.

## Step 6: Use Splunk Dashboards

1. Open Splunk Web.
2. Confirm dashboards are imported (or run `./scripts/import-dashboards.sh`).
3. Validate key dashboard categories:
   - Overview
   - Infrastructure
   - Network
   - Routing
   - Power and PoE
   - Security
   - Telemetry Health

## Troubleshooting (OTel + Splunk Only)

### No telemetry reaching collector

1. Verify switch receiver IP/port/protocol in subscription config.
2. Confirm collector is listening on `57500`.
3. Validate routing/firewall between switch and collector host.

### Collector sees traffic but Splunk is empty

1. Verify `splunk_hec` endpoint/token/index in collector config.
2. Confirm Splunk HEC service is enabled.
3. Check collector logs for exporter retry/drop messages.

### Dashboard panels show sparse dimensions

1. Add/download YANG models and point `models_dir` appropriately.
2. Re-check configured subscription paths versus dashboard expectations.

### TLS/mTLS issues

1. Use `grpc-tls` on switch only when collector TLS is configured.
2. Validate certificate chain/trustpoint setup.
3. Align switch trust settings with collector `tls` server settings.

## Recommended Operational Checks

Run these checks each time you update subscriptions:

1. `show telemetry ietf subscription all` on switch.
2. `curl http://localhost:8888/metrics | grep cisco_telemetry` on collector.
3. Splunk search proving metric name cardinality in `cisco_mdt` index.
4. Dashboard panel refresh with current time range.

## References

- OTel Cisco telemetry receiver project:
  - https://github.com/jeremycohoe/otel-grpc-cisco-receiver
- Splunk setup details in upstream repo:
  - https://github.com/jeremycohoe/otel-grpc-cisco-receiver/blob/main/SPLUNK-SETUP.md
- OTel collector config reference in upstream repo:
  - https://github.com/jeremycohoe/otel-grpc-cisco-receiver/blob/main/docs/CONFIG.md
- Security and TLS reference in upstream repo:
  - https://github.com/jeremycohoe/otel-grpc-cisco-receiver/blob/main/docs/SECURITY.md

---

## Next Step

Proceed to [gNXI Innovations](gnxi-innovations.md) to extend operational visibility and control with advanced gRPC-based interfaces.

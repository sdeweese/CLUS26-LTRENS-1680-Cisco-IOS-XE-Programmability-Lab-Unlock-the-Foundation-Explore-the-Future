# gNXI Innovations

## Day 2 Network Operations with gNXI & gNMI

### Introduction to gNXI

**gNXI** (gRPC Network Extensibility Interface) is a collection of microservices that extends traditional network management protocols with modern, streaming-capable APIs. It includes:

- **gNMI** (gRPC Network Management Interface) - Configuration and telemetry
- **gNOI** (gRPC Network Operations Interface) - Operational tasks (ping, traceroute, file ops)
- **gRIBI** (gRPC Routing Information Base Interface) - Dynamic route injection

**Why gNXI Matters:**

| Traditional Protocols | gNXI Advantages |
|----------------------|-----------------|
| SNMP polling (high overhead) | Streaming telemetry (push model) |
| CLI scraping (error-prone) | Structured YANG data |
| NETCONF (XML only) | Efficient binary encoding (Protobuf) |
| Per-connection security | Per-RPC access control with ACLs |

**IOS XE 26.1.1+ Features:**
- Service-level ACLs for fine-grained security
- Streaming telemetry with multiple modes (STREAM, SAMPLE, ONCE, POLL)
- OpenConfig and Cisco YANG model support
- Integration with modern observability stacks

---

### What's New in IOS XE 26.1

!!! success "New in 26.1"
    Cisco IOS XE 26.1 introduces significant enhancements to the gNMI implementation:
    
    - **Subscribe ONCE mode** - Single data dump without persistent subscription
    - **Subscribe POLL mode** - Client-driven update requests (pull on-demand)
    - **gNMI ACL support** - Service-level access control with per-RPC validation
    
    These features bring IOS XE gNMI to feature parity with industry-leading gNMI implementations!

### gNMI Feature Evolution

The following table shows when key gNMI capabilities were introduced in Cisco IOS XE:

| Feature | IOS XE Version | Description |
|---------|----------------|-------------|
| **gNMI Basic Support** | **16.8.1a** | Initial gNMI server implementation with Get/Set operations |
| **Subscribe STREAM Mode with SAMPLE** | **16.12.1** | Periodic sampling at fixed intervals (time-series metrics) |
| **Subscribe STREAM Mode with ON_CHANGE** | **17.14.1** | Real-time streaming on value changes (event-driven telemetry) |
| **Subscribe ONCE Mode** | **26.1.1** | Single snapshot without persistent connection |
| **Subscribe POLL Mode** | **26.1.1** | Client-triggered updates on-demand |
| **gNMI ACL Support** | **26.1.1** | Service-level access control lists with graceful error handling |

> **Note**: IOS XE 26.1 represents a major milestone, achieving feature parity with industry-leading gNMI implementations.

---

### Prerequisites

Before starting this lab, ensure:

1. **gNMI enabled on switch** (10.1.1.15) - Already configured
2. **gnmic CLI tool installed** on management VM (10.1.1.3) - Pre-installed
3. **Network connectivity** between VM and switch

> **Note**: `gnmic` is pre-installed in this lab. For your own environments, see installation at [https://gnmic.openconfig.net/install/](https://gnmic.openconfig.net/install/)

---

## Part 1: Securing gNMI with Access Control Lists

!!! success "New in IOS XE 26.1"
    Service-level ACL support for gNMI is a new security feature in IOS XE 26.1, providing fine-grained per-RPC authorization with graceful error handling using standard gRPC status codes.

Unlike NETCONF/RESTCONF which terminate connections when ACLs block access, gNMI provides graceful per-RPC authorization using standard gRPC error codes.

### Understanding gNMI ACL Architecture

```
┌─────────────┐                              ┌──────────────────┐
│             │   gNMI request               │                  │
│   Client    ├─────────────────────────────►│  Switch (gNMI)   │
│ 10.1.1.3    │                              │  10.1.1.15:9339  │
│             │◄─────────────────────────────┤                  │
└─────────────┘   gNMI ACL permit response   └────────┬─────────┘
                                                      │
                                              ┌───────▼──────────┐
                                              │  ACL Validation  │
┌─────────────┐                              │  acl_proxy lib   │
│             │   gNMI request               └──────────────────┘
│  Attacker   ├──────────────────────────────►
│ 10.1.1.20   │                              │
│             │◄──────────────────────────────┤
└─────────────┘   PERMISSION_DENIED          │
```

### Step 1: Verify Existing gNMI Configuration

The switch should already have gNMI enabled. Let's verify:

```bash
# SSH to the switch
ssh admin@10.1.1.15
# Password: Cisco123
```

Once connected, check gNMI status:

```cisco
show gnxi state detail
```

**Expected output:**
```
Settings
========
  Server: Disabled
  Secure server: Enabled
  Secure server port: 9339
  Secure password authentication: Enabled
  Secure trustpoint: TP-self-signed-4127246821
```

Check the running configuration:

```cisco
show running-config | section gnxi
```

**Expected output:**
```
gnxi
 secure-init
 secure-password-auth
```

### Step 2: Create gNMI Access Control List

We'll create an ACL that permits only the management VM (10.1.1.3) and logs denied attempts:

```cisco
configure terminal

! Create named ACL for gNMI access control
ip access-list standard GNMI_ALLOWED_HOSTS
 remark Allow only management VM at 10.1.1.3
 permit host 10.1.1.3
 deny any log
exit
```

### Step 3: Apply ACL to gNMI Service

```cisco
! Bind ACL to gNMI service (service-level enforcement)
gnxi access-list ipv4 name GNMI_ALLOWED_HOSTS

! Save configuration
end
write memory
```

### Step 4: Verify ACL Configuration

```cisco
! Confirm ACL is applied
show running-config | section gnxi

! View ACL contents
show ip access-lists GNMI_ALLOWED_HOSTS
```

**Expected ACL output:**
```
Standard IP access list GNMI_ALLOWED_HOSTS
    10 permit host 10.1.1.3
    20 deny any log
```

---

## Part 2: Testing gNMI Access Control

### Test Case 1: Permitted Access (Management VM)

From your management VM (10.1.1.3), test gNMI connectivity:

```bash
# Simple Get operation - retrieve system hostname
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  get --path /system/state/hostname
```

**Expected result:** ✅ **SUCCESS** - Hostname returned in JSON format

```json
{
  "source": "10.1.1.15:9339",
  "timestamp": 1748089991741481417,
  "time": "2026-05-25T13:14:59.59.177414017-07:00",
  "updates": [
    {
      "Path": "/system/state/hostname",
      "values": {
        "/system/state/hostname": "cat9350-pod07c"
      }
    }
  ]
}
```

### Test Case 2: Denied Access (Unauthorized Host)

To test ACL enforcement, you would need to try from a different IP (e.g., 10.1.1.20 or 192.168.1.x). 

**Expected result:** ❌ **PERMISSION_DENIED**

```
target "10.1.1.15:9339" get request failed: "10.1.1.15:9339" GetRequest failed:
rpc error: code = PermissionDenied 
desc = Connection rejected by ACL
```

**Key Difference from NETCONF:**
- **NETCONF**: Abruptly terminates connection (connection reset)
- **gNMI**: Returns graceful gRPC error code `PERMISSION_DENIED`

### Verify ACL Hit Counters

Back on the switch, check ACL statistics:

```cisco
show ip access-lists GNMI_ALLOWED_HOSTS
```

You should see match counts increment:
```
Standard IP access list GNMI_ALLOWED_HOSTS
    10 permit host 10.1.1.3 (5 matches)
    20 deny any log
```

---

## Part 3: gNMI Get Operations - On-Demand Data Retrieval

### Demo 1: Interface Operational Status

Query the operational status of a specific interface:

```bash
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  get --path /interfaces/interface[name=GigabitEthernet1/0/1]/state/oper-status
```

**Response breakdown:**
```json
{
  "source": "10.1.1.15:9339",
  "updates": [{
    "Path": "/interfaces/interface[name=GigabitEthernet1/0/1]/state/oper-status",
    "values": {
      "oper-status": "UP"
    }
  }]
}
```

### Demo 2: Interface Statistics (Traffic Counters)

Retrieve detailed interface statistics:

```bash
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  get --path /interfaces/interface[name=GigabitEthernet1/0/1]/state/counters
```

**Key metrics returned:**
- `in-octets`: Bytes received
- `out-octets`: Bytes transmitted
- `in-pkts`: Packets received
- `out-pkts`: Packets transmitted
- `in-errors`: Input errors
- `out-errors`: Output errors

**Practical use:** Calculate bandwidth utilization by polling octets at intervals.

### Demo 3: Power over Ethernet (PoE) Monitoring

Monitor PoE consumption and status:

```bash
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  get --path /Cisco-IOS-XE-poe-oper:poe-oper-data/poe-port
```

**Response includes:**
- `oper-state`: Operational status (on/off/faulty)
- `power`: Current power draw (mW)
- `power-class`: IEEE 802.3af/at class (0-8)
- `priority`: Port power priority (critical/high/low)

**Practical use:** Prevent power budget overruns, identify faulty PoE devices.

---

## Part 4: gNMI Subscribe - Streaming Telemetry

Unlike polling (Get), subscriptions push data changes to clients in real-time.

### Subscription Modes

Understanding when to use each subscription mode is critical for efficient telemetry collection:

| Mode | IOS XE Version | How It Works | Update Frequency | Data Volume | Best For | Example Use Case |
|------|----------------|--------------|------------------|-------------|----------|------------------|
| **STREAM (SAMPLE)** | **16.12.1** | Device sends updates at fixed intervals | User-defined (e.g., 5s, 30s, 1m) | High (continuous) | Time-series metrics, trending analysis | Interface counters for bandwidth graphs, CPU/memory monitoring |
| **STREAM (ON_CHANGE)** | **17.14.1** | Device sends updates only when value changes | Event-driven (immediate) | Low (sparse) | Event monitoring, state changes | Interface up/down events, BGP neighbor state changes, alarm conditions |
| **ONCE** | **26.1.1** 🆕 | Device sends complete snapshot then closes subscription | Single transmission | Low (one-time) | Initial state sync, config audits | Baseline capture before maintenance, inventory collection |
| **POLL** | **26.1.1** 🆕 | Client requests updates when needed, device responds | Client-controlled (on-demand) | Low (request-driven) | Dashboard refresh, manual queries | User clicks "Refresh" button, ad-hoc troubleshooting queries |

**Key Differences:**

- **STREAM (SAMPLE)**: Think of it as a heartbeat—you get data at regular intervals whether it changed or not. Perfect for creating time-series graphs where you need continuous data points.
  
- **STREAM (ON_CHANGE)**: Event-driven—only sends updates when something actually changes. Dramatically reduces bandwidth for data that changes infrequently (e.g., port status).

- **ONCE**: Like taking a photo—you get one complete snapshot, then the connection closes. Ideal when you need current state but don't want an ongoing stream.

- **POLL**: You're in control—the device waits for you to request an update. Best when updates are needed sporadically and you don't want continuous streaming.

**Practical Decision Guide:**

```
Need continuous metrics? → STREAM (SAMPLE)
  └─ Example: Monitor interface bandwidth every 30s for graphs

Value changes rarely? → STREAM (ON_CHANGE)
  └─ Example: Track interface oper-status (up/down events)

One-time data retrieval? → ONCE
  └─ Example: Get current config snapshot before change window

Manual refresh needed? → POLL
  └─ Example: Network dashboard with "Refresh" button
```

### Demo 4: Stream Interface Status Changes

Monitor interface state changes in real-time:

```bash
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  subscribe \
  --path /interfaces/interface[name=GigabitEthernet1/0/1]/state/oper-status \
  --stream-mode stream \
  --updates-only
```

**What happens:**
- Initial status returned immediately
- Client waits for changes
- **Any status change** (UP → DOWN or DOWN → UP) triggers instant update

**Try it:** While subscription is active, shut/no shut the interface:

```cisco
configure terminal
interface GigabitEthernet1/0/1
 shutdown
 ! Wait 5 seconds
 no shutdown
exit
```

You'll see real-time updates in your gnmic output!

### Demo 5: Sample Interface Counters (Time-Series)

Stream interface statistics every 5 seconds:

```bash
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  subscribe \
  --path /interfaces/interface[name=GigabitEthernet1/0/1]/state/counters \
  --stream-mode sample \
  --sample-interval 5s
```

**Output:** JSON updates every 5 seconds with latest counter values.

**Calculate bandwidth utilization:**

```bash
# Sample 1 (t=0s): in-octets = 1,234,567 bytes
# Sample 2 (t=5s): in-octets = 1,734,567 bytes
# Delta = 500,000 bytes in 5 seconds
# Bandwidth = (500,000 * 8 bits) / 5 seconds = 800,000 bps = 800 Kbps
```

### Demo 6: PoE Power Consumption Monitoring

Stream PoE power draw in real-time:

```bash
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  subscribe \
  --path /Cisco-IOS-XE-poe-oper:poe-oper-data/poe-port[interface="GigabitEthernet1/0/1"]/power \
  --stream-mode sample \
  --sample-interval 10s
```

**Practical scenario:**
- Plug in/unplug a PoE device (IP phone, camera)
- Watch power consumption change in real-time
- Set alerts when power exceeds thresholds

---

## Part 5: Advanced Operations

### POLL Mode - On-Demand Streaming Updates

!!! info "New in IOS XE 26.1"
    POLL mode is a new subscription type introduced in IOS XE 26.1, enabling client-driven telemetry updates instead of automatic streaming.

POLL mode allows clients to request updates at arbitrary times instead of automatic intervals:

```bash
# Start POLL subscription
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  subscribe \
  --path /interfaces/interface/state/counters \
  --stream-mode poll
```

**How it works:**
1. Client establishes subscription
2. Client sends POLL request when it wants data
3. Device responds with current values
4. Repeat step 2 as needed

**Use case:** Dashboards that update on user refresh, not continuous streaming.

### ONCE Mode - Initial State Snapshot

!!! info "New in IOS XE 26.1"
    ONCE mode is a new subscription type introduced in IOS XE 26.1, providing efficient one-time data retrieval without maintaining a persistent subscription.

Get a one-time dump of all data matching the path:

```bash
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  subscribe \
  --path /interfaces/interface/state \
  --stream-mode once
```

**Use case:** 
- Baseline configuration snapshots
- Initial state before starting event monitoring
- Ad-hoc queries without maintaining persistent connection

---

## Part 6: Real-World Integration

### Exporting Telemetry to InfluxDB

`gnmic` can write telemetry directly to time-series databases:

```bash
# Stream to InfluxDB
gnmic -a 10.1.1.15:9339 \
  -u admin -p Cisco123 \
  --skip-verify \
  subscribe \
  --path /interfaces/interface/state/counters \
  --stream-mode sample \
  --sample-interval 30s \
  --output influxdb \
  --influxdb-address http://localhost:8086 \
  --influxdb-org myorg \
  --influxdb-bucket network_metrics \
  --influxdb-token <your-token>
```

### Integration with Prometheus

Export as Prometheus metrics endpoint:

```bash
gnmic --config gnmic-prom.yml
```

**gnmic-prom.yml:**
```yaml
targets:

  - 10.1.1.15:9339

subscriptions:
  interfaces:
    paths:

      - /interfaces/interface/state/counters
    mode: sample
    sample-interval: 30s

outputs:
  prometheus:
    type: prometheus
    listen: :9804
    path: /metrics
```

Then configure Prometheus to scrape `http://management-vm:9804/metrics`.

---

## Comparing gNMI vs NETCONF/RESTCONF

### Security Enforcement

| Feature | gNMI | NETCONF | RESTCONF |
|---------|------|---------|----------|
| **ACL Rejection** | gRPC `PERMISSION_DENIED` | Connection reset (TCP RST) | HTTP 403 Forbidden |
| **Error Message** | Graceful with details | No error returned | JSON error body |
| **Connection State** | Stays open | Terminated | HTTP request-response |
| **Per-RPC Validation** | ✅ Yes | ❌ Per-connection only | ✅ Per-request |

### Protocol Comparison

| Aspect | gNMI | NETCONF | RESTCONF |
|--------|------|---------|----------|
| **Encoding** | Protobuf (binary) | XML | JSON/XML |
| **Transport** | gRPC/HTTP2 | SSH | HTTPS |
| **Streaming** | Native (Subscribe) | Requires extensions | SSE (limited) |
| **Efficiency** | High (binary) | Medium | Medium |
| **Firewall Friendly** | Port 9339 (single) | Port 830 | Port 443 |

---

## Troubleshooting Guide

### Issue: "connection refused" or "connection timeout"

**Checks:**
1. Verify gNMI is enabled: `show gnxi state detail`
2. Check if port 9339 is listening: `show control-plane host open-ports`
3. Verify network connectivity: Can you ping 10.1.1.15?
4. Check firewall rules between VM and switch

### Issue: "PERMISSION_DENIED" error

**Checks:**
1. Verify your source IP: `curl ifconfig.me` or `ip addr show`
2. Check ACL configuration: `show ip access-lists GNMI_ALLOWED_HOSTS`
3. Verify ACL is applied to gNMI: `show run | sec gnxi`
4. Check ACL hit counters: Look for deny rule matches

**Common mistake:** Client IP is NATted, and actual source IP differs from expected.

### Issue: Authentication failures

**Checks:**
1. Verify credentials: Username/password correct?
2. Check AAA: `show aaa servers` and `show aaa sessions`
3. Try explicit authentication method: Add `--username admin --password Cisco123`

### Issue: Path not found or empty data

**Checks:**
1. Verify YANG path exists: Use `gnmic capabilities` to list supported paths
2. Check device feature support: Not all features available on all platforms
3. Try browsing schema: `gnmic -a 10.1.1.15:9339 -u admin -p Cisco123 --skip-verify get --path /`

---

## gnmic CLI Quick Reference

### Installation

`gnmic` is pre-installed in this lab. For other environments:

**Linux/macOS:**
```bash
# Using bash script
bash -c "$(curl -sL https://get-gnmic.openconfig.net)"

# Using package managers
# Homebrew (macOS)
brew install gnmic

# APT (Ubuntu/Debian)
echo "deb [trusted=yes] https://netdevops.fury.site/apt/ /" | sudo tee /etc/apt/sources.list.d/netdevops.list
sudo apt update
sudo apt install gnmic
```

**Documentation:** [https://gnmic.openconfig.net](https://gnmic.openconfig.net)

### Common Commands

```bash
# Get single value
gnmic -a <IP>:9339 -u <user> -p <pass> --skip-verify get --path <yang-path>

# Subscribe (streaming)
gnmic -a <IP>:9339 -u <user> -p <pass> --skip-verify subscribe --path <yang-path> --stream-mode <mode>

# List device capabilities
gnmic -a <IP>:9339 -u <user> -p <pass> --skip-verify capabilities

# Set configuration (if supported)
gnmic -a <IP>:9339 -u <user> -p <pass> --skip-verify set --update-path <path> --update-value <value>
```

### Flags Reference

| Flag | Description |
|------|-------------|
| `-a, --address` | Target device (IP:port) |
| `-u, --username` | Username for authentication |
| `-p, --password` | Password for authentication |
| `--skip-verify` | Skip TLS certificate validation (use for self-signed certs) |
| `--path` | YANG data path to query |
| `--stream-mode` | Subscription mode (stream\|sample\|once\|poll) |
| `--sample-interval` | Interval for SAMPLE mode (e.g., 5s, 1m) |
| `--updates-only` | Skip initial sync, only show updates |
| `--format` | Output format (json\|protojson\|prototext\|event) |

---

## Key Takeaways

1. **gNMI ACLs provide service-level security** - Fine-grained per-RPC authorization with graceful error handling
2. **Streaming telemetry is more efficient than polling** - STREAM mode for events, SAMPLE for metrics
3. **YANG models ensure structured data** - No CLI scraping or regex parsing required
4. **Integration-ready** - Export directly to InfluxDB, Prometheus, Kafka, etc.
5. **Production-proven** - Used by hyperscalers for real-time network telemetry at scale

### Next Steps

Continue exploring:

- **gNOI** (gRPC Network Operations) - Ping, traceroute, file operations via gRPC
- **gRIBI** (gRPC Routing) - Programmatic route injection for traffic engineering
- **Streaming Telemetry Architecture** - Build end-to-end observability pipelines

---

## Additional Resources

- [OpenConfig gNMI Specification](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md)
- [gnmic Documentation](https://gnmic.openconfig.net/)
- [Cisco IOS XE YANG Models](https://github.com/YangModels/yang/tree/main/vendor/cisco/xe)
- [OpenConfig YANG Models](https://github.com/openconfig/public)
- [gNMI ACL Configuration Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/1711/b_1711_programmability_cg/grpc_network_management_interface.html)

---

## Next Steps

✅ Completed: Day 2 - gNXI Innovations

**Ready for Day N?**

➡️ [Day N: Device Optimization Overview](../day-n/index.md) - Learn application hosting

**Or return to:**
- [Day 2 Overview](index.md)
- [OpenTelemetry + Splunk](opentelemetry-splunk.md)

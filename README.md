# Welcome to the Cisco Live 26 IOS XE Programmability Lab

## Unlock the Foundation, Explore the Future

### Cisco IOS XE Version 26.1

This lab guide serves as the comprehensive resource for the Cisco Live US (Las Vegas) **Programmability and Automation Lab with Catalyst IOS XE Platforms** - Session **LTRENS-1680**.

---

## Lab Introduction

Welcome to the IOS XE Programmability Lab! This hands-on lab takes you through the complete lifecycle of modern network device management, from initial onboarding through ongoing operations and optimization.

### Lab Access

To access the lab, you will need to SSH to your assigned VM host. From the VM, you will have access to the switch and all required software dependencies.

**See lab environment access information provided by instructors.**

---

## Lab Environment & Access

### Accessing Your Lab Pod

1. **Identify your pod number** (provided by instructors)

2. **Open two terminal windows** for SSH connections:
   - **Terminal 1**: VM configuration and automation
   - **Terminal 2**: Direct switch access via telnet

3. **SSH to the VM** (Terminal 1):
   ```bash
   ssh -p 3389 -L 18480:localhost:8480 -L 13000:localhost:3000 auto@pod##-xelab.cisco.com
   ```
   Replace `##` with your pod number. Use the password provided by the facilitator.
   
   First-time login will prompt:
   ```
   Are you sure you want to continue connecting (yes/no/[fingerprint])?
   ```
   Type `yes` to continue.

4. **SSH to the VM** (Terminal 2):
   ```bash
   ssh auto@pod##-xelab.cisco.com
   ```
   Use the same credentials.
   
   Then telnet to the Catalyst 9350:
   ```bash
   telnet 10.1.1.15
   ```
   Credentials: `admin` / `Cisco123`

5. **You're ready!** Once connected via SSH and telnet, you can proceed with the lab modules.

---

## Learning Path

This lab follows a structured "Day 0 to Day N" approach, mirroring real-world network device lifecycle management:

### [Introduction](intro/index.md)
- YANG Model Innovations in IOS XE 26.1

### [Day 0 - Device Onboarding](day-0/index.md)
**Secure Zero Touch Provisioning (SZTP)**
- Automated device onboarding
- Ownership voucher generation
- Bootstrap configuration
- Certificate-based authentication

### [Day 1 - Device Configuration](day-1/index.md)
**Configuration Management & Automation**
- Atomic Config Replace (NETCONF)
- Terraform + NETCONF (Infrastructure as Code)
- Ansible + gNMI (Configuration Automation)
- PyATS (Automated Testing)

### [Day 2 - Device Monitoring](day-2/index.md)
**Observability & Telemetry**
- OpenTelemetry + Splunk Integration
- gNXI Innovations (POLL/ONCE, ACL & VRF)
- Model-Driven Telemetry

### [Day N - Device Optimization](day-n/index.md)
**Advanced Features**
- Application Hosting with Smart Switches
- Edge computing on network devices

### [Resources](resources/index.md)
**Additional Tools & References**
- YANG Suite Labs
- DevNet Sandboxes
- Swagger API Documentation

---

## Lab Modules

Lab modules can be completed in **any order**. Feel free to jump to topics that interest you most!

---

## Getting Started

### Recommended Learning Path

For the best learning experience, follow this sequence:

1. **[Introduction: YANG Model Innovations](intro/index.md)** (~15 min)
2. **[Day 0: SZTP Onboarding](day-0/index.md)** (~60 min)
3. **[Day 1: Atomic Config Replace](day-1/atomic-operations.md)** (~60 min)
4. **[Day 2: OpenTelemetry + Splunk](day-2/opentelemetry-splunk.md)** (~90 min)

### Choose Your Own Adventure

Prefer to explore specific topics? Jump directly to:

- **Configuration Management**: [Terraform](day-1/terraform-netconf.md) or [Ansible](day-1/ansible-gnmi.md)
- **Testing**: [PyATS](day-1/pyats-testing.md)
- **Advanced Monitoring**: [gNXI Innovations](day-2/gnxi-innovations.md)
- **Edge Computing**: [Application Hosting](day-n/app-hosting.md)

---

## Technical Support

If you encounter issues during the lab:

1. Check the **Troubleshooting** sections in each module
2. Ask lab proctors for assistance
3. Visit the DevNet Zone for additional support

---

## Additional Resources

- [Cisco DevNet](https://developer.cisco.com)
- [IOS XE Programmability Documentation](https://developer.cisco.com/docs/ios-xe/)
- [YANG Models GitHub](https://github.com/YangModels/yang/tree/master/vendor/cisco/xe)
- [DevNet Sandboxes](https://developer.cisco.com/site/sandbox/)

---

**Ready to begin?**

➡️ **[Start with the Introduction](intro/index.md)**

Or jump to a specific day:

- [Day 0: Device Onboarding](day-0/index.md)
- [Day 1: Device Configuration](day-1/index.md)
- [Day 2: Device Monitoring](day-2/index.md)
- [Day N: Device Optimization](day-n/index.md)

- **Atomic operations**: All changes are applied together or rolled back completely
- **Syntax validation**: Pre-checks configuration syntax before applying
- **Dependency checking**: Verifies configuration dependencies
- **Automatic rollback**: Returns to previous state if not confirmed
- **Error isolation**: Identifies exact line numbers of configuration errors

For more information and Python examples, visit the [Cisco IOS XE Atomic Config Replace GitHub repository](https://github.com/jeremycohoe/cisco-ios-xe-atomic-config-replace).

### Python Script Workflow Overview

The ACR Python script follows a 13-step workflow to safely apply configuration changes:

1. Start
2. Initialize Device
3. Netconf Connect
4. Discard Changes
5. Get Pre-check Config
6. Apply Config (edit_config)
7. Get Post-check Config
8. Compare Pre & Post Configs
9. Confirmed Commit
10. Get Post-confirmed Commit Config
11. Commit Changes
12. Compare Pre & Final Configs
13. End

### Prerequisites

Before starting the ACR demos, ensure you have:

1. SSH access to the lab VM
2. Telnet access to the C9300 switch (10.1.1.15)
3. Python 3 installed on the VM
4. Required Python libraries (ncclient, xml, netmiko, difflib, lxml)

### Lab Setup

From your SSH session on the VM, clone the ACR repository and navigate to the directory:

```bash
cd ~
git clone https://github.com/jeremycohoe/cisco-ios-xe-atomic-config-replace.git
cd cisco-ios-xe-atomic-config-replace
```

Install required Python dependencies:

```bash
pip3 install ncclient netmiko lxml --user
```

### Demo 1: Syntax & Dependency Error Isolation

In this demo, you will learn how ACR detects and isolates syntax errors in configuration files, providing the exact line number where errors occur.

#### Objective
Experience how ACR validates configuration syntax before applying changes and identifies the specific line where errors exist.

#### Steps

**Step 1: Prepare the target configuration file**

First, let's create a configuration file with an intentional syntax error. Create a file called `target_C9K_config.xml`:

```bash
nano target_C9K_config.xml
```

Add a basic configuration with a syntax error (we'll intentionally add an invalid line). For example:

```xml
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>C9300-ACR-Test</hostname>
    <interface>
      <GigabitEthernet>
        <name>1/0/1</name>
        <description>Test Interface with Error</description>
        <invalid-command>this-will-cause-error</invalid-command>
      </GigabitEthernet>
    </interface>
  </native>
</config>
```

Save and exit (Ctrl+X, Y, Enter).

**Step 2: Run the ACR operation with the erroneous configuration**

Execute the Python script to send a full-replace operation to the C9300 switch:

```bash
python3 acr.py --host 10.1.1.15 --username admin --password Cisco123 --config target_C9K_config.xml
```

**Step 3: Observe the syntax error detection**

The ACR process will validate the configuration and identify the syntax error. You should see output similar to:

```
Error detected in configuration file: target_C9K_config.xml
Line 9: <invalid-command>this-will-cause-error</invalid-command>
Syntax Error: Invalid configuration command
```

ACR provides the **exact line number** where the error occurs, making it easy to identify and fix issues.

**Step 4: Fix the syntax error**

Edit the configuration file and remove or correct the invalid line:

```bash
nano target_C9K_config.xml
```

Remove the line with `<invalid-command>` and save the file.

**Step 5: Send the corrected configuration**

Run the ACR operation again with the corrected file:

```bash
python3 acr.py --host 10.1.1.15 --username admin --password Cisco123 --config target_C9K_config.xml
```

**Step 6: Verify successful application**

You should now see output indicating:

```
Configuration validation: SUCCESS
Configuration applied successfully
Waiting for confirmation...
```

**Key Takeaway**: ACR performs pre-validation of configuration syntax, catching errors before they impact the device and providing precise error locations for quick troubleshooting.

---

### Demo 2: Automatic Rollback Without Confirm Commit

This demo demonstrates ACR's automatic rollback feature. When a configuration is applied but not confirmed within the timeout period, the device automatically reverts to its previous known-good state.

#### Objective
Understand the safety mechanism of ACR's automatic rollback when a confirm commit is not issued.

#### Steps

**Step 1: Prepare a valid target configuration**

Create a new configuration file that will be applied but not confirmed:

```bash
nano target_C9K_rollback_test.xml
```

Add a valid configuration (example):

```xml
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>C9300-ACR-Rollback-Test</hostname>
    <interface>
      <GigabitEthernet>
        <name>1/0/2</name>
        <description>Testing ACR Rollback Feature</description>
      </GigabitEthernet>
    </interface>
  </native>
</config>
```

Save and exit.

**Step 2: Check the current hostname**

From your telnet session to the switch, verify the current hostname:

```
show run | include hostname
```

Note the current hostname for comparison.

**Step 3: Send the full-replace operation without confirming**

Run the ACR script with the `--no-confirm` flag (if available) or simply don't send the confirm commit:

```bash
python3 acr.py --host 10.1.1.15 --username admin --password Cisco123 --config target_C9K_rollback_test.xml --no-confirm
```

**Step 4: Observe the configuration is applied**

Immediately check from your telnet session that the configuration has been applied:

```
show run | include hostname
```

You should see the new hostname: `C9300-ACR-Rollback-Test`

**Step 5: Wait for automatic rollback**

The ACR process has a default timeout (typically 30-60 seconds). Since no confirm commit was issued, watch as the device automatically rolls back to its previous configuration.

After the timeout period, check the hostname again:

```
show run | include hostname
```

**Step 6: Verify the rollback**

The hostname should have reverted to its original value. The configuration has automatically rolled back because no "confirm commit" was issued within the timeout window.

**Step 7: Apply configuration with proper confirmation**

Now run the script properly and send the confirm commit:

```bash
python3 acr.py --host 10.1.1.15 --username admin --password Cisco123 --config target_C9K_rollback_test.xml --confirm
```

When prompted, confirm the changes. The configuration will now persist.

**Key Takeaway**: ACR provides a safety net for configuration changes. If the network operator loses connectivity or fails to confirm the changes, the device automatically returns to its previous known-good state, preventing accidental lockouts or misconfigurations.

---

### Understanding the ACR Lifecycle: Day 1 to Day N

ACR is designed for ongoing configuration management throughout the device lifecycle:

- **Day 1**: Initial device configuration applied with ACR (e.g., `acr-day1.py` and `day1.xml`)
  - Config: `ACR/jcohoe-c9300x-border1-acr-day1.xml`
  - Hostname: `jcohoe-c9300x-border1-acr-day1`
  
- **Day N**: Subsequent configuration updates applied with ACR (e.g., `acr-dayn.py` and `dayn.xml`)
  - Config: `ACR/jcohoe-c9300x-border1-acr-dayn.xml`
  - Hostname: `jcohoe-c9300x-border1-acr-dayn`

Each iteration replaces the entire configuration atomically, ensuring consistency and enabling easy rollback to previous day configurations if needed.

---

### Additional Exercises (Optional)

1. **Compare configurations**: Use the Python script's diff functionality to compare pre and post configurations
2. **Test dependency errors**: Create a configuration with dependency issues (e.g., referencing a non-existent VLAN)
3. **Timing tests**: Experiment with different confirm-timeout values
4. **Configuration templates**: Create your own XML configuration templates for common deployment scenarios

---

### Troubleshooting Tips

- **NETCONF not enabled**: Ensure NETCONF is enabled on the switch with `netconf-yang`
- **Connection errors**: Verify IP reachability to 10.1.1.15 and correct credentials (admin/Cisco123)
- **XML syntax errors**: Validate XML structure using online validators before applying
- **Python library errors**: Ensure all required libraries are installed with `pip3 list`

---

### Summary

In this module, you've learned how to:
- Use Atomic Config Replace for full configuration management
- Identify and isolate syntax errors in configurations
- Leverage automatic rollback for safe configuration changes
- Apply ACR in a Day 1 to Day N operational model

ACR provides a robust, safe, and efficient method for managing Cisco IOS XE device configurations at scale using NETCONF/YANG.


## Day 2 Device Monitoring with OpenTelemetry & Splunk

### Introduction to Model-Driven Telemetry

Model-Driven Telemetry (MDT) is a modern approach to monitoring network devices that provides real-time, high-frequency operational data streaming. Unlike traditional polling methods (SNMP), MDT uses a push model where the device streams data to collectors at defined intervals.

**Benefits of Model-Driven Telemetry:**
- **Real-time monitoring**: Sub-second visibility into device operations
- **High-frequency data**: Stream data at intervals as low as 100ms
- **Structured data**: Uses YANG models for consistent data format
- **Reduced overhead**: Push model reduces network traffic vs polling
- **Scalable**: Efficiently monitor thousands of data points

**MDT Architecture Components:**

1. **Publisher (Network Device)**: Cisco IOS XE device that streams telemetry data
2. **Collector**: Receives and processes telemetry streams (e.g., Telegraf, Pipeline)
3. **Time-Series Database**: Stores telemetry data (e.g., InfluxDB, Prometheus)
4. **Visualization**: Displays data in dashboards (e.g., Grafana, Splunk)

### Configuring Telemetry Subscriptions on the Catalyst 9300

This section focuses on configuring Model-Driven Telemetry subscriptions on the Catalyst 9300 switch to monitor key operational metrics.

#### Understanding Telemetry Subscriptions

Every process or metric you want to monitor requires a subscription. A subscription defines:

- **What to monitor**: XPath filter specifying YANG data path
- **Encoding**: Data format (encode-kvgpb, encode-json, encode-xml)
- **Stream type**: yang-push (for operational data)
- **Update policy**: How often to send data (periodic or on-change)
- **Receiver**: Where to send the telemetry data (IP, port, protocol)

#### Lab Scenario

We'll create four telemetry subscriptions to monitor:

1. **CPU Utilization** - Track processor usage
2. **Power over Ethernet (PoE)** - Monitor PoE operational data
3. **Memory Statistics** - Track memory consumption
4. **Temperature** - Monitor device temperature sensors

#### Configuration Details

- **Encoding**: `encode-kvgpb` (Key-Value Google Protocol Buffers)
- **Stream**: `yang-push` (for operational datastore monitoring)
- **Update interval**: `6000` milliseconds (6 seconds)
- **Source address**: Switch IP `10.1.1.15`
- **Receiver**: Collector at `10.1.1.3` port `57500` using `grpc-tcp`

#### Step-by-Step Configuration

**Step 1: Access the switch**

From your telnet session to the Catalyst 9300:

```
telnet 10.1.1.15
```

Login with credentials: admin / Cisco123

**Step 2: Configure CPU Utilization Subscription**

```
configure terminal
telemetry ietf subscription 1010
 encoding encode-kvgpb
 filter xpath /process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds
 source-address 10.1.1.15
 stream yang-push
 update-policy periodic 6000
 receiver ip address 10.1.1.3 57500 protocol grpc-tcp
```

**Explanation:**
- `subscription 1010`: Unique subscription ID
- `filter xpath`: Points to CPU utilization data in the YANG model
- `five-seconds`: Monitors 5-second CPU average
- `periodic 6000`: Sends updates every 6 seconds

**Step 3: Configure PoE Subscription**

```
telemetry ietf subscription 1020
 encoding encode-kvgpb 
 filter xpath /poe-ios-xe-oper:poe-oper-data
 source-address 10.1.1.15
 stream yang-push
 update-policy periodic 6000
 receiver ip address 10.1.1.3 57500 protocol grpc-tcp
```

**Explanation:**
- Monitors Power over Ethernet operational data
- Tracks power consumption and PoE port status

**Step 3: Configure Memory Statistics Subscription**

```
telemetry ietf subscription 1030
 encoding encode-kvgpb
 filter xpath /memory-ios-xe-oper:memory-statistics/memory-statistic
 source-address 10.1.1.15
 stream yang-push
 update-policy periodic 6000
 receiver ip address 10.1.1.3 57500 protocol grpc-tcp
```

**Explanation:**
- Monitors memory usage statistics
- Tracks used, free, and total memory

**Step 4: Configure Temperature Subscription**

```
telemetry ietf subscription 1040
 encoding encode-kvgpb
 filter xpath /oc-platform:components/component/state/temperature
 source-address 10.1.1.15
 stream yang-push
 update-policy periodic 6000
 receiver ip address 10.1.1.3 57500 protocol grpc-tcp
```

**Explanation:**
- Uses OpenConfig YANG model for platform data
- Monitors temperature sensors across device components

**Step 5: Exit and save configuration**

```
end
write memory
```

**Step 6: Verify subscriptions**

Check that subscriptions are active:

```
show telemetry ietf subscription all
```

You should see all four subscriptions (1010, 1020, 1030, 1040) listed with their status.

Check subscription details:

```
show telemetry ietf subscription 1010 detail
```

---

### Visualizing Telemetry Data with Grafana

Grafana is an open-source analytics and visualization platform that connects to time-series databases to create real-time dashboards.

**Grafana Benefits:**
- **Multi-datasource support**: Connects to InfluxDB, Prometheus, Elasticsearch, etc.
- **Customizable dashboards**: Create tailored views for your metrics
- **Alerting**: Set thresholds and receive notifications
- **Plugin ecosystem**: Extend functionality with community plugins

#### Data Flow Architecture

```
Catalyst 9300 → gRPC/TCP → Telegraf Collector → InfluxDB → Grafana Dashboard
```

1. **Switch**: Streams telemetry data via gRPC
2. **Telegraf**: Collects and processes telemetry streams
3. **InfluxDB**: Stores time-series data
4. **Grafana**: Queries InfluxDB and displays dashboards

#### Accessing the Grafana Dashboard

**Step 1: Open Grafana in your browser**

The SSH tunnel you created earlier forwards Grafana to your local machine:

```
http://localhost:13000/
```

**Step 2: Login to Grafana**

- **Username**: admin
- **Password**: Cisco123

**Step 3: Navigate to the IOS XE Telemetry Dashboard**

Once logged in, you should see a pre-configured dashboard with panels for:

- **CPU Utilization**: 5-second CPU usage trends
- **Memory Consumption**: Current and average memory usage
- **Temperature Readings**: Max, min, and average temperatures
- **Power Statistics**: PoE consumption and status

**Step 4: Adjust time range (if needed)**

If data isn't displaying, adjust the time range in the top-right corner:
- Click the time range selector
- Select "Last 5 minutes" or "Last 15 minutes"
- Enable auto-refresh (5s or 10s intervals)

#### Understanding the Dashboard Panels

**CPU Utilization Panel:**
- Shows real-time CPU usage from subscription 1010
- Displays 5-second average CPU percentage
- Useful for identifying performance issues

**Memory Statistics Panel:**
- Tracks memory consumption patterns
- Shows used vs. free memory
- Helps identify memory leaks or capacity issues

**Temperature Panel:**
- Displays temperature sensors from subscription 1040
- Shows min, max, and average temperatures
- Critical for thermal monitoring

**PoE Power Panel:**
- Shows PoE operational data from subscription 1020
- Tracks power consumption per port
- Monitors PoE budget utilization

#### Exploring Grafana Features

**Create Custom Panels:**

1. Click "Add panel" on the dashboard
2. Select your data source (InfluxDB)
3. Build queries to visualize specific metrics
4. Customize visualization type (graph, gauge, table)

**Set Up Alerts:**

1. Edit a panel
2. Navigate to the "Alert" tab
3. Configure alert conditions (e.g., CPU > 80%)
4. Add notification channels (email, Slack, etc.)

**Export Dashboards:**

- Share dashboards with team members
- Export as JSON for version control
- Import community dashboards from Grafana.com

---

### Introduction to OpenTelemetry

OpenTelemetry (OTel) is an open-source observability framework that provides a vendor-agnostic approach to collecting, processing, and exporting telemetry data (metrics, logs, and traces).

**OpenTelemetry Benefits:**
- **Vendor-neutral**: Works with any observability backend (Splunk, Datadog, etc.)
- **Unified instrumentation**: Single standard for metrics, logs, and traces
- **Language support**: SDKs for Python, Go, Java, and more
- **Flexible architecture**: Collectors can process and route data

**OpenTelemetry Architecture:**

```
Data Sources → OTel Collector → Processors → Exporters → Backends (Splunk, etc.)
```

#### OpenTelemetry Components

1. **Instrumentation**: SDKs and libraries to generate telemetry
2. **Collector**: Receives, processes, and exports telemetry
3. **Protocol (OTLP)**: Standard protocol for telemetry data exchange
4. **Exporters**: Send data to observability platforms

---

### Integrating Network Telemetry with OpenTelemetry and Splunk

Splunk is a powerful platform for searching, monitoring, and analyzing machine-generated data. By integrating OpenTelemetry with Splunk, you can correlate network telemetry with application and infrastructure data.

#### Architecture: IOS XE → OpenTelemetry → Splunk

```
Catalyst 9300 → Telegraf → OpenTelemetry Collector → Splunk HEC
                                                     ↓
                                               Splunk Enterprise
```

**Integration Benefits:**
- **Centralized observability**: Network + App + Infra in one platform
- **Advanced analytics**: Use Splunk's search and correlation capabilities
- **Alerting and dashboards**: Splunk's visualization and alerting
- **Compliance**: Meet audit and compliance requirements

#### OpenTelemetry Collector Configuration

The OpenTelemetry Collector receives telemetry data and exports it to Splunk using the HTTP Event Collector (HEC).

**Example OTel Collector Configuration (otel-collector-config.yaml):**

```yaml
receivers:
  # Receive telemetry from Telegraf
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  # Add resource attributes
  resource:
    attributes:
      - key: deployment.environment
        value: "production"
        action: upsert
      - key: device.type
        value: "catalyst-9300"
        action: upsert
  
  # Batch telemetry for efficiency
  batch:
    timeout: 10s
    send_batch_size: 1024

exporters:
  # Export to Splunk HEC
  splunk_hec:
    token: "YOUR-SPLUNK-HEC-TOKEN"
    endpoint: "https://splunk.example.com:8088/services/collector"
    source: "iosxe:telemetry"
    sourcetype: "iosxe:mdt"
    index: "network_telemetry"
    tls:
      insecure_skip_verify: false

  # Also export to logging for debugging
  logging:
    loglevel: info

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [resource, batch]
      exporters: [splunk_hec, logging]
```

#### Configuring Splunk HTTP Event Collector (HEC)

**Step 1: Enable HEC in Splunk**

1. Log into Splunk Web
2. Navigate to **Settings → Data Inputs**
3. Click **HTTP Event Collector**
4. Click **Global Settings**
5. Enable "All Tokens"
6. Set HTTP Port (default: 8088)

**Step 2: Create HEC Token**

1. Click **New Token**
2. Name: "iosxe-telemetry"
3. Source type: "iosxe:mdt"
4. Index: "network_telemetry"
5. Click **Review → Submit**
6. Copy the token value

**Step 3: Configure OpenTelemetry Collector**

Update the `otel-collector-config.yaml` with your Splunk details:

```yaml
exporters:
  splunk_hec:
    token: "PASTE-YOUR-TOKEN-HERE"
    endpoint: "https://your-splunk-server:8088/services/collector"
    source: "catalyst-9300"
    sourcetype: "iosxe:mdt"
    index: "network_telemetry"
```

**Step 4: Start OpenTelemetry Collector**

```bash
cd ~/otel-collector
./otelcol --config otel-collector-config.yaml
```

#### Configuring Telegraf to Export to OpenTelemetry

Modify the Telegraf configuration to forward to OTel Collector:

**Edit telegraf.conf:**

```toml
# Receive gRPC telemetry from IOS XE
[[inputs.cisco_telemetry_mdt]]
  transport = "grpc"
  service_address = ":57500"

# Output to OpenTelemetry Collector
[[outputs.opentelemetry]]
  service_address = "localhost:4317"
  compression = "gzip"
  
  [outputs.opentelemetry.attributes]
    source = "catalyst-9300"
    location = "datacenter-1"
```

**Restart Telegraf:**

```bash
sudo systemctl restart telegraf
```

---

### Creating Splunk Dashboards for Network Telemetry

Once telemetry data flows into Splunk, you can create powerful dashboards and searches.

#### Basic Splunk Searches for IOS XE Telemetry

**Search 1: View all telemetry data**

```spl
index=network_telemetry sourcetype=iosxe:mdt
| table _time, source, metric_name, metric_value
```

**Search 2: CPU Utilization over time**

```spl
index=network_telemetry sourcetype=iosxe:mdt metric_name="cpu-utilization"
| timechart avg(metric_value) as "Average CPU %"
```

**Search 3: Memory usage trends**

```spl
index=network_telemetry sourcetype=iosxe:mdt metric_name="memory-usage"
| timechart avg(metric_value) as "Memory Used (MB)"
```

**Search 4: Temperature alerts**

```spl
index=network_telemetry sourcetype=iosxe:mdt metric_name="temperature"
| where metric_value > 75
| stats count by source, component
```

**Search 5: Correlate network and application metrics**

```spl
index=network_telemetry OR index=application_logs
| stats avg(cpu_usage) as network_cpu, avg(app_response_time) as app_latency by _time span=5m
| eval correlation=if(network_cpu>80 AND app_latency>1000, "High", "Normal")
```

#### Creating a Splunk Dashboard

**Step 1: Save your searches**

After running searches, click "Save As → Dashboard Panel"

**Step 2: Build the dashboard**

1. Navigate to **Dashboards → Create New Dashboard**
2. Name: "IOS XE Network Telemetry"
3. Add panels for each metric:
   - CPU Utilization (Line chart)
   - Memory Usage (Area chart)
   - Temperature (Single value with trend)
   - Interface Statistics (Table)

**Step 3: Set up real-time monitoring**

- Enable real-time search on panels
- Set refresh intervals (30s, 1m, etc.)
- Configure drill-downs for detailed analysis

**Step 4: Create alerts**

1. Click **Settings → Searches, reports, and alerts**
2. Create new alert
3. Define search query
4. Set trigger conditions
5. Configure alert actions (email, webhook, etc.)

**Example Alert: High CPU**

```spl
index=network_telemetry sourcetype=iosxe:mdt metric_name="cpu-utilization"
| stats avg(metric_value) as cpu_avg by source
| where cpu_avg > 80
```

Trigger: When number of results > 0
Action: Send email to network-ops@company.com

---

### Advanced Use Cases

#### Use Case 1: Predictive Analytics

Use Splunk's Machine Learning Toolkit to predict issues:

```spl
index=network_telemetry sourcetype=iosxe:mdt metric_name="cpu-utilization"
| fit DensityFunction metric_value by source
| predict metric_value as predicted_cpu
```

#### Use Case 2: Anomaly Detection

Identify unusual patterns:

```spl
index=network_telemetry sourcetype=iosxe:mdt
| anomalydetection metric_value by metric_name
```

#### Use Case 3: Multi-Device Correlation

Compare metrics across multiple switches:

```spl
index=network_telemetry sourcetype=iosxe:mdt
| stats avg(metric_value) as avg_value by source, metric_name
| where metric_name="cpu-utilization"
| sort -avg_value
```

---

### Troubleshooting

**Issue 1: No data in Grafana**

- Verify subscriptions are active: `show telemetry ietf subscription all`
- Check Telegraf is running: `sudo systemctl status telegraf`
- Verify InfluxDB is storing data: `influx -execute 'SHOW DATABASES'`
- Check time range in Grafana dashboard

**Issue 2: OTel Collector not forwarding to Splunk**

- Verify HEC token is valid
- Check network connectivity to Splunk server
- Review OTel Collector logs: `journalctl -u otel-collector -f`
- Test HEC endpoint with curl:

```bash
curl -k https://splunk-server:8088/services/collector \
  -H "Authorization: Splunk YOUR-TOKEN" \
  -d '{"event": "test"}'
```

**Issue 3: Telegraf not receiving telemetry**

- Verify switch can reach receiver IP (10.1.1.3)
- Check firewall rules allow gRPC traffic (port 57500)
- Review Telegraf logs: `sudo journalctl -u telegraf -f`

---

### Key Takeaways

1. **Model-Driven Telemetry provides real-time visibility** into network device operations
2. **Subscriptions are flexible** - monitor any YANG data path with custom intervals
3. **Grafana offers powerful visualization** for time-series telemetry data
4. **OpenTelemetry provides vendor-neutral observability** with flexible routing
5. **Splunk integration enables advanced analytics** and correlation with other data sources
6. **Combining MDT + OTel + Splunk** creates a comprehensive observability platform

### Additional Resources

- [Cisco Model-Driven Telemetry Documentation](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/179/b_179_programmability_cg/model_driven_telemetry.html)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Splunk HEC Documentation](https://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector)
- [Grafana Documentation](https://grafana.com/docs/)
- [Telegraf Cisco MDT Input Plugin](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/cisco_telemetry_mdt)

### Next Steps

You've now completed:
- **Day 0**: Secure device onboarding with SZTP
- **Day 1**: Configuration management with Atomic Config Replace
- **Day 2**: Monitoring and observability with MDT, OpenTelemetry, and Splunk

Continue exploring the **Tooling Module** to learn Infrastructure as Code with Terraform!


---

# Tooling Module

## Infrastructure as Code with Terraform and Cisco IOS XE

### Introduction to Terraform Provider for IOS XE

Terraform is a declarative Infrastructure as Code (IaC) tool that allows you to define and provision network infrastructure using configuration files. The [Cisco IOS XE Terraform Provider](https://registry.terraform.io/providers/CiscoDevNet/iosxe/latest/docs) enables you to manage IOS XE devices using both NETCONF and RESTCONF protocols.

**Benefits of using Terraform with IOS XE:**
- **Declarative configuration**: Define desired state, Terraform handles the how
- **Version control**: Track configuration changes in Git
- **Repeatability**: Apply the same configuration across multiple devices
- **Idempotent**: Safe to run multiple times without side effects
- **State management**: Track actual vs. desired configuration state

### Prerequisites

Before starting, ensure you have:

1. Terraform installed on the VM
2. Access to the C9300 switch (10.1.1.15)
3. NETCONF enabled on the switch

### Lab Setup

**Step 1: Install Terraform**

From your SSH session on the VM, install Terraform:

```bash
# Download Terraform (check for latest version at terraform.io) This step has already been done for you in this environment
# cd ~
# wget https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip
# unzip terraform_1.7.0_linux_amd64.zip
# sudo mv terraform /usr/local/bin/
# terraform version
```

**Step 2: Create a working directory**

```bash
mkdir -p ~/CLUS2026-terraform-iosxe-lab
cd ~/CLUS2026-terraform-iosxe-lab
```

### Demo 1: Configure Extended ACLs and Apply to Interface

In this demo, you'll use Terraform to create an extended Access Control List (ACL) and apply it to an interface on the C9300 switch.

#### Objective
Learn how to use Terraform to configure network security policies using ACLs via NETCONF/YANG.

#### Steps

**Step 1: Create the Terraform provider configuration**

Create a file called `provider.tf`:

```bash
nano provider.tf
```

Add the following content:

```hcl
terraform {
  required_providers {
    iosxe = {
      source  = "CiscoDevNet/iosxe"
      version = "~> 0.17.0"
    }
  }
}

provider "iosxe" {
  username = "admin"
  password = "Cisco123"
  host     = "10.1.1.15"
  protocol = "netconf"
  insecure = true
}
```

Save and exit (Ctrl+X, Y, Enter).

**Step 2: Create the Extended ACL configuration**

Create a file called `acl.tf`:

```bash
nano acl.tf
```

Add the following configuration to create an extended ACL:

```hcl
# Extended ACL for securing management traffic
resource "iosxe_access_list_extended" "management_acl" {
  name = "MGMT_ACCESS"
  
  entries = [
    {
      sequence                 = 10
      remark                   = "Allow SSH from management subnet"
      ace_rule_action          = "permit"
      ace_rule_protocol        = "tcp"
      source_prefix            = "10.0.0.0"
      source_prefix_mask       = "0.0.255.255"
      destination_any          = true
      destination_port_equal   = "22"
    },
    {
      sequence                 = 20
      remark                   = "Allow HTTPS from management subnet"
      ace_rule_action          = "permit"
      ace_rule_protocol        = "tcp"
      source_prefix            = "10.0.0.0"
      source_prefix_mask       = "0.0.255.255"
      destination_any          = true
      destination_port_equal   = "443"
    },
    {
      sequence                 = 30
      remark                   = "Allow ICMP for troubleshooting"
      ace_rule_action          = "permit"
      ace_rule_protocol        = "icmp"
      source_any               = true
      destination_any          = true
    },
    {
      sequence                 = 40
      remark                   = "Deny all other traffic"
      ace_rule_action          = "deny"
      ace_rule_protocol        = "ip"
      source_any               = true
      destination_any          = true
      log                      = true
    }
  ]
}

# Additional ACL for data plane traffic
resource "iosxe_access_list_extended" "data_acl" {
  name = "DATA_TRAFFIC"
  
  entries = [
    {
      sequence                 = 10
      remark                   = "Permit established TCP connections"
      ace_rule_action          = "permit"
      ace_rule_protocol        = "tcp"
      source_any               = true
      destination_any          = true
      established              = true
    },
    {
      sequence                 = 20
      remark                   = "Permit HTTP traffic"
      ace_rule_action          = "permit"
      ace_rule_protocol        = "tcp"
      source_any               = true
      destination_any          = true
      destination_port_equal   = "80"
    },
    {
      sequence                 = 30
      remark                   = "Permit DNS queries"
      ace_rule_action          = "permit"
      ace_rule_protocol        = "udp"
      source_any               = true
      destination_any          = true
      destination_port_equal   = "53"
    }
  ]
}
```

Save and exit.

**Step 3: Apply ACL to an interface**

Create a file called `interface.tf`:

```bash
nano interface.tf
```

Add configuration to apply the ACL to an interface:

```hcl
# Configure GigabitEthernet interface with ACL
resource "iosxe_interface_ethernet" "ge1_0_1" {
  type                      = "GigabitEthernet"
  name                      = "1/0/1"
  description               = "Managed by Terraform - ACL Applied"
  shutdown                  = false
  ip_access_group_in_enable = true
  ip_access_group_in        = iosxe_access_list_extended.data_acl.name
  ip_access_group_out_enable = true
  ip_access_group_out       = iosxe_access_list_extended.management_acl.name
}
```

Save and exit.

**Step 4: Initialize Terraform**

Initialize Terraform to download the IOS XE provider:

```bash
terraform init
```

You should see output indicating the provider was successfully installed.

**Step 5: Validate the configuration**

Check for syntax errors:

```bash
terraform validate
```

**Step 6: Preview the changes**

See what Terraform will configure:

```bash
terraform plan
```

Review the output carefully. Terraform will show you:
- Resources to be created
- ACL entries that will be configured
- Interface settings that will be applied

**Step 7: Apply the configuration**

Apply the configuration to the switch:

```bash
terraform apply
```

Type `yes` when prompted to confirm.

**Step 8: Verify on the device**

From your telnet session to the switch, verify the ACLs were created:

```
show ip access-lists MGMT_ACCESS
show ip access-lists DATA_TRAFFIC
show running-config interface GigabitEthernet1/0/1
```

**Key Takeaway**: Terraform provides a declarative way to configure ACLs and apply them to interfaces, with built-in validation and state tracking.

---

### Demo 2: VLAN Configuration with Terraform

In this demo, you'll create VLANs using Terraform and understand how to manage switching configurations as code.

#### Objective
Learn how to provision VLANs declaratively using Terraform.

#### Steps

**Step 1: Create VLAN configuration**

Create a file called `vlans.tf`:

```bash
nano vlans.tf
```

Add VLAN definitions:

```hcl
# Development VLAN
resource "iosxe_vlan" "dev_vlan" {
  vlan_id  = 100
  name     = "DEVELOPMENT"
  shutdown = false
}

# Production VLAN
resource "iosxe_vlan" "prod_vlan" {
  vlan_id  = 200
  name     = "PRODUCTION"
  shutdown = false
}

# Guest VLAN
resource "iosxe_vlan" "guest_vlan" {
  vlan_id  = 300
  name     = "GUEST_NETWORK"
  shutdown = false
}

# Management VLAN
resource "iosxe_vlan" "mgmt_vlan" {
  vlan_id  = 999
  name     = "MANAGEMENT"
  shutdown = false
}
```

Save and exit.

**Step 2: Plan and apply**

Preview the changes:

```bash
terraform plan
```

Apply the VLAN configuration:

```bash
terraform apply
```

Type `yes` to confirm.

**Step 3: Verify on the device**

From the switch:

```
show vlan brief
show vlan id 100
show vlan id 200
```

**Step 4: Modify a VLAN (demonstrating updates)**

Edit `vlans.tf` to change a VLAN name:

```bash
nano vlans.tf
```

Change the Development VLAN name:

```hcl
resource "iosxe_vlan" "dev_vlan" {
  vlan_id  = 100
  name     = "DEV_UPDATED"  # Changed from DEVELOPMENT
  shutdown = false
}
```

Save and apply:

```bash
terraform apply
```

Terraform will detect the change and update only that VLAN. Verify:

```
show vlan id 100
```

**Key Takeaway**: Terraform tracks state and only applies changes that differ from the current configuration, making updates efficient and predictable.

---

### Demo 3: Complete Network Segment with ACL, VLAN, and Interface

This comprehensive demo combines ACLs, VLANs, and interface configuration to provision a complete network segment.

#### Objective
Build a complete network configuration using Infrastructure as Code principles.

#### Steps

**Step 1: Create a complete configuration file**

Create `complete_config.tf`:

```bash
nano complete_config.tf
```

Add a comprehensive configuration:

```hcl
# Security VLAN
resource "iosxe_vlan" "security_vlan" {
  vlan_id  = 500
  name     = "SECURITY_ZONE"
  shutdown = false
}

# Security ACL
resource "iosxe_access_list_extended" "security_acl" {
  name = "SECURITY_ZONE_ACL"
  
  entries = [
    {
      sequence                 = 10
      remark                   = "Allow HTTPS to security appliances"
      ace_rule_action          = "permit"
      ace_rule_protocol        = "tcp"
      source_any               = true
      destination_prefix       = "10.5.5.0"
      destination_prefix_mask  = "0.0.0.255"
      destination_port_equal   = "443"
    },
    {
      sequence                 = 20
      remark                   = "Allow syslog"
      ace_rule_action          = "permit"
      ace_rule_protocol        = "udp"
      source_any               = true
      destination_prefix       = "10.5.5.10"
      destination_prefix_mask  = "0.0.0.0"
      destination_port_equal   = "514"
    },
    {
      sequence                 = 30
      remark                   = "Deny and log all other traffic"
      ace_rule_action          = "deny"
      ace_rule_protocol        = "ip"
      source_any               = true
      destination_any          = true
      log                      = true
    }
  ]
}

# Configure interface for security VLAN
resource "iosxe_interface_ethernet" "security_interface" {
  type                      = "GigabitEthernet"
  name                      = "1/0/2"
  description               = "Security Zone - Managed by Terraform"
  shutdown                  = false
  ip_access_group_in_enable = true
  ip_access_group_in        = iosxe_access_list_extended.security_acl.name
  
  # Dependencies ensure proper order
  depends_on = [
    iosxe_vlan.security_vlan,
    iosxe_access_list_extended.security_acl
  ]
}
```

Save and exit.

**Step 2: Apply the complete configuration**

```bash
terraform plan
terraform apply
```

**Step 3: View Terraform state**

Terraform maintains state of all managed resources:

```bash
terraform show
terraform state list
```

**Step 4: Verify the complete configuration**

From the switch:

```
show vlan id 500
show ip access-lists SECURITY_ZONE_ACL
show running-config interface GigabitEthernet1/0/2
```

---

### Terraform Best Practices for IOS XE

1. **Use version control**: Store `.tf` files in Git for change tracking
2. **State management**: Keep `terraform.tfstate` backed up (or use remote state)
3. **Module reuse**: Create reusable modules for common patterns
4. **Validate before apply**: Always run `terraform plan` first
5. **Use variables**: Parameterize configurations with `variables.tf`
6. **Documentation**: Comment your code with `#` and resource descriptions

### Advanced Exercise: Using Variables

Create a `variables.tf` file to make your configuration more flexible:

```hcl
variable "switch_ip" {
  description = "IP address of the IOS XE device"
  type        = string
  default     = "10.1.1.15"
}

variable "switch_username" {
  description = "Username for device authentication"
  type        = string
  default     = "admin"
  sensitive   = true
}

variable "switch_password" {
  description = "Password for device authentication"
  type        = string
  default     = "Cisco123"
  sensitive   = true
}
```

Then update `provider.tf` to use variables:

```hcl
provider "iosxe" {
  username = var.switch_username
  password = var.switch_password
  host     = var.switch_ip
  protocol = "netconf"
  insecure = true
}
```

### Cleanup (Optional)

To remove all Terraform-managed resources:

```bash
terraform destroy
```

Type `yes` to confirm. This will remove all ACLs, VLANs, and interface configurations created by Terraform.

### Additional Resources

- [Terraform IOS XE Provider Documentation](https://registry.terraform.io/providers/CiscoDevNet/iosxe/latest/docs)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)
- [IOS XE YANG Models](https://github.com/YangModels/yang/tree/master/vendor/cisco/xe)

### Summary

In this module, you learned how to:
- Install and configure the Terraform IOS XE provider
- Create extended ACLs using declarative configuration
- Provision VLANs with Infrastructure as Code
- Apply ACLs to interfaces programmatically
- Manage configuration state with Terraform
- Build complete network segments using IaC principles

Terraform provides a powerful, version-controlled approach to network configuration management that integrates seamlessly with modern DevOps workflows.



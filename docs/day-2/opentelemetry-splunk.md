# OpenTelemetry + Splunk

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

### Production-Ready OpenTelemetry Collector for Cisco IOS XE

!!! info "Advanced Implementation Available"
    This lab guide covers the fundamentals of Model-Driven Telemetry with Telegraf and OpenTelemetry concepts. For a **production-ready implementation**, see Jeremy Cohoe's comprehensive OpenTelemetry Collector with native Cisco IOS XE support:
    
    🔗 **[otel-grpc-cisco-receiver](https://github.com/jeremycohoe/otel-grpc-cisco-receiver)**
    
    **Key Features:**
    
    - **Native Cisco MDT Receiver**: Direct gRPC dial-out support with kvGPB decoding (no Telegraf intermediary)
    - **YANG Model Processing**: Automatic key propagation and type awareness for all IOS XE paths
    - **7 Splunk Dashboards**: Ready-to-import dashboards for infrastructure, network, routing, power, security
    - **49 Pre-configured Subscriptions**: Complete MDT subscription set for production monitoring
    - **Production Features**: TLS/mTLS, Docker Compose stack, automated deployment scripts
    - **Performance**: >1,000 messages/sec with <10ms p99 latency
    
    The repository includes complete setup guides, configuration examples, and Splunk integration ready for production deployment.

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
- **[Production OpenTelemetry Collector for Cisco IOS XE](https://github.com/jeremycohoe/otel-grpc-cisco-receiver)** - Native receiver with 7 Splunk dashboards and 49 subscriptions

### Next Steps

You've now completed:

- **Day 0**: Secure device onboarding with SZTP
- **Day 1**: Configuration management with Atomic Config Replace
- **Day 2**: Monitoring and observability with MDT, OpenTelemetry, and Splunk

Continue exploring the **Tooling Module** to learn Infrastructure as Code with Terraform!


---


---

## Next Steps

✅ Completed: Day 2 - OpenTelemetry + Splunk

**Continue with Day 2:**

➡️ [gNXI Innovations](gnxi-innovations.md) - Explore advanced gNXI features

**Or navigate to:**
- [Day 2 Overview](index.md)
- [Day N: Device Optimization](../day-n/index.md)

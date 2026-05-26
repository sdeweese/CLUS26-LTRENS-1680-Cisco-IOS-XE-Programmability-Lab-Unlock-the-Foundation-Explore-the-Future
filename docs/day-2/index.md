# Day 2 - Device Monitoring

## Overview

Day 2 focuses on modern network observability using model-driven telemetry, OpenTelemetry, and Splunk.

This track uses an OTel-only pipeline for telemetry collection and export.

### What You'll Learn

- Model-Driven Telemetry (MDT) fundamentals
- OpenTelemetry integration with IOS XE telemetry
- Splunk HEC ingestion and dashboard-based analytics
- gNXI innovations (POLL/ONCE, ACL & VRF enhancements)

### Topics Covered

1. **OpenTelemetry + Splunk**: Centralized observability platform
2. **gNXI Innovations**: Advanced gRPC network management features

---

## Lab Modules

### [OpenTelemetry + Splunk](opentelemetry-splunk.md)
Learn how to ingest IOS XE telemetry directly into OpenTelemetry and export to Splunk.

**Topics:**

- Model-Driven Telemetry configuration
- OpenTelemetry Collector (`cisco_telemetry`) setup
- Splunk HEC integration
- Dashboard import and validation

**Reference implementation (upstream repo):**

- [otel-grpc-cisco-receiver repository](https://github.com/jeremycohoe/otel-grpc-cisco-receiver)
- [README.md](https://github.com/jeremycohoe/otel-grpc-cisco-receiver/blob/main/README.md)
- [SPLUNK-SETUP.md](https://github.com/jeremycohoe/otel-grpc-cisco-receiver/blob/main/SPLUNK-SETUP.md)
- [docs/CONFIG.md](https://github.com/jeremycohoe/otel-grpc-cisco-receiver/blob/main/docs/CONFIG.md)
- [docs/SECURITY.md](https://github.com/jeremycohoe/otel-grpc-cisco-receiver/blob/main/docs/SECURITY.md)

---

### [gNXI Innovations](gnxi-innovations.md)
Explore advanced gNXI features including POLL/ONCE operations and API security enhancements.

**Topics:**

- gNXI POLL/ONCE for on-demand data
- API Security: ACL and VRF support
- Advanced use cases

---

## Next Steps

✅ Completed: Day 2 Overview

**Start with a topic:**

- ➡️ [OpenTelemetry + Splunk](opentelemetry-splunk.md) - Recommended starting point
- [gNXI Innovations](gnxi-innovations.md)

**Or navigate to:**
- [Day N: Device Optimization](../day-n/index.md)
- [Back to Day 1](../day-1/index.md)

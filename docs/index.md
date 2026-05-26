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

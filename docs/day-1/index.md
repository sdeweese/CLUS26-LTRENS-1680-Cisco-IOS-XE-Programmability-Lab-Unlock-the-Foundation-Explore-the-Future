# Day 1 - Device Configuration

## Overview

Day 1 covers modern configuration management approaches for Cisco IOS XE devices, focusing on atomic operations, network-as-code, and automation frameworks.

### What You'll Learn

- Atomic configuration operations with NETCONF
- Infrastructure as Code with Terraform
- Configuration automation with Ansible and gNMI
- Network testing and validation with PyATS

### Topics Covered

1. **Atomic Config Replace (ACR)**: Safe, atomic configuration changes via NETCONF
2. **Terraform + NETCONF**: Declarative infrastructure as code
3. **Ansible + gNMI**: Configuration management with gNMI protocol
4. **PyATS**: Automated testing and validation

### Key Concepts

- **Atomic Operations**: All-or-nothing configuration changes
- **Declarative Configuration**: Define desired state, let tools handle implementation
- **Idempotency**: Safe to run multiple times without side effects
- **Version Control**: Track configuration changes in Git

---

## Lab Modules

### [Atomic Config Replace](atomic-operations.md)
Learn how to safely replace device configurations using NETCONF atomic operations. Includes error detection, automatic rollback, and confirmed commits.

**Topics:**

- ACR fundamentals and workflow
- Syntax and dependency error isolation
- Automatic rollback without confirm commit
- Day 1 to Day N lifecycle management

---

### [Terraform + NETCONF](terraform-netconf.md)
Build network infrastructure as code using Terraform's IOS XE provider with NETCONF protocol.

**Topics:**

- Terraform IOS XE provider setup
- Creating ACLs and VLANs declaratively
- State management and drift detection
- Modular configuration patterns

---

### [Ansible + gNMI](ansible-gnmi.md)
Automate configuration management using Ansible with gNMI (gRPC Network Management Interface).

**Topics:**

- Ansible gNMI module configuration
- Playbook development for IOS XE
- Template-based configuration
- Role-based automation

---

### [PyATS Testing](pyats-testing.md)
Implement automated network testing and validation using Cisco's PyATS framework.

**Topics:**

- PyATS testbed setup
- Writing test cases for configuration validation
- Automated testing workflows
- Integration with CI/CD pipelines

---

## Next Steps

✅ Completed: Day 1 Overview

**Start with a topic:**

- ➡️ [Atomic Config Replace](atomic-operations.md) - Recommended starting point
- [Terraform + NETCONF](terraform-netconf.md)
- [Ansible + gNMI](ansible-gnmi.md)
- [PyATS Testing](pyats-testing.md)

**Or navigate to:**
- [Day 2: Device Monitoring](../day-2/index.md)
- [Back to Day 0](../day-0/index.md)

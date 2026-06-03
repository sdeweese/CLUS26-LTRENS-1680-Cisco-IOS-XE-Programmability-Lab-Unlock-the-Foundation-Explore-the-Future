# Day 1 - Device Configuration

## Overview

Day 1 covers modern configuration management approaches for Cisco IOS XE devices, focusing on atomic operations, network-as-code, and automation frameworks.

### What You'll Learn

- Infrastructure as Code with Terraform
- Network testing and validation with PyATS
- Atomic configuration operations with NETCONF

### Topics Covered

1. **Terraform + NETCONF**: Declarative infrastructure as code
2. **PyATS**: Automated testing and validation
3. **Atomic Config Replace (ACR)**: Safe, atomic configuration changes via NETCONF

### Key Concepts

- **Atomic Operations**: All-or-nothing configuration changes
- **Declarative Configuration**: Define desired state, let tools handle implementation
- **Idempotency**: Safe to run multiple times without side effects
- **Version Control**: Track configuration changes in Git

---

## Lab Modules

### [Terraform + NETCONF](terraform-netconf.md)
Build network infrastructure as code using Terraform's IOS XE provider with NETCONF protocol.

**Topics:**

- Terraform IOS XE provider setup
- Creating ACLs and VLANs declaratively
- State management and drift detection
- Modular configuration patterns

---

### [PyATS Testing](pyats-testing.md)
Implement automated network testing and validation using Cisco's PyATS framework.

**Topics:**

- PyATS testbed setup
- Writing test cases for configuration validation
- Automated testing workflows
- Integration with CI/CD pipelines

---

### [Atomic Config Replace](atomic-operations.md)
Learn how to safely replace device configurations using NETCONF atomic operations. Includes error detection, automatic rollback, and confirmed commits.

**Topics:**

- ACR fundamentals and workflow
- Syntax and dependency error isolation
- Automatic rollback without confirm commit
- Day 1 to Day N lifecycle management

---

## Next Steps

✅ Completed: Day 1 Overview

**Start with a topic:**

- ➡️ [Terraform + NETCONF](terraform-netconf.md) - Recommended starting point
- [PyATS Testing](pyats-testing.md)
- [Atomic Config Replace](atomic-operations.md)

**Or navigate to:**
- [Day 2: Device Monitoring](../day-2/index.md)
- [Back to Day 0](../day-0/index.md)

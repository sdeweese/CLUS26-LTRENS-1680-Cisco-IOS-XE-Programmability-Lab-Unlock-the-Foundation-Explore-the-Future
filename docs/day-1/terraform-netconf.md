# Terraform + NETCONF

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

### NETCONF vs RESTCONF Support

The Cisco IOS XE Terraform provider has evolved to support multiple management protocols:

- **Version 0.10.0 (Oct 2023)**: NETCONF support added (experimental) - first version to support both protocols
- **Version 0.15.0 (Jan 2024)**: **Default changed from RESTCONF to NETCONF** (breaking change)
- **Current versions (0.15.0+)**: NETCONF is the default and recommended protocol

**Why NETCONF is now the default:**

| Feature | NETCONF | RESTCONF |
|---------|---------|----------|
| Transport | SSH (port 830) | HTTP/HTTPS (port 443) |
| Data format | XML | JSON/XML |
| Operations | Rich RPC operations, candidate datastore | REST CRUD operations |
| Performance | Lower overhead, persistent connection | Higher overhead, stateless |
| Atomic commits | Yes (with candidate datastore) | Limited |
| Industry standard | IETF RFC 6241 | IETF RFC 8040 |

**When to use RESTCONF:**
- Legacy environments that require HTTPS-only management
- Integration with REST-based automation tools
- Environments where SSH/NETCONF is blocked

**Configuration Resources:**

All Terraform resources use YANG models for configuration. For detailed documentation on YANG-based resources and their attributes, see:

- [IOS XE YANG Resources Documentation](https://registry.terraform.io/providers/CiscoDevNet/iosxe/latest/docs/resources/yang)
- [Provider Configuration Guide](https://registry.terraform.io/providers/CiscoDevNet/iosxe/latest/docs)

> **Note**: In this lab, we use NETCONF as it provides better performance and supports advanced features like candidate datastores and atomic commits.

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
  
  # Protocol: "netconf" (default, recommended) or "restconf"
  # NETCONF provides better performance and atomic operations
  protocol = "netconf"
  
  # Skip TLS certificate verification (lab environment only)
  insecure = true
}

# Optional: To use RESTCONF instead, change protocol:
# provider "iosxe" {
#   username = "admin"
#   password = "Cisco123"
#   host     = "10.1.1.15"
#   protocol = "restconf"
#   url      = "https://10.1.1.15"  # Required for RESTCONF
#   insecure = true
# }
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



---

## Next Steps

✅ Completed: Day 1 - Terraform + NETCONF

**Continue with Day 1:**

➡️ [Ansible + gNMI](ansible-gnmi.md) - Learn configuration automation

**Or explore:**
- [Atomic Config Replace](atomic-operations.md)
- [PyATS Testing](pyats-testing.md)
- [Day 1 Overview](index.md)
- [Day 2: Device Monitoring](../day-2/index.md)

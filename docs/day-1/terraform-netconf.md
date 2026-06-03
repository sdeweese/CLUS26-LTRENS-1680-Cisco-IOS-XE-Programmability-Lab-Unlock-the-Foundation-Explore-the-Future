# Terraform + NETCONF

# Tooling Module

## Infrastructure as Code with Terraform and Cisco IOS XE

!!! info "Tested on"
    - **Device:** Cisco Catalyst C9300 running IOS XE 26.1
    - **Terraform:** 1.3.4+
    - **Provider:** `CiscoDevNet/iosxe ~> 0.18.0` (NETCONF transport)

## Student Quick Path (Pre-Provisioned Lab)

This module is structured so you build confidence before making any changes:

1. **Demo 1 — Read-only sanity check.** Use a Terraform `data` source to read device state. Proves auth + transport + provider without any device risk. **Always run this first.**
2. **Demo 2 — Create an ACL + Loopback.** First write. Smallest blast radius (loopback interface, never a front-panel port).
3. **Demo 3 — VLAN configuration.** Demonstrates `terraform apply` updating only what changed.

A side-by-side **NetasCode intent ↔ Terraform** mapping is included at the **end** of this guide for reference and design discussion. You do not need to run any of those files — the lab is driven entirely by the three demos above.


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

- **Version 0.10.0 (Oct 2023)**: NETCONF support added; first version to support both NETCONF & RESTCONF protocols
- **Version 0.15.0 (Jan 2024)**: **Default changed from RESTCONF to NETCONF** (major change)
- **Current versions (0.18.0+)**: NETCONF is the default and recommended protocol

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
2. Access to the C9300 switch (10.1.1.55)
3. NETCONF enabled on the switch

### Lab Setup

**Step 0: Open a Terminal tab to connect to your 9300 switch**

In a new terminal window, SSH to your 9300 switch

```
ssh admin@10.1.1.55
```

Password

```
Cisco123
```

Once you are connected to the device, run this command to learn about the current NETCONF & RESTCONF configuration
```
show running-config | include netconf-yang|restconf|atomic|candidate
```

Confirm that the output resembles this:
```
netconf-yang
netconf-yang feature candidate-datastore
netconf-yang ssh local-vrf guestshell enable
restconf
yang-interfaces feature atomic-config
```

**Step 1: Install Terraform**

From your SSH session on the VM, ensure Terraform is installed.

In this lab image, Terraform is already installed, so this step is typically not required for you. However, if you are running this in your own environment, you will need to run the following commands:

```bash
# Download Terraform (check for latest version at terraform.io) This step has already been done for you in this environment
# cd ~
# wget https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip
# unzip terraform_1.7.0_linux_amd64.zip
# sudo mv terraform /usr/local/bin/
# terraform version
```

**Step 2: Navigate to the working directory with the Terraform files**

Each demo lives in its own subdirectory under `~/CLUS2026-terraform-iosxe-lab/` so they have independent Terraform state and can be applied/destroyed without affecting each other:

```
~/CLUS2026-terraform-iosxe-lab/
├── tf-read/           (Demo 1)
│   └── main.tf
├── tf-acl-loopback/   (Demo 2)
│   ├── provider.tf
│   ├── acl.tf
│   └── loopback.tf
└── tf-vlans/          (Demo 3)
    ├── provider.tf
    └── vlans.tf
```

You will `cd` into the appropriate directory at the start of each demo and run `terraform init` once per directory.

### Demo 1: Get Current Configurations on Device using Terraform + NETCONF

Before you write *anything* to the device, prove that Terraform can talk to it. A Terraform `data` source fetches device state read-only. Nothing is created, modified, or removed. If this demo fails, the problem is authentication, networking, NETCONF, or the provider, not your config files. Ensure this step works before proceeding to the next steps.

#### Objective
Validate the full Terraform → NETCONF → Cisco IOS XE path using a read-only data source.

#### Steps

**Step 1: Navigate to the pre-staged read-only demo directory**

```bash
cd ~/CLUS2026-terraform-iosxe-lab/tf-read
```

**Step 2: Examine `main.tf`**

```bash
cat main.tf
```

You should see:

```hcl
terraform {
  required_providers {
    iosxe = {
      source  = "CiscoDevNet/iosxe"
      version = "~> 0.18.0"
    }
  }
}

provider "iosxe" {
  username = "admin"
  password = "Cisco123"
  host     = "10.1.1.55"
  protocol = "netconf"
  insecure = true
}

# READ-ONLY: fetch device system info via NETCONF get-config
data "iosxe_system" "this" {}

output "hostname" {
  value = data.iosxe_system.this.hostname
}

output "ip_routing_enabled" {
  value = data.iosxe_system.this.ip_routing
}
```

**Step 3: Initialize and run**

```bash
terraform init
terraform plan
terraform apply -auto-approve
```

Expected output ends with something like:

```
data.iosxe_system.this: Reading...
data.iosxe_system.this: Read complete after 5s [id=Cisco-IOS-XE-native:native]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real
infrastructure against your configuration
and found no differences, so no changes
are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

hostname           = "cat9300-pod-##c-sztp"
ip_routing_enabled = true
```

Note: ## will be your pod number


**Step 4: Interpret the result**

| Result | Meaning | Next step |
|---|---|---|
| Outputs print real values | NETCONF + auth + provider all healthy | Move on to Demo 2 |
| `Error: Client Error` on the data source | Provider can't reach NETCONF (auth, port 830, or transport) | Check `ssh -p 830 admin@10.1.1.55`; confirm `netconf-yang` is configured on device |
| Outputs are blank / null | YANG path returned no data | Run `show platform software yang-management process` on device — all should be `Running` |

**Key Takeaway**: `data` sources read; `resource` blocks write. Always read first when bringing a new device or provider version into your workflow — it isolates 90% of problems in 30 seconds, with zero device risk.

---

### Demo 2: Create an Extended ACL and a Loopback Interface

In this demo, you'll use Terraform to create an extended Access Control List (ACL) and a Loopback interface on the C9300 switch.
The ACL is created independently of any production interface so it cannot affect connectivity.

#### Objective
Learn how to use Terraform to configure ACLs and an isolated test interface via NETCONF/YANG.

#### Steps to create a Loopback and ACL with Terraform

**Step 0: Confirm that the following config does not yet exist on your device** Note: Through the following steps, we will add this configuration using Terraform and NETCONF. 

On your switch, type the following commands

```
show ip access-lists LAB_TEST_ACL
show running-config interface Loopback100
show ip interface Loopback100
```

Note: the last line should show an error because you don't have a Loopback100 interface configured yet.

Expected output:

```
cat9300-pod03b-sztp#
cat9300-pod03b-sztp#$LAB_TEST_ACL      
cat9300-pod03b-sztp#$oopback100        
show running-config interface Loopback100
% Invalid input detected at '^' marker.
```

**Step 1: Create the Terraform provider configuration**

The following steps should be completed from your VM tab (NOT your switch tab since we are using APIs to programmatically configure your switch.)

Navigate to the Demo 2 working directory:

```bash
cd ~/CLUS2026-terraform-iosxe-lab/tf-acl-loopback
```

Examine a file called `provider.tf`:

```bash
cat provider.tf
```

Review the following content:

```hcl
terraform {
  required_providers {
    iosxe = {
      source  = "CiscoDevNet/iosxe"
      version = "~> 0.18.0"
    }
  }
}

provider "iosxe" {
  username = "admin"
  password = "Cisco123"
  host     = "10.1.1.55"
  
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
#   host     = "10.1.1.55"
#   protocol = "restconf"
#   url      = "https://10.1.1.55"  # Required for RESTCONF
#   insecure = true
# }
```

**Step 2: Create the Extended ACL configuration**

Examine a file called `acl.tf`:

```bash
cat acl.tf
```

Examine the ACL that will be configured. Each entry uses only fields supported by the
Cisco-IOS-XE-native YANG `acl` model on 26.1. **Do not** add `remark`, `established`, or `log` to the same entry as a `permit`/`deny` rule. A `remark` is its own Access Control Entry (ACE)
type in the YANG model, and the device will refuse the commit if they are combined.

```hcl
# Simple extended ACL (no remark/established/log mixed in)
resource "iosxe_access_list_extended" "lab_test_acl" {
  name = "LAB_TEST_ACL"

  entries = [
    {
      sequence               = 10
      ace_rule_action        = "permit"
      ace_rule_protocol      = "tcp"
      source_any             = true
      destination_any        = true
      destination_port_equal = "22"
    },
    {
      sequence               = 20
      ace_rule_action        = "permit"
      ace_rule_protocol      = "tcp"
      source_any             = true
      destination_any        = true
      destination_port_equal = "443"
    },
    {
      sequence          = 30
      ace_rule_action   = "permit"
      ace_rule_protocol = "icmp"
      source_any        = true
      destination_any   = true
    },
    {
      sequence          = 40
      ace_rule_action   = "deny"
      ace_rule_protocol = "ip"
      source_any        = true
      destination_any   = true
    },
  ]
}
```


**Step 3: Create a safe Loopback interface**

Review a file called `loopback.tf`. We deliberately use `Loopback100` instead of a
front-panel port so the change has zero blast radius — a loopback never carries
production traffic and can be removed at any time.

```bash
cat loopback.tf
```

Examine the file to see the interface loopback configuration that will be applied

```hcl
resource "iosxe_interface_loopback" "lab_loopback" {
  name              = 100
  description       = "Terraform-managed lab loopback"
  ipv4_address      = "192.0.2.1"
  ipv4_address_mask = "255.255.255.0"
}
```

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
terraform apply --auto-approve
```

The output should show green + signs for all the configuration that was added and the last line should say "Apply complete! Resources: 2 added, 0 changed, 0 destroyed."

**Step 8: Verify on the device**

From your telnet session to the switch, verify the ACL and loopback were created:

```
show ip access-lists LAB_TEST_ACL
show running-config interface Loopback100
show ip interface Loopback100
```

The output should look similar to this:
```
Building configuration...

Current configuration : 123 bytes
!
interface Loopback100
 description Terraform-managed lab loopback
 ip address 192.0.2.1 255.255.255.0
 ip proxy-arp
end

cat9300-pod03b-sztp#$erface Loopback100
Loopback100 is up, line protocol is up
  Internet address is 192.0.2.1/24
  Broadcast address is 255.255.255.255
  Address determined by configuration file
  MTU is 1514 bytes
  Helper address is not set
  Directed broadcast forwarding is disabled
  Outgoing Common access list is not set 
  Outgoing access list is not set
  Inbound Common access list is not set 
  Inbound  access list is not set
  Proxy ARP is enabled
  Local Proxy ARP is disabled
  Security level is default
  Split horizon is enabled
  ICMP redirects are always sent
  ICMP unreachables are always sent
  ICMP mask replies are never sent
  IP fast switching is enabled
  IP Flow switching is disabled
  IP CEF switching is enabled
  ...
```

**Key Takeaway**: Terraform provides a declarative way to configure ACLs and isolated test interfaces with built-in validation and state tracking, without risking production connectivity.

---

### Demo 3: VLAN Configuration with Terraform

In this demo, you'll create VLANs using Terraform and understand how to manage switching configurations as code.

#### Objective
Learn how to provision VLANs declaratively using Terraform.

#### Steps

**Step 1: Examine the VLAN configuration**

Navigate to the Demo 3 working directory:

```bash
cd ~/CLUS2026-terraform-iosxe-lab/tf-vlans
```

View the VLAN definitions:

```bash
cat vlans.tf
```

You should see the following VLAN definition:

```hcl
# Management VLAN
resource "iosxe_vlan" "mgmt_vlan" {
  vlan_id  = 999
  name     = "MANAGEMENT"
  shutdown = false
}
```

**Step 2: Plan and apply**

Initialize this directory (one-time per working directory):

```bash
terraform init
```

Preview the changes:

```bash
terraform plan
```

Apply the VLAN configuration:

```bash
terraform apply --auto-approve
```

**Step 3: Verify on the device**

From the switch:

```
show vlan brief
show vlan id 999
```

**Step 4: Modify a VLAN (demonstrating updates)**

Open `vlans.tf` in your preferred editor and change the Management VLAN name from `MANAGEMENT` to `MGMT_UPDATED`:

```hcl
resource "iosxe_vlan" "mgmt_vlan" {
  vlan_id  = 999
  name     = "MGMT_UPDATED"  # Changed from MANAGEMENT
  shutdown = false
}
```

Save the file, then apply:

```bash
terraform apply --auto-approve
```

Terraform will detect the change and update only that VLAN. Verify:

```
show vlan id 999
```

**Step 5: Tear down with `terraform destroy`**

To return the device to its pre-demo state, destroy every resource Terraform created in this working directory. Because Demo 3 lives in its own subdirectory with its own state file, this only removes VLAN 999 — Demo 2's ACL and Loopback are untouched.

```bash
terraform destroy --auto-approve
```

Expected tail of output:

```
Destroy complete! Resources: 1 destroyed.
```

Verify on the switch that the VLAN is gone:

```
show vlan id 999
```

You should see `VLAN id 999 not found in current VLAN database`.

> **Tip**: Repeat the same pattern in `~/CLUS2026-terraform-iosxe-lab/tf-acl-loopback` (`terraform destroy --auto-approve`) to also remove Demo 2's ACL and Loopback when you're done with the module.

**Key Takeaway**: Terraform tracks state and only applies changes that differ from the current configuration, making updates efficient and predictable. `terraform destroy` is the inverse of `apply` and uses the same state file to cleanly roll back exactly what was created.

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
  default     = "10.1.1.55"
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

## Appendix: NetasCode for Cisco IOS XE
REFERENCE ONLY

[NetasCode](https://netascode.cisco.com/) is Cisco's higher-level **intent abstraction** over raw Terraform provider resources. You describe *what* the network should look like in compact YAML; NetasCode-distributed Terraform modules render that intent into the same `iosxe_*` resources you used in Demos 2–3.

The promise: you stop hand-writing HCL for every VLAN, ACL, and interface. You describe the desired switch in a few lines of YAML, and a curated module library handles the translation, schema validation, and dependency wiring.

### Intent ↔ Terraform mapping (reference)

These examples are **side-by-side reference only** — you do not run them in this lab. They show how a NetasCode-style intent file collapses verbose HCL into compact YAML.

#### Example 1: VLAN intent

```yaml
switches:
  - name: c9300-lab
    vlans:
      - id: 110
        name: DEV
      - id: 120
        name: PROD
```

Equivalent Terraform provider resources (what you'd write by hand without NetasCode):

```hcl
resource "iosxe_vlan" "dev_vlan" {
  vlan_id = 110
  name    = "DEV"
}

resource "iosxe_vlan" "prod_vlan" {
  vlan_id = 120
  name    = "PROD"
}
```

#### Example 2: ACL + interface attachment intent

```yaml
switches:
  - name: c9300-lab
    acls:
      - name: MGMT_ACL
        type: extended
        entries:
          - sequence: 10
            action: permit
            protocol: tcp
            source: 10.10.10.0/24
            destination: any
            destination_port: 22
          - sequence: 20
            action: deny
            protocol: ip
            source: any
            destination: any
    interfaces:
      - name: Loopback100
        acl_in: MGMT_ACL
```

Equivalent hand-written Terraform (~30+ lines of HCL) is shown in [Demo 2](#demo-2-create-an-extended-acl-and-a-loopback-interface).

### How to consume NetasCode without writing Terraform yourself

The repos and module families below let you treat Terraform as an *engine* and edit only YAML day to day. Pick the path that matches your environment:

1. **NetasCode for IOS XE — `terraform-iosxe-nac-modules`**
    - Cisco-published Terraform modules ([github.com/netascode](https://github.com/netascode)) that consume a YAML data model and produce the right `iosxe_*` resources.
    - Workflow: edit `data/switches.yaml` → `terraform plan` → `terraform apply`. You never open an `.hcl` file.
2. **`nac-data` + `nac-validate` CLI**
    - `pip install nac-validate` to lint your YAML against the published schema *before* Terraform sees it. Catches typos and structural mistakes without burning a `plan` cycle.
3. **Excel / Catalyst Center / NSO ingestion**
    - The same YAML schema can be generated from an Excel template (`nac-data` includes an XLSX → YAML converter), Catalyst Center inventory exports, or as the southbound output of an NSO service. Useful when the source of truth lives outside Git.
4. **CI/CD pipeline pattern**
    - GitHub Actions / GitLab CI runs: `nac-validate` (schema) → `terraform fmt -check` → `terraform plan` (uploaded as artifact for review) → manual approval → `terraform apply`. Operators only ever edit YAML.

### When to use NetasCode vs raw Terraform

| Use raw `iosxe_*` resources when… | Use NetasCode modules when… |
|---|---|
| You're learning the provider or debugging a specific resource | You manage 10+ devices with similar config patterns |
| You need a feature not yet in the abstraction layer | You want operators to edit YAML, not HCL |
| You're doing a one-off proof of concept | You need schema validation in CI |
| The provider is your only tool | You also use NSO, Catalyst Center, or Excel-based inventory and want one source of truth |

### Lab follow-on (do at your desk, not in the pod)

If you want to try NetasCode end-to-end against your own lab gear after the conference:

1. Clone an example NetasCode IOS XE repo: `git clone https://github.com/netascode/terraform-iosxe-nac-modules-example`
2. Edit `data/switches.yaml` for your devices.
3. Run `nac-validate data/`.
4. Run `terraform init && terraform plan && terraform apply`.
5. Compare the generated state to what your Demo 2–3 HCL produced — same provider, same NETCONF traffic, half the code.

---

## Lab Transition

Before moving to PyATS:

1. Run `terraform plan` one last time and confirm expected state.
2. If needed for a clean handoff, run `terraform destroy` to reset lab-created resources.
3. Return to your base lab workspace directory before starting the next module.

## Next Steps

✅ Completed: Day 1 - Terraform + NETCONF

**Continue with Day 1:**

➡️ [PyATS Testing](pyats-testing.md) - Automated network testing and validation

**Or explore:**
- [Atomic Config Replace](atomic-operations.md)
- [Day 1 Overview](index.md)
- [Day 2: Device Monitoring](../day-2/index.md)

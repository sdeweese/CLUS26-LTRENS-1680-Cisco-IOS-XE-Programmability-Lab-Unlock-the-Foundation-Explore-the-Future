# Atomic Config Replace (ACR)

## Introduction to Atomic Config Replace (ACR)

Atomic Config Replace (ACR) is a powerful NETCONF operation that allows network operators to fully replace the entire running configuration on a Cisco IOS XE device in a single atomic transaction. Unlike traditional configuration methods that apply changes line-by-line, ACR provides:


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



---

## Next Steps

✅ Completed: Day 1 - Atomic Config Replace

**Continue with Day 1:**

➡️ [Terraform + NETCONF](terraform-netconf.md) - Learn Infrastructure as Code

**Or explore:**

- [Ansible + gNMI](ansible-gnmi.md)
- [PyATS Testing](pyats-testing.md)
- [Day 1 Overview](index.md)
- [Day 2: Device Monitoring](../day-2/index.md)

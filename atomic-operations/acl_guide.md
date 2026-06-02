# gNMI ACL Lab Guide and Test Plan

## Overview
This guide provides step-by-step instructions to configure gNMI on IOS-XE, implement service-level ACLs, and test access control functionality.

---

## Part 1: Initial gNMI Setup

### Prerequisites
- IOS-XE device (version 26.1.1 or later for full gNxI, gNMI & gNOI, ACL support)
- Management interface with IP connectivity
- Admin/privilege 15 credentials

### Step 1: Enable gNMI Server

**Option A: Insecure Mode (Recommended for Lab Testing)**
note: this has already been done for you!

```cisco-ios
! Enter configuration mode
configure terminal

! Enable gNMI secure server using primary self-signed certificate
gnxi
  gnxi secure-init
exit

! This automatically enables the secure server with a self-signed cert
! Default port: 9339
```

**Option B: Secure Mode (Production - Requires Certificate)**

For production with a custom certificate:

```cisco-ios
configure terminal

! Create a self-signed certificate (for testing)
crypto pki trustpoint GNXI_TRUSTPOINT
 enrollment selfsigned
 subject-name CN=gnxi.example.com
 revocation-check none
 rsakeypair GNXI_KEYS 2048
exit

! Generate the self-signed certificate
crypto pki enroll GNXI_TRUSTPOINT

! Configure gNMI to use the trustpoint and enable secure server
gnxi
 secure-trustpoint GNXI_TRUSTPOINT
 secure-server
exit
```

**Note**: The old `gnxi server` command is deprecated. Use `secure-server` or `secure-init` instead.

### Step 2: Configure AAA (if not already configured)
Note: this has already been done for you!

```cisco-ios
configure terminal

! Enable AAA
aaa new-model

! Create local user for gNMI access
username admin privilege 15 secret Cisco123

! Configure AAA authentication for gNMI
aaa authentication login default local
aaa authorization exec default local
exit
```

### Step 3: Verify gNMI is Running
First step for this lab to confirm the necessary gNMI configuration is on your device.

Review the gnxi state and running config
```
show gnxi state
show running-config | section gnxi
```
Example response

![show gnxi state](assets/show_gnxi_state.png)


Review the gNMI server status to ensure gNMI is running (note, this may take a minute to start)
```cisco-ios
! Check gNMI server status
show gnxi state detail

! Expected output should show:
! - Secure Server: Enabled
! - Port: 9339 (default secure port)
! - State: Running
```

Example response

![show gnxi state detail](assets/show_gnxi_state_detail.png)



---

## Part 2: Configure gNMI ACLs

### Scenario Setup
- **Management VM (ALLOWED)**: 10.1.1.3 - gNMI client for testing
- **Catalyst 9300 (TARGET)**: 10.1.1.55 - Device under test
- **Catalyst 9300X (TARGET)**: 10.1.1.5 - Device under test
- **Catalyst 9350 (TARGET)**: 10.1.1.15 - Device under test
- **Any other host (DENIED)**: e.g., 10.1.1.20, 192.168.1.x

### Step 1: Create IPv4 Named ACL

**Option A: Allow only Management VM (Most Restrictive)**
```cisco-ios
configure terminal

! Create ACL to permit only management VM
ip access-list standard GNMI_ALLOWED_HOSTS
 remark Allow only management VM at 10.1.1.3
 permit host 10.1.1.3
 deny any log
exit
```

**Option B: Allow Management VM + Inter-Switch Communication**
```cisco-ios
configure terminal

! Create ACL to permit management VM and switches
ip access-list standard GNMI_ALLOWED_HOSTS
 remark Allow management VM
 permit host 10.1.1.3
 remark Allow 9300 switch
 permit host 10.1.1.55
 remark Allow 9300X switch
 permit host 10.1.1.5
 remark Allow 9350 switch
 permit host 10.1.1.15
 remark Deny everything else
 deny any log
exit
```

**Option C: Allow Entire Management Subnet (Least Restrictive)**
```cisco-ios
configure terminal

! Create ACL to permit entire 10.1.1.0/24 subnet
ip access-list standard GNMI_ALLOWED_HOSTS
 remark Allow entire management subnet
 permit 10.1.1.0 0.0.0.255
 deny any log
exit
```

### Step 2: Apply ACL to gNMI Service

```cisco-ios
! Apply ACL at the service level
configure terminal
gnxi access-list ipv4 name GNMI_ALLOWED_HOSTS

! Save configuration
write memory
```

### Step 3: Verify ACL Configuration

```cisco-ios
! Check gNMI configuration
show running-config | section gnxi

! Expected output:
! gnxi
!  secure-init
!  access-list ipv4 GNMI_ALLOWED_HOSTS

! Verify ACL contents
show ip access-lists GNMI_ALLOWED_HOSTS
```

### Optional: Configure IPv6 ACL

```cisco-ios
configure terminal

! Create IPv6 ACL
ipv6 access-list GNMI_ALLOWED_HOSTS_V6
 remark Allow authorized IPv6 management station
 permit host 2001:db8::10
 deny any log
exit

! Apply IPv6 ACL to gNMI
gnxi access-list ipv6 name GNMI_ALLOWED_HOSTS_V6
```

---

## Part 3: Test Plan - Verify ACL Functionality

### Test Environment Requirements
- **gNMI client tool** (gNMIc, gnmi_cli, or similar)
- Access from both allowed and denied IP addresses

### Test Case 1: Baseline - Verify gNMI Works WITHOUT ACL

**Objective**: Confirm gNMI is functional before applying ACL

**Steps**:
```bash
# From any management station (e.g., 10.1.1.10)
# Using secure mode (port 9339) - skip TLS verification for self-signed cert
# Note: you will need to first allow secure-password-auth on your device
configure terminal

gnxi
 gnxi secure-password-auth
 exit
exit

end

```
Then verify that show gnxi state detail includes 
    "Secure password authentication: Enabled"

```
C9350-SJC23-01#show gnxi state detail
Settings
========
  Server: Disabled
  Server port: 50052
  Secure server: Enabled
  Secure server port: 9339
  Secure client authentication: Disabled
  Secure trustpoint: TP-self-signed-4127246821
  Secure client trustpoint: 
  Secure password authentication: Enabled
```

Now you are ready to test with your gNMI client tool.  Here is an example using gNMIc.  You will need to update the device IP and credentials.

```bash
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  get --path /interfaces/interface[name=GigabitEthernet1]/state/admin-status

# Alternative using gnmi_cli
# gnmi_cli \
#   -address 10.1.1.15:9339 \
#   -username admin \
#   -password Cisco123 \
#   -skip-verify \
#   -get \
#   -path /interfaces/interface[name=GigabitEthernet1]/state/admin-status

# Note: --skip-verify flag skips TLS certificate validation (use for self-signed certs)
```

**Expected Result**: ✅ SUCCESS - Data returned (e.g., admin-status: UP)

---

### Test Case 2: PERMIT - Allowed IP Address

**Objective**: Verify that client from allowed IP (10.1.1.3 - Management VM) can access gNMI after ACL is applied

**Configuration**:
```cisco-ios
! Ensure ACL is applied (from Part 2, Step 2)
show running-config | section gnxi
```

**Test Steps**:
```bash
# From Management VM (10.1.1.3) - testing against 9300 at 10.1.1.55
gnmic -a 10.1.1.55:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  get --path /interfaces/interface[name=GigabitEthernet1/0/1]/state/oper-status

# Test against 9300X at 10.1.1.5
gnmic -a 10.1.1.5:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  get --path /interfaces/interface[name=GigabitEthernet1/0/1]/state/oper-status

# Test against 9350 at 10.1.1.15
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  get --path /interfaces/interface[name=GigabitEthernet1/0/1]/state/oper-status
```

**Expected Result**: ✅ SUCCESS
- gNMI returns requested data from all switches
- Connection succeeds
- No error messages

**Verification on Device**:
```cisco-ios
! Check ACL hit counters (run on each switch)
show ip access-lists GNMI_ALLOWED_HOSTS

! Expected: "permit host 10.1.1.3" should show packet matches

! Check gNMI connections
show gnxi state sessions
```

---

### Test Case 3: DENY - Blocked IP Address (Non-Matching)

**Objective**: Verify that client from denied IP (10.1.1.20) is rejected

**Test Steps**:
```bash
# From a DENIED host (e.g., 10.1.1.20 - NOT in ACL)
# Try to connect to 9300 at 10.1.1.55
gnmic -a 10.1.1.55:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  get --path /interfaces/interface[name=GigabitEthernet1/0/1]/state/oper-status
```

**Expected Result**: ❌ PERMISSION_DENIED
- gRPC error: `PERMISSION_DENIED`
- Error message indicating access denied due to ACL
- Connection should NOT be abruptly closed (unlike NETCONF)

**Example Error Output**:
```
Error: rpc error: code = PermissionDenied desc = "Access denied by ACL"
```

**Verification on Device**:
```cisco-ios
! Check ACL denies
show ip access-lists GNMI_ALLOWED_HOSTS

! Expected: "deny any log" entry should show packet matches

! Check syslog for ACL denial
show logging | include GNMI|ACL

! Expected syslog message similar to:
! %SEC-6-IPACCESSLOGP: list GNMI_ALLOWED_HOSTS denied tcp 10.1.1.20(xxxxx) -> 10.1.1.15(9339)
```

---

### Test Case 4: DENY - Different Network Range

**Objective**: Verify ACL blocks completely different subnet

**Test Steps**:
```bash
# From test host (192.168.1.100 - different network)
gnmic -a 10.1.1.15:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  get --path /system/state/hostname

# Alternative using gnmi_cli
# gnmi_cli \
#   -address 10.1.1.15:9339 \
#   -username admin \
#   -password Cisco123 \
#   -skip-verify \
#   -get \
#   -path /system/state/hostname
```

**Expected Result**: ❌ PERMISSION_DENIED
- Same behavior as Test Case 3
- gRPC `PERMISSION_DENIED` error
- ACL hit counter increments

---

### Test Case 5: Per-RPC Validation

**Objective**: Verify ACL is validated on EVERY RPC call, not just at connection establishment

**Test Steps**:
```bash
# From Management VM (10.1.1.3), establish gNMI subscription to 9300
gnmic -a 10.1.1.55:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  subscribe \
  --path /interfaces/interface/state/oper-status \
  --stream-mode sample \
  --sample-interval 5s

# Let subscription run for 30 seconds

# While subscription is active, modify ACL to DENY the VM
# (on the 9300 switch at 10.1.1.55)
configure terminal
ip access-list standard GNMI_ALLOWED_HOSTS
 no permit host 10.1.1.3
 deny host 10.1.1.3 log
 deny any log
end
```

**Expected Result**:
- Initial RPCs succeed (connection established)
- After ACL change, subsequent RPCs should receive `PERMISSION_DENIED`
- Demonstrates per-RPC validation (not just per-connection)

**Restore ACL**:
```cisco-ios
configure terminal
ip access-list standard GNMI_ALLOWED_HOSTS
 no deny host 10.1.1.3 log
 permit host 10.1.1.3
end
```

---

### Test Case 6: ACL Removal - Feature Disable

**Objective**: Verify that removing ACL restores unrestricted access

**Disable ACL**:
```cisco-ios
configure terminal
no gnxi access-list ipv4 name GNMI_ALLOWED_HOSTS
```

**Test Steps**:
```bash
# From previously DENIED host (10.1.1.20) trying to access 9300
gnmic -a 10.1.1.55:9339 \
  -u admin \
  -p Cisco123 \
  --skip-verify \
  get --path /interfaces/interface[name=GigabitEthernet1/0/1]/state/oper-status
```

**Expected Result**: ✅ SUCCESS
- Connection succeeds from previously denied IP (10.1.1.20)
- Demonstrates ACL feature is optional and can be disabled

**Re-enable ACL**:
```cisco-ios
configure terminal
gnxi access-list ipv4 name GNMI_ALLOWED_HOSTS
```

---

## Part 4: Monitoring and Troubleshooting

### Check Active gNMI Sessions
```cisco-ios
show gnxi state sessions

! Output shows:
! - Client IP addresses
! - Connection state
! - RPC statistics
```

### Monitor ACL Hit Counters
```cisco-ios
! View permit/deny statistics
show ip access-lists GNMI_ALLOWED_HOSTS

! Clear counters for fresh test
clear ip access-list counters GNMI_ALLOWED_HOSTS
```

### Enable Debug Logging
```cisco-ios
! Enable debugging (use with caution in production)
debug gnxi detail

! View real-time syslog
terminal monitor
```

### Check gNMI Configuration
```cisco-ios
show running-config | section gnxi
show gnxi state detail
```

---

## Part 5: Advanced Scenarios

### Scenario A: Complex ACL with Multiple Subnets

```cisco-ios
configure terminal

ip access-list extended GNMI_MULTI_SUBNET
 remark Permit entire management network
 permit ip 10.1.1.0 0.0.0.255 any
 remark Permit specific admin workstation
 permit host 172.16.100.50 any
 remark Deny everything else
 deny ip any any log
exit

gnxi access-list ipv4 name GNMI_MULTI_SUBNET
```

### Scenario B: Dual-Stack (IPv4 + IPv6) ACL

```cisco-ios
configure terminal

! IPv4 ACL
ip access-list standard GNMI_V4
 permit 10.1.1.0 0.0.0.255
 deny any log
exit

! IPv6 ACL
ipv6 access-list GNMI_V6
 permit ipv6 2001:db8::/32 any
 deny ipv6 any any log
exit

! Apply both
gnxi access-list ipv4 name GNMI_V4
gnxi access-list ipv6 name GNMI_V6
```

---

## Summary Checklist

**Configuration Checklist**:
- [ ] gNMI server enabled and running (use `gnxi secure-init` or configure trustpoint)
- [ ] AAA configured with local user credentials
- [ ] IPv4 named ACL created with permit/deny rules
- [ ] ACL applied to gNMI service using `gnxi access-list ipv4 name <acl-name>`
- [ ] Configuration saved

**Test Validation Checklist**:
- [ ] Test Case 1: Baseline connectivity (PASS)
- [ ] Test Case 2: Permitted IP access (PASS)
- [ ] Test Case 3: Denied IP rejected with PERMISSION_DENIED (PASS)
- [ ] Test Case 4: Different subnet blocked (PASS)
- [ ] Test Case 5: Per-RPC validation verified (PASS)
- [ ] Test Case 6: ACL removal restores access (PASS)

**Verification Points**:
- [ ] ACL hit counters show permit/deny matches
- [ ] Syslog shows denied connection attempts
- [ ] gNMI sessions display only allowed clients
- [ ] Error handling uses standard gRPC codes (not connection termination)

---

## Key Differences vs. NETCONF/RESTCONF

| Aspect | gNMI/gNOI | NETCONF | RESTCONF |
|--------|-----------|---------|----------|
| **Error Response** | gRPC `PERMISSION_DENIED` | Connection reset (no error msg) | HTTP 403 with JSON error |
| **Connection Handling** | Graceful error, connection maintained | Abrupt termination | Graceful HTTP response |
| **Validation Level** | Per-RPC | Per-connection | Per-HTTP request |
| **ACL Enforcement** | Application-level (gnmib + acl_proxy) | Application-level | Application-level |

---

## Notes
- **Security Best Practice**: Always use ACLs in combination with TLS and strong authentication
- **Service-Level vs Interface-Level**: Service-level ACLs (this feature) validate at the application layer. To block traffic before it reaches gNMI, use interface-level ACLs
- **Internal Architecture**: gNMI server (gnmib) validates ACLs by communicating with IOSd via the `acl_proxy` library
- **Default Behavior**: When no ACL is configured, gNMI allows all authenticated connections

---

## Troubleshooting Guide

**Problem**: Can't connect to gNMI at all

**Solutions**:
1. Verify gNMI server is enabled: `show gnxi state detail`
2. Check firewall/routing: Can you ping the device?
3. Verify port 9339 is listening: `show control-plane host open-ports`
4. Check credentials: AAA authentication properly configured?
5. Verify certificate: `show crypto pki trustpoints` or check if `secure-init` was used

**Problem**: Getting PERMISSION_DENIED from allowed IP

**Solutions**:
1. Verify ACL syntax: `show ip access-lists <name>`
2. Check source IP from client perspective: Client may be NATed
3. Review ACL order: First match wins - is there a deny before your permit?
4. Check ACL binding: `show run | sec gnxi` - Is correct ACL applied?
5. Check ACL hit counters: `show ip access-lists GNMI_ALLOWED_HOSTS`

**Problem**: Denied IP can still connect

**Solutions**:
1. Verify ACL is applied: `show run | sec gnxi`
2. Check ACL has explicit deny: Standard ACLs need explicit `deny any`
3. Clear and retest: `clear ip access-list counters` then retry
4. Reload gNMI server:
   ```
   configure terminal
   gnxi
    no secure-server
    secure-server
   exit
   ```

**Problem**: Error about trustpoint when enabling secure-server

**Solution**: Use `gnxi secure-init` instead (uses primary self-signed cert), or configure a custom trustpoint first (see Part 1, Step 1, Option B)

---

**Document Version**: 1.1  
**Last Updated**: April 2026  
**IOS-XE Version**: 26.1.1 (tested) - Commands verified against actual device CLI


# Secure Zero Touch Provisioning (SZTP)

## What is SZTP?

Secure Zero Touch Provisioning (SZTP) is an automated, secure method for onboarding enterprise network devices. It enables devices to bootstrap themselves with minimal manual intervention while maintaining strong security through certificate-based authentication.

### SZTP Workflow

1. **Device Powers On**: New device boots up for the first time
2. **DHCP Discovery**: Device obtains IP and bootstrap server information
3. **Ownership Verification**: Device contacts MASA to verify ownership voucher
4. **Bootstrap Configuration**: Device downloads initial configuration
5. **Production Ready**: Device joins the network with proper config and credentials

## Ownership Voucher Generation

The first step in SZTP is generating ownership vouchers for your devices. An ownership voucher is a cryptographically signed artifact from the Manufacturer Authorized Signing Authority (MASA) that proves your organization owns specific devices. These vouchers are essential for secure device onboarding and prevent unauthorized devices from joining your network.

### Understanding MASA

Cisco's MASA service (https://masa.cisco.com) validates device ownership and generates ownership vouchers. When you request a voucher, MASA verifies:

1. Your organization has a valid entitlement for the device serial number
2. The device hasn't been claimed by another organization
3. Your API token has proper authorization

The MASA service then generates a signed ownership voucher that your bootstrap server presents to the device during the SZTP process. This ensures that only devices you own can successfully onboard to your network.

**📚 For complete instructions on obtaining a MASA API token and generating ownership vouchers, see the [SZTP Scripts README](https://github.com/sdeweese/CLUS26-LTRENS-1680-Cisco-IOS-XE-Programmability-Lab-Unlock-the-Foundation-Explore-the-Future/blob/main/sztp/README.md) in this repository.**

### Prerequisites

- Cisco MASA account and API token (see [sztp/README.md](https://github.com/sdeweese/CLUS26-LTRENS-1680-Cisco-IOS-XE-Programmability-Lab-Unlock-the-Foundation-Explore-the-Future/blob/main/sztp/README.md) for details)
- Device serial numbers
- Domain certificate for authentication

### Quick Start

For detailed instructions on generating ownership vouchers, see the [SZTP Scripts Documentation](https://github.com/sdeweese/CLUS26-LTRENS-1680-Cisco-IOS-XE-Programmability-Lab-Unlock-the-Foundation-Explore-the-Future/blob/main/sztp/README.md).

**Basic steps:**

1. **Set MASA token**:
   ```bash
   export MASA_API_TOKEN="your-token-here"
   ```

2. **Generate certificate**:
   ```bash
   openssl ecparam -out pinned-domain-cert.key -name prime256v1 -genkey
   openssl req -new -sha256 -key pinned-domain-cert.key -out pinned-domain-cert.csr
   openssl x509 -req -sha256 -days 365 -in pinned-domain-cert.csr -signkey pinned-domain-cert.key -out pinned-domain-cert.crt
   ```

3. **Generate vouchers**:
   ```bash
   cd sztp/
   ./run_bulk_vouchers.sh --serial-source pod-devices-table.md
   ```

### SZTP Scripts

The repository includes comprehensive scripts for voucher generation:

- **masa_ov_request.py**: Request new vouchers from MASA
- **masa_get_voucher.py**: Download existing vouchers
- **run_bulk_vouchers.sh**: Bulk voucher generation

📚 **Full documentation**: [SZTP README](https://github.com/sdeweese/CLUS26-LTRENS-1680-Cisco-IOS-XE-Programmability-Lab-Unlock-the-Foundation-Explore-the-Future/blob/main/sztp/README.md)

## Bootstrap Server Setup

After generating ownership vouchers, you need to set up a bootstrap server to deliver configurations to devices.

### Bootstrap Server Components

1. **DHCP Server**: Provides bootstrap server URL via option 143
2. **Web Server**: Hosts bootstrap configuration files
3. **Certificate Authority**: Issues device certificates
4. **Configuration Templates**: Device-specific configs

### Example Bootstrap Configuration

```json
{
  "ietf-sztp-bootstrap-server:bootstrap-information": {
    "boot-image": {
      "download-uri": "https://bootstrap.example.com/images/iosxe-17.12.1.bin",
      "image-verification": {
        "hash-algorithm": "sha-256",
        "hash-value": "a1b2c3..."
      }
    },
    "configuration": {
      "download-uri": "https://bootstrap.example.com/configs/device-{{serial}}.cfg"
    },
    "ownership-voucher": {
      "artifact": "base64-encoded-voucher"
    }
  }
}
```

## Device Onboarding Demo

### Step 1: Prepare Device

1. Connect device to network with DHCP
2. Ensure device can reach bootstrap server
3. Verify device has factory default config

### Step 2: Power On Device

Device will automatically:

- Obtain IP via DHCP
- Discover bootstrap server
- Validate ownership voucher
- Download bootstrap configuration
- Apply configuration

### Step 3: Verify Onboarding

Check device logs:
```
show logging | include SZTP
```

Verify configuration:
```
show running-config
```

## Security Considerations

- **Certificate Validation**: Always validate device and server certificates
- **Encrypted Transport**: Use HTTPS for all bootstrap communications
- **Ownership Vouchers**: Store vouchers securely
- **Access Control**: Restrict bootstrap server access
- **Audit Logging**: Monitor all onboarding activities

## Troubleshooting

### Device Not Bootstrapping

**Check DHCP option 143**:
```bash
# On DHCP server
show ip dhcp binding
```

**Verify bootstrap server reachability**:
```bash
# From device
ping bootstrap.example.com
```

### Ownership Voucher Rejected

- Verify voucher was generated for correct serial number
- Check certificate validity period
- Ensure MASA registration is current
- Validate voucher format (must be valid JSON)

### Configuration Download Failed

- Check bootstrap server HTTPS certificate
- Verify configuration file exists at specified URL
- Ensure device has internet connectivity
- Check firewall rules

## Additional Resources

- [IETF RFC 8572 - Secure Zero Touch Provisioning](https://datatracker.ietf.org/doc/html/rfc8572)
- [Cisco SZTP Documentation](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9000/sztp-guide.html)
- [SZTP Scripts Repository](https://github.com/sdeweese/sztp)
- [SZTP Scripts README](https://github.com/sdeweese/CLUS26-LTRENS-1680-Cisco-IOS-XE-Programmability-Lab-Unlock-the-Foundation-Explore-the-Future/blob/main/sztp/README.md)

---

## Next Steps

✅ Completed: Day 0 - SZTP Onboarding

**Continue your learning journey:**

➡️ [Day 1: Device Configuration Overview](../day-1/index.md) - Learn configuration management with ACR, Terraform, and Ansible

**Or explore:**
- [Atomic Config Replace](../day-1/atomic-operations.md)
- [Back to Day 0 Overview](index.md)

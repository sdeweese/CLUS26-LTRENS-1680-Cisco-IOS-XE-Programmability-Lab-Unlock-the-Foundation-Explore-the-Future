# MASA OV Voucher Request

This folder contains scripts for generating **Ownership Vouchers (OV)** as part of the Secure Zero Touch Provisioning (SZTP) process for Cisco IOS XE devices.

**Important:** These scripts handle **only the voucher generation step** of SZTP. For complete details on the full SZTP workflow, including device onboarding, bootstrapping, and deployment, refer to the comprehensive guide: [https://github.com/sdeweese/sztp](https://github.com/sdeweese/sztp)

## Scripts Included

- **masa_ov_request.py**: Requests a voucher from Cisco MASA and saves usable output as .vcj only.
- **masa_get_voucher.py**: Downloads an existing voucher only via GET /api/download/device/{serial}.
- **run_bulk_vouchers.sh**: Runs voucher requests in bulk.

## Prerequisites

Before running any scripts, ensure you're in the correct directory:

```bash
cd /path/to/your/sztp/folder
```

## 1. Obtain MASA API Token

Get your API token from the Cisco MASA UI:

1. Log in to the Cisco MASA portal at https://masa.cisco.com
2. Navigate to **Settings** or **API Access** section
3. Click **Generate New Token** or **Create API Key**
4. Copy the token value (it will only be shown once)
5. Save it securely

**Set the token as an environment variable** so it's not stored in scripts:

```bash
read -s -p "Enter MASA token: " MASA_API_TOKEN; echo; export MASA_API_TOKEN
```

**Verify the token is set:**

```bash
if [ -n "$MASA_API_TOKEN" ]; then echo "MASA_API_TOKEN is set"; else echo "MASA_API_TOKEN is not set"; fi
```

## 2. Generate Pinned Domain Certificate

The MASA API requires a PEM certificate in the request field `certificate`. Follow these steps to generate the required certificate files:

### Step 1: Create the private key

```bash
openssl ecparam -out pinned-domain-cert.key -name prime256v1 -genkey
```

### Step 2: Create a Certificate Signing Request (CSR)

```bash
openssl req -new -sha256 -key pinned-domain-cert.key -out pinned-domain-cert.csr
```

When prompted, enter the following information (or use your own values):

- **Country Name (2 letter code)**: US
- **State or Province Name**: (leave blank or enter your state)
- **Locality Name**: (leave blank or enter your city)
- **Organization Name**: Your Organization Name
- **Organizational Unit Name**: (leave blank)
- **Common Name**: Your Domain or Organization Name
- **Email Address**: your.email@example.com
- **Challenge password**: (leave blank)
- **Optional company name**: (leave blank)

### Step 3: Self-sign the certificate

```bash
openssl x509 -req -sha256 -days 365 -in pinned-domain-cert.csr -signkey pinned-domain-cert.key -out pinned-domain-cert.crt
```

### Step 4: Verify the files were created

```bash
ls pinned-domain-cert.*
```

You should see:
- `pinned-domain-cert.key` (private key)
- `pinned-domain-cert.csr` (certificate signing request)
- `pinned-domain-cert.crt` (certificate)

### Step 5: Register certificate in MASA

1. Log in to the Cisco MASA portal
2. Navigate to the **Certificates** or **Domain Certificates** section
3. Upload or paste the contents of `pinned-domain-cert.crt`
4. Ensure **IOS XE** is selected as the platform
5. Associate serial numbers with this certificate as needed

**Important:**
- The `.crt` file (certificate) is used for MASA API requests
- Do NOT use the `.key` file (private key) as the pinned domain certificate input
- The certificate file must contain `BEGIN CERTIFICATE` / `END CERTIFICATE` headers

Default filename used by scripts: `pinned-domain-cert.crt`

## 3. Usage Options

There are **three main ways** to use these scripts:

### Option A: Single Serial Number (Command Line)

Request a voucher for a single device by providing the serial number as a command-line argument:

```bash
python masa_ov_request.py SERIALNUMBER123 \
  --platform XE \
  --pinned-domain-cert-file pinned-domain-cert.crt \
  --output vouchers/SERIALNUMBER123.vcj
```

**Example:**
```bash
python masa_ov_request.py FCW12345678 \
  --platform XE \
  --pinned-domain-cert-file pinned-domain-cert.crt \
  --output vouchers/FCW12345678.vcj
```

### Option B: Bulk Processing from File

Process multiple serial numbers from an input file. The script supports three file formats:

#### Format 1: Newline-Separated (Simple Text File)

Create a text file with one serial number per line:

**serials.txt:**
```
FCW12345678
FCW23456789
FCW34567890
```

**Run:**
```bash
./run_bulk_vouchers.sh --serial-source serials.txt
```

#### Format 2: Comma-Separated Values (CSV)

Create a CSV file with serial numbers (comma-separated on a single line or one per line):

**serials.csv:**
```
FCW12345678,FCW23456789,FCW34567890
```

Or one per line:
```
FCW12345678
FCW23456789
FCW34567890
```

**Run:**
```bash
./run_bulk_vouchers.sh --serial-source serials.csv
```

#### Format 3: Markdown Table (Organized by Platform)

Create a markdown table with serial numbers organized by device type. This format automatically organizes output vouchers into platform-specific subdirectories.

**pod-devices-table.md:**
```markdown
# Device Serial Numbers

| Pod | C9300X | C9300 | C9350 |
|-----|----------|---------|---------|
| 01 | FOC12345678 | FCW12345678 | FVH12345678 |
| 02 | FOC23456789 | FCW23456789 | FVH23456789 |
| 03 | FOC34567890 | FCW34567890 | FVH34567890 |
```

**Run:**
```bash
./run_bulk_vouchers.sh --serial-source pod-devices-table.md
```

**Output structure with table format:**
```
vouchers/api_generated/
├── C9300X/
│   ├── FOC12345678.vcj
│   └── FOC23456789.vcj
├── C9300/
│   ├── FCW12345678.vcj
│   └── FCW23456789.vcj
└── C9350/
    ├── FVH12345678.vcj
    └── FVH23456789.vcj
```

### Option C: Download Existing Voucher Only

If a voucher already exists in MASA and you just want to download it (without creating a new one):

```bash
python masa_get_voucher.py SERIALNUMBER123 \
  --output vouchers/SERIALNUMBER123.vcj
```

**Example:**
```bash
python masa_get_voucher.py FCW12345678 \
  --output vouchers/C9300/FCW12345678.vcj
```

## 4. Run Bulk Generation

Default behavior of `run_bulk_vouchers.sh`:

- Reads serials from `pod-devices-table.md` (or specified file)
- If a markdown table is used, writes vouchers under header-based folders:
  - `vouchers/api_generated/C9300X`
  - `vouchers/api_generated/C9300`
  - `vouchers/api_generated/C9350`
- Writes `.vcj` files only

**Basic run:**

```bash
./run_bulk_vouchers.sh
```

**Dry-run** (preview without creating vouchers):

```bash
./run_bulk_vouchers.sh --dry-run
```

**Custom options:**

```bash
./run_bulk_vouchers.sh \
  --serial-source serials.txt \
  --pinned-cert-file pinned-domain-cert.crt \
  --output-dir vouchers/api_generated
```

## 5. Advanced Usage

### Existing Voucher Behavior

If MASA returns "active voucher already exists":

- The script automatically falls back to download the active voucher from `/api/download/device/{serial}`
- Saves it to your requested `.vcj` output path

**To force regeneration** instead of fallback, use `--override`:

```bash
python masa_ov_request.py FCW12345678 \
  --platform XE \
  --pinned-domain-cert-file pinned-domain-cert.crt \
  --output vouchers/FCW12345678.vcj \
  --override
```

### Authentication Methods

Auth credentials are read from (in order of precedence):

1. **Token-based** (recommended):
   - `--token` flag or `MASA_API_TOKEN` environment variable

2. **Certificate-based**:
   - `--cert` + `--key` flags
   - or `MASA_CLIENT_CERT` + `MASA_CLIENT_KEY` environment variables

## Troubleshooting

**Token not recognized:**
```bash
# Verify token is set
echo $MASA_API_TOKEN
```

**Certificate errors:**
- Ensure you're using the `.crt` file, not the `.key` file
- Verify the certificate contains `BEGIN CERTIFICATE` and `END CERTIFICATE` headers
- Check that the certificate is registered in MASA portal

**Serial number format:**
- Cisco serial numbers typically follow patterns like:
  - C9300X: FOC + 8 alphanumeric characters
  - C9300: FCW + 8 alphanumeric characters
  - C9350: FVH + 8 alphanumeric characters

**File not found:**
- Ensure you're in the correct directory
- Check file paths are relative to your current working directory

## Example Workflows

### Workflow 1: Generate vouchers for a new pod

```bash
# 1. Set token
export MASA_API_TOKEN="your-token-here"

# 2. Create serial list
cat > serials.txt << EOF
FCW12345678
FCW23456789
FCW34567890
EOF

# 3. Run bulk generation
./run_bulk_vouchers.sh --serial-source serials.txt
```

### Workflow 2: Download existing vouchers

```bash
# Download a single existing voucher
python masa_get_voucher.py FCW12345678 \
  --output vouchers/FCW12345678.vcj
```

### Workflow 3: Table-based organization

```bash
# Use markdown table for organized output
./run_bulk_vouchers.sh --serial-source pod-devices-table.md
# Output will be organized by platform in subdirectories
```

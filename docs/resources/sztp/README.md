# MASA OV Voucher Request

This folder contains scripts for generating **Ownership Vouchers (OV)** as part of the Secure Zero Touch Provisioning (SZTP) process for Cisco IOS XE devices.

**Important:** These scripts handle **only the voucher generation step** of SZTP. For complete details on the full SZTP workflow, including device onboarding, bootstrapping, and deployment, refer to the comprehensive guide: [https://github.com/sdeweese/sztp](https://github.com/sdeweese/sztp)

## Scripts Included

- **masa_ov_request.py**: Requests a voucher from Cisco MASA and saves usable output as .vcj only.
- **masa_get_voucher.py**: Downloads an existing voucher only via GET /api/download/device/{serial}.
- **run_bulk_vouchers.sh**: Runs voucher requests in bulk.

## Quick Start

If you're ready to get started immediately:

1. **Install Python dependencies**: `pip install requests` (or use virtual environment - see Prerequisites)
2. **Get MASA token**: From Cisco MASA portal (see Section 1)
3. **Generate certificate**: Follow OpenSSL commands (see Section 2)
4. **Run script**: `./run_bulk_vouchers.sh` or customize as needed (see Section 4-5)

For detailed setup instructions, continue reading below.

## Prerequisites

Before running any scripts, ensure you have the required dependencies installed.

### System Requirements

- **Python 3.7+** (Python 3.8 or later recommended)
- **Bash shell** (for running `.sh` scripts)
- **OpenSSL** (for generating certificates)

### Python Dependencies

The scripts require the following Python packages:

**Required:**
- `requests` - For making HTTP/HTTPS API calls to MASA

**Optional but recommended:**
- `cryptography` - For advanced certificate handling (if needed)

### Installation Options

#### Option 1: Using Virtual Environment (Recommended)

Create and activate a virtual environment, then install dependencies:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install required packages
pip install requests

# Optional: Install all common dependencies
pip install requests cryptography
```

**To deactivate the virtual environment when done:**
```bash
deactivate
```

#### Option 2: System-Wide Installation (Not Recommended)

Install packages globally (may require sudo/admin privileges):

```bash
pip3 install requests

# Optional
pip3 install cryptography
```

#### Option 3: Using requirements.txt

The repository includes a `requirements.txt` file for easy installation:

```bash
# With virtual environment active
pip install -r requirements.txt

# Or system-wide
pip3 install -r requirements.txt
```

**requirements.txt contents:**
```
requests>=2.28.0
cryptography>=41.0.0  # Optional
```

### Verifying Installation

Check that Python and dependencies are properly installed:

```bash
# Check Python version
python3 --version  # Should be 3.7 or higher

# Check if requests is installed
python3 -c "import requests; print(requests.__version__)"

# Check OpenSSL
openssl version
```

### Script Configuration

If using a virtual environment, the `run_bulk_vouchers.sh` script is already configured to use `.venv/bin/python`.

If **NOT** using a virtual environment, you need to edit the script:

```bash
nano run_bulk_vouchers.sh
```

Change this line:
```bash
python_cmd=".venv/bin/python"
```

To:
```bash
python_cmd="python3"
```

### Directory Setup

Before running any scripts, ensure you're in the correct directory:

```bash
cd /path/to/your/sztp/folder
```

### Shell Script Dependencies

The `run_bulk_vouchers.sh` script requires standard Unix/Linux utilities:

- `bash` - Shell interpreter
- `grep`, `awk`, `sed` - Text processing (for parsing serial files)
- Standard coreutils (`cat`, `echo`, `mkdir`, etc.)

These are typically pre-installed on macOS and Linux systems.

### Quick Environment Check

Run these commands to verify your environment is ready:

```bash
# Check all requirements
python3 --version && \
python3 -c "import requests; print('✓ requests installed')" && \
openssl version && \
bash --version | head -1 && \
echo "✓ Environment ready!"
```

If any command fails, install the missing requirement using the instructions above.

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

## 4. Configuring run_bulk_vouchers.sh

The `run_bulk_vouchers.sh` script is a **wrapper** that calls `masa_ov_request.py` for multiple serial numbers. By examining the script, you can see exactly how the Python script is invoked and customize it for your needs.

### Understanding the Script Structure

The shell script:
1. **Reads serial numbers** from your input file (text, CSV, or markdown table)
2. **Loops through each serial** and calls the Python script
3. **Passes arguments** to `masa_ov_request.py` for each device
4. **Organizes output** into folders (especially useful with markdown tables)

**Example of how the script calls Python internally:**

```bash
.venv/bin/python masa_ov_request.py FCW12345678 \
  --platform XE \
  --pinned-domain-cert-file pinned-domain-cert.crt \
  --token "$MASA_API_TOKEN" \
  --output vouchers/api_generated/C9300/FCW12345678.vcj
```

By opening and reading the script, you can see this pattern and understand how to:
- Call the Python script directly for single devices
- Customize the arguments being passed
- Modify the output folder structure
- Add custom logic for your environment

### Method 1: Edit Default Values in Script (Recommended for Permanent Changes)

Open the script and modify the default configuration variables near the top:

```bash
nano run_bulk_vouchers.sh
```

**Key configuration variables:**

```bash
platform="XE"                              # Platform type (typically XE)
serial_source="serials.txt"                # Default serial number source file
# serial_source="pod-devices-table.md"    # Uncomment to use table format by default
pinned_cert_file="pinned-domain-cert.pem"  # Path to your pinned domain certificate
output_dir="vouchers/api_generated"        # Where to save generated .vcj files
python_cmd=".venv/bin/python"              # Python interpreter (use system python if no venv)
script_path="masa_ov_request.py"           # Path to the request script
```

**When to edit these:**
- You always use the same certificate file name
- You prefer markdown table format over plain text serials
- You want to change default output directory
- You're not using a Python virtual environment (change to `python3`)

**Example edits:**

```bash
# Use system python instead of virtual environment
python_cmd="python3"

# Always use table format by default
serial_source="pod-devices-table.md"

# Change certificate filename to match your setup
pinned_cert_file="pinned-domain-cert.crt"
```

### Method 2: Use Command-Line Flags (Recommended for One-Time Changes)

Override defaults without editing the script:

```bash
./run_bulk_vouchers.sh \
  --serial-source my-custom-serials.txt \
  --pinned-cert-file pinned-domain-cert.crt \
  --output-dir custom-output/ \
  --platform XE
```

**Available flags:**
- `--serial-source FILE` - Serial source file
- `-p, --pinned-cert-file FILE` - Pinned domain certificate
- `--platform VALUE` - Platform (default: XE)
- `-o, --output-dir DIR` - Output directory
- `--python CMD` - Python command to use
- `--script FILE` - Request script path
- `--dry-run` - Preview without making API calls
- `-h, --help` - Show help

### Making the Script Executable

If you get a "permission denied" error, make the script executable:

```bash
chmod +x run_bulk_vouchers.sh
```

### Testing Your Configuration

Use dry-run mode to verify your setup without making API calls:

```bash
./run_bulk_vouchers.sh --dry-run
```

This will show you exactly what the script would do without actually generating vouchers.

### Viewing and Editing the Script

**To view the script and learn how it works:**

```bash
cat run_bulk_vouchers.sh
# or
nano run_bulk_vouchers.sh  # View and edit
```

**What you'll find in the script:**
- Configuration variables at the top (lines ~25-35)
- Command-line argument parsing logic
- Serial number extraction (handles text, CSV, and markdown formats)
- The actual Python command that gets executed for each serial
- Error handling and validation

**Common customizations:**

1. **Change Python interpreter** (if not using virtual environment):
   ```bash
   # Change this line:
   python_cmd=".venv/bin/python"
   # To:
   python_cmd="python3"
   ```

2. **Add custom logic** (e.g., skip certain serials, add logging):
   ```bash
   # You can add conditional logic in the loop where Python is called
   # Example: Skip serials starting with "TEST"
   if [[ "$serial" == TEST* ]]; then
     echo "Skipping test serial: $serial"
     continue
   fi
   ```

3. **Customize output paths** (change folder structure):
   ```bash
   # Modify the output path construction logic
   output_dir="vouchers/by-date/$(date +%Y-%m-%d)"
   ```

4. **Add additional Python arguments**:
   ```bash
   # Find the line that calls the Python script and add flags:
   "$python_cmd" "$script_path" "$serial" \
     --platform "$platform" \
     --pinned-domain-cert-file "$pinned_cert_file" \
     --timeout 60 \  # Add timeout
     --retry 3 \     # Add retry logic
     --output "$output_file"
   ```

**Save your changes:**
```bash
# After editing
Ctrl+O (save), Enter, Ctrl+X (exit in nano)
# Or in vim: :wq
```

**Pro Tip:** By reading the shell script, you'll learn the exact Python command syntax, which helps you understand how to run `masa_ov_request.py` directly for single devices or custom workflows.

## 5. Run Bulk Generation

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

## 6. Advanced Usage

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

**Python module not found:**
```bash
# Error: ModuleNotFoundError: No module named 'requests'
# Solution: Install the requests package
pip install requests
# or with virtual environment:
source .venv/bin/activate && pip install requests
```

**Virtual environment not found:**
```bash
# Error: .venv/bin/python: No such file or directory
# Solution 1: Create virtual environment
python3 -m venv .venv && source .venv/bin/activate && pip install requests

# Solution 2: Use system Python (edit run_bulk_vouchers.sh)
# Change: python_cmd=".venv/bin/python"
# To:     python_cmd="python3"
```

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

**Permission denied on shell script:**
```bash
# Make script executable
chmod +x run_bulk_vouchers.sh
```

**OpenSSL not found:**
```bash
# macOS (using Homebrew)
brew install openssl

# Ubuntu/Debian
sudo apt-get install openssl

# RHEL/CentOS
sudo yum install openssl
```

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

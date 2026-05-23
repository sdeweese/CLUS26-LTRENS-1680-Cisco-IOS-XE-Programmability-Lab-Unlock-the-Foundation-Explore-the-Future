from ncclient import manager
from ncclient.xml_ import to_ele
import socket
from ncclient.operations import RPCError

HOST = "10.1.1.5"
USER = "admin"
PASS = "Cisco123"
PORT = 830

# Test configuration staged to candidate datastore
candidate_config = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>CLI-PREVIEW-TEST</hostname>
  </native>
</config>
"""

# Preview candidate datastore changes
candidate_preview_rpc = """
<candidate-preview xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-cli-preview-rpc">
  <custom-timeout>60</custom-timeout>
</candidate-preview>
"""

print(f"Testing TCP {HOST}:{PORT}...")
with socket.create_connection((HOST, PORT), timeout=10):
    print("TCP 830 reachable\n")

with manager.connect(
    host=HOST,
    port=PORT,
    username=USER,
    password=PASS,
    hostkey_verify=False,
    device_params={"name": "iosxe"},
    look_for_keys=False,
    allow_agent=False,
    timeout=90,
) as m:
  print("Testing candidate-preview RPC...\n")

  m.lock("candidate")
  try:
    print("Staging test config in candidate datastore...")
    m.edit_config(target="candidate", config=candidate_config, default_operation="merge")

    print("Attempting candidate-preview RPC...")
    reply = m.dispatch(to_ele(candidate_preview_rpc))
    print("✓ SUCCESS! candidate-preview RPC worked!")
    print("\n" + "=" * 70)
    print("PREVIEW OUTPUT (CLI commands that would be generated):")
    print("=" * 70)
    print(reply.xml)
  except RPCError as e:
    print("✗ FAILED with RPC Error")
    print("\nError Details:")
    print(f"  - Tag: {e.tag}")
    print(f"  - Type: {e.type}")
    print(f"  - Severity: {e.severity}")
    print(f"  - Message: {e.message}")
    if e.info is not None:
      print(f"  - Info: {e.info}")

    print("\nThis RPC may not be supported on your IOS XE version/platform.")
    print("Try checking: show version")
  finally:
    # Keep this as a preview-only test by discarding staged candidate changes.
    try:
      m.discard_changes()
      print("\nCandidate changes discarded.")
    except RPCError:
      print("\nCould not discard candidate changes.")
    m.unlock("candidate")

from ncclient import manager
from ncclient.xml_ import to_ele
import socket

HOST = "10.1.1.5"
USER = "admin"
PASS = "Cisco123"
PORT = 830

candidate_config = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>CANDIDATE-PREVIEW-TEST</hostname>
  </native>
</config>
"""

get_candidate_cli = """
<get-modelled-config-clis xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-cli-rpc">
  <datastore>candidate</datastore>
</get-modelled-config-clis>
"""

print(f"Testing TCP {HOST}:{PORT}...")
with socket.create_connection((HOST, PORT), timeout=10):
    print("TCP 830 reachable")

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
    m.lock("candidate")
    try:
        print("Updating candidate datastore...")
        m.edit_config(
            target="candidate",
            config=candidate_config,
            default_operation="merge",
        )

        print("Candidate as CLI:")
        reply = m.dispatch(to_ele(get_candidate_cli))
        print(reply.xml)

        print("Discarding candidate changes...")
        m.discard_changes()

        # If you actually wanted to apply it, use this instead:
        # m.commit()

    finally:
        m.unlock("candidate")

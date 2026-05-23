from ncclient import manager
from ncclient.xml_ import to_ele
import socket

HOST = "10.1.1.5"
USER = "admin"
PASS = "Cisco123"
PORT = 830

get_running_rpc = """
<get-modelled-config-clis xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-cli-rpc">
  <datastore>running</datastore>
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
    print("Retrieving running datastore as CLI...")
    reply = m.dispatch(to_ele(get_running_rpc))
    print(reply.xml)

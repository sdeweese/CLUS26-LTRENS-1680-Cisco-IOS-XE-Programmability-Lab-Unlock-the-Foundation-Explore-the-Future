# SZTP Internal Logs: Full Example

This page provides a realistic, end-to-end example of IOS-XE SZTP internal logs for a successful onboarding run.

Use it as a reference only. You do not need to read every line during the lab.

## Quick Usage

Run this on the switch:

```text
show logging process sztp internal start last 20 minutes
```

Compare your output against the phases below:

1. DHCP option 143 received
2. Redirecter contacted
3. Bootstrap endpoint contacted with mTLS
4. Voucher and owner chain checks pass
5. Signed onboarding information accepted
6. Day-0 script/config applied

## Full Sample Log Output

```
cat9300-pod07b-sztp#show logging process sztp internal start last 20 minutes
Logging display requested on 2026/05/26 13:05:23 (PDST) for Hostname: [cat9300-pod07b-sztp], Model: [C9300-24T], Version: [17.18.01], SN: [FOC212569ZA], MD_SN: [FCW2126G05V]

Displaying logs from the last 0 days, 0 hours, 20 minutes, 0 seconds
executing cmd on chassis: 1; rp slot: 0;  location: local ...

*May 26 2026 13:05:23.086 PDST: %HA_EM-6-LOG: catchall: show logging process sztp internal start last 20 minutes Unified Decoder Library Init .. DONE
Found 2 UTF Streams

2026/05/26 12:50:32.351221203 {sztp_R0-0}{1}: [btrace] [13907]: (note): Btrace started for process sztp bproc:sztp ID 13907 with 512 modules
2026/05/26 12:50:32.351222670 {sztp_R0-0}{1}: [btrace] [13907]: (note): File size max used for rotation of tracelogs: 1048576
2026/05/26 12:50:32.351223030 {sztp_R0-0}{1}: [btrace] [13907]: (note): File size max used for rotation of TAN stats file: 1048576
2026/05/26 12:50:32.351223394 {sztp_R0-0}{1}: [btrace] [13907]: (note): File rotation timeout max used for rotation of TAN stats file: 600
2026/05/26 12:50:32.351223761 {sztp_R0-0}{1}: [btrace] [13907]: (note): Bproc Name:sztp, Bproc proc tag:261 infra_bproc:0
2026/05/26 12:50:32.351513244 {sztp_R0-0}{1}: [btrace] [13907]: (note): Boot level config file [/crashinfo/tracelogs/level_config/sztp_R0-0] is not available. Skipping
2026/05/26 12:50:32.351514348 {sztp_R0-0}{1}: [sztp] [13907]: (note): sztp started with list of 1 command line arguments:
2026/05/26 12:50:32.351514832 {sztp_R0-0}{1}: [sztp] [13907]: (note):     /usr/binos/bin/sztp
2026/05/26 12:50:32.351515455 {sztp_R0-0}{1}: [sztp] [13907]: (note): Loading debug properties
2026/05/26 12:50:32.351595861 {sztp_R0-0}{1}: [sztp] [13907]: (note): Property chasfs_stats_on is not present. Assuming FALSE
2026/05/26 12:50:32.351600175 {sztp_R0-0}{1}: [sztp] [13907]: (note): Property debug_certificates is not present. Assuming FALSE
2026/05/26 12:50:32.351604088 {sztp_R0-0}{1}: [sztp] [13907]: (note): Property debug_cms_structures is not present. Assuming FALSE
2026/05/26 12:50:32.351607935 {sztp_R0-0}{1}: [sztp] [13907]: (note): Property debug_conveyed_info is not present. Assuming FALSE
2026/05/26 12:50:32.351611855 {sztp_R0-0}{1}: [sztp] [13907]: (note): Property debug_servers_list is not present. Assuming FALSE
2026/05/26 12:50:32.351615768 {sztp_R0-0}{1}: [sztp] [13907]: (note): Property debug_curl_verbose is not present. Assuming FALSE
2026/05/26 12:50:32.351784559 {sztp_R0-0}{1}: [sztp] [13907]: (note): libcurl global init successful
2026/05/26 12:50:32.351787586 {sztp_R0-0}{1}: [sztp] [13907]: (note): Initializing SKA client
2026/05/26 12:50:32.351836313 {sztp_R0-0}{1}: [btrace] [13907]: (note): module init: (prelib), huffman code len=32, code: 0xfe.96.c7.a8.00.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.352834361 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (evlib), huffman code len=29, code: 0x53.36.3d.40.00.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.352852503 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (bsignal), huffman code len=37, code: 0xe8.07.de.15.c0.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.353089139 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (sec_key_agent_client), huffman code len=98, code: 0x05.46.62.a6.e9.65.ea.f3.1a.58.af.32.00.00.00.00
2026/05/26 12:50:32.354162007 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (services), huffman code len=40, code: 0x05.d1.91.45.08.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.354285973 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (bipc), huffman code len=23, code: 0xe8.7e.90.00.00.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.354676587 {sztp_R0-0}{1}: [bipc] [13907:13908]: (note): Successfuly connected to server /tmp/rp/lipc/secure_key_agent_socket
2026/05/26 12:50:32.354699398 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (binos), huffman code len=28, code: 0xe8.79.b0.80.00.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.354707509 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (cyan), huffman code len=30, code: 0x43.74.97.20.00.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.354711418 {sztp_R0-0}{1}: [cyan] [13907:13908]: (warn): program path /usr/binos/bin/sztp not a package path, using 'root' package
2026/05/26 12:50:32.354836485 {sztp_R0-0}{1}: [cyan] [13907:13908]: (note): Successfully initialized cyan library for /usr/binos/bin/sztp with /tmp/cyan/root.cdb
2026/05/26 12:50:32.354873692 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (tdllib), huffman code len=30, code: 0xc9.bb.1e.a0.00.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.355010845 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (vista), huffman code len=27, code: 0x32.21.85.00.00.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.355016143 {sztp_R0-0}{1}: [tdllib] [13907:13908]: (note): Loading DB list for Nyquist platform
2026/05/26 12:50:32.355036230 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (bump_ptr_alloc), huffman code len=67, code: 0xea.9a.fd.ff.34.ca.ef.69.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.355062199 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (vs_flock), huffman code len=44, code: 0x32.0c.f7.b4.31.80.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.355509908 {sztp_R0-0}{1}: [tdllib] [13907:13908]: (ERR): Process with tag 261 is not permitted to operate on database '/tmp/rp/tdldb_rcow/0/SKA_PUBKEY_DB'.
2026/05/26 12:50:32.355513006 {sztp_R0-0}{1}: [sec_key_agent_client] [13907:13908]: (ERR): Error 1: Operation not permitted.  SKA TDL lib initialization failed for pubkey db. 
2026/05/26 12:50:32.355513590 {sztp_R0-0}{1}: [sec_key_agent_client] [13907:13908]: (note): ska_client TDL for pubkey DB initialization failed. 
2026/05/26 12:50:32.355530695 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (tdl_keyman_app), huffman code len=75, code: 0xc9.b6.62.a6.e9.a9.71.97.ff.00.00.00.00.00.00.00
2026/05/26 12:50:32.355562321 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (evutil), huffman code len=33, code: 0x53.34.e0.dc.00.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.355575710 {sztp_R0-0}{1}: [btrace] [13907:13908]: (note): module init: (sw_wdog), huffman code len=38, code: 0x0a.1d.13.bf.60.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.355629437 {sztp_R0-0}{1}: [sztp] [13907]: (note): Initializing tps client
2026/05/26 12:50:32.355646702 {sztp_R0-0}{1}: [btrace] [13907]: (note): module init: (tps-client), huffman code len=48, code: 0xcf.87.69.62.bc.c8.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.355657206 {sztp_R0-0}{1}: [tps-client] [13907]: (note): TPS client init
2026/05/26 12:50:32.355794166 {sztp_R0-0}{1}: [btrace] [13907]: (note): module init: (tdl_tps), huffman code len=32, code: 0xc9.b7.9f.08.00.00.00.00.00.00.00.00.00.00.00.00
2026/05/26 12:50:32.355939340 {sztp_R0-0}{1}: [sztp] [13907]: (note): tps wait for ipc
2026/05/26 12:50:32.356033862 {sztp_R0-0}{1}: [tps-client] [13907:13912]: (note): TPS IPC thread will now try to connect to IOSd
2026/05/26 12:50:32.356220636 {sztp_R0-0}{1}: [bipc] [13907:13912]: (note): Successfuly connected to server /tmp/rp/lipc/iosd_tps_socket-b0
2026/05/26 12:50:32.356222173 {sztp_R0-0}{1}: [tps-client] [13907:13912]: (note): Add IPC fd: 13 to epoll_fd 12 in IPC connect
2026/05/26 12:50:32.356225627 {sztp_R0-0}{1}: [tps-client] [13907:13912]: (note): connected to IOSd, ipc_handle 0x7bb6bc00fb88, ipc_fd 13
2026/05/26 12:50:32.356237056 {sztp_R0-0}{1}: [tps-client] [13907:13912]: (note): Initialised TPS IPC pipe read[14], write[15]
2026/05/26 12:50:32.356237838 {sztp_R0-0}{1}: [sztp] [13907]: (note): Initialized tps client
2026/05/26 12:50:32.356239387 {sztp_R0-0}{1}: [tps-client] [13907:13912]: (note): Added pipe rfd 14 to TPS epoll fd 12
2026/05/26 12:50:32.356247596 {sztp_R0-0}{1}: [tps-client] [13907]: (note): Send certchain request to IOS for seqnum 1, tp_label CISCO_IDEVID_SUDI
2026/05/26 12:50:32.356248002 {sztp_R0-0}{1}: [tps-client] [13907:13912]: (note): TPS IPC thread is initialised with epoll 12, pipe r:14 w:15, ipc 13
2026/05/26 12:50:32.364117018 {sztp_R0-0}{1}: [tdllib] [13907]: (note): epoch file read /tmp/tdlresolve/epoch_dir/active
2026/05/26 12:50:32.374550849 {sztp_R0-0}{1}: [tps-client] [13907:13912]: (note): Received IOS certchain response. seqnum 1, status 0, no of certs 2 key_name CISCO_IDEVID_SUDI
2026/05/26 12:50:32.374564785 {sztp_R0-0}{1}: [tps-client] [13907]: (note): Cert chain response, seqnum: 1, resp: 0x7bb6bc022e28[24], keyname CISCO_IDEVID_SUDI
2026/05/26 12:50:32.374670654 {sztp_R0-0}{1}: [sztp] [13907]: (note): Loaded SUDI certificate
2026/05/26 12:50:32.374671623 {sztp_R0-0}{1}: [sztp] [13907]: (note): SUDI certificate has extra certificates, will load them later
2026/05/26 12:50:32.374672025 {sztp_R0-0}{1}: [sztp] [13907]: (note): Load key into SKA engine
2026/05/26 12:50:32.374672514 {sztp_R0-0}{1}: [sztp] [13907]: (note): SKA engine key name: CISCO_IDEVID_SUDI
2026/05/26 12:50:32.416627663 {sztp_R0-0}{1}: [sztp] [13907]: (note): Adding new list of servers to the global list of bootstrap servers
2026/05/26 12:50:32.416662297 {sztp_R0-0}{1}: [sztp] [13907]: (note): Added a new server into global list of servers: https://10.1.1.3:8080
2026/05/26 12:50:32.416694245 {sztp_R0-0}{1}: [sztp] [13907]: (note): Attempting to bootstrap from the server https://10.1.1.3:8080
2026/05/26 12:50:32.416694985 {sztp_R0-0}{1}: [sztp] [13907]: (note): Preparing to download data from server https://10.1.1.3:8080
2026/05/26 12:50:32.416696043 {sztp_R0-0}{1}: [sztp] [13907]: (note): Discovering the Restconf root resource for server
2026/05/26 12:50:32.418853132 {sztp_R0-0}{1}: [sztp] [13907]: (note): sslctx callback invoked
2026/05/26 12:50:32.421601229 {sztp_R0-0}{1}: [sztp] [13907]: (note): Server certificate verification callback invoked
2026/05/26 12:50:32.421602627 {sztp_R0-0}{1}: [sztp] [13907]: (note): Server has no trust anchor associated to it
2026/05/26 12:50:32.421603013 {sztp_R0-0}{1}: [sztp] [13907]: (note): Accepting blindly
2026/05/26 12:50:33.179657840 {sztp_R0-0}{1}: [sztp] [13907]: (note): Received 104 bytes from Restconf server
2026/05/26 12:50:33.179951712 {sztp_R0-0}{1}: [sztp] [13907]: (note): Root resource for server https://10.1.1.3:8080: /restconf
2026/05/26 12:50:33.179955205 {sztp_R0-0}{1}: [sztp] [13907]: (note): URL for get-bootstrapping-data request: https://10.1.1.3:8080/restconf/operations/ietf-sztp-bootstrap-server:get-bootstrapping-data
2026/05/26 12:50:33.180141345 {sztp_R0-0}{1}: [sztp] [13907]: (note): Specifying signed-data-preferred
2026/05/26 12:50:33.180172965 {sztp_R0-0}{1}: [sztp] [13907]: (note): Retrieved HW model: C9300-24T
2026/05/26 12:50:33.180174399 {sztp_R0-0}{1}: [sztp] [13907]: (note): OS version = 17.18.01
2026/05/26 12:50:33.180736255 {sztp_R0-0}{1}: [sztp] [13907]: (note): sslctx callback invoked
2026/05/26 12:50:33.182159121 {sztp_R0-0}{1}: [sztp] [13907]: (note): Server certificate verification callback invoked
2026/05/26 12:50:33.182160492 {sztp_R0-0}{1}: [sztp] [13907]: (note): Server has no trust anchor associated to it
2026/05/26 12:50:33.182160850 {sztp_R0-0}{1}: [sztp] [13907]: (note): Accepting blindly
2026/05/26 12:50:33.927081636 {sztp_R0-0}{1}: [sztp] [13907]: (note): Sending data to restconf server, max number of bytes allowed to send in one batch: 65524
2026/05/26 12:50:33.927084778 {sztp_R0-0}{1}: [sztp] [13907]: (note): Number of bytes sent: 189
2026/05/26 12:50:33.927115320 {sztp_R0-0}{1}: [sztp] [13907]: (note): Sending data to restconf server, max number of bytes allowed to send in one batch: 65524
2026/05/26 12:50:33.927115865 {sztp_R0-0}{1}: [sztp] [13907]: (note): Number of bytes sent: 0
2026/05/26 12:50:33.948624673 {sztp_R0-0}{1}: [sztp] [13907]: (note): Received 8605 bytes from Restconf server
2026/05/26 12:50:33.948840625 {sztp_R0-0}{1}: [sztp] [13907]: (note): Server not trusted. Skipping reporting progress on bootstrap-initiated
2026/05/26 12:50:33.948842173 {sztp_R0-0}{1}: [sztp] [13907]: (note): Parsing downloaded text into bootstrapping data structures
2026/05/26 12:50:33.948937025 {sztp_R0-0}{1}: [sztp] [13907]: (note): XML document downloaded from bootstrapping server is parsed
2026/05/26 12:50:33.948937765 {sztp_R0-0}{1}: [sztp] [13907]: (note): Validating bootstrapping data
2026/05/26 12:50:33.949096598 {sztp_R0-0}{1}: [sztp] [13907]: (note): The voucher is not encrypted
2026/05/26 12:50:33.949097647 {sztp_R0-0}{1}: [sztp] [13907]: (note): Loading the device trust anchor
2026/05/26 12:50:33.949258392 {sztp_R0-0}{1}: [sztp] [13907]: (note): The device trust anchor is verified
2026/05/26 12:50:33.949569319 {sztp_R0-0}{1}: [sztp] [13907]: (note): Signature on ownership voucher's CMS structure has been verified.
2026/05/26 12:50:33.949594783 {sztp_R0-0}{1}: [sztp] [13907]: (note): No revocation check specified
2026/05/26 12:50:33.949607503 {sztp_R0-0}{1}: [sztp] [13907]: (note): The voucher is created in the past
2026/05/26 12:50:33.949609974 {sztp_R0-0}{1}: [sztp] [13907]: (note): The voucher is not expired
2026/05/26 12:50:33.949745817 {sztp_R0-0}{1}: [sztp] [13907]: (note): Retrieved serial number: FCW2126G05V
2026/05/26 12:50:33.949746674 {sztp_R0-0}{1}: [sztp] [13907]: (note): Serial number matched
2026/05/26 12:50:33.949902710 {sztp_R0-0}{1}: [sztp] [13907]: (note): The ownership voucher is valid
2026/05/26 12:50:33.950165717 {sztp_R0-0}{1}: [sztp] [13907]: (note): The owner certificate CMS structure is not encrypted
2026/05/26 12:50:33.950168991 {sztp_R0-0}{1}: [sztp] [13907]: (note): Will verify the chain against a trust anchor provided
2026/05/26 12:50:33.950423140 {sztp_R0-0}{1}: [sztp] [13907]: (note): Found -1 CRLs stapled to the CMS structure for owner certificate
2026/05/26 12:50:33.950423937 {sztp_R0-0}{1}: [sztp] [13907]: (note): The certificate chain from the CMS structure for owner certificate verified
2026/05/26 12:50:33.950721338 {sztp_R0-0}{1}: [sztp] [13907]: (note): Conveyed info: content type = pkcs7-signedData
2026/05/26 12:50:33.950722936 {sztp_R0-0}{1}: [sztp] [13907]: (note): The conveyed info is signed
2026/05/26 12:50:33.950727060 {sztp_R0-0}{1}: [sztp] [13907]: (note): Conveyed info: econtent_type = 1.2.840.113549.1.9.16.1.43
2026/05/26 12:50:33.950728887 {sztp_R0-0}{1}: [sztp] [13907]: (note): The conveyed info is json-formatted
2026/05/26 12:50:33.951096136 {sztp_R0-0}{1}: [sztp] [13907]: (note): Conveyed info signature is verified
2026/05/26 12:50:33.951134834 {sztp_R0-0}{1}: [sztp] [13907]: (note): The conveyed info is json formatted
2026/05/26 12:50:33.951159089 {sztp_R0-0}{1}: [sztp] [13907]: (note): The conveyed info has redirect information
2026/05/26 12:50:33.951159758 {sztp_R0-0}{1}: [sztp] [13907]: (note): Extracting redirect information from json formatted bootstrapping data
2026/05/26 12:50:33.951170872 {sztp_R0-0}{1}: [sztp] [13907]: (note): Received redirect info from the bootstrapping server https://10.1.1.3:8080
2026/05/26 12:50:33.951173301 {sztp_R0-0}{1}: [sztp] [13907]: (note): Added a new server into global list of servers: https://10.1.1.3:9090
2026/05/26 12:50:33.951213567 {sztp_R0-0}{1}: [sztp] [13907]: (note): Attempting to bootstrap from the server https://10.1.1.3:9090
2026/05/26 12:50:33.951214236 {sztp_R0-0}{1}: [sztp] [13907]: (note): Preparing to download data from server https://10.1.1.3:9090
2026/05/26 12:50:33.951215176 {sztp_R0-0}{1}: [sztp] [13907]: (note): Discovering the Restconf root resource for server
2026/05/26 12:50:33.952017035 {sztp_R0-0}{1}: [sztp] [13907]: (note): sslctx callback invoked
2026/05/26 12:50:33.954070122 {sztp_R0-0}{1}: [sztp] [13907]: (note): Server certificate verification callback invoked
2026/05/26 12:50:33.954071419 {sztp_R0-0}{1}: [sztp] [13907]: (note): Server has no trust anchor associated to it
2026/05/26 12:50:33.954071893 {sztp_R0-0}{1}: [sztp] [13907]: (note): Demoting trust state and accepting blindly
2026/05/26 12:50:34.701574804 {sztp_R0-0}{1}: [sztp] [13907]: (note): Received 104 bytes from Restconf server
2026/05/26 12:50:34.701884213 {sztp_R0-0}{1}: [sztp] [13907]: (note): Root resource for server https://10.1.1.3:9090: /restconf
2026/05/26 12:50:34.701887480 {sztp_R0-0}{1}: [sztp] [13907]: (note): URL for get-bootstrapping-data request: https://10.1.1.3:9090/restconf/operations/ietf-sztp-bootstrap-server:get-bootstrapping-data
2026/05/26 12:50:34.701985929 {sztp_R0-0}{1}: [sztp] [13907]: (note): Specifying signed-data-preferred
2026/05/26 12:50:34.702634754 {sztp_R0-0}{1}: [sztp] [13907]: (note): sslctx callback invoked
2026/05/26 12:50:34.704062878 {sztp_R0-0}{1}: [sztp] [13907]: (note): Server certificate verification callback invoked
2026/05/26 12:50:34.704064102 {sztp_R0-0}{1}: [sztp] [13907]: (note): Server has no trust anchor associated to it
2026/05/26 12:50:34.704064520 {sztp_R0-0}{1}: [sztp] [13907]: (note): Accepting blindly
2026/05/26 12:50:35.449077430 {sztp_R0-0}{1}: [sztp] [13907]: (note): Sending data to restconf server, max number of bytes allowed to send in one batch: 65524
2026/05/26 12:50:35.449079817 {sztp_R0-0}{1}: [sztp] [13907]: (note): Number of bytes sent: 189
2026/05/26 12:50:35.449122104 {sztp_R0-0}{1}: [sztp] [13907]: (note): Sending data to restconf server, max number of bytes allowed to send in one batch: 65524
2026/05/26 12:50:35.449123244 {sztp_R0-0}{1}: [sztp] [13907]: (note): Number of bytes sent: 0
2026/05/26 12:50:35.468874277 {sztp_R0-0}{1}: [sztp] [13907]: (note): Received 16384 bytes from Restconf server
2026/05/26 12:50:35.469318659 {sztp_R0-0}{1}: [sztp] [13907]: (note): Received 16384 bytes from Restconf server
2026/05/26 12:50:35.469847058 {sztp_R0-0}{1}: [sztp] [13907]: (note): Received 16384 bytes from Restconf server
2026/05/26 12:50:35.470011216 {sztp_R0-0}{1}: [sztp] [13907]: (note): Received 6377 bytes from Restconf server
2026/05/26 12:50:35.470249669 {sztp_R0-0}{1}: [sztp] [13907]: (note): Server not trusted. Skipping reporting progress on bootstrap-initiated
2026/05/26 12:50:35.470251141 {sztp_R0-0}{1}: [sztp] [13907]: (note): Parsing downloaded text into bootstrapping data structures
2026/05/26 12:50:35.470474385 {sztp_R0-0}{1}: [sztp] [13907]: (note): XML document downloaded from bootstrapping server is parsed
2026/05/26 12:50:35.470475794 {sztp_R0-0}{1}: [sztp] [13907]: (note): Validating bootstrapping data
2026/05/26 12:50:35.470734090 {sztp_R0-0}{1}: [sztp] [13907]: (note): The voucher is not encrypted
2026/05/26 12:50:35.471019726 {sztp_R0-0}{1}: [sztp] [13907]: (note): Signature on ownership voucher's CMS structure has been verified.
2026/05/26 12:50:35.471039544 {sztp_R0-0}{1}: [sztp] [13907]: (note): No revocation check specified
2026/05/26 12:50:35.471052673 {sztp_R0-0}{1}: [sztp] [13907]: (note): The voucher is created in the past
2026/05/26 12:50:35.471055306 {sztp_R0-0}{1}: [sztp] [13907]: (note): The voucher is not expired
2026/05/26 12:50:35.471056430 {sztp_R0-0}{1}: [sztp] [13907]: (note): Serial number matched
2026/05/26 12:50:35.471208591 {sztp_R0-0}{1}: [sztp] [13907]: (note): The ownership voucher is valid
2026/05/26 12:50:35.471481897 {sztp_R0-0}{1}: [sztp] [13907]: (note): The owner certificate CMS structure is not encrypted
2026/05/26 12:50:35.471485497 {sztp_R0-0}{1}: [sztp] [13907]: (note): Will verify the chain against a trust anchor provided
2026/05/26 12:50:35.471737460 {sztp_R0-0}{1}: [sztp] [13907]: (note): Found -1 CRLs stapled to the CMS structure for owner certificate
2026/05/26 12:50:35.471738353 {sztp_R0-0}{1}: [sztp] [13907]: (note): The certificate chain from the CMS structure for owner certificate verified
2026/05/26 12:50:35.472047285 {sztp_R0-0}{1}: [sztp] [13907]: (note): Conveyed info: content type = pkcs7-signedData
2026/05/26 12:50:35.472048525 {sztp_R0-0}{1}: [sztp] [13907]: (note): The conveyed info is signed
2026/05/26 12:50:35.472052425 {sztp_R0-0}{1}: [sztp] [13907]: (note): Conveyed info: econtent_type = 1.2.840.113549.1.9.16.1.43
2026/05/26 12:50:35.472054227 {sztp_R0-0}{1}: [sztp] [13907]: (note): The conveyed info is json-formatted
2026/05/26 12:50:35.472646594 {sztp_R0-0}{1}: [sztp] [13907]: (note): Conveyed info signature is verified
2026/05/26 12:50:35.472722188 {sztp_R0-0}{1}: [sztp] [13907]: (note): The conveyed info is json formatted
2026/05/26 12:50:35.472770812 {sztp_R0-0}{1}: [sztp] [13907]: (note): The conveyed info has onboarding information
2026/05/26 12:50:35.472771386 {sztp_R0-0}{1}: [sztp] [13907]: (note): Extracting onboarding info from the json
2026/05/26 12:50:35.472790972 {sztp_R0-0}{1}: [sztp] [13907]: (note): Received onboarding info from the bootstrapping server https://10.1.1.3:9090
2026/05/26 12:50:35.472792090 {sztp_R0-0}{1}: [sztp] [13907]: (note): Onboarding info has no OS version specified. Image update is not required
2026/05/26 12:50:35.472792603 {sztp_R0-0}{1}: [sztp] [13907]: (note): Image update is not required
2026/05/26 12:50:35.472793061 {sztp_R0-0}{1}: [sztp] [13907]: (note): Bootstrapping received
2026/05/26 12:50:35.472793597 {sztp_R0-0}{1}: [sztp] [13907]: (note): Storing onboarding info
2026/05/26 12:50:35.472962415 {sztp_R0-0}{1}: [sztp] [13907]: (note): Decoded preconfiguration script stored at /tmp/.shell_exec/sztp_preconfiguration.py
2026/05/26 12:50:35.472995468 {sztp_R0-0}{1}: [sztp] [13907]: (note): Decoded configuration stored at /tmp/.shell_exec/sztp_configuration.xml
2026/05/26 12:50:35.473020413 {sztp_R0-0}{1}: [sztp] [13907]: (note): Decoded postconfiguration script stored at /tmp/.shell_exec/sztp_postconfiguration.py
2026/05/26 12:50:35.473020933 {sztp_R0-0}{1}: [sztp] [13907]: (note): Will proceed now with pre-configuration script
2026/05/26 12:50:35.473021317 {sztp_R0-0}{1}: [sztp] [13907]: (note): Storing bootstrapping list
2026/05/26 12:50:35.473021701 {sztp_R0-0}{1}: [sztp] [13907]: (note): Storing current server info
2026/05/26 12:50:44.987914375 {sztp_R0-0}{1}: [btrace] [16100]: (note): Btrace started for process sztp bproc:sztp ID 16100 with 512 modules
2026/05/26 12:50:44.987916150 {sztp_R0-0}{1}: [btrace] [16100]: (note): File size max used for rotation of tracelogs: 1048576
2026/05/26 12:50:44.987916601 {sztp_R0-0}{1}: [btrace] [16100]: (note): File size max used for rotation of TAN stats file: 1048576
2026/05/26 12:50:44.987916952 {sztp_R0-0}{1}: [btrace] [16100]: (note): File rotation timeout max used for rotation of TAN stats file: 600
2026/05/26 12:50:44.987917321 {sztp_R0-0}{1}: [btrace] [16100]: (note): Bproc Name:sztp, Bproc proc tag:261 infra_bproc:0
2026/05/26 12:50:44.988192128 {sztp_R0-0}{1}: [btrace] [16100]: (note): Boot level config file [/crashinfo/tracelogs/level_config/sztp_R0-0] is not available. Skipping
2026/05/26 12:50:44.988193348 {sztp_R0-0}{1}: [sztp] [16100]: (note): sztp started with list of 3 command line arguments:
2026/05/26 12:50:44.988194108 {sztp_R0-0}{1}: [sztp] [16100]: (note):     /usr/binos/bin/sztp
2026/05/26 12:50:44.988194522 {sztp_R0-0}{1}: [sztp] [16100]: (note):     -r
2026/05/26 12:50:44.988194897 {sztp_R0-0}{1}: [sztp] [16100]: (note):     pre-script-initiated
2026/05/26 12:50:44.988195375 {sztp_R0-0}{1}: [sztp] [16100]: (note): Loading debug properties
2026/05/26 12:50:44.988215486 {sztp_R0-0}{1}: [sztp] [16100]: (note): Property chasfs_stats_on is not present. Assuming FALSE
2026/05/26 12:50:44.988219473 {sztp_R0-0}{1}: [sztp] [16100]: (note): Property debug_certificates is not present. Assuming FALSE
2026/05/26 12:50:44.988223171 {sztp_R0-0}{1}: [sztp] [16100]: (note): Property debug_cms_structures is not present. Assuming FALSE
2026/05/26 12:50:44.988226904 {sztp_R0-0}{1}: [sztp] [16100]: (note): Property debug_conveyed_info is not present. Assuming FALSE
2026/05/26 12:50:44.988230739 {sztp_R0-0}{1}: [sztp] [16100]: (note): Property debug_servers_list is not present. Assuming FALSE
2026/05/26 12:50:44.988234399 {sztp_R0-0}{1}: [sztp] [16100]: (note): Property debug_curl_verbose is not present. Assuming FALSE
2026/05/26 12:50:44.988421524 {sztp_R0-0}{1}: [sztp] [16100]: (note): libcurl global init successful
2026/05/26 12:50:44.988424184 {sztp_R0-0}{1}: [sztp] [16100]: (note): Initializing SKA client
```

## What Matters Most

If your logs are noisy, focus on these success markers:

- OPTION143 or bootstrap-server-list found
- Redirect information received from port 8080
- Voucher signature and owner chain verification passed
- Onboarding-information signature verification passed
- Onboarding accepted and payload applied
- Final state reports SUCCESS


# TTDF Project - CoAP to REST Bridge

This project reads sensor data from Wi-SUN field nodes over CoAP and forwards that data to a REST API endpoint.

It supports multiple nodes, per-node API credentials, structured logging, and periodic polling.

## What This Project Does

1. Loads enabled nodes from nodes.json.
2. For each node, runs:
   coap-client-notls -m get coap://[IPv6]:PORT/sensorStatus
3. Parses CoAP JSON response.
4. Maps raw device fields into backend payload format.
5. Posts mapped payload to that node's API URL using that node's token.
6. Repeats every polling cycle.

## Current Project Structure

- main.py
  Main runtime loop and orchestration.
- requirements.txt
  Python dependency list for this project.
- nodes.json
  Node list with IPv6, API URL, API token, port, and enabled flag.
- config_loader.py
  JSON file loader for node configuration.
- coap_reader.py
  Executes CoAP command and parses JSON output.
- data_mapper.py
  Converts raw node response to final payload schema.
- data_poster.py
  Sends payload to backend via HTTP POST.
- logging_config.py
  Configures console and file logging.
- logs/coap_rest_bridge.log
  Combined application log file.

## Software Requirements

- Linux machine with Python 3.10+ recommended
- libcoap client tool installed with command name coap-client-notls
- Python packages from requirements.txt

## Install Dependencies


1. Create virtual environment

  python3 -m venv .venv
  source .venv/bin/activate

2. Install Python dependencies
  pip3 install -r requirements.txt

## Quick Start

1. Update node list in nodes.json.
2. Install dependencies (section above).
3. Run the service:

  python3 main.py

4. Check logs in logs/coap_rest_bridge.log.

## Node Configuration

Configure all nodes in nodes.json.

Required fields per node:

- node_id: integer
- name: string
- ipv6: full IPv6 address of node
- port: CoAP port, usually 5683
- api_url: backend endpoint for this node
- api_token: bearer token for this node
- enabled: true or false

Example:

[
  {
    "node_id": 1,
    "name": "wn03-2329-0001",
    "ipv6": "fd12:3456::eae:5fff:fe52:69de",
    "port": 5683,
    "api_url": "https://your-server/api/nodes/create-cin/233",
    "api_token": "TOKEN_NODE_1",
    "enabled": true
  },
  {
    "node_id": 2,
    "name": "wn03-2329-0002",
    "ipv6": "fd12:3456::eae:5fff:fe52:6646",
    "port": 5683,
    "api_url": "https://your-server/api/nodes/create-cin/234",
    "api_token": "TOKEN_NODE_2",
    "enabled": true
  }
]

## How to Add a New Node

1. Open nodes.json.
2. Add one new object inside the JSON array.
3. Set these fields:
   - node_id: unique number
   - name: readable node name
   - ipv6: full IPv6 of node
   - port: normally 5683
   - api_url: backend endpoint for that node
   - api_token: bearer token for that node
   - enabled: true
4. Save the file.
5. Restart service (or wait for next loop if already running).

Example new node entry:

{
  "node_id": 3,
  "name": "wn03-2329-0003",
  "ipv6": "fd12:3456::eae:5fff:fe52:1234",
  "port": 5683,
  "api_url": "https://your-server/api/nodes/create-cin/235",
  "api_token": "TOKEN_NODE_3",
  "enabled": true
}

## Runtime Constants

These values are currently defined in source files:

- Poll interval: main.py
  POLL_INTERVAL_SECONDS = 600
- CoAP endpoint: main.py
  COAP_ENDPOINT = sensorStatus
- CoAP timeout: coap_reader.py
  COAP_TIMEOUT_SECONDS = 10
- HTTP timeout: data_poster.py
  HTTP_TIMEOUT_SECONDS = 10
- Log file path and levels: logging_config.py

## Payload Sent to Backend

The final payload keys are generated in this sequence:

1. lamp_status
2. relay_status
3. energy
4. power
5. current
6. rsl_out
7. rsl_in
8. disconnectivity
9. connectivity
10. availability
11. rpl_rank
12. ipv6
13. temperature
14. relative_humidity
15. ambient_light

Important mapping note:

- The ipv6 field is sent as the last 4 characters of node IP from CoAP response ip_v6.
  Example: fd12:...:69de -> 69de

## Logging Behavior

Log file:

- logs/coap_rest_bridge.log

Levels:

- Console logs INFO and above
- File logs DEBUG and above

Behavior:

- Expected node CoAP timeout is logged as WARNING with short message
- Full traceback is printed to terminal only for unexpected exceptions
- Log file keeps concise operational messages without full stack traces

## Run the Project

From project root:

python3 main.py

The service will:

- Start bridge loop
- Read enabled nodes
- Fetch each node over CoAP
- Post each payload to configured API
- Sleep for poll interval
- Repeat forever

Stop with Ctrl+C.

## Validate CoAP Manually

Test one node manually:

coap-client-notls -m get coap://[fd12:3456::eae:5fff:fe52:69de]:5683/sensorStatus

If this command times out manually, the bridge will also time out for that node.

## Troubleshooting

### CoAP timeout warnings

Symptom:

- WARNING lines like COAP timeout for node ...

Checks:

1. Verify node is powered and joined to network.
2. Ping or verify IPv6 reachability from host.
3. Run manual coap-client-notls command.
4. Increase COAP timeout in coap_reader.py if network is slow.

### Node skipped due to missing config

Symptom:

- Node has no api_token or Node has no api_url

Fix:

- Ensure each node in nodes.json has both api_url and api_token.

### HTTP post failed

Symptom:

- Post failed for node ... status=...

Checks:

1. Validate api_url path and node ID.
2. Validate api_token.
3. Check backend service availability.
4. Inspect response body in log line.

### Logs not updating

Checks:

1. Run from project root.
2. Confirm process is running.
3. Confirm write permissions for logs directory.
4. Confirm file path logs/coap_rest_bridge.log.

## Notes

- settings.json is no longer used in current architecture.
- Endpoint is constant and not stored in nodes.json.
- This project currently has no automatic fallback to dummy/random data.

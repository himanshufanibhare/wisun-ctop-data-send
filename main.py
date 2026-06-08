import subprocess
import time
import traceback

from coap_reader import fetch_sensor_status
from config_loader import load_nodes
from csv_storage import append_sensor_row
from data_mapper import map_sensor_data
from data_poster import post_payload
from logging_config import setup_logging


POLL_INTERVAL_SECONDS = 600
COAP_ENDPOINT = "sensorStatus"


def build_dummy_payload(node):
    return {
    "lux": 0.0,
    "humidity": 0.0,
    "temperature": 0.0,
    "ipv6_address": "NA",
    "rpl": 0,
    "availability": "NA",
    "connectivity": "NA",
    "disconnectivity": "NA",
    "rsl_in": 0,
    "rsl_out": 0,
    "current": 0.0,
    "power": 0.0,
    "energy": 0.0,
    "relay_status": "NA",
    "lamp_status": "NA",    }


def process_node(node, logger):
    node_name = node.get("name", "unknown-node")
    ipv6 = node.get("ipv6")
    port = int(node.get("port", 5683))
    endpoint = COAP_ENDPOINT
    api_url = node.get("api_url")
    api_token = node.get("api_token")

    if not ipv6:
        logger.error("Node '%s' is missing IPv6 address. Skipping.", node_name)
        return

    if not api_token:
        logger.error(
            "Node '%s' has no api_token. Skipping.",
            node_name,
        )
        return

    if not api_url:
        logger.error(
            "Node '%s' has no api_url. Skipping.",
            node_name,
        )
        return

    logger.debug(
        "Node '%s' config: ipv6=%s port=%s endpoint=%s api_url=%s",
        node_name,
        ipv6,
        port,
        endpoint,
        api_url,
    )

    logger.info("Fetching COAP data from node '%s' (%s)", node_name, ipv6)
    try:
        raw_data = fetch_sensor_status(
            ipv6=ipv6,
            port=port,
            endpoint=endpoint,
        )
        payload = map_sensor_data(raw_data)
        logger.debug("Mapped payload for node '%s': %s", node_name, payload)
    except subprocess.TimeoutExpired:
        logger.warning(
            "COAP timeout for node '%s' (%s). Sending dummy payload.",
            node_name,
            ipv6,
        )
        payload = build_dummy_payload(node)
    except Exception as coap_error:
        logger.warning(
            "COAP fetch failed for node '%s' (%s): %s. Sending dummy payload.",
            node_name,
            ipv6,
            coap_error,
        )
        payload = build_dummy_payload(node)

    csv_record = {
        "node_id": node.get("node_id", ""),
        "node_name": node_name,
        **payload,
    }
    csv_file_path = append_sensor_row(csv_record)
    logger.debug("Stored sensor row for node '%s' in %s", node_name, csv_file_path)

    response = post_payload(
        url=api_url,
        token=api_token,
        payload=payload,
    )

    if response.status_code in (200, 201):
        logger.info(
            "Posted node '%s' successfully with status %s",
            node_name,
            response.status_code,
        )
    else:
        logger.warning(
            "Post failed for node '%s': status=%s body=%s",
            node_name,
            response.status_code,
            response.text,
        )


def main():
    logger = setup_logging()

    logger.info("COAP to REST bridge started")
    logger.debug("Poll interval configured to %s seconds", POLL_INTERVAL_SECONDS)

    while True:
        try:
            nodes = load_nodes("nodes.json")
            logger.debug("Loaded %s enabled node(s)", len(nodes))
            if not nodes:
                logger.warning("No enabled nodes found in nodes.json")

            for node in nodes:
                try:
                    process_node(node, logger)
                except Exception as node_error:
                    logger.error(
                        "Failed processing node '%s': %s",
                        node.get("name", "unknown-node"),
                        node_error,
                    )
                    traceback.print_exc()

        except Exception as loop_error:
            logger.error("Main loop error: %s", loop_error)
            traceback.print_exc()

        logger.info("Sleeping for %s seconds", POLL_INTERVAL_SECONDS)
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

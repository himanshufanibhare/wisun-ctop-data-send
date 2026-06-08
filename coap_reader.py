import json
import logging
import subprocess
from typing import Any, Dict, Optional


COAP_TIMEOUT_SECONDS = 10
logger = logging.getLogger("coap_rest_bridge.coap_reader")


def fetch_sensor_status(
    ipv6: str,
    port: int,
    endpoint: str,
    timeout_seconds: Optional[int] = None,
) -> Dict[str, Any]:
    coap_uri = f"coap://[{ipv6}]:{port}/{endpoint}"
    command = ["coap-client-notls", "-m", "get", coap_uri]
    request_timeout = COAP_TIMEOUT_SECONDS if timeout_seconds is None else timeout_seconds

    logger.debug("Running COAP command: %s (timeout=%ss)", " ".join(command), request_timeout)

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=request_timeout,
    )

    logger.debug("COAP command return code for %s: %s", coap_uri, result.returncode)

    if result.returncode != 0:
        stderr_text = result.stderr.strip()
        logger.error("COAP command failed for %s: %s", coap_uri, stderr_text)
        raise RuntimeError(
            f"COAP command failed for {coap_uri} with code {result.returncode}: {stderr_text}"
        )

    output = result.stdout.strip()
    start = output.find("{")
    end = output.rfind("}")

    if start == -1 or end == -1 or end < start:
        logger.error("COAP response did not contain valid JSON for %s: %s", coap_uri, output)
        raise ValueError(f"No JSON object found in COAP output for {coap_uri}: {output}")

    parsed_data = json.loads(output[start : end + 1])
    logger.debug("Parsed COAP payload for %s: %s", coap_uri, parsed_data)
    return parsed_data

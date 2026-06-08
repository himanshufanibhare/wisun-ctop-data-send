import logging
from typing import Any, Dict, Optional

import requests


HTTP_TIMEOUT_SECONDS = 10
logger = logging.getLogger("coap_rest_bridge.data_poster")


def post_payload(
    url: str,
    token: str,
    payload: Dict[str, Any],
    timeout_seconds: Optional[int] = None,
) -> requests.Response:
    request_timeout = HTTP_TIMEOUT_SECONDS if timeout_seconds is None else timeout_seconds

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    logger.debug("Sending POST request to %s (timeout=%ss)", url, request_timeout)
    logger.debug("Payload keys: %s", list(payload.keys()))

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=request_timeout,
    )

    if response.status_code in (200, 201):
        logger.debug("POST success for %s: status=%s", url, response.status_code)
    else:
        logger.error("POST failed for %s: status=%s body=%s", url, response.status_code, response.text)

    return response

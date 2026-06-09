import logging
from typing import Any, Dict, Optional
import requests

logger = logging.getLogger("coap_rest_bridge.data_poster")

HTTP_TIMEOUT_SECONDS = 10


def post_payload(
    url: str,
    token: str,
    payload: Dict[str, Any],
    timeout_seconds: Optional[int] = None,
):
    request_timeout = (
        HTTP_TIMEOUT_SECONDS
        if timeout_seconds is None
        else timeout_seconds
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.post(
            url=url,
            json=payload,
            headers=headers,
            timeout=request_timeout,
        )

        response.raise_for_status()

        logger.info(
            "POST success %s status=%s",
            url,
            response.status_code,
        )

        return response

    except requests.RequestException as error:
        logger.error(
            "POST failed for %s : %s",
            url,
            error,
        )
        raise
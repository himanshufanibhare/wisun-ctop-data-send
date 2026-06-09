import os
from dotenv import load_dotenv

load_dotenv()


def get_api_details(node_id: int):
    api_url = os.getenv(f"API_URL_{node_id}")
    api_token = os.getenv(f"API_TOKEN_{node_id}")

    if not api_url:
        raise ValueError(f"Missing API_URL_{node_id}")

    if not api_token:
        raise ValueError(f"Missing API_TOKEN_{node_id}")

    return api_url, api_token
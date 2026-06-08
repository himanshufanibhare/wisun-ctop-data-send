import json
from pathlib import Path
from typing import Any, Dict, List


def _load_json_file(file_path: str) -> Any:
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_nodes(file_path: str = "nodes.json") -> List[Dict[str, Any]]:
    data = _load_json_file(file_path)
    if not isinstance(data, list):
        raise ValueError(f"Nodes file must contain a JSON array: {file_path}")
    return [node for node in data if isinstance(node, dict) and node.get("enabled", True)]

from typing import Any, Dict


def map_sensor_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    ipv6_full = str(raw_data.get("ip_v6", ""))
    ipv6_last4 = ipv6_full[-4:] if ipv6_full else ""

    return {
    "lux": float(raw_data.get("lux", 0.0)),
    "humidity": float(raw_data.get("humidity", 0.0)),
    "temperature": float(raw_data.get("temperature", 0.0)),
    "ipv6_address": ipv6_last4,
    "rpl": int(raw_data.get("rpl", 0)),
    "availability": str(raw_data.get("availability", "0")),
    "connectivity": str(raw_data.get("connectivity", "0-00:00:00")),
    "disconnectivity": str(raw_data.get("disconnectivity", "0-00:00:00")),
    "rsl_in": int(raw_data.get("rsl_in", 0)),
    "rsl_out": int(raw_data.get("rsl_out", 0)),
    "current": float(raw_data.get("current", 0.0)),
    "power": float(raw_data.get("power", 0.0)),
    "energy": float(raw_data.get("energy", 0.0)),
    "relay_status": str(raw_data.get("relay_status", "OFF")),
    "lamp_status": str(raw_data.get("lamp_status", "OFF"))
    }

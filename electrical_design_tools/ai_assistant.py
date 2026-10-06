from __future__ import annotations

from typing import Iterable

from .calculators import calculate_current, calculate_total_load, calculate_voltage_drop, choose_wire_size


class DesignAssistant:
    """Simple rule-based assistant for early electrical design calculations."""

    def __init__(self, voltage_v: float = 230.0):
        self.voltage_v = voltage_v

    def summarize(self, load_items: Iterable[dict], current_limit_a: float | None = None) -> dict:
        items = []
        for item in load_items:
            items.append({
                "name": item.get("name", "Unnamed"),
                "power_w": float(item.get("power_w", 0.0)),
                "quantity": int(item.get("quantity", 1)),
                "demand_factor": float(item.get("demand_factor", 1.0)),
            })

        parsed = []
        for item in items:
            parsed.append({
                "name": item["name"],
                "power_w": item["power_w"],
                "quantity": item["quantity"],
                "demand_factor": item["demand_factor"],
                "total_power_w": item["power_w"] * item["quantity"] * item["demand_factor"],
            })

        total_power = sum(entry["total_power_w"] for entry in parsed)
        total_current = calculate_current(total_power, self.voltage_v)
        recommended_wire = choose_wire_size(total_current)

        summary = {
            "total_power_w": total_power,
            "total_current_a": total_current,
            "recommended_wire": recommended_wire,
            "notes": [
                "Toplam yük, önerilen akım ve kablo seçimi temel olarak hesaplanmıştır.",
                "Yönetmelik ve yerel koşullar için uzman denetim gereklidir.",
            ],
        }

        if current_limit_a is not None:
            summary["current_limit_check"] = total_current <= current_limit_a

        return summary

    def estimate_voltage_drop(self, current_a: float, cable_length_m: float, resistance_ohm_per_km: float) -> dict:
        drop = calculate_voltage_drop(current_a, cable_length_m, resistance_ohm_per_km)
        return {
            "current_a": current_a,
            "cable_length_m": cable_length_m,
            "resistance_ohm_per_km": resistance_ohm_per_km,
            "voltage_drop_v": drop,
            "message": "Gerilim düşümü kısa mesafeli tasarım için incelenmelidir.",
        }


__all__ = ["DesignAssistant"]

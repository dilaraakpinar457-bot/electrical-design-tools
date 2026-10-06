from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import List


@dataclass
class LoadItem:
    name: str
    power_w: float
    quantity: int = 1
    demand_factor: float = 1.0

    @property
    def total_power_w(self) -> float:
        return self.power_w * self.quantity * self.demand_factor


def calculate_total_load(items: List[LoadItem]) -> float:
    return sum(item.total_power_w for item in items)


def calculate_current(power_w: float, voltage_v: float, power_factor: float = 1.0, three_phase: bool = False) -> float:
    if voltage_v <= 0:
        raise ValueError("Voltage must be greater than zero.")
    if power_factor <= 0:
        raise ValueError("Power factor must be greater than zero.")

    if three_phase:
        return power_w / (sqrt(3) * voltage_v * power_factor)
    return power_w / (voltage_v * power_factor)


def choose_wire_size(current_a: float, material: str = "cu") -> dict:
    """Return the smallest approximate wire size that meets the current requirement.

    Values are generic and intended for quick design estimation.
    """
    if current_a <= 0:
        raise ValueError("Current must be greater than zero.")

    ampacity_by_awg = {
        14: 15,
        12: 20,
        10: 30,
        8: 40,
        6: 55,
        4: 70,
        2: 95,
        1: 110,
        1 / 0: 125,
    }

    if material.lower() != "cu":
        # Allow aluminum to fail safe by being more conservative.
        ampacity_by_awg = {key: value * 0.8 for key, value in ampacity_by_awg.items()}

    for gauge, ampacity in sorted(ampacity_by_awg.items(), key=lambda item: item[0]):
        if ampacity >= current_a:
            return {"awg": gauge, "ampacity_a": ampacity, "material": material}

    raise ValueError("No supported wire size found for the required current.")


def calculate_voltage_drop(current_a: float, cable_length_m: float, resistance_ohm_per_km: float, power_factor: float = 0.85, three_phase: bool = False) -> float:
    if current_a <= 0:
        raise ValueError("Current must be greater than zero.")
    if cable_length_m <= 0:
        raise ValueError("Cable length must be greater than zero.")
    if resistance_ohm_per_km <= 0:
        raise ValueError("Resistance must be greater than zero.")

    length_km = cable_length_m / 1000.0
    if three_phase:
        drop = sqrt(3) * current_a * length_km * resistance_ohm_per_km * power_factor
    else:
        drop = 2 * current_a * length_km * resistance_ohm_per_km * power_factor

    return drop


def estimate_lighting_requirement(room_area_m2: float, target_lux: float, lamp_lumens: float, system_efficiency: float = 0.8) -> dict:
    if room_area_m2 <= 0:
        raise ValueError("Room area must be greater than zero.")
    if target_lux <= 0:
        raise ValueError("Target lux must be greater than zero.")
    if lamp_lumens <= 0:
        raise ValueError("Lamp lumens must be greater than zero.")
    if system_efficiency <= 0:
        raise ValueError("System efficiency must be greater than zero.")

    total_lumens = room_area_m2 * target_lux / system_efficiency
    quantity = total_lumens / lamp_lumens

    return {
        "room_area_m2": room_area_m2,
        "target_lux": target_lux,
        "lamp_lumens": lamp_lumens,
        "required_lumens": total_lumens,
        "lamp_quantity": quantity,
    }


__all__ = [
    "LoadItem",
    "calculate_total_load",
    "calculate_current",
    "choose_wire_size",
    "calculate_voltage_drop",
    "estimate_lighting_requirement",
]

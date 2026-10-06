from __future__ import annotations

import argparse
from pathlib import Path

from electrical_design_tools.calculators import (
    LoadItem,
    calculate_current,
    calculate_total_load,
    calculate_voltage_drop,
    choose_wire_size,
    estimate_lighting_requirement,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Electrical design toolset")
    parser.add_argument("--load", nargs="*", help="Load values as name:power_w")
    parser.add_argument("--voltage", type=float, default=230.0, help="System voltage in volts")
    parser.add_argument("--length", type=float, default=30.0, help="Cable length in meters")
    parser.add_argument("--resistance", type=float, default=2.2, help="Cable resistance in ohm/km")
    parser.add_argument("--room-area", type=float, default=20.0, help="Room area in m2")
    parser.add_argument("--lux", type=float, default=300.0, help="Target illuminance in lux")
    parser.add_argument("--lamp-lumens", type=float, default=1200.0, help="Lamp lumens")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    items = []
    if args.load:
        for entry in args.load:
            try:
                name, raw_power = entry.split(":")
                items.append(LoadItem(name=name.strip(), power_w=float(raw_power.strip())))
            except ValueError as exc:
                raise ValueError(f"Invalid format for load item: {entry!r}. Use name:power_w") from exc

    if not items:
        items = [
            LoadItem("Aydınlatma", 1500),
            LoadItem("Priz", 1200),
            LoadItem("Klima", 2200),
        ]

    total_power = calculate_total_load(items)
    total_current = calculate_current(total_power, args.voltage)
    wire = choose_wire_size(total_current)
    drop = calculate_voltage_drop(total_current, args.length, args.resistance)
    lighting = estimate_lighting_requirement(args.room_area, args.lux, args.lamp_lumens)

    print("Toplam güç (W):", round(total_power, 2))
    print("Toplam akım (A):", round(total_current, 2))
    print("Önerilen kablo:", wire)
    print("Gerilim düşümü (V):", round(drop, 2))
    print("Aydınlatma hesabı:", lighting)


if __name__ == "__main__":
    main()

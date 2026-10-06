from electrical_design_tools.calculators import (
    LoadItem,
    calculate_current,
    calculate_total_load,
    calculate_voltage_drop,
    choose_wire_size,
    estimate_lighting_requirement,
)
from electrical_design_tools.ai_assistant import DesignAssistant


def main() -> None:
    sample_items = [
        LoadItem("Aydınlatma", 1500),
        LoadItem("Priz", 1200),
        LoadItem("Klima", 2200),
    ]

    total_power = calculate_total_load(sample_items)
    total_current = calculate_current(total_power, 230)
    wire = choose_wire_size(total_current)
    voltage_drop = calculate_voltage_drop(total_current, 30, 2.2)
    lighting = estimate_lighting_requirement(20, 300, 1200)

    assistant = DesignAssistant()
    summary = assistant.summarize([
        {"name": "Aydınlatma", "power_w": 1500, "quantity": 1},
        {"name": "Priz", "power_w": 1200, "quantity": 1},
        {"name": "Klima", "power_w": 2200, "quantity": 1},
    ])

    print("Toplam güç (W):", total_power)
    print("Toplam akım (A):", total_current)
    print("Kablo seçimi:", wire)
    print("Gerilim düşümü (V):", voltage_drop)
    print("Aydınlatma önerisi:", lighting)
    print("AI tasarım özeti:", summary)


if __name__ == "__main__":
    main()

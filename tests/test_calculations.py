from electrical_design_tools.calculators import LoadItem, calculate_current, calculate_total_load, calculate_voltage_drop, choose_wire_size, estimate_lighting_requirement


def test_total_load() -> None:
    items = [
        LoadItem("Aydınlatma", 1500),
        LoadItem("Priz", 1200),
        LoadItem("Klima", 2200),
    ]
    assert round(calculate_total_load(items), 2) == 4900.0


def test_calculate_current() -> None:
    assert round(calculate_current(4900, 230), 2) == 21.3


def test_choose_wire_size() -> None:
    result = choose_wire_size(21.3)
    assert result["awg"] == 12


def test_voltage_drop() -> None:
    drop = calculate_voltage_drop(20, 30, 2.2)
    assert round(drop, 2) == 2.64


def test_lighting_requirement() -> None:
    result = estimate_lighting_requirement(20, 300, 1200)
    assert round(result["lamp_quantity"], 2) == 5.0

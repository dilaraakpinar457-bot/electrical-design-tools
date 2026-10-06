# electrical-design-tools

Elektrik tasarım, kablo seçimi, aydınlatma hesabı ve yükleme cetveli için Python tabanlı yardımcı araçlar içerir.

## Özellikler

- Kablo kesiti seçimi (AWG ve yaklaşık uygunluk)
- Gerilim düşümü hesaplama
- Aydınlatma hesabı
- Toplam yük ve akım hesaplama
- Elektrik tasarım önerisi üretme
- Python CLI ve örnek kullanım

## Proje yapısı

```text
.
├── README.md
├── pyproject.toml
├── requirements.txt
├── electrical_design_tools/
│   ├── __init__.py
│   ├── __main__.py
│   ├── calculators.py
│   └── ai_assistant.py
├── examples/
│   └── basic_design.py
└── tests/
    └── test_calculations.py
```

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Kullanım

### CLI

```bash
python -m electrical_design_tools --help
```

### Python

```python
from electrical_design_tools.calculators import (
    LoadItem,
    calculate_total_load,
    choose_wire_size,
    calculate_voltage_drop,
    estimate_lighting_requirement,
)

items = [
    LoadItem("Aydınlatma", 1500),
    LoadItem("Priz", 1200),
    LoadItem("Klima", 2200),
]

print(calculate_total_load(items))
print(choose_wire_size(20))
print(calculate_voltage_drop(230, 15, 30, 2.2))
print(estimate_lighting_requirement(20, 300, 1200))
```

## Geliştirme hedefleri

- IEC/NEC uyumlu gelişmiş seçim algoritmaları
- Excel ve CSV export imkanı
- Çoklu odalı bina tasarım özeti
- Yapay zeka destekli öneri motoru

## Not

Bu araç, tasarım standartlarını doğrulayan profesyonel mühendislik kontrolünün yerini tutmaz. Son kararlar yerel yönetmelik ve uzman denetim ile birlikte değerlendirilmelidir.

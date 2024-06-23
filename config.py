class Config:
    DATABASE_URL = "sqlite:///./hospital.db"
    INITIAL_RESOURCES = [
        {"id": "intake", "value": 4},
        {"id": "er", "value": 9},
        {"id": "surgery", "value": 5},
        {"id": "nursing_a", "value": 30},
        {"id": "nursing_b", "value": 60},
    ]
    RESOURCE_REQUIREMENTS = {
        'A1': {'intake': 1, 'nursing_a': 1},
        'A2': {'intake': 1, 'surgery': 1, 'nursing_a': 1},
        'A3': {'intake': 1, 'surgery': 1, 'nursing_a': 1},
        'A4': {'intake': 1, 'surgery': 1, 'nursing_a': 1},
        'B1': {'intake': 1, 'nursing_b': 1},
        'B2': {'intake': 1, 'nursing_b': 1},
        'B3': {'intake': 1, 'surgery': 1, 'nursing_b': 1},
        'B4': {'intake': 1, 'surgery': 1, 'nursing_b': 1},
        'EM': {'er': 1, 'surgery': 1, 'nursing_a_or_b': 1}
    }

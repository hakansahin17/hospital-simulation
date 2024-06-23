class Config:
    DATABASE_URL = "sqlite:///./hospital.db"
    INITIAL_RESOURCES = [
        {"id": "intake", "value": 4},
        {"id": "er", "value": 9},
        {"id": "surgery", "value": 5},
        {"id": "nursing_a", "value": 30},
        {"id": "nursing_b", "value": 60},
    ]

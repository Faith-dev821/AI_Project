import os
from typing import Dict, Any

class Config:
    EMOTION_THRESHOLDS = {
        'low': 0.2,
        'medium': 0.5,
        'high': 0.8,
        'critical': 0.95
    }
    
    VOLATILITY_THRESHOLD = 0.3
    
    SAFETY_BOUNDARIES = {
        'emotion_intensity': 0.9,
        'volatility': 0.4,
        'conflict_count': 3,
        'deadline_urgency': 0.85,
        'suicide_risk': 0.7
    }
    
    EGG_TRIGGERS = {
        'crisis_intervention': {'emotion_intensity': 0.9, 'volatility': 0.35},
        'breathing_guide': {'emotion_intensity': 0.7, 'volatility': 0.25},
        'time_management': {'deadline_pressure': 0.7},
        'workplace_boundary': {'conflict_count': 2},
        'motivation': {'low_mood_duration': 3},
        'distraction': {'anxiety_level': 0.6},
        'celebration': {'positive_trend': 0.4},
        'sleep_advice': {'fatigue_level': 0.7}
    }
    
    STYLE_COEFFICIENTS = {
        'gentle': 0.7,
        'sarcastic': 0.3,
        'mixed': 0.5
    }
    
    CONTEXT_WINDOW_SIZE = 10
    HISTORY_RETENTION_DAYS = 30
    
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models')
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        return getattr(cls, key, default)
    
    @classmethod
    def update(cls, updates: Dict[str, Any]) -> None:
        for key, value in updates.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
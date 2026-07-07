import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from collections import deque

class EmotionEntry:
    def __init__(self, emotion_type: str, intensity: float, confidence: float, timestamp: datetime = None):
        self.emotion_type = emotion_type
        self.intensity = intensity
        self.confidence = confidence
        self.timestamp = timestamp or datetime.now()

class EmotionTracker:
    EMOTION_TYPES = ['happy', 'sad', 'angry', 'anxious', 'neutral', 'surprised', 'disgusted', 'fearful']
    
    def __init__(self, window_size: int = 10, decay_factor: float = 0.9):
        self.emotion_history = deque(maxlen=window_size)
        self.decay_factor = decay_factor
        self.current_emotion = None
        self.trend = 'stable'
        self.volatility = 0.0
        self.conflict_count = 0
        
    def add_emotion(self, emotion_type: str, intensity: float, confidence: float = 0.85) -> None:
        if emotion_type not in self.EMOTION_TYPES:
            emotion_type = 'neutral'
        
        intensity = max(0.0, min(1.0, intensity))
        self.emotion_history.append(EmotionEntry(emotion_type, intensity, confidence))
        self._update_state()
    
    def _update_state(self) -> None:
        if len(self.emotion_history) < 2:
            self.current_emotion = self.emotion_history[-1] if self.emotion_history else None
            return
        
        recent = list(self.emotion_history)[-3:] if len(self.emotion_history) >= 3 else list(self.emotion_history)
        recent_intensities = [e.intensity for e in recent]
        
        self.volatility = np.std(recent_intensities) if len(recent_intensities) > 1 else 0.0
        
        weights = [self.decay_factor ** i for i in range(len(recent))][::-1]
        weighted_avg = np.average(recent_intensities, weights=weights)
        
        prev_entries = list(self.emotion_history)[:-len(recent)]
        if prev_entries:
            prev_intensities = [e.intensity for e in prev_entries]
            prev_avg = np.mean(prev_intensities)
            
            if weighted_avg > prev_avg + 0.1:
                self.trend = 'rising'
            elif weighted_avg < prev_avg - 0.1:
                self.trend = 'falling'
            else:
                self.trend = 'stable'
        else:
            self.trend = 'stable'
        
        self.current_emotion = EmotionEntry(
            recent[-1].emotion_type,
            weighted_avg,
            recent[-1].confidence
        )
    
    def get_emotion_trend(self) -> str:
        return self.trend
    
    def get_emotion_intensity(self) -> float:
        return self.current_emotion.intensity if self.current_emotion else 0.0
    
    def get_volatility(self) -> float:
        return self.volatility
    
    def detect_emotion_inconsistency(self) -> bool:
        if len(self.emotion_history) < 3:
            return False
        
        history_list = list(self.emotion_history)
        emotions = [e.emotion_type for e in history_list[-3:]]
        return len(set(emotions)) >= 3
    
    def is_crisis_indicator(self, threshold: float = 0.9) -> bool:
        if not self.current_emotion:
            return False
        
        return (self.trend == 'rising' and 
                self.volatility > 0.3 and 
                self.detect_emotion_inconsistency() and
                self.current_emotion.intensity > threshold)
    
    def detect_gradual_change(self, min_duration: int = 3, threshold: float = 0.2) -> Optional[str]:
        if len(self.emotion_history) < min_duration:
            return None
        
        first_intensity = self.emotion_history[0].intensity
        last_intensity = self.current_emotion.intensity
        change = last_intensity - first_intensity
        
        if change > threshold:
            return 'gradual_increase'
        elif change < -threshold:
            return 'gradual_decrease'
        return None
    
    def check_safety_boundary(self, boundaries: Dict[str, float]) -> List[str]:
        breaches = []
        
        if self.current_emotion and self.current_emotion.intensity > boundaries.get('emotion_intensity', 0.9):
            breaches.append('emotion_intensity')
        
        if self.volatility > boundaries.get('volatility', 0.4):
            breaches.append('volatility')
        
        if self.conflict_count >= boundaries.get('conflict_count', 3):
            breaches.append('conflict_count')
        
        return breaches
    
    def increment_conflict(self) -> None:
        self.conflict_count += 1
    
    def reset_conflict_count(self) -> None:
        self.conflict_count = 0
    
    def get_history(self) -> List[Dict]:
        return [{
            'emotion_type': e.emotion_type,
            'intensity': e.intensity,
            'confidence': e.confidence,
            'timestamp': e.timestamp.isoformat()
        } for e in self.emotion_history]
    
    def get_summary(self) -> Dict:
        return {
            'current_emotion': self.current_emotion.emotion_type if self.current_emotion else None,
            'current_intensity': self.get_emotion_intensity(),
            'trend': self.get_emotion_trend(),
            'volatility': self.get_volatility(),
            'is_inconsistent': self.detect_emotion_inconsistency(),
            'is_crisis': self.is_crisis_indicator(),
            'conflict_count': self.conflict_count
        }
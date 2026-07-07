from typing import Dict, Optional, List
from datetime import datetime
import json
import os

from .l1_emotion_tracker import EmotionTracker
from .l2_context_encoder import ContextEncoder
from .l3_user_profile import UserProfile
from .decision_engine import DecisionEngine

class MentalModelSystem:
    def __init__(self, user_id: str, config: Dict = None, data_path: str = None):
        self.user_id = user_id
        self.config = config or {}
        self.data_path = data_path
        
        self.emotion_tracker = EmotionTracker(
            window_size=config.get('CONTEXT_WINDOW_SIZE', 10),
            decay_factor=0.9
        )
        self.context_encoder = ContextEncoder()
        self.user_profile = UserProfile(user_id, data_path)
        self.decision_engine = DecisionEngine(config)
        
        self.conversation_history = []
        self.last_process_time = None
        
    def process_input(self, user_input: str, emotion_type: str = 'neutral', emotion_intensity: float = 0.5, 
                      emotion_confidence: float = 0.85) -> Dict:
        timestamp = datetime.now()
        
        self.emotion_tracker.add_emotion(emotion_type, emotion_intensity, emotion_confidence)
        self.context_encoder.add_conversation(user_input, timestamp)
        self.user_profile.update_emotion(emotion_type, emotion_intensity)
        
        detected_stressors = self.context_encoder.detect_stressors(user_input)
        for stressor, _ in detected_stressors:
            self.user_profile.update_stressor(stressor)
        
        decision = self.decision_engine.make_decision(
            self.emotion_tracker,
            self.context_encoder,
            self.user_profile
        )
        
        self.conversation_history.append({
            'user_input': user_input,
            'emotion_type': emotion_type,
            'emotion_intensity': emotion_intensity,
            'timestamp': timestamp.isoformat(),
            'decision': decision
        })
        
        self.last_process_time = timestamp
        
        return decision
    
    def get_emotion_trend(self) -> str:
        return self.emotion_tracker.get_emotion_trend()
    
    def get_emotion_intensity(self) -> float:
        return self.emotion_tracker.get_emotion_intensity()
    
    def get_volatility(self) -> float:
        return self.emotion_tracker.get_volatility()
    
    def detect_gradual_change(self) -> Optional[str]:
        return self.emotion_tracker.detect_gradual_change()
    
    def check_safety_boundary(self) -> List[str]:
        return self.emotion_tracker.check_safety_boundary(self.config.get('SAFETY_BOUNDARIES', {}))
    
    def is_crisis(self) -> bool:
        return self.emotion_tracker.is_crisis_indicator()
    
    def get_user_profile(self) -> Dict:
        return self.user_profile.get_profile_summary()
    
    def get_context_summary(self) -> Dict:
        return self.context_encoder.get_context_summary()
    
    def get_system_summary(self) -> Dict:
        return {
            'user_id': self.user_id,
            'emotion_summary': self.emotion_tracker.get_summary(),
            'context_summary': self.context_encoder.get_context_summary(),
            'profile_summary': self.user_profile.get_profile_summary(),
            'conversation_count': len(self.conversation_history),
            'last_process_time': self.last_process_time.isoformat() if self.last_process_time else None,
            'is_crisis': self.is_crisis(),
            'safety_breaches': self.check_safety_boundary()
        }
    
    def update_style_preference(self, style: str, feedback_score: float) -> None:
        self.user_profile.update_style_preference(style, feedback_score)
    
    def reset_emotion_tracker(self) -> None:
        self.emotion_tracker = EmotionTracker(
            window_size=self.config.get('CONTEXT_WINDOW_SIZE', 10),
            decay_factor=0.9
        )
    
    def save_state(self, filepath: str = None) -> None:
        if not filepath:
            filepath = os.path.join(self.data_path or '.', f'{self.user_id}_state.json')
        
        state = {
            'user_id': self.user_id,
            'emotion_history': self.emotion_tracker.get_history(),
            'conversation_history': self.conversation_history,
            'last_process_time': self.last_process_time.isoformat() if self.last_process_time else None,
            'saved_at': datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def load_state(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            self.conversation_history = state.get('conversation_history', [])
            self.last_process_time = datetime.fromisoformat(state['last_process_time']) if state.get('last_process_time') else None
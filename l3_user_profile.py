import json
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class UserProfile:
    STYLE_TYPES = ['gentle', 'sarcastic', 'mixed']
    
    def __init__(self, user_id: str, data_path: str = None):
        self.user_id = user_id
        self.data_path = data_path
        
        self.emotion_distribution = defaultdict(int)
        self.stressor_frequency = defaultdict(int)
        self.preferred_style = 'mixed'
        self.style_scores = {'gentle': 0.5, 'sarcastic': 0.5}
        
        self.total_interactions = 0
        self.positive_interactions = 0
        self.negative_interactions = 0
        
        self.last_update = None
        self.low_mood_duration = 0
        
        self._load_profile()
    
    def _load_profile(self) -> None:
        if self.data_path:
            profile_file = os.path.join(self.data_path, f'{self.user_id}_profile.json')
            if os.path.exists(profile_file):
                try:
                    with open(profile_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.emotion_distribution = defaultdict(int, data.get('emotion_distribution', {}))
                        self.stressor_frequency = defaultdict(int, data.get('stressor_frequency', {}))
                        self.preferred_style = data.get('preferred_style', 'mixed')
                        self.style_scores = data.get('style_scores', {'gentle': 0.5, 'sarcastic': 0.5})
                        self.total_interactions = data.get('total_interactions', 0)
                        self.positive_interactions = data.get('positive_interactions', 0)
                        self.negative_interactions = data.get('negative_interactions', 0)
                        self.last_update = datetime.fromisoformat(data['last_update']) if data.get('last_update') else None
                except Exception:
                    pass
    
    def _save_profile(self) -> None:
        if self.data_path:
            os.makedirs(self.data_path, exist_ok=True)
            profile_file = os.path.join(self.data_path, f'{self.user_id}_profile.json')
            data = {
                'emotion_distribution': dict(self.emotion_distribution),
                'stressor_frequency': dict(self.stressor_frequency),
                'preferred_style': self.preferred_style,
                'style_scores': self.style_scores,
                'total_interactions': self.total_interactions,
                'positive_interactions': self.positive_interactions,
                'negative_interactions': self.negative_interactions,
                'last_update': datetime.now().isoformat()
            }
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    def update_emotion(self, emotion_type: str, intensity: float) -> None:
        self.emotion_distribution[emotion_type] += 1
        self.total_interactions += 1
        
        if emotion_type in ['happy', 'surprised']:
            self.positive_interactions += 1
        elif emotion_type in ['sad', 'angry', 'anxious', 'fearful']:
            self.negative_interactions += 1
        
        if intensity > 0.7 and emotion_type in ['sad', 'anxious']:
            self.low_mood_duration += 1
        else:
            self.low_mood_duration = 0
        
        self.last_update = datetime.now()
        self._save_profile()
    
    def update_stressor(self, stressor: str) -> None:
        self.stressor_frequency[stressor] += 1
        self._save_profile()
    
    def update_style_preference(self, style: str, feedback_score: float) -> None:
        if style in self.STYLE_TYPES:
            current_score = self.style_scores.get(style, 0.5)
            self.style_scores[style] = (current_score + feedback_score) / 2
            
            if self.style_scores['gentle'] > self.style_scores['sarcastic'] + 0.2:
                self.preferred_style = 'gentle'
            elif self.style_scores['sarcastic'] > self.style_scores['gentle'] + 0.2:
                self.preferred_style = 'sarcastic'
            else:
                self.preferred_style = 'mixed'
            
            self._save_profile()
    
    def get_emotion_statistics(self) -> Dict[str, float]:
        total = sum(self.emotion_distribution.values())
        if total == 0:
            return {}
        return {emotion: count / total for emotion, count in self.emotion_distribution.items()}
    
    def get_top_stressors(self, n: int = 3) -> List[str]:
        sorted_stressors = sorted(self.stressor_frequency.items(), key=lambda x: -x[1])
        return [s[0] for s in sorted_stressors[:n]]
    
    def get_preferred_style(self) -> str:
        return self.preferred_style
    
    def get_style_coefficient(self) -> float:
        return self.style_scores.get(self.preferred_style, 0.5)
    
    def get_mood_trend(self) -> str:
        if self.total_interactions < 5:
            return 'insufficient_data'
        
        ratio = self.positive_interactions / self.total_interactions
        if ratio > 0.6:
            return 'positive'
        elif ratio < 0.4:
            return 'negative'
        else:
            return 'neutral'
    
    def get_profile_summary(self) -> Dict:
        return {
            'user_id': self.user_id,
            'total_interactions': self.total_interactions,
            'mood_trend': self.get_mood_trend(),
            'emotion_statistics': self.get_emotion_statistics(),
            'top_stressors': self.get_top_stressors(),
            'preferred_style': self.get_preferred_style(),
            'style_coefficient': self.get_style_coefficient(),
            'low_mood_duration': self.low_mood_duration,
            'last_update': self.last_update.isoformat() if self.last_update else None
        }
    
    def get_positive_trend(self) -> float:
        if self.total_interactions == 0:
            return 0.0
        return self.positive_interactions / self.total_interactions
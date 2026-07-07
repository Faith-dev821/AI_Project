import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from collections import Counter

class ContextEncoder:
    STRESSORS = ['deadline', 'conflict', 'recognition', 'overload']
    TOPICS = ['work_stress', 'interpersonal_conflict', 'self_growth', 'daily_rant', 'seeking_advice']
    SPECIAL_PERIODS = ['monday_blues', 'exam_season', 'morning_rush', 'weekend', 'holiday']
    
    KEYWORDS = {
        'deadline': ['deadline', 'due', '截止', '到期', '赶工', '加班'],
        'conflict': ['冲突', '吵架', '矛盾', '不爽', '讨厌', '争执'],
        'recognition': ['表扬', '认可', '奖励', '升职', '加薪', '肯定'],
        'overload': ['忙', '累', '疲惫', '超负荷', '太多', '喘不过气'],
        'work_stress': ['工作', '项目', '任务', '老板', '同事', '职场'],
        'interpersonal_conflict': ['同事', '朋友', '家人', '沟通', '误会', '争吵'],
        'self_growth': ['学习', '成长', '进步', '提升', '目标', '计划'],
        'daily_rant': ['吐槽', '抱怨', '烦', '郁闷', '无聊', '没意思'],
        'seeking_advice': ['怎么办', '建议', '如何', '求助', '帮忙', '指导']
    }
    
    def __init__(self):
        self.conversation_history = []
        self.stressor_scores = {s: 0.0 for s in self.STRESSORS}
        self.topic_scores = {t: 0.0 for t in self.TOPICS}
        self.current_period = None
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        scores = {}
        
        for stressor, keywords in self.KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in text.lower())
            scores[stressor] = min(count / 3, 1.0)
        
        return scores
    
    def detect_stressors(self, text: str) -> List[Tuple[str, float]]:
        scores = self.analyze_text(text)
        detected = []
        
        for stressor in self.STRESSORS:
            score = scores.get(stressor, 0.0)
            if score > 0.3:
                detected.append((stressor, score))
        
        self.stressor_scores = {s: max(self.stressor_scores[s], scores.get(s, 0.0)) for s in self.STRESSORS}
        
        return detected
    
    def classify_topic(self, text: str) -> Tuple[str, float]:
        scores = self.analyze_text(text)
        topic_scores = {t: scores.get(t, 0.0) for t in self.TOPICS}
        
        max_topic = max(topic_scores, key=topic_scores.get)
        max_score = topic_scores[max_topic]
        
        self.topic_scores = {t: (self.topic_scores[t] + topic_scores[t]) / 2 for t in self.TOPICS}
        
        return max_topic, max_score
    
    def detect_special_period(self) -> Optional[str]:
        now = datetime.now()
        
        if now.weekday() == 0:
            hour = now.hour
            if 6 <= hour <= 10:
                return 'monday_blues'
        
        month = now.month
        if month in [1, 6, 12]:
            return 'exam_season'
        
        hour = now.hour
        if 7 <= hour <= 9:
            return 'morning_rush'
        
        if now.weekday() in [5, 6]:
            return 'weekend'
        
        return None
    
    def add_conversation(self, user_input: str, timestamp: datetime = None) -> None:
        self.conversation_history.append({
            'text': user_input,
            'timestamp': timestamp or datetime.now(),
            'stressors': self.detect_stressors(user_input),
            'topic': self.classify_topic(user_input)
        })
        
        self.current_period = self.detect_special_period()
    
    def get_stressor_summary(self) -> Dict[str, float]:
        return dict(self.stressor_scores)
    
    def get_topic_summary(self) -> Dict[str, float]:
        return dict(self.topic_scores)
    
    def get_context_summary(self) -> Dict:
        return {
            'detected_stressors': [(s, score) for s, score in self.stressor_scores.items() if score > 0.3],
            'dominant_topic': max(self.topic_scores, key=self.topic_scores.get),
            'topic_confidence': self.topic_scores[max(self.topic_scores, key=self.topic_scores.get)],
            'special_period': self.current_period,
            'conversation_count': len(self.conversation_history)
        }
    
    def get_deadline_pressure(self) -> float:
        return self.stressor_scores.get('deadline', 0.0)
    
    def has_high_conflict(self) -> bool:
        return self.stressor_scores.get('conflict', 0.0) > 0.5
    
    def get_anxiety_level(self) -> float:
        stress_sum = sum(self.stressor_scores[s] for s in ['deadline', 'overload'])
        return min(stress_sum / 2, 1.0)
    
    def get_fatigue_level(self) -> float:
        return self.stressor_scores.get('overload', 0.0)
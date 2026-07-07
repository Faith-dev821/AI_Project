from typing import List, Dict, Optional, Tuple
from .l1_emotion_tracker import EmotionTracker
from .l2_context_encoder import ContextEncoder
from .l3_user_profile import UserProfile

class DecisionEngine:
    EGG_TYPES = [
        'crisis_intervention',
        'breathing_guide',
        'time_management',
        'workplace_boundary',
        'motivation',
        'distraction',
        'celebration',
        'sleep_advice'
    ]
    
    def __init__(self, config: Dict):
        self.config = config
        self.safety_boundaries = config.get('SAFETY_BOUNDARIES', {})
        self.egg_triggers = config.get('EGG_TRIGGERS', {})
        self.style_coefficients = config.get('STYLE_COEFFICIENTS', {})
        
        self.active_eggs = []
        self.last_egg_time = {}
    
    def evaluate_emotion_rules(self, emotion_tracker: EmotionTracker) -> List[str]:
        triggers = []
        summary = emotion_tracker.get_summary()
        
        if summary['is_crisis']:
            triggers.append('crisis_intervention')
        
        if summary['current_intensity'] > 0.7 and summary['volatility'] > 0.25:
            triggers.append('breathing_guide')
        
        if emotion_tracker.detect_gradual_change() == 'gradual_increase' and summary['current_intensity'] > 0.6:
            triggers.append('breathing_guide')
        
        return triggers
    
    def evaluate_context_rules(self, context_encoder: ContextEncoder) -> List[str]:
        triggers = []
        
        if context_encoder.get_deadline_pressure() > 0.7:
            triggers.append('time_management')
        
        if context_encoder.has_high_conflict():
            triggers.append('workplace_boundary')
        
        if context_encoder.get_anxiety_level() > 0.6:
            triggers.append('distraction')
        
        if context_encoder.get_fatigue_level() > 0.7:
            triggers.append('sleep_advice')
        
        return triggers
    
    def evaluate_profile_rules(self, user_profile: UserProfile) -> List[str]:
        triggers = []
        
        if user_profile.low_mood_duration >= 3:
            triggers.append('motivation')
        
        if user_profile.get_positive_trend() > 0.4:
            triggers.append('celebration')
        
        return triggers
    
    def check_safety_boundaries(self, emotion_tracker: EmotionTracker) -> List[str]:
        return emotion_tracker.check_safety_boundary(self.safety_boundaries)
    
    def select_egg(self, triggers: List[str]) -> Optional[str]:
        priority_order = [
            'crisis_intervention',
            'breathing_guide',
            'time_management',
            'workplace_boundary',
            'motivation',
            'distraction',
            'sleep_advice',
            'celebration'
        ]
        
        for egg_type in priority_order:
            if egg_type in triggers:
                return egg_type
        
        return None
    
    def get_response_template(self, egg_type: str, style: str = 'mixed') -> Dict:
        templates = {
            'crisis_intervention': {
                'gentle': '我很担心你，现在感觉怎么样？如果你需要帮助，我可以陪你聊一会儿，或者帮你联系专业人士。',
                'sarcastic': '喂，看起来你状态不太对。别硬撑了，要么说出来，要么去寻求专业帮助。',
                'mixed': '我注意到你现在情绪比较激动，需要聊一聊吗？如果需要专业帮助，我也可以提供一些资源。'
            },
            'breathing_guide': {
                'gentle': '让我们一起做个深呼吸吧。吸气4秒，屏住4秒，呼气6秒。重复几次，让自己慢慢平静下来。',
                'sarcastic': '嘿，先别激动。深呼吸会吗？吸进去，呼出来，别把自己憋坏了。',
                'mixed': '试试深呼吸吧，吸气...呼气...让身体放松下来，事情会慢慢好起来的。'
            },
            'time_management': {
                'gentle': '看起来你有很多事情要处理，我们可以一起梳理一下优先级。先列出最重要的任务，一步一步来。',
                'sarcastic': '截止日期要到了？早干嘛去了？不过现在开始规划还不算晚，先把事情排个序。',
                'mixed': 'deadline压力很大吧？我们可以一起制定一个简单的时间管理计划，把大任务拆分成小步骤。'
            },
            'workplace_boundary': {
                'gentle': '职场中的人际关系确实很复杂。记得保护好自己的边界，有时候学会说"不"也很重要。',
                'sarcastic': '又跟同事杠上了？职场如战场，但你得有自己的底线，别让人随便欺负。',
                'mixed': '人际冲突确实让人头疼。建议你先冷静下来，理清事实，然后设定好自己的边界。'
            },
            'motivation': {
                'gentle': '我知道最近可能有些难，但你已经很棒了。小小的进步也是进步，相信自己，慢慢来。',
                'sarcastic': '怎么，又丧了？人生嘛，总有起起落落。不过你还在坚持，这就比很多人强了。',
                'mixed': '低谷期谁都会经历，重要的是别放弃。你已经走了这么远，再坚持一下，光明就在前方。'
            },
            'distraction': {
                'gentle': '要不要暂时放下烦恼，做点让自己开心的事情？听听音乐、看看风景，或者做点深呼吸。',
                'sarcastic': '别想那些烦心事了，找点乐子吧。人生苦短，别跟自己过不去。',
                'mixed': '焦虑的时候，试试转移注意力。做点喜欢的事情，让大脑暂时休息一下。'
            },
            'celebration': {
                'gentle': '太棒了！你做得很好，值得庆祝一下。继续保持这份积极的心态！',
                'sarcastic': '哟，今天心情不错嘛。继续保持，别骄傲哦。',
                'mixed': '看到你状态变好真开心！继续加油，你值得拥有这份好心情！'
            },
            'sleep_advice': {
                'gentle': '看起来你有点疲惫，要注意休息哦。保证充足的睡眠对身心健康很重要。',
                'sarcastic': '累了就去睡觉，别硬撑。身体垮了，什么都干不了。',
                'mixed': '注意休息，别太累了。适当放松，才能更好地应对挑战。'
            }
        }
        
        return templates.get(egg_type, {}).get(style, templates[egg_type].get('mixed', ''))
    
    def make_decision(self, emotion_tracker: EmotionTracker, context_encoder: ContextEncoder, user_profile: UserProfile) -> Dict:
        emotion_triggers = self.evaluate_emotion_rules(emotion_tracker)
        context_triggers = self.evaluate_context_rules(context_encoder)
        profile_triggers = self.evaluate_profile_rules(user_profile)
        
        all_triggers = list(set(emotion_triggers + context_triggers + profile_triggers))
        
        safety_breaches = self.check_safety_boundaries(emotion_tracker)
        
        selected_egg = self.select_egg(all_triggers)
        
        style = user_profile.get_preferred_style()
        response = self.get_response_template(selected_egg, style) if selected_egg else None
        
        return {
            'selected_egg': selected_egg,
            'response': response,
            'triggers': all_triggers,
            'safety_breaches': safety_breaches,
            'style': style,
            'emotion_summary': emotion_tracker.get_summary(),
            'context_summary': context_encoder.get_context_summary(),
            'profile_summary': user_profile.get_profile_summary()
        }
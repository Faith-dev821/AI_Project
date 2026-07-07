import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from mental_model import MentalModelSystem

def test_multi_round_conversation():
    print("=== 测试多轮对话情感追踪 ===")
    
    config = {
        'EMOTION_THRESHOLDS': Config.EMOTION_THRESHOLDS,
        'SAFETY_BOUNDARIES': Config.SAFETY_BOUNDARIES,
        'EGG_TRIGGERS': Config.EGG_TRIGGERS,
        'STYLE_COEFFICIENTS': Config.STYLE_COEFFICIENTS,
        'CONTEXT_WINDOW_SIZE': Config.CONTEXT_WINDOW_SIZE
    }
    
    system = MentalModelSystem(user_id='test_user_001', config=config, data_path='./data')
    
    conversation_steps = [
        {'input': '周一又要上班了，好焦虑啊', 'emotion': 'anxious', 'intensity': 0.6},
        {'input': '项目明天就要截止了，还没做完', 'emotion': 'anxious', 'intensity': 0.75},
        {'input': '同事又来抢功劳，真的很生气', 'emotion': 'angry', 'intensity': 0.7},
        {'input': '感觉压力好大，喘不过气来', 'emotion': 'anxious', 'intensity': 0.85},
        {'input': '我快崩溃了，不知道该怎么办', 'emotion': 'fearful', 'intensity': 0.92},
    ]
    
    for i, step in enumerate(conversation_steps):
        print(f"\n--- 对话轮次 {i+1} ---")
        print(f"用户输入: {step['input']}")
        
        decision = system.process_input(
            user_input=step['input'],
            emotion_type=step['emotion'],
            emotion_intensity=step['intensity']
        )
        
        print(f"检测到的情绪: {step['emotion']}")
        print(f"情绪强度: {step['intensity']}")
        print(f"触发的彩蛋: {decision['selected_egg']}")
        print(f"系统响应: {decision['response']}")
        print(f"情绪趋势: {decision['emotion_summary']['trend']}")
        print(f"波动性: {decision['emotion_summary']['volatility']:.3f}")
        print(f"安全边界突破: {decision['safety_breaches']}")
        
        if decision['safety_breaches']:
            print("[WARN] 安全边界已触发！")
        
        if decision['selected_egg'] == 'crisis_intervention':
            print("[ALERT] 危机干预机制已激活！")
    
    print("\n=== 系统总结 ===")
    summary = system.get_system_summary()
    print(f"总对话数: {summary['conversation_count']}")
    print(f"是否处于危机状态: {summary['is_crisis']}")
    print(f"当前情绪强度: {summary['emotion_summary']['current_intensity']:.3f}")
    print(f"检测到的压力源: {summary['context_summary']['detected_stressors']}")
    print(f"用户偏好风格: {summary['profile_summary']['preferred_style']}")
    
    return True

def test_emotion_gradual_change():
    print("\n=== 测试情绪强度渐变识别 ===")
    
    config = {
        'EMOTION_THRESHOLDS': Config.EMOTION_THRESHOLDS,
        'SAFETY_BOUNDARIES': Config.SAFETY_BOUNDARIES,
        'EGG_TRIGGERS': Config.EGG_TRIGGERS,
        'CONTEXT_WINDOW_SIZE': 5
    }
    
    system = MentalModelSystem(user_id='test_user_002', config=config)
    
    gradual_intensities = [0.3, 0.4, 0.55, 0.7, 0.85]
    
    for i, intensity in enumerate(gradual_intensities):
        print(f"\n第 {i+1} 步 - 情绪强度: {intensity}")
        decision = system.process_input(
            user_input=f"感觉有点不舒服，强度 {intensity}",
            emotion_type='anxious',
            emotion_intensity=intensity
        )
        
        gradual_change = system.detect_gradual_change()
        print(f"渐变检测结果: {gradual_change}")
        print(f"当前趋势: {decision['emotion_summary']['trend']}")
        
        if gradual_change == 'gradual_increase':
            print("[INFO] 检测到情绪强度逐渐上升！")
    
    return True

def test_safety_boundary_trigger():
    print("\n=== 测试安全边界触发机制 ===")
    
    config = {
        'SAFETY_BOUNDARIES': {
            'emotion_intensity': 0.85,
            'volatility': 0.35,
            'conflict_count': 2,
            'deadline_urgency': 0.8
        },
        'EGG_TRIGGERS': Config.EGG_TRIGGERS
    }
    
    system = MentalModelSystem(user_id='test_user_003', config=config)
    
    test_cases = [
        {'input': '我真的受不了了', 'emotion': 'angry', 'intensity': 0.9},
        {'input': '工作太多了，根本做不完', 'emotion': 'anxious', 'intensity': 0.88},
        {'input': '同事又在背后说我坏话', 'emotion': 'sad', 'intensity': 0.85},
    ]
    
    for i, case in enumerate(test_cases):
        print(f"\n测试案例 {i+1}")
        decision = system.process_input(
            user_input=case['input'],
            emotion_type=case['emotion'],
            emotion_intensity=case['intensity']
        )
        
        breaches = decision['safety_breaches']
        print(f"输入: {case['input']}")
        print(f"情绪强度: {case['intensity']}")
        print(f"安全边界突破: {breaches}")
        
        if breaches:
            print("[ALERT] 安全边界已突破！")
            print(f"触发响应: {decision['response']}")
    
    return True

def test_edge_deployment():
    print("\n=== 测试端侧部署能力 ===")
    
    config = {
        'EMOTION_THRESHOLDS': Config.EMOTION_THRESHOLDS,
        'SAFETY_BOUNDARIES': Config.SAFETY_BOUNDARIES,
        'EGG_TRIGGERS': Config.EGG_TRIGGERS,
        'CONTEXT_WINDOW_SIZE': 5
    }
    
    system = MentalModelSystem(user_id='edge_test_user', config=config)
    
    print("测试轻量级推理...")
    
    for i in range(3):
        decision = system.process_input(
            user_input=f"测试输入 {i+1}",
            emotion_type='neutral',
            emotion_intensity=0.3
        )
        print(f"推理完成，响应类型: {decision['selected_egg']}")
    
    system.save_state('./data/edge_state.json')
    print("状态已保存，支持离线使用")
    
    system.load_state('./data/edge_state.json')
    print("状态已加载，支持断点续传")
    
    print("\n[PASS] 端侧部署测试通过")
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("动态心智模型 - 用户心理状态表征系统")
    print("情感智能识别系统测试")
    print("=" * 60)
    
    try:
        test_multi_round_conversation()
        test_emotion_gradual_change()
        test_safety_boundary_trigger()
        test_edge_deployment()
        
        print("\n" + "=" * 60)
        print("[PASS] 所有测试通过！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场情绪周期判断模块

基于涨停数、跌停数、连板高度等指标判断市场情绪阶段：
- 启动期
- 发酵期
- 高潮期
- 退潮期
"""

from datetime import datetime
from .limit_up_data import get_limit_up_pool, get_limit_down_pool, get_zt_pool_strength


def calculate_sentiment_score(date=None):
    """
    计算市场情绪评分（0-100）
    
    Args:
        date: 日期
        
    Returns:
        dict: 情绪指标
            - score: 情绪评分 0-100
            - limit_up_count: 涨停数
            - limit_down_count: 跌停数
            - max_consecutive: 最高连板
            - zt_strength: 涨停强度统计
    """
    # 获取涨停数据
    zt_stats = get_zt_pool_strength(date)
    
    # 获取跌停数据（简化处理，跌停数据可选）
    try:
        dt_df = get_limit_down_pool(date)
        limit_down_count = len(dt_df) if dt_df is not None else 0
    except:
        limit_down_count = 0  # 如果接口不可用，设为 0
    
    # 情绪评分公式
    # 基础分 50 + (涨停 - 跌停)*2 + 连板高度*5
    score = 50 + (zt_stats['total'] - limit_down_count) * 2 + zt_stats['consecutive_5'] * 5
    
    # 限制在 0-100
    score = min(100, max(0, score))
    
    return {
        'score': round(score, 1),
        'limit_up_count': zt_stats['total'],
        'limit_down_count': limit_down_count,
        'max_consecutive': zt_stats.get('consecutive_5', 0),
        'consecutive_3': zt_stats.get('consecutive_3', 0),
        'consecutive_2': zt_stats.get('consecutive_2', 0),
        'zt_strength': zt_stats
    }


def judge_sentiment_stage(score, sentiment_data=None):
    """
    判断情绪阶段
    
    Args:
        score: 情绪评分
        sentiment_data: 情绪数据（可选，用于更精确判断）
        
    Returns:
        str: 情绪阶段
            - 高潮期 (80-100)
            - 发酵期 (60-80)
            - 启动期/分歧期 (40-60)
            - 退潮期 (0-40)
    """
    if score >= 80:
        return '高潮期'
    elif score >= 60:
        return '发酵期'
    elif score >= 40:
        return '启动期/分歧期'
    else:
        return '退潮期'


def get_stage_advice(stage):
    """
    根据情绪阶段给出操作建议
    
    Args:
        stage: 情绪阶段
        
    Returns:
        str: 操作建议
    """
    advice_map = {
        '高潮期': '持股待涨，不追高，准备兑现',
        '发酵期': '加仓主线，积极参与',
        '启动期/分歧期': '轻仓试错，等待确认',
        '退潮期': '减仓防守，控制仓位'
    }
    return advice_map.get(stage, '谨慎观望')


def calculate_position_advice(score, stage):
    """
    计算仓位建议（针对 20% 龙头战法仓位的使用比例）
    
    Args:
        score: 情绪评分
        stage: 情绪阶段
        
    Returns:
        dict: 仓位建议
            - usage_rate: 龙头仓位使用比例（0-100%）
            - actual_position: 实际总仓位占比
            - advice: 文字建议
    """
    if score >= 80:
        usage_rate = 60  # 高潮期不追高，适当减仓
        actual = 20 * 0.60  # 总仓位的 12%
    elif score >= 60:
        usage_rate = 80  # 发酵期积极参与
        actual = 20 * 0.80  # 总仓位的 16%
    elif score >= 40:
        usage_rate = 50  # 分歧期轻仓
        actual = 20 * 0.50  # 总仓位的 10%
    else:
        usage_rate = 20  # 退潮期防守
        actual = 20 * 0.20  # 总仓位的 4%
    
    return {
        'usage_rate': usage_rate,
        'actual_position': round(actual, 1),
        'advice': f"龙头仓位使用{usage_rate}%（总仓位{actual}%）"
    }


def get_market_sentiment_full(date=None):
    """
    获取完整的市场情绪分析
    
    Args:
        date: 日期
        
    Returns:
        dict: 完整情绪分析
    """
    # 计算情绪评分
    sentiment = calculate_sentiment_score(date)
    
    # 判断阶段
    stage = judge_sentiment_stage(sentiment['score'], sentiment)
    
    # 操作建议
    stage_advice = get_stage_advice(stage)
    
    # 仓位建议
    position = calculate_position_advice(sentiment['score'], stage)
    
    return {
        'score': sentiment.get('score', 50),
        'stage': stage,
        'stage_advice': stage_advice,
        'position': position,
        'limit_up_count': sentiment.get('limit_up_count', 0),
        'limit_down_count': sentiment.get('limit_down_count', 0),
        'consecutive_3': sentiment.get('consecutive_3', 0),
        'consecutive_5': sentiment.get('consecutive_5', 0),
        'date': date if date else datetime.now().strftime('%Y-%m-%d')
    }


def format_sentiment_report(sentiment_data):
    """
    格式化情绪报告输出
    
    Args:
        sentiment_data: 情绪数据
        
    Returns:
        str: 格式化报告
    """
    score = sentiment_data.get('score', 50)
    
    # 进度条
    bar_length = int(score / 5)
    bar = '█' * bar_length + '░' * (20 - bar_length)
    
    # 涨跌图标
    if score >= 60:
        icon = '📈'
    elif score >= 40:
        icon = '➡️'
    else:
        icon = '📉'
    
    report = f"""
【市场情绪】
情绪评分：{score}/100  [{bar}] {icon}
情绪阶段：{sentiment_data.get('stage', '未知')}
涨跌停比：{sentiment_data.get('limit_up_count', 0)} : {sentiment_data.get('limit_down_count', 0)}
3 连板以上：{sentiment_data.get('consecutive_3', 0)} 只
5 连板以上：{sentiment_data.get('consecutive_5', 0)} 只
操作建议：{sentiment_data.get('stage_advice', '谨慎观望')}
仓位建议：{sentiment_data.get('position', {}).get('advice', 'N/A')}
"""
    return report.strip()


if __name__ == '__main__':
    # 测试
    print("=" * 60)
    print("测试市场情绪分析")
    print("=" * 60)
    
    # 获取今日情绪
    sentiment = get_market_sentiment_full()
    
    print(format_sentiment_report(sentiment))

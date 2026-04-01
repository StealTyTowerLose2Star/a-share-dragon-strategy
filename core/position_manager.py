#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仓位管理模块

根据情绪评分和持仓情况，计算：
- 总仓位使用比例
- 各等级龙头股仓位分配
- 单只股票仓位上限
"""


def calculate_position_allocation(sentiment_score, stage, leader_count=None):
    """
    计算仓位分配
    
    Args:
        sentiment_score: 情绪评分
        stage: 情绪阶段
        leader_count: 各等级龙头股数量 dict
            {'总龙头': 0, '主线龙头': 2, '板块龙头': 3, '补涨龙': 5}
        
    Returns:
        dict: 仓位分配
    """
    # 基础仓位使用比例
    if sentiment_score >= 80:
        base_rate = 60  # 高潮期
    elif sentiment_score >= 60:
        base_rate = 80  # 发酵期
    elif sentiment_score >= 40:
        base_rate = 50  # 分歧期
    else:
        base_rate = 20  # 退潮期
    
    # 总仓位（20% 的龙头战法仓位）
    total_position = 20 * base_rate / 100  # 总资金的百分比
    
    # 各等级分配比例
    if leader_count:
        # 根据实际龙头股数量调整
        total_leaders = sum(leader_count.values())
        
        if total_leaders == 0:
            # 无合适龙头，降低仓位
            allocation = {
                '总龙头': 0,
                '主线龙头': 0,
                '板块龙头': 0,
                '补涨龙': 0,
                '现金': total_position
            }
        else:
            # 按等级分配
            allocation = {}
            
            # 总龙头：单只最多 10%
            if leader_count.get('总龙头', 0) > 0:
                allocation['总龙头'] = min(total_position * 0.5, 10)
            
            # 主线龙头：单只最多 8%
            if leader_count.get('主线龙头', 0) > 0:
                allocation['主线龙头'] = min(total_position * 0.3, 8)
            
            # 板块龙头：单只最多 6%
            if leader_count.get('板块龙头', 0) > 0:
                allocation['板块龙头'] = min(total_position * 0.15, 6)
            
            # 补涨龙：单只最多 4%
            if leader_count.get('补涨龙', 0) > 0:
                allocation['补涨龙'] = min(total_position * 0.05, 4)
            
            # 现金
            allocated = sum(allocation.values())
            allocation['现金'] = total_position - allocated
    else:
        # 默认分配
        allocation = {
            '总龙头': total_position * 0.0,  # 通常无
            '主线龙头': total_position * 0.5,
            '板块龙头': total_position * 0.3,
            '补涨龙': total_position * 0.1,
            '现金': total_position * 0.1
        }
    
    return {
        'total_position': round(total_position, 1),
        'usage_rate': base_rate,
        'allocation': {k: round(v, 1) for k, v in allocation.items()}
    }


def get_single_stock_limit(level):
    """
    获取单只股票仓位上限
    
    Args:
        level: 龙头等级
        
    Returns:
        float: 仓位上限（%）
    """
    limits = {
        '总龙头': 10,
        '主线龙头': 8,
        '板块龙头': 6,
        '补涨龙': 4
    }
    return limits.get(level, 5)


def adjust_position_for_risk(position_data, risk_level='high'):
    """
    根据风险等级调整仓位
    
    Args:
        position_data: 仓位分配数据
        risk_level: 风险等级（low/medium/high）
        
    Returns:
        dict: 调整后的仓位
    """
    if risk_level == 'high':
        # 高风险：降低 50%
        factor = 0.5
    elif risk_level == 'medium':
        # 中风险：降低 20%
        factor = 0.8
    else:
        # 低风险：不调整
        factor = 1.0
    
    adjusted = {
        'total_position': position_data['total_position'] * factor,
        'usage_rate': position_data['usage_rate'] * factor,
        'allocation': {}
    }
    
    for k, v in position_data['allocation'].items():
        adjusted['allocation'][k] = v * factor
    
    # 重新计算现金
    allocated = sum(v for k, v in adjusted['allocation'].items() if k != '现金')
    adjusted['allocation']['现金'] = adjusted['total_position'] - allocated
    
    # 四舍五入
    adjusted['total_position'] = round(adjusted['total_position'], 1)
    adjusted['usage_rate'] = round(adjusted['usage_rate'], 1)
    adjusted['allocation'] = {k: round(v, 1) for k, v in adjusted['allocation'].items()}
    
    return adjusted


def format_position_report(position_data, leader_count=None):
    """
    格式化仓位报告
    
    Args:
        position_data: 仓位数据
        leader_count: 龙头股数量
        
    Returns:
        str: 格式化报告
    """
    report = f"""
【仓位建议】

总仓位架构:
  龙头战法：20%（固定配置）
  趋势策略：80%（待开发）

今日龙头战法仓位使用:
  使用比例：{position_data['usage_rate']}%
  实际仓位：{position_data['total_position']}%（总资金的{position_data['total_position']}%）

仓位分配:
"""
    
    allocation = position_data['allocation']
    if allocation.get('主线龙头', 0) > 0:
        report += f"  • 主线龙头：{allocation['主线龙头']}%\n"
    if allocation.get('板块龙头', 0) > 0:
        report += f"  • 板块龙头：{allocation['板块龙头']}%\n"
    if allocation.get('补涨龙', 0) > 0:
        report += f"  • 补涨龙：{allocation['补涨龙']}%\n"
    if allocation.get('总龙头', 0) > 0:
        report += f"  • 总龙头：{allocation['总龙头']}%\n"
    if allocation.get('现金', 0) > 0:
        report += f"  • 现金保留：{allocation['现金']}%\n"
    
    report += "\n单只股票上限:\n"
    report += "  • 总龙头：≤10%\n"
    report += "  • 主线龙头：≤8%\n"
    report += "  • 板块龙头：≤6%\n"
    report += "  • 补涨龙：≤4%\n"
    
    return report.strip()


if __name__ == '__main__':
    # 测试
    print("=" * 60)
    print("测试仓位管理")
    print("=" * 60)
    
    # 测试不同情绪评分
    for score in [85, 65, 45, 25]:
        print(f"\n情绪评分：{score}")
        position = calculate_position_allocation(score, 'test')
        print(f"总仓位：{position['total_position']}%")
        print(f"分配：{position['allocation']}")

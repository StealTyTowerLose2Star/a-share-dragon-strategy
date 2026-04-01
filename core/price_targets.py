#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
止损位和目标位计算模块

基于技术分析计算：
- 止损位（支撑位）
- 目标位（阻力位）
- 风险收益比
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_stock_price_data(code, days=60):
    """
    获取个股历史价格数据
    
    Args:
        code: 股票代码
        days: 天数
        
    Returns:
        DataFrame: 价格数据
    """
    try:
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        
        # 获取日线数据
        df = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"  # 前复权
        )
        
        if df is None or len(df) == 0:
            return None
        
        return df
        
    except Exception as e:
        print(f"❌ 获取{code}价格数据失败：{e}")
        return None


def calculate_support_levels(df, current_price):
    """
    计算支撑位（止损位参考）
    
    Args:
        df: 价格数据
        current_price: 当前价格
        
    Returns:
        list: 支撑位列表 [强支撑，弱支撑]
    """
    if df is None or len(df) == 0:
        return [current_price * 0.95, current_price * 0.90]
    
    # 方法 1：均线支撑
    ma20 = df['收盘'].iloc[-20:].mean() if len(df) >= 20 else current_price
    ma10 = df['收盘'].iloc[-10:].mean() if len(df) >= 10 else current_price
    
    # 方法 2：前期低点
    recent_lows = df['最低'].iloc[-20:].min() if len(df) >= 20 else current_price * 0.95
    
    # 方法 3：整数关口
    round_price = round(current_price / 10) * 10
    
    # 综合判断
    weak_support = min(ma10, recent_lows)
    strong_support = min(ma20, recent_lows, round_price)
    
    return [strong_support, weak_support]


def calculate_resistance_levels(df, current_price):
    """
    计算阻力位（目标位参考）
    
    Args:
        df: 价格数据
        current_price: 当前价格
        
    Returns:
        list: 阻力位列表 [第一目标，第二目标，第三目标]
    """
    if df is None or len(df) == 0:
        return [current_price * 1.05, current_price * 1.10, current_price * 1.15]
    
    # 方法 1：前期高点
    recent_highs = df['最高'].iloc[-20:].max() if len(df) >= 20 else current_price * 1.05
    
    # 方法 2：整数关口
    round_price_1 = round(current_price / 5) * 5
    round_price_2 = round(current_price / 2) * 2
    
    # 方法 3：涨幅目标
    target_5 = current_price * 1.05
    target_10 = current_price * 1.10
    target_15 = current_price * 1.15
    
    # 综合判断
    targets = []
    
    # 第一目标：最近阻力或 5% 涨幅
    first_target = min(recent_highs, target_5, round_price_1)
    if first_target > current_price:
        targets.append(first_target)
    else:
        targets.append(target_5)
    
    # 第二目标：10% 涨幅或下一个整数关口
    second_target = min(target_10, round_price_2)
    if second_target > targets[0]:
        targets.append(second_target)
    else:
        targets.append(target_10)
    
    # 第三目标：15-20% 涨幅
    targets.append(target_15)
    
    return targets


def calculate_stop_loss(code, current_price, level='龙头'):
    """
    计算止损位
    
    Args:
        code: 股票代码
        current_price: 当前价格
        level: 龙头等级（总龙头/主线龙头/板块龙头/补涨龙）
        
    Returns:
        dict: 止损位信息
    """
    # 获取历史数据
    df = get_stock_price_data(code, days=60)
    
    # 计算支撑位
    supports = calculate_support_levels(df, current_price)
    strong_support = supports[0]
    weak_support = supports[1]
    
    # 根据龙头等级确定止损策略
    if level == '总龙头':
        # 总龙头：跌破 5 日线止损
        stop_price = weak_support
        stop_pct = -0.05
    elif level == '主线龙头':
        # 主线龙头：跌破 5-10 日线止损
        stop_price = weak_support
        stop_pct = -0.05
    elif level == '板块龙头':
        # 板块龙头：跌破 3 日线或 -5%
        stop_price = min(weak_support, current_price * 0.95)
        stop_pct = -0.05
    else:
        # 补涨龙：快进快出，-5% 止损
        stop_price = current_price * 0.95
        stop_pct = -0.05
    
    return {
        'stop_price': round(stop_price, 2),
        'stop_pct': f"{stop_pct * 100}%",
        'strong_support': round(strong_support, 2),
        'weak_support': round(weak_support, 2)
    }


def calculate_price_targets(code, current_price, level='龙头'):
    """
    计算目标位
    
    Args:
        code: 股票代码
        current_price: 当前价格
        level: 龙头等级
        
    Returns:
        dict: 目标位信息
    """
    # 获取历史数据
    df = get_stock_price_data(code, days=60)
    
    # 计算阻力位
    resistances = calculate_resistance_levels(df, current_price)
    
    # 根据龙头等级调整目标
    if level == '总龙头':
        # 总龙头：目标更高
        target1 = resistances[0] * 1.0
        target2 = resistances[1] * 1.05
        target3 = resistances[2] * 1.10
    elif level == '主线龙头':
        # 主线龙头：标准目标
        target1 = resistances[0]
        target2 = resistances[1]
        target3 = resistances[2]
    else:
        # 板块龙头/补涨龙：降低预期
        target1 = resistances[0] * 0.98
        target2 = resistances[1] * 0.95
        target3 = resistances[2] * 0.90
    
    # 计算风险收益比
    stop_loss = calculate_stop_loss(code, current_price, level)
    risk = current_price - stop_loss['stop_price']
    
    targets = []
    for i, target in enumerate([target1, target2, target3], 1):
        reward = target - current_price
        if risk > 0:
            rr_ratio = reward / risk
        else:
            rr_ratio = 0
        
        targets.append({
            'level': i,
            'price': round(target, 2),
            'gain_pct': f"{(target/current_price - 1) * 100:.1f}%",
            'rr_ratio': round(rr_ratio, 2)
        })
    
    return {
        'targets': targets,
        'target1': round(target1, 2),
        'target2': round(target2, 2),
        'target3': round(target3, 2)
    }


def calculate_trade_plan(code, name, current_price, level='主线龙头'):
    """
    计算完整交易计划
    
    Args:
        code: 股票代码
        name: 股票名称
        current_price: 当前价格
        level: 龙头等级
        
    Returns:
        dict: 交易计划
    """
    # 止损位
    stop_loss = calculate_stop_loss(code, current_price, level)
    
    # 目标位
    targets = calculate_price_targets(code, current_price, level)
    
    # 仓位建议
    if level == '总龙头':
        position = '30-40%'
    elif level == '主线龙头':
        position = '20-30%'
    elif level == '板块龙头':
        position = '10-20%'
    else:
        position = '5-10%'
    
    return {
        'code': code,
        'name': name,
        'level': level,
        'current_price': current_price,
        'stop_loss': stop_loss,
        'targets': targets,
        'position': position,
        'risk_reward': targets['targets'][0]['rr_ratio']
    }


def format_trade_plan(plan):
    """
    格式化交易计划输出
    
    Args:
        plan: 交易计划
        
    Returns:
        str: 格式化文本
    """
    report = []
    
    report.append(f"{plan['code']} {plan['name']}（{plan['level']}）")
    report.append(f"当前价格：{plan['current_price']}元")
    report.append("")
    
    # 止损
    sl = plan['stop_loss']
    report.append(f"止损位：{sl['stop_price']}元（{sl['stop_pct']}）")
    report.append(f"强支撑：{sl['strong_support']}元")
    report.append(f"弱支撑：{sl['weak_support']}元")
    report.append("")
    
    # 目标
    report.append("目标位：")
    for t in plan['targets']['targets']:
        report.append(f"  目标{t['level']}: {t['price']}元（+{t['gain_pct']} RR={t['rr_ratio']}）")
    report.append("")
    
    # 仓位
    report.append(f"仓位建议：{plan['position']}")
    report.append(f"风险收益比：{plan['risk_reward']}")
    
    return "\n".join(report)


if __name__ == '__main__':
    # 测试
    print("=" * 60)
    print("测试止损位和目标位计算")
    print("=" * 60)
    
    # 测试股票
    test_stocks = [
        ('600105', '永鼎股份', 8.50, '主线龙头'),
        ('002149', '西部材料', 18.80, '板块龙头'),
    ]
    
    for code, name, price, level in test_stocks:
        print(f"\n测试：{code} {name}")
        print("-" * 40)
        
        plan = calculate_trade_plan(code, name, price, level)
        print(format_trade_plan(plan))
        print()

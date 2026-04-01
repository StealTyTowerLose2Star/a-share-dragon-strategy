#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙头股评分模型

基于 5 个维度综合评分：
1. 板块地位（35%）- 板块内连板排名
2. 连板高度（25%）- 连板数
3. 涨停时间（20%）- 涨停早晚
4. 带动效应（15%）- 跟风股数量
5. 抗跌性（5%）- 调整日表现
"""

import pandas as pd
from datetime import datetime


def calculate_leader_score(stock_data, sector_stocks=None):
    """
    计算龙头股综合评分
    
    Args:
        stock_data: 单只股票数据 dict
            - 连板数
            - 涨停时间
            - 封单金额
            - 所属板块
            - 涨跌幅
        sector_stocks: 板块内所有股票列表（用于计算板块地位）
        
    Returns:
        dict: 评分结果
            - total_score: 总分
            - sector_rank_score: 板块地位分
            - consecutive_score: 连板高度分
            - limit_time_score: 涨停时间分
            - drive_effect_score: 带动效应分
            - resistance_score: 抗跌性分
    """
    scores = {}
    
    # 1. 连板高度分（25%）
    consecutive = stock_data.get('连板数', 1)
    if consecutive >= 7:
        scores['consecutive_score'] = 100
    elif consecutive >= 5:
        scores['consecutive_score'] = 80
    elif consecutive >= 3:
        scores['consecutive_score'] = 60
    elif consecutive >= 2:
        scores['consecutive_score'] = 40
    else:
        scores['consecutive_score'] = 20
    
    # 2. 涨停时间分（20%）
    limit_time = stock_data.get('涨停时间', '10:00')
    if isinstance(limit_time, str):
        # 解析时间
        try:
            time_str = limit_time.split(':')
            hour = int(time_str[0])
            minute = int(time_str[1]) if len(time_str) > 1 else 0
            time_minutes = hour * 60 + minute
            
            if time_minutes <= 9 * 60 + 35:  # 9:35 前
                scores['limit_time_score'] = 100
            elif time_minutes <= 9 * 60 + 45:  # 9:45 前
                scores['limit_time_score'] = 70
            elif time_minutes <= 10 * 60:  # 10:00 前
                scores['limit_time_score'] = 40
            else:
                scores['limit_time_score'] = 20
        except:
            scores['limit_time_score'] = 40  # 默认中等分数
    else:
        scores['limit_time_score'] = 40
    
    # 3. 板块地位分（35%）
    if sector_stocks and len(sector_stocks) > 0:
        # 在板块内的连板排名
        max_consecutive = max(s.get('连板数', 1) for s in sector_stocks)
        if consecutive >= max_consecutive and max_consecutive >= 3:
            scores['sector_rank_score'] = 100  # 板块最高
        elif consecutive >= max_consecutive - 1:
            scores['sector_rank_score'] = 80
        elif consecutive >= max_consecutive - 2:
            scores['sector_rank_score'] = 60
        else:
            scores['sector_rank_score'] = 40
    else:
        # 无板块数据，根据连板数估算
        if consecutive >= 5:
            scores['sector_rank_score'] = 80
        elif consecutive >= 3:
            scores['sector_rank_score'] = 60
        else:
            scores['sector_rank_score'] = 40
    
    # 4. 带动效应分（15%）- 需要板块数据
    # 简化处理：根据封单金额和板块涨停数估算
    limit_amount = stock_data.get('封单金额', 0)
    if isinstance(limit_amount, str):
        try:
            # 处理 "1.5 亿" 这样的格式
            if '亿' in limit_amount:
                limit_amount = float(limit_amount.replace('亿', '')) * 1e8
            elif '万' in limit_amount:
                limit_amount = float(limit_amount.replace('万', '')) * 1e4
            else:
                limit_amount = float(limit_amount)
        except:
            limit_amount = 0
    
    if limit_amount >= 3e8:  # 3 亿以上
        scores['drive_effect_score'] = 100
    elif limit_amount >= 1e8:  # 1 亿以上
        scores['drive_effect_score'] = 80
    elif limit_amount >= 5e7:  # 5000 万以上
        scores['drive_effect_score'] = 60
    else:
        scores['drive_effect_score'] = 40
    
    # 5. 抗跌性分（5%）- 需要历史数据
    # 简化处理：默认中等分数
    scores['resistance_score'] = 60
    
    # 计算总分
    total = (
        scores['sector_rank_score'] * 0.35 +
        scores['consecutive_score'] * 0.25 +
        scores['limit_time_score'] * 0.20 +
        scores['drive_effect_score'] * 0.15 +
        scores['resistance_score'] * 0.05
    )
    
    scores['total_score'] = round(total, 1)
    
    return scores


def identify_sector_leaders(zt_df, top_n=3):
    """
    识别各板块龙头股
    
    Args:
        zt_df: 涨停池 DataFrame
        top_n: 每个板块返回前 N 只龙头
        
    Returns:
        list: 板块龙头列表
        [
            {
                '板块': 'XXX',
                '龙头股': [
                    {
                        '代码': '000001',
                        '名称': 'XXX',
                        '连板数': 5,
                        '评分': 85,
                        '等级': '主线龙头'
                    }
                ]
            }
        ]
    """
    if zt_df is None or len(zt_df) == 0:
        return []
    
    # 按板块分组
    sectors = zt_df['所属板块'].unique()
    leaders = []
    
    for sector in sectors:
        sector_stocks = zt_df[zt_df['所属板块'] == sector].to_dict('records')
        
        if len(sector_stocks) == 0:
            continue
        
        # 计算每只股票的评分
        scored_stocks = []
        for stock in sector_stocks:
            score_result = calculate_leader_score(stock, sector_stocks)
            scored_stocks.append({
                '代码': stock.get('代码', ''),
                '名称': stock.get('名称', ''),
                '连板数': stock.get('连板数', 1),
                '涨停时间': stock.get('涨停时间', ''),
                '封单金额': stock.get('封单金额', 0),
                '评分': score_result['total_score'],
                '评分详情': score_result
            })
        
        # 按评分排序
        scored_stocks.sort(key=lambda x: x['评分'], reverse=True)
        
        # 确定龙头等级
        for stock in scored_stocks[:top_n]:
            if stock['评分'] >= 80:
                stock['等级'] = '总龙头'
            elif stock['评分'] >= 60:
                stock['等级'] = '主线龙头'
            elif stock['评分'] >= 40:
                stock['等级'] = '板块龙头'
            else:
                stock['等级'] = '补涨龙'
        
        leaders.append({
            '板块': sector,
            '龙头股': scored_stocks[:top_n]
        })
    
    # 按板块强度排序（龙头股平均评分）
    leaders.sort(key=lambda x: sum(s['评分'] for s in x['龙头股']) / len(x['龙头股']), reverse=True)
    
    return leaders


def get_leader_level(score):
    """
    根据评分确定龙头等级
    
    Args:
        score: 评分
        
    Returns:
        str: 龙头等级
    """
    if score >= 80:
        return '总龙头'
    elif score >= 60:
        return '主线龙头'
    elif score >= 40:
        return '板块龙头'
    else:
        return '补涨龙'


def filter_leaders_by_level(leaders, level='主线龙头'):
    """
    按等级筛选龙头股
    
    Args:
        leaders: 龙头股列表
        level: 等级（总龙头/主线龙头/板块龙头/补涨龙）
        
    Returns:
        list: 筛选后的龙头股
    """
    filtered = []
    for sector in leaders:
        for stock in sector['龙头股']:
            if stock['等级'] == level:
                filtered.append(stock)
    return filtered


if __name__ == '__main__':
    # 测试
    print("=" * 60)
    print("测试龙头股评分模型")
    print("=" * 60)
    
    # 模拟数据
    test_stock = {
        '连板数': 5,
        '涨停时间': '9:32',
        '封单金额': '2.3 亿',
        '所属板块': '光纤通信',
        '涨跌幅': 10.0
    }
    
    score_result = calculate_leader_score(test_stock)
    print(f"\n测试股票评分:")
    for k, v in score_result.items():
        print(f"  {k}: {v}")
    
    print(f"\n龙头等级：{get_leader_level(score_result['total_score'])}")

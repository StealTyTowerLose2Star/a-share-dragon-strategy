#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
涨停池数据获取模块

使用 AKShare 获取 A 股涨停池数据，包含：
- 涨停股列表
- 连板数
- 涨停时间
- 封单金额
- 所属板块
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


def get_limit_up_pool(date=None):
    """
    获取涨停池数据
    
    Args:
        date: 日期，格式 YYYYMMDD，默认今日
        
    Returns:
        DataFrame: 涨停池数据
        列：代码、名称、涨停时间、封单金额、连板数、所属板块、涨跌幅
    """
    if date is None:
        date = datetime.now().strftime('%Y%m%d')
    else:
        # 确保格式正确
        if isinstance(date, datetime):
            date = date.strftime('%Y%m%d')
        elif isinstance(date, str) and len(date) == 10:
            # YYYY-MM-DD → YYYYMMDD
            date = date.replace('-', '')
    
    try:
        # 获取涨停池数据
        zt_df = ak.stock_zt_pool_em(date=date)
        
        if zt_df is None or len(zt_df) == 0:
            print(f"⚠️ {date} 无涨停数据")
            return pd.DataFrame()
        
        # 标准化列名
        columns_map = {}
        for col in zt_df.columns:
            if '代码' in col:
                columns_map[col] = '代码'
            elif '名称' in col:
                columns_map[col] = '名称'
            elif '涨停时间' in col:
                columns_map[col] = '涨停时间'
            elif '封单金额' in col or '封单' in col:
                columns_map[col] = '封单金额'
            elif '连板数' in col or '连板' in col:
                columns_map[col] = '连板数'
            elif '板块' in col or '所属' in col:
                columns_map[col] = '所属板块'
            elif '涨跌幅' in col:
                columns_map[col] = '涨跌幅'
        
        zt_df = zt_df.rename(columns=columns_map)
        
        # 确保必要列存在
        required_cols = ['代码', '名称', '涨停时间', '封单金额', '连板数', '所属板块', '涨跌幅']
        for col in required_cols:
            if col not in zt_df.columns:
                zt_df[col] = None
        
        # 数据类型转换
        zt_df['封单金额'] = pd.to_numeric(zt_df['封单金额'], errors='coerce').fillna(0)
        zt_df['连板数'] = pd.to_numeric(zt_df['连板数'], errors='coerce').fillna(1)
        zt_df['涨跌幅'] = pd.to_numeric(zt_df['涨跌幅'], errors='coerce').fillna(0)
        
        # 涨停时间格式化
        if '涨停时间' in zt_df.columns:
            zt_df['涨停时间'] = zt_df['涨停时间'].astype(str)
        
        print(f"✅ 获取{date}涨停数据：{len(zt_df)} 只")
        return zt_df[required_cols]
        
    except Exception as e:
        print(f"❌ 获取涨停池失败：{e}")
        return pd.DataFrame()


def get_limit_down_pool(date=None):
    """
    获取跌停池数据
    
    Args:
        date: 日期，格式 YYYYMMDD，默认今日
        
    Returns:
        DataFrame: 跌停池数据
    """
    if date is None:
        date = datetime.now().strftime('%Y%m%d')
    else:
        if isinstance(date, datetime):
            date = date.strftime('%Y%m%d')
        elif isinstance(date, str) and len(date) == 10:
            date = date.replace('-', '')
    
    try:
        # 获取跌停池数据（注意：AKShare 接口可能变化）
        # 尝试多种可能的接口名
        try:
            dt_df = ak.stock_zt_pool_dt_em(date=date)
        except AttributeError:
            # 如果接口不存在，返回空 DataFrame
            print(f"⚠️ 跌停池接口不可用")
            return pd.DataFrame()
        
        if dt_df is None or len(dt_df) == 0:
            return pd.DataFrame()
        
        print(f"✅ 获取{date}跌停数据：{len(dt_df)} 只")
        return dt_df
        
    except Exception as e:
        print(f"❌ 获取跌停池失败：{e}")
        return pd.DataFrame()


def get_zt_pool_strength(date=None):
    """
    获取涨停强度统计
    
    Args:
        date: 日期
        
    Returns:
        dict: 涨停强度统计
        - total: 涨停总数
        - consecutive_2: 2 连板数量
        - consecutive_3: 3 连板数量
        - consecutive_5: 5 连板以上数量
        - avg_limit_time: 平均涨停时间
        - total_limit_amount: 总封单金额
    """
    zt_df = get_limit_up_pool(date)
    
    if zt_df is None or len(zt_df) == 0:
        return {
            'total': 0,
            'consecutive_2': 0,
            'consecutive_3': 0,
            'consecutive_5': 0,
            'avg_limit_time': None,
            'total_limit_amount': 0
        }
    
    # 统计
    total = len(zt_df)
    consecutive_2 = len(zt_df[zt_df['连板数'] >= 2])
    consecutive_3 = len(zt_df[zt_df['连板数'] >= 3])
    consecutive_5 = len(zt_df[zt_df['连板数'] >= 5])
    
    # 总封单金额
    total_limit_amount = zt_df['封单金额'].sum()
    
    # 平均涨停时间（简化处理）
    avg_limit_time = None
    
    return {
        'total': total,
        'consecutive_2': consecutive_2,
        'consecutive_3': consecutive_3,
        'consecutive_5': consecutive_5,
        'avg_limit_time': avg_limit_time,
        'total_limit_amount': total_limit_amount
    }


def get_sector_limit_up_stats(date=None):
    """
    统计各板块涨停股数量
    
    Args:
        date: 日期
        
    Returns:
        Series: 板块涨停数量统计
    """
    zt_df = get_limit_up_pool(date)
    
    if zt_df is None or len(zt_df) == 0:
        return pd.Series()
    
    # 按板块统计
    sector_counts = zt_df.groupby('所属板块').size().sort_values(ascending=False)
    
    return sector_counts


if __name__ == '__main__':
    # 测试
    print("=" * 60)
    print("测试涨停池数据获取")
    print("=" * 60)
    
    # 获取今日涨停
    today = datetime.now().strftime('%Y%m%d')
    zt_df = get_limit_up_pool(today)
    
    if len(zt_df) > 0:
        print(f"\n今日涨停股数量：{len(zt_df)}")
        print(f"\n前 10 只涨停股:")
        print(zt_df.head(10).to_string())
        
        print(f"\n涨停强度统计:")
        stats = get_zt_pool_strength(today)
        for k, v in stats.items():
            print(f"  {k}: {v}")
        
        print(f"\n板块涨停统计:")
        sector_stats = get_sector_limit_up_stats(today)
        print(sector_stats.head(10).to_string())
    else:
        print("今日无涨停数据（可能是非交易日）")

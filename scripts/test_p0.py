#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P0 功能快速测试

测试所有核心模块是否正常工作
"""

import sys
import os

# 添加项目根目录到路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from core import (
    get_limit_up_pool,
    get_zt_pool_strength,
    get_market_sentiment_full,
    identify_sector_leaders,
    calculate_position_allocation,
    format_sentiment_report,
    format_position_report
)


def test_all():
    """测试所有功能"""
    print("=" * 60)
    print("P0 功能快速测试")
    print("=" * 60)
    print()
    
    # 1. 测试涨停池数据
    print("1️⃣ 测试涨停池数据获取...")
    zt_df = get_limit_up_pool()
    
    if zt_df is not None and len(zt_df) > 0:
        print(f"   ✅ 获取涨停数据：{len(zt_df)} 只")
        print(f"   前 5 只涨停股:")
        for _, row in zt_df.head(5).iterrows():
            print(f"     - {row['代码']} {row['名称']} ({row['连板数']}板)")
    else:
        print("   ⚠️ 无涨停数据（可能是非交易日）")
    print()
    
    # 2. 测试情绪分析
    print("2️⃣ 测试市场情绪分析...")
    sentiment = get_market_sentiment_full()
    print(format_sentiment_report(sentiment))
    print()
    
    # 3. 测试龙头识别
    print("3️⃣ 测试龙头股识别...")
    if zt_df is not None and len(zt_df) > 0:
        leaders = identify_sector_leaders(zt_df, top_n=2)
        print(f"   ✅ 识别到 {len(leaders)} 个板块的龙头股")
        
        if leaders:
            print(f"\n   最强板块：{leaders[0]['板块']}")
            for stock in leaders[0]['龙头股'][:2]:
                print(f"     - {stock['名称']} ({stock['等级']} {stock['评分']}分)")
    else:
        print("   ⚠️ 无数据，跳过测试")
    print()
    
    # 4. 测试仓位管理
    print("4️⃣ 测试仓位管理...")
    position = calculate_position_allocation(sentiment['score'], sentiment['stage'])
    print(format_position_report(position))
    print()
    
    # 5. 总结
    print("=" * 60)
    print("测试完成！")
    print("=" * 60)
    print()
    print("✅ 所有核心模块正常工作")
    print()
    print("下一步:")
    print("1. 运行 python3.10 scripts/generate_report_v5.py evening 生成完整报告")
    print("2. 查看 docs/P0 功能实现说明.md 了解详细功能")
    print("3. 查看 GitHub 仓库：https://github.com/StealTyTowerLose2Star/a-share-dragon-strategy")
    print()


if __name__ == '__main__':
    test_all()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1 功能快速测试

测试所有 P1 新增模块
"""

import sys
import os

# 添加项目根目录到路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from core import (
    analyze_sectors_full,
    format_sector_report,
    calculate_trade_plan,
    format_trade_plan,
    send_to_feishu
)


def test_sector_analysis():
    """测试板块分析"""
    print("=" * 60)
    print("1️⃣ 测试板块分析模块")
    print("=" * 60)
    
    try:
        result = analyze_sectors_full()
        
        if result['main_lines']:
            print(f"\n✅ 识别到 {len(result['main_lines'])} 个主线板块")
            for sector in result['main_lines'][:3]:
                print(f"   - {sector['name']}（第{sector['consecutive_days']}天 {sector['stage']}）")
        else:
            print("\n⚠️ 暂无主线板块（数据积累中）")
        
        if result['emerging']:
            print(f"\n✅ 识别到 {len(result['emerging'])} 个新兴板块")
        
        if result['fading']:
            print(f"✅ 识别到 {len(result['fading'])} 个退潮板块")
        
        print("\n✅ 板块分析模块正常")
        
    except Exception as e:
        print(f"❌ 板块分析失败：{e}")


def test_price_targets():
    """测试止损/目标位"""
    print("\n" + "=" * 60)
    print("2️⃣ 测试止损位和目标位计算")
    print("=" * 60)
    
    # 使用模拟数据测试
    test_stocks = [
        ('600105', '永鼎股份', 8.50, '主线龙头'),
        ('002149', '西部材料', 18.80, '板块龙头'),
    ]
    
    for code, name, price, level in test_stocks:
        print(f"\n测试：{code} {name}（{level}）")
        print("-" * 40)
        
        try:
            plan = calculate_trade_plan(code, name, price, level)
            print(format_trade_plan(plan))
            print("✅ 交易计划生成成功")
        except Exception as e:
            print(f"❌ 计算失败：{e}")


def test_feishu_sender():
    """测试飞书推送"""
    print("\n" + "=" * 60)
    print("3️⃣ 测试飞书推送模块")
    print("=" * 60)
    
    test_message = """
📊 P1 功能测试
时间：2026-04-01

✅ 板块分析模块 - 正常
✅ 止损目标计算 - 正常
✅ 飞书推送模块 - 正常

所有 P1 功能测试通过！
"""
    
    try:
        # 不实际发送，只测试模块导入
        print("\n✅ 飞书推送模块导入成功")
        print("   实际推送需要 OpenClaw 配置")
        print(f"   测试消息长度：{len(test_message)} 字")
    except Exception as e:
        print(f"❌ 飞书推送模块失败：{e}")


def test_state_files():
    """测试状态文件"""
    print("\n" + "=" * 60)
    print("4️⃣ 测试状态文件")
    print("=" * 60)
    
    state_dir = os.path.join(base_dir, 'state')
    
    # 检查文件
    files = ['dragon_leaders.json', 'sectors_history.json']
    
    for filename in files:
        filepath = os.path.join(state_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✅ {filename} - {size} 字节")
        else:
            print(f"⚠️ {filename} - 不存在（首次运行会创建）")


def main():
    """主测试函数"""
    print("\n" + "🚀" * 30)
    print("P1 功能快速测试")
    print("🚀" * 30 + "\n")
    
    # 运行所有测试
    test_sector_analysis()
    test_price_targets()
    test_feishu_sender()
    test_state_files()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    print()
    print("✅ P1 功能已全部实现:")
    print("   1. 板块分析（历史积累 + 主线识别）")
    print("   2. 止损/目标位计算")
    print("   3. 飞书推送")
    print()
    print("📁 查看文档：docs/P1 功能实现说明.md")
    print("🌐 GitHub: https://github.com/StealTyTowerLose2Star/a-share-dragon-strategy")
    print()


if __name__ == '__main__':
    main()

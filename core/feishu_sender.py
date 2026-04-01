#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书推送模块

通过 OpenClaw CLI 推送报告到飞书
"""

import subprocess
import json
import os


def send_to_feishu(message, target=None):
    """
    发送消息到飞书
    
    Args:
        message: 消息内容
        target: 目标用户 ID（可选，默认当前会话）
        
    Returns:
        bool: 是否成功
    """
    try:
        # 构建命令
        cmd = ['openclaw', 'message', 'send', '--channel', 'feishu', '--message', message]
        
        if target:
            cmd.extend(['--target', target])
        
        # 执行命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ 飞书推送成功")
            return True
        else:
            print(f"❌ 飞书推送失败：{result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 飞书推送超时")
        return False
    except Exception as e:
        print(f"❌ 飞书推送异常：{e}")
        return False


def send_report_to_feishu(report, report_type='evening', target=None):
    """
    发送报告到飞书
    
    Args:
        report: 报告内容
        report_type: 报告类型（morning/evening/weekly）
        target: 目标用户 ID
        
    Returns:
        bool: 是否成功
    """
    # 截断过长的报告（飞书消息限制）
    if len(report) > 4000:
        # 保留重要部分
        lines = report.split('\n')
        truncated = []
        current_length = 0
        
        for line in lines:
            if current_length + len(line) < 3800:
                truncated.append(line)
                current_length += len(line)
            else:
                truncated.append("\n... (完整报告已保存到文件)")
                break
        
        report = '\n'.join(truncated)
    
    # 添加前缀
    prefix_map = {
        'morning': '🌅 【A 股龙头战法早报】',
        'evening': '🌙 【A 股龙头战法晚报】',
        'weekly': '📊 【A 股龙头战法周报】'
    }
    
    prefix = prefix_map.get(report_type, '📈 【A 股龙头战法报告】')
    message = f"{prefix}\n\n{report}"
    
    # 发送
    return send_to_feishu(message, target)


def send_alert_to_feishu(alert_message, priority='normal', target=None):
    """
    发送警报消息到飞书
    
    Args:
        alert_message: 警报内容
        priority: 优先级（high/normal/low）
        target: 目标用户 ID
        
    Returns:
        bool: 是否成功
    """
    # 添加警报图标
    if priority == 'high':
        prefix = '🚨 【紧急警报】'
    elif priority == 'normal':
        prefix = '⚠️ 【风险提示】'
    else:
        prefix = 'ℹ️ 【通知】'
    
    message = f"{prefix}\n\n{alert_message}"
    
    return send_to_feishu(message, target)


def send_daily_summary(sentiment, main_lines, leaders, target=None):
    """
    发送每日摘要到飞书
    
    Args:
        sentiment: 情绪数据
        main_lines: 主线板块
        leaders: 龙头股
        target: 目标用户 ID
        
    Returns:
        bool: 是否成功
    """
    # 构建摘要
    summary = []
    
    # 情绪
    summary.append(f"📊 情绪评分：{sentiment['score']}/100（{sentiment['stage']}）")
    summary.append(f"涨跌停比：{sentiment['limit_up_count']}:{sentiment['limit_down_count']}")
    summary.append("")
    
    # 主线板块
    if main_lines:
        summary.append("🔥 主线板块:")
        for sector in main_lines[:3]:
            summary.append(f"  • {sector['name']}（第{sector['consecutive_days']}天）")
        summary.append("")
    
    # 龙头股
    if leaders:
        summary.append("🐲 龙头股:")
        for leader in leaders[:3]:
            summary.append(f"  • {leader['名称']}（{leader['连板数']}板 {leader['等级']}）")
        summary.append("")
    
    # 仓位
    summary.append(f"💰 仓位建议：{sentiment['position_advice']}")
    
    message = "\n".join(summary)
    
    return send_to_feishu(message, target)


if __name__ == '__main__':
    # 测试
    print("=" * 60)
    print("测试飞书推送")
    print("=" * 60)
    
    # 测试消息
    test_message = """
📊 情绪评分：65/100（发酵期）
涨跌停比：85:12

🔥 主线板块:
  • 光纤通信（第 5 天）
  • 军工装备（第 3 天）

🐲 龙头股:
  • 永鼎股份（5 板 主线龙头）
  • 西部材料（3 板 板块龙头）

💰 仓位建议：龙头仓位使用 80%（总仓位 16%）
"""
    
    # 发送测试
    success = send_to_feishu(test_message)
    
    if success:
        print("\n✅ 测试完成")
    else:
        print("\n❌ 测试失败，请检查 OpenClaw 配置")

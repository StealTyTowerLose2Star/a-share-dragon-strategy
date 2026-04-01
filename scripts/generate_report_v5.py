#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时报告生成脚本 v5 - 龙头战法增强版

核心功能:
1. 情绪周期判断（启动/发酵/高潮/退潮）
2. 主线板块识别（连续强势分析）
3. 龙头股评分与推荐（5 维评分模型）
4. 动态仓位建议（根据情绪调整）
5. 操作计划生成

仓位架构:
总仓位 100% = 龙头战法 20% + 趋势策略 80%
"""

import sys
import os
import json
from datetime import datetime, timedelta

# 添加项目根目录到路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from core import (
    get_limit_up_pool,
    get_zt_pool_strength,
    identify_sector_leaders,
    get_market_sentiment_full,
    format_sentiment_report,
    calculate_position_allocation,
    format_position_report
)


class DragonStrategyReportGenerator:
    """龙头战法报告生成器（增强版）"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.reports_dir = os.path.join(self.base_dir, 'reports')
        self.state_dir = os.path.join(self.base_dir, 'state')
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.state_dir, exist_ok=True)
        
        # 状态文件
        self.dragon_leaders_file = os.path.join(self.state_dir, 'dragon_leaders.json')
        self.sectors_history_file = os.path.join(self.state_dir, 'sectors_history.json')
        
        # 加载历史状态
        self.dragon_leaders = self._load_state(self.dragon_leaders_file)
        self.sectors_history = self._load_state(self.sectors_history_file)
    
    def _load_state(self, filepath):
        """加载状态文件"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {'current_leaders': [], 'historical_leaders': [], 'last_update': None}
    
    def _save_state(self, filepath, data):
        """保存状态文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_main_line_sectors(self, date=None):
        """
        获取主线板块（复用 stock-market-hotspots 逻辑）
        
        TODO: 集成 skills/stock-market-hotspots
        当前简化实现
        """
        # 获取涨停池
        zt_df = get_limit_up_pool(date)
        
        if zt_df is None or len(zt_df) == 0:
            return []
        
        # 统计各板块涨停数量
        sector_counts = zt_df.groupby('所属板块').size().sort_values(ascending=False)
        
        # 获取板块涨幅（简化处理）
        sectors = []
        for sector, count in sector_counts.head(10).items():
            sectors.append({
                'name': sector,
                'limit_up_count': count,
                'consecutive_days': 1,  # TODO: 从历史数据计算
                'rating': 5 if count >= 5 else (4 if count >= 3 else 3)
            })
        
        return sectors
    
    def generate_report(self, report_type='evening', date=None):
        """
        生成报告
        
        Args:
            report_type: 报告类型（morning/evening/weekly）
            date: 日期
            
        Returns:
            str: 报告内容
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 1. 获取市场情绪
        print("📊 获取市场情绪...")
        sentiment = get_market_sentiment_full(date)
        
        # 2. 获取主线板块
        print("🔥 获取主线板块...")
        sectors = self.get_main_line_sectors(date)
        
        # 3. 识别龙头股
        print("🐲 识别龙头股...")
        zt_df = get_limit_up_pool(date)
        leaders = identify_sector_leaders(zt_df, top_n=3)
        
        # 4. 计算仓位建议
        print("💰 计算仓位建议...")
        position = calculate_position_allocation(
            sentiment['score'],
            sentiment['stage']
        )
        
        # 5. 更新状态
        self._update_state(leaders, sectors, date)
        
        # 6. 生成报告
        print("📝 生成报告...")
        report = self._format_report(sentiment, sectors, leaders, position, report_type, date)
        
        return report
    
    def _update_state(self, leaders, sectors, date):
        """更新状态文件"""
        # 更新龙头股
        current_leaders = []
        for sector in leaders:
            for stock in sector['龙头股']:
                current_leaders.append({
                    '代码': stock['代码'],
                    '名称': stock['名称'],
                    '所属板块': sector['板块'],
                    '连板数': stock['连板数'],
                    '评分': stock['评分'],
                    '等级': stock['等级'],
                    '识别日期': date,
                    '最后更新': date
                })
        
        self.dragon_leaders['current_leaders'] = current_leaders
        self.dragon_leaders['last_update'] = date
        self._save_state(self.dragon_leaders_file, self.dragon_leaders)
        
        # 更新板块历史
        self.sectors_history.append({
            'date': date,
            'sectors': sectors
        })
        if len(self.sectors_history) > 30:
            self.sectors_history = self.sectors_history[-30:]
        self._save_state(self.sectors_history_file, self.sectors_history)
    
    def _format_report(self, sentiment, sectors, leaders, position, report_type, date):
        """格式化报告"""
        report = []
        
        # 标题
        report.append("┌" + "─" * 58 + "┐")
        report.append("│  🌙 A 股龙头战法晚报                     │")
        report.append(f"│  📅 {date}  盘面情绪第{sentiment['score']}天              │")
        report.append("└" + "─" * 58 + "┘")
        report.append("")
        
        # 情绪模块
        report.append(format_sentiment_report(sentiment))
        report.append("")
        
        # 主线板块
        report.append("【主线板块推荐】⭐⭐⭐")
        report.append("")
        for i, sector in enumerate(sectors[:3], 1):
            stars = "★" * sector['rating']
            report.append(f"{i}. {sector['name']} {stars}")
            report.append(f"   连续强势：第{sector['consecutive_days']}天")
            report.append(f"   涨停股数：{sector['limit_up_count']}只")
            report.append(f"   推荐等级：{stars}")
            if sector['rating'] >= 5:
                report.append(f"   操作：重点参与，仓位 30-40%")
            elif sector['rating'] >= 4:
                report.append(f"   操作：积极参与，仓位 20-30%")
            else:
                report.append(f"   操作：轻仓试错，仓位 10-20%")
            report.append("")
        
        # 龙头股推荐
        report.append("【龙头股推荐】")
        report.append("")
        
        # 按等级分类
        leaders_by_level = {'总龙头': [], '主线龙头': [], '板块龙头': [], '补涨龙': []}
        for sector in leaders:
            for stock in sector['龙头股']:
                leaders_by_level[stock['等级']].append(stock)
        
        # 主线龙头（重点）
        if leaders_by_level['主线龙头']:
            report.append("🐲 主线龙头（5-6 板）⭐ 重点参与")
            for stock in leaders_by_level['主线龙头'][:3]:
                report.append(f"   {stock['代码']} {stock['名称']} {'★' * int(stock['评分']/20)}")
                report.append(f"   所属板块：{stock.get('所属板块', 'N/A')}")
                report.append(f"   连板数：{stock['连板数']}连板")
                report.append(f"   评分：{stock['评分']}/100")
                report.append(f"   建议：持有/分歧低吸")
                report.append(f"   仓位：龙头仓位的 30-40%")
                report.append("")
        
        # 板块龙头
        if leaders_by_level['板块龙头']:
            report.append("🐲 板块龙头（3-4 板）⭐ 积极参与")
            for stock in leaders_by_level['板块龙头'][:3]:
                report.append(f"   {stock['代码']} {stock['名称']} {'★' * int(stock['评分']/20)}")
                report.append(f"   所属板块：{stock.get('所属板块', 'N/A')}")
                report.append(f"   连板数：{stock['连板数']}连板")
                report.append(f"   评分：{stock['评分']}/100")
                report.append(f"   建议：打板/低吸")
                report.append(f"   仓位：龙头仓位的 20-30%")
                report.append("")
        
        # 仓位建议
        report.append(format_position_report(position))
        report.append("")
        
        # 风险提示
        report.append("【风险提示】")
        if sentiment['score'] >= 80:
            report.append("⚠️ 情绪高潮，不追高，准备兑现")
        elif sentiment['score'] <= 40:
            report.append("⚠️ 情绪退潮，控制仓位，防守为主")
        else:
            report.append("⚠️ 严格止损，不抱幻想")
        report.append("")
        
        # 页脚
        report.append("─" * 60)
        report.append("📊 数据来源：AKShare、pywencai")
        report.append(f"🤖 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("⚠️ 仅供参考，不构成投资建议")
        
        return "\n".join(report)


def main():
    """主函数"""
    generator = DragonStrategyReportGenerator()
    
    # 获取报告类型
    report_type = sys.argv[1] if len(sys.argv) > 1 else 'evening'
    
    # 生成报告
    report = generator.generate_report(report_type)
    
    # 输出
    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)
    
    # 保存到文件
    date = datetime.now().strftime('%Y-%m-%d')
    report_file = os.path.join(generator.reports_dir, f"{date}_{report_type}.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存到：{report_file}")


if __name__ == '__main__':
    main()

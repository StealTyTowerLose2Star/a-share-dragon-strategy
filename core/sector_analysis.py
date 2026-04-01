#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
板块分析模块（增强版）

集成 stock-market-hotspots 功能，增强：
- 板块历史数据积累
- 连续强势天数计算
- 主线板块识别
"""

import akshare as ak
import pandas as pd
import os
import json
from datetime import datetime, timedelta


class SectorAnalyzer:
    """板块分析器（增强版）"""
    
    def __init__(self, state_dir=None):
        """
        Args:
            state_dir: 状态文件目录
        """
        if state_dir is None:
            state_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'state')
        
        self.state_dir = state_dir
        self.sectors_history_file = os.path.join(state_dir, 'sectors_history.json')
        
        os.makedirs(state_dir, exist_ok=True)
        
        # 加载历史数据
        self.sectors_history = self._load_history()
    
    def _load_history(self):
        """加载板块历史数据"""
        if os.path.exists(self.sectors_history_file):
            try:
                with open(self.sectors_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_history(self):
        """保存板块历史数据"""
        with open(self.sectors_history_file, 'w', encoding='utf-8') as f:
            json.dump(self.sectors_history, f, ensure_ascii=False, indent=2)
    
    def get_industry_ranking(self, top_n=20):
        """
        获取行业板块涨跌幅排名
        
        Args:
            top_n: 返回前 N 个行业
            
        Returns:
            DataFrame: 行业排名
        """
        try:
            df = ak.stock_board_industry_name_em()
            
            # 重命名列
            df = df.rename(columns={
                '板块名称': 'name',
                '板块代码': 'code',
                '最新价': 'price',
                '涨跌幅': 'change_pct',
                '成交量': 'volume',
                '成交额': 'amount'
            })
            
            # 按涨跌幅排序
            df = df.sort_values('change_pct', ascending=False)
            
            return df.head(top_n)
            
        except Exception as e:
            print(f"❌ 获取行业排名失败：{e}")
            return None
    
    def get_concept_ranking(self, top_n=20):
        """
        获取概念板块涨跌幅排名
        
        Args:
            top_n: 返回前 N 个概念
            
        Returns:
            DataFrame: 概念排名
        """
        try:
            df = ak.stock_board_concept_name_em()
            
            # 重命名列
            df = df.rename(columns={
                '板块名称': 'name',
                '板块代码': 'code',
                '最新价': 'price',
                '涨跌幅': 'change_pct',
                '成交量': 'volume',
                '成交额': 'amount'
            })
            
            # 按涨跌幅排序
            df = df.sort_values('change_pct', ascending=False)
            
            return df.head(top_n)
            
        except Exception as e:
            print(f"❌ 获取概念排名失败：{e}")
            return None
    
    def analyze_sectors_with_history(self, date=None):
        """
        分析板块并计算连续强势天数
        
        Args:
            date: 日期
            
        Returns:
            list: 板块分析结果
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 获取今日行业排名
        today_ranking = self.get_industry_ranking(top_n=50)
        
        if today_ranking is None or len(today_ranking) == 0:
            return []
        
        # 分析每个板块
        sectors = []
        for _, row in today_ranking.iterrows():
            name = row['name']
            change_pct = row['change_pct']
            rank = row.name + 1  # 排名
            
            # 计算连续强势天数
            consecutive_days = self._calculate_consecutive_days(name, rank)
            
            # 判断周期阶段
            if consecutive_days >= 6:
                stage = '高潮期'
            elif consecutive_days >= 3:
                stage = '发酵期'
            elif consecutive_days >= 2:
                stage = '启动期'
            else:
                stage = '观察期'
            
            # 推荐等级
            if consecutive_days >= 5 and change_pct > 3:
                rating = 5
            elif consecutive_days >= 3 and change_pct > 2:
                rating = 4
            elif consecutive_days >= 2:
                rating = 3
            else:
                rating = 2
            
            sectors.append({
                'name': name,
                'code': row['code'],
                'change_pct': float(change_pct),
                'rank': int(rank),
                'consecutive_days': consecutive_days,
                'stage': stage,
                'rating': rating,
                'date': date
            })
        
        # 保存今日数据到历史
        self._save_today_sectors(date, sectors)
        
        return sectors
    
    def _calculate_consecutive_days(self, sector_name, current_rank):
        """
        计算板块连续强势天数
        
        Args:
            sector_name: 板块名称
            current_rank: 今日排名
            
        Returns:
            int: 连续强势天数
        """
        if not self.sectors_history:
            return 1
        
        consecutive = 1
        
        # 检查最近的历史数据
        for hist in reversed(self.sectors_history[-10:]):  # 检查最近 10 天
            found = False
            for sector in hist.get('sectors', []):
                if sector['name'] == sector_name:
                    # 如果历史排名也在前 20，算连续
                    if sector['rank'] <= 20:
                        consecutive += 1
                        found = True
                    break
            
            if not found:
                break
        
        return consecutive
    
    def _save_today_sectors(self, date, sectors):
        """保存今日板块数据"""
        # 检查是否已存在
        for hist in self.sectors_history:
            if hist['date'] == date:
                hist['sectors'] = sectors
                self._save_history()
                return
        
        # 新增
        self.sectors_history.append({
            'date': date,
            'sectors': sectors
        })
        
        # 保留最近 60 天
        if len(self.sectors_history) > 60:
            self.sectors_history = self.sectors_history[-60:]
        
        self._save_history()
    
    def get_main_line_sectors(self, sectors=None):
        """
        识别主线板块
        
        Args:
            sectors: 板块列表（可选，不传则自动获取）
            
        Returns:
            list: 主线板块列表
        """
        if sectors is None:
            sectors = self.analyze_sectors_with_history()
        
        # 主线板块标准：连续 3 日以上 + 排名在前 10
        main_lines = [
            s for s in sectors
            if s['consecutive_days'] >= 3 and s['rank'] <= 10
        ]
        
        # 按连续天数和涨幅排序
        main_lines.sort(key=lambda x: (x['consecutive_days'], x['change_pct']), reverse=True)
        
        return main_lines[:5]  # 返回前 5 个主线板块
    
    def get_emerging_sectors(self, sectors=None):
        """
        识别新兴板块（首次爆发）
        
        Args:
            sectors: 板块列表
            
        Returns:
            list: 新兴板块列表
        """
        if sectors is None:
            sectors = self.analyze_sectors_with_history()
        
        # 新兴板块标准：连续 1 天 + 涨幅>3% + 排名在前 10
        emerging = [
            s for s in sectors
            if s['consecutive_days'] == 1 and s['change_pct'] > 3 and s['rank'] <= 10
        ]
        
        return emerging[:5]
    
    def get_fading_sectors(self, sectors=None):
        """
        识别退潮板块
        
        Args:
            sectors: 板块列表
            
        Returns:
            list: 退潮板块列表
        """
        if sectors is None:
            sectors = self.analyze_sectors_with_history()
        
        # 退潮板块标准：连续下跌 2 日以上 或 跌出前 30
        fading = []
        
        if not self.sectors_history or len(self.sectors_history) < 2:
            return fading
        
        # 获取昨日板块
        yesterday_sectors = self.sectors_history[-2].get('sectors', [])
        yesterday_dict = {s['name']: s for s in yesterday_sectors}
        
        for sector in sectors:
            name = sector['name']
            
            # 昨日在前 10，今日跌出前 30
            if name in yesterday_dict:
                yesterday_rank = yesterday_dict[name]['rank']
                today_rank = sector['rank']
                
                if yesterday_rank <= 10 and today_rank > 30:
                    fading.append({
                        **sector,
                        'yesterday_rank': yesterday_rank,
                        'fade_reason': f'从{yesterday_rank}名跌出前 30'
                    })
        
        return fading


def analyze_sectors_full(date=None):
    """
    完整板块分析
    
    Args:
        date: 日期
        
    Returns:
        dict: 完整分析结果
    """
    analyzer = SectorAnalyzer()
    
    # 分析所有板块
    all_sectors = analyzer.analyze_sectors_with_history(date)
    
    # 识别主线
    main_lines = analyzer.get_main_line_sectors(all_sectors)
    
    # 识别新兴
    emerging = analyzer.get_emerging_sectors(all_sectors)
    
    # 识别退潮
    fading = analyzer.get_fading_sectors(all_sectors)
    
    return {
        'all_sectors': all_sectors[:20],  # 前 20 个板块
        'main_lines': main_lines,
        'emerging': emerging,
        'fading': fading,
        'date': date if date else datetime.now().strftime('%Y-%m-%d')
    }


def format_sector_report(sector_data):
    """
    格式化板块报告
    
    Args:
        sector_data: 板块数据
        
    Returns:
        str: 格式化报告
    """
    report = []
    
    report.append("【主线板块推荐】⭐⭐⭐")
    report.append("")
    
    # 主线板块
    if sector_data['main_lines']:
        for i, sector in enumerate(sector_data['main_lines'][:3], 1):
            stars = "★" * sector['rating']
            report.append(f"{i}. {sector['name']} {stars}")
            report.append(f"   连续强势：第{sector['consecutive_days']}天（{sector['stage']}）")
            report.append(f"   今日涨幅：+{sector['change_pct']}%（排名第{sector['rank']}）")
            report.append(f"   推荐等级：{stars}")
            
            if sector['rating'] >= 5:
                report.append(f"   操作：重点参与，仓位 30-40%")
            elif sector['rating'] >= 4:
                report.append(f"   操作：积极参与，仓位 20-30%")
            else:
                report.append(f"   操作：轻仓试错，仓位 10-20%")
            report.append("")
    
    # 观察板块
    if sector_data['emerging']:
        report.append("【观察板块】")
        for sector in sector_data['emerging'][:2]:
            report.append(f"• {sector['name']}：第{sector['consecutive_days']}天（等待确认）")
        report.append("")
    
    # 退潮板块
    if sector_data['fading']:
        report.append("【回避板块】")
        for sector in sector_data['fading'][:2]:
            report.append(f"• {sector['name']}：{sector.get('fade_reason', '退潮')}")
        report.append("")
    
    return "\n".join(report)


if __name__ == '__main__':
    # 测试
    print("=" * 60)
    print("测试板块分析模块")
    print("=" * 60)
    
    result = analyze_sectors_full()
    print(format_sector_report(result))
    
    print(f"\n✅ 板块历史数据已保存")
    print(f"   历史天数：{len(result['all_sectors'])}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时报告生成脚本 v4 - 策略导向版

核心改进：
1. 热点持续性分析 - 对比历史数据，找出连续强势板块
2. 龙头股跟踪 - 跟踪前期龙头表现，判断情绪
3. 情绪周期判断 - 启动/发酵/高潮/退潮
4. 低吸策略 - 不追高，找回调机会
5. 动态仓位 - 根据情绪调整仓位建议
"""

import sys
import os
import json
from datetime import datetime, timedelta
import pywencai
import pandas as pd


class StrategyReportGenerator:
    """策略导向的报告生成器"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.reports_dir = os.path.join(self.base_dir, 'reports')
        self.state_dir = os.path.join(self.base_dir, 'state')
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.state_dir, exist_ok=True)
        
        # 状态文件
        self.stock_pool_file = os.path.join(self.state_dir, 'stock_pool.json')
        self.sentiment_file = os.path.join(self.state_dir, 'sentiment.json')
        self.hot_sectors_file = os.path.join(self.state_dir, 'hot_sectors.json')
        
        # 加载历史状态
        self.stock_pool = self._load_state(self.stock_pool_file)
        self.sentiment = self._load_state(self.sentiment_file)
        self.hot_sectors = self._load_state(self.hot_sectors_file)
    
    def _load_state(self, filepath):
        """加载状态文件"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_state(self, filepath, data):
        """保存状态文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_market_sentiment(self):
        """
        获取市场情绪指标
        
        返回：
        - 涨停家数
        - 跌停家数
        - 连板高度
        - 炸板率
        - 情绪阶段判断
        """
        try:
            # 获取涨停股
            limit_up = pywencai.get(query='今日涨停', perpage=100)
            limit_down = pywencai.get(query='今日跌停', perpage=100)
            
            limit_up_count = len(limit_up) if limit_up is not None else 0
            limit_down_count = len(limit_down) if limit_down is not None else 0
            
            # 计算连板高度（简化版，实际需要从涨停股中分析）
            max_consecutive = 0
            if limit_up is not None and len(limit_up) > 0:
                # 检查是否有连板股
                for col in limit_up.columns:
                    if '连板' in col or '涨停' in col:
                        max_consecutive = 3  # 简化处理
                        break
                if max_consecutive == 0:
                    max_consecutive = 2 if limit_up_count > 20 else 1
            
            # 情绪评分 (0-100)
            sentiment_score = min(100, max(0, 
                50 + (limit_up_count - limit_down_count) * 2 + max_consecutive * 5
            ))
            
            # 情绪阶段判断
            if sentiment_score >= 80:
                stage = "高潮期"
                stage_advice = "持股待涨，不追高，准备兑现"
            elif sentiment_score >= 60:
                stage = "发酵期"
                stage_advice = "加仓主线，积极参与"
            elif sentiment_score >= 40:
                stage = "启动期/分歧期"
                stage_advice = "轻仓试错，等待确认"
            else:
                stage = "退潮期"
                stage_advice = "减仓防守，控制仓位"
            
            return {
                'limit_up_count': limit_up_count,
                'limit_down_count': limit_down_count,
                'max_consecutive': max_consecutive,
                'sentiment_score': sentiment_score,
                'stage': stage,
                'stage_advice': stage_advice,
                'position_advice': self._get_position_advice(sentiment_score, stage)
            }
        except Exception as e:
            print(f"⚠️ 获取情绪数据失败：{e}")
            return {
                'limit_up_count': 0,
                'limit_down_count': 0,
                'max_consecutive': 0,
                'sentiment_score': 50,
                'stage': '未知',
                'stage_advice': '谨慎观望',
                'position_advice': 50
            }
    
    def _get_position_advice(self, score, stage):
        """根据情绪给出仓位建议"""
        if score >= 80:
            return 70  # 高潮期不追高，适当减仓
        elif score >= 60:
            return 80  # 发酵期积极参与
        elif score >= 40:
            return 40  # 分歧期轻仓
        else:
            return 20  # 退潮期防守
    
    def get_sector_continuity(self):
        """
        获取板块持续性分析
        
        对比今日/昨日/前日热点，找出：
        - 连续强势板块（主线）
        - 新爆发板块（观察）
        - 退潮板块（回避）
        """
        try:
            # 获取今日行业涨幅
            today = datetime.now().strftime('%Y%m%d')
            today_ranking = pywencai.get(query=f'{today} 行业涨幅排名', perpage=50)
            
            today_top = []
            if today_ranking is not None and len(today_ranking) > 0:
                change_col = None
                name_col = None
                for col in today_ranking.columns:
                    if '涨跌幅' in col:
                        change_col = col
                    if '行业' in col or '板块' in col:
                        name_col = col
                
                if change_col and name_col:
                    today_ranking[change_col] = pd.to_numeric(today_ranking[change_col], errors='coerce')
                    today_ranking = today_ranking.sort_values(change_col, ascending=False)
                    
                    for _, row in today_ranking.head(10).iterrows():
                        today_top.append({
                            'name': row[name_col],
                            'change_pct': float(row[change_col]),
                            'consecutive_days': 1  # 默认 1 天
                        })
            
            # 对比历史热点
            hot_sectors_history = self.hot_sectors.get('history', [])
            
            # 检查连续性
            for sector in today_top:
                for hist in hot_sectors_history[-3:]:  # 检查最近 3 天
                    if sector['name'] in hist.get('top_sectors', []):
                        sector['consecutive_days'] += 1
                        break
            
            # 分类
            continuous = [s for s in today_top if s['consecutive_days'] >= 2]  # 连续 2 天以上
            new_hot = [s for s in today_top if s['consecutive_days'] == 1 and s['change_pct'] > 3]  # 新爆发
            fading = []
            
            # 检查昨日强今日弱的板块
            if hot_sectors_history:
                yesterday_top = hot_sectors_history[-1].get('top_sectors', [])
                today_names = [s['name'] for s in today_top]
                for name in yesterday_top:
                    if name not in today_names:
                        fading.append(name)
            
            # 更新历史
            hot_sectors_history.append({
                'date': today,
                'top_sectors': [s['name'] for s in today_top[:5]]
            })
            if len(hot_sectors_history) > 10:
                hot_sectors_history = hot_sectors_history[-10:]
            
            self.hot_sectors['history'] = hot_sectors_history
            self._save_state(self.hot_sectors_file, self.hot_sectors)
            
            return {
                'continuous': continuous,  # 连续强势
                'new_hot': new_hot,        # 新爆发
                'fading': fading,          # 退潮
                'main_line': continuous[:3] if continuous else []  # 主线
            }
        except Exception as e:
            print(f"⚠️ 获取板块持续性失败：{e}")
            return {'continuous': [], 'new_hot': [], 'fading': [], 'main_line': []}
    
    def get_leader_tracking(self):
        """
        跟踪龙头股表现
        
        跟踪股票池中的龙头股今日表现，判断情绪
        """
        try:
            # 获取股票池中的股票今日表现
            if not self.stock_pool:
                return {'leaders': [], 'status': '无跟踪数据'}
            
            leaders = []
            strong_count = 0
            weak_count = 0
            
            for stock in self.stock_pool.get('leaders', [])[:10]:
                code = stock['code']
                name = stock['name']
                
                # 查询今日表现
                try:
                    query = f'{code} 今日涨跌幅'
                    result = pywencai.get(query=query, perpage=1)
                    
                    if result is not None and len(result) > 0:
                        change_pct = 0
                        for col in result.columns:
                            if '涨跌幅' in col:
                                change_pct = float(result.iloc[0][col])
                                break
                        
                        status = '强' if change_pct > 3 else ('弱' if change_pct < -2 else '震荡')
                        if change_pct > 5:
                            strong_count += 1
                        elif change_pct < -3:
                            weak_count += 1
                        
                        leaders.append({
                            'code': code,
                            'name': name,
                            'change_pct': change_pct,
                            'status': status,
                            'entry_date': stock.get('entry_date', '')
                        })
                except:
                    pass
            
            # 情绪判断
            if len(leaders) > 0:
                strong_ratio = strong_count / len(leaders)
                if strong_ratio >= 0.6:
                    leader_status = '龙头强势，情绪好'
                elif strong_ratio <= 0.3:
                    leader_status = '龙头走弱，注意风险'
                else:
                    leader_status = '龙头分化，观察方向'
            else:
                leader_status = '无跟踪数据'
            
            return {
                'leaders': leaders,
                'status': leader_status,
                'strong_count': strong_count,
                'weak_count': weak_count
            }
        except Exception as e:
            print(f"⚠️ 跟踪龙头失败：{e}")
            return {'leaders': [], 'status': '跟踪失败', 'strong_count': 0, 'weak_count': 0}
    
    def get_main_force_with_trend(self):
        """
        获取主力资金流向，带趋势分析
        
        不仅看今日流入，还要看连续流入
        """
        try:
            today = datetime.now().strftime('%Y%m%d')
            result = pywencai.get(query=f'{today} 主力净流入排名', perpage=20)
            
            inflows = []
            if result is not None and len(result) > 0:
                for i in range(min(10, len(result))):
                    row = result.iloc[i]
                    
                    # 查找列
                    code = name = ''
                    inflow = change_pct = 0
                    
                    for col in result.columns:
                        if '代码' in col:
                            code = str(row[col])
                        elif '简称' in col:
                            name = str(row[col])
                        elif '主力' in col and '流向' in col:
                            try:
                                inflow = float(row[col])
                            except:
                                pass
                        elif '涨跌幅' in col:
                            try:
                                change_pct = float(row[col])
                            except:
                                pass
                    
                    # 检查是否在股票池中（连续流入）
                    consecutive = 1
                    for pool_stock in self.stock_pool.get('watching', []):
                        if pool_stock['code'] == code.split('.')[0]:
                            consecutive = pool_stock.get('consecutive_days', 0) + 1
                            break
                    
                    inflows.append({
                        'code': code.split('.')[0] if '.' in code else code,
                        'name': name,
                        'inflow': inflow,
                        'change_pct': change_pct,
                        'consecutive_days': consecutive
                    })
            
            # 更新股票池
            self.stock_pool['watching'] = inflows[:10]
            self._save_state(self.stock_pool_file, self.stock_pool)
            
            return inflows[:5]
        except Exception as e:
            print(f"⚠️ 获取主力资金失败：{e}")
            return []
    
    def generate_report(self, report_type='morning', date=None):
        """生成策略导向的报告"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        print("=" * 80)
        print(f"📊 生成策略报告 - {report_type} - {date}")
        print("=" * 80)
        
        # 获取市场情绪
        print("\n【1】获取市场情绪...")
        sentiment = self.get_market_sentiment()
        print(f"  ✅ 情绪评分：{sentiment['sentiment_score']} - {sentiment['stage']}")
        
        # 获取板块持续性
        print("\n【2】分析板块持续性...")
        sector = self.get_sector_continuity()
        print(f"  ✅ 主线板块：{len(sector['main_line'])} 个")
        
        # 获取龙头跟踪
        print("\n【3】跟踪龙头表现...")
        leaders = self.get_leader_tracking()
        print(f"  ✅ {leaders['status']}")
        
        # 获取主力资金
        print("\n【4】获取主力资金...")
        main_force = self.get_main_force_with_trend()
        print(f"  ✅ 获取到 {len(main_force)} 只主力股")
        
        # 生成报告
        content = self.format_report(report_type, date, sentiment, sector, leaders, main_force)
        
        # 保存
        today_dir = os.path.join(self.reports_dir, datetime.now().strftime('%Y-%m-%d'))
        os.makedirs(today_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%H%M')
        filename = f"{timestamp}_{report_type}.md"
        filepath = os.path.join(today_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ 报告已保存：{filepath}")
        return filepath, content
    
    def format_report(self, report_type, date, sentiment, sector, leaders, main_force):
        """格式化策略报告 - 优化排版"""
        lines = []
        
        # 标题
        if report_type == 'morning':
            title = "🌅 A 股策略早报"
            time_str = "08:00"
        elif report_type == 'evening':
            title = "🌙 A 股策略晚报"
            time_str = "20:00"
        else:
            title = "📊 A 股策略周报"
            time_str = ""
        
        lines.append(f"┌{'─' * 76}┐")
        lines.append(f"│  {title}{' ' * (70 - len(title))}│")
        lines.append(f"│  📅 {date} {time_str}{' ' * (65 - len(time_str))}│")
        lines.append(f"└{'─' * 76}┘")
        
        # 情绪周期
        lines.append("")
        lines.append("┌─ 📈 市场情绪 " + "─" * 64)
        score = sentiment['sentiment_score']
        score_bar = self._get_score_bar(score)
        lines.append(f"│  情绪评分：{score}/100  {score_bar}")
        lines.append(f"│  情绪阶段：{sentiment['stage']}")
        lines.append(f"│  涨跌停比：{sentiment['limit_up_count']} : {sentiment['limit_down_count']}")
        lines.append(f"│  连板高度：{sentiment['max_consecutive']}板")
        lines.append(f"│  操作建议：{sentiment['stage_advice']}")
        lines.append(f"│  仓位建议：{sentiment['position_advice']}%")
        lines.append("└" + "─" * 76)
        
        # 主线板块（连续强势）
        lines.append("")
        lines.append("┌─ 🔥 主线板块 (连续强势，可参与) " + "─" * 40)
        if sector['main_line']:
            for i, s in enumerate(sector['main_line'], 1):
                lines.append(f"│  {i}. {s['name']:<15} {s['consecutive_days']}日连涨  {s['change_pct']:>+7.2f}%")
        else:
            lines.append("│  ⚠️  暂无明确主线，谨慎参与")
        lines.append("└" + "─" * 76)
        
        # 新爆发板块
        if sector['new_hot']:
            lines.append("")
            lines.append("┌─ ⚡ 新爆发板块 (观察确认) " + "─" * 48)
            for i, s in enumerate(sector['new_hot'][:3], 1):
                lines.append(f"│  {i}. {s['name']:<15} {s['change_pct']:>+7.2f}%  → 等待 2 日确认")
            lines.append("└" + "─" * 76)
        
        # 龙头跟踪
        lines.append("")
        lines.append("┌─ 🐲 龙头跟踪 " + "─" * 64)
        lines.append(f"│  状态：{leaders['status']}")
        if leaders['leaders']:
            for l in leaders['leaders'][:5]:
                emoji = "✅" if l['status'] == '强' else ("❌" if l['status'] == '弱' else "➖")
                lines.append(f"│  {emoji} {l['code']} {l['name']:<10} {l['change_pct']:>+7.2f}%")
        else:
            lines.append("│  (数据积累中，第 1 天起开始跟踪)")
        lines.append("└" + "─" * 76)
        
        # 主力资金（连续流入）
        lines.append("")
        lines.append("┌─ 💰 主力资金 (连续流入) " + "─" * 52)
        if main_force:
            for i, m in enumerate(main_force, 1):
                days = "首现" if m['consecutive_days'] == 1 else f"{m['consecutive_days']}日"
                inflow_bn = m['inflow'] / 1e8
                lines.append(f"│  {i}. {m['code']} {m['name']:<10} 净流入{inflow_bn:>6.2f}亿  [{days:>3}]  {m['change_pct']:>+7.2f}%")
        else:
            lines.append("│  暂无数据")
        lines.append("└" + "─" * 76)
        
        # 策略建议
        lines.append("")
        lines.append("┌─ 📋 今日策略 " + "─" * 64)
        if sentiment['stage'] == '发酵期':
            lines.append("│  ① 主线板块回调低吸")
            lines.append("│  ② 龙头首阴可参与")
            lines.append("│  ③ 仓位 70-80%")
        elif sentiment['stage'] == '高潮期':
            lines.append("│  ① 持股待涨，不追高")
            lines.append("│  ② 分批兑现利润")
            lines.append("│  ③ 仓位降至 50-60%")
        elif sentiment['stage'] == '退潮期':
            lines.append("│  ① 空仓或轻仓观望")
            lines.append("│  ② 等待新周期信号")
            lines.append("│  ③ 仓位 20% 以下")
        else:
            lines.append("│  ① 轻仓试错新热点")
            lines.append("│  ② 等待主线确认")
            lines.append("│  ③ 仓位 40-50%")
        lines.append("└" + "─" * 76)
        
        # 风险提示
        lines.append("")
        lines.append("┌─ ⚠️ 风险提示 " + "─" * 64)
        if sector['fading'] and len(sector['fading']) > 0:
            fading_valid = [str(x) for x in sector['fading'][:3] if str(x) != 'nan' and x is not None]
            if fading_valid:
                lines.append(f"│  • 回避退潮板块：{', '.join(fading_valid)}")
        lines.append("│  • 单只股票 ≤ 总仓位 20%")
        lines.append("│  • 跌破 5 日线止损")
        lines.append("└" + "─" * 76)
        
        return "\n".join(lines)
    
    def _get_score_bar(self, score):
        """生成情绪评分进度条"""
        filled = int(score / 5)
        bar = "█" * filled + "░" * (20 - filled)
        if score >= 80:
            return f"[{bar}] 🔥"
        elif score >= 60:
            return f"[{bar}] 📈"
        elif score >= 40:
            return f"[{bar}] ➖"
        else:
            return f"[{bar}] 🛡️"


def send_to_feishu(content, report_type):
    """推送报告到飞书"""
    import subprocess
    
    titles = {
        'morning': '🌅 A 股策略早报',
        'evening': '🌙 A 股策略晚报',
        'weekly': '📊 A 股策略周报'
    }
    title = titles.get(report_type, '📈 A 股策略报告')
    
    message = f"{title}\n{content}"
    
    try:
        cmd = [
            'openclaw', 'message', 'send',
            '--channel', 'feishu',
            '--target', 'user:ou_63dec12dd1a535c7a6fed8557023ad10',
            '--message', message
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ 已推送到飞书：{title}")
            return True
        else:
            print(f"❌ 飞书推送失败：{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 飞书推送异常：{e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 generate_report_v4.py [morning|evening|weekly]")
        sys.exit(1)
    
    report_type = sys.argv[1]
    generator = StrategyReportGenerator()
    filepath, content = generator.generate_report(report_type)
    
    print("\n")
    print(content)
    
    # 自动推送
    print("\n" + "=" * 80)
    print("【飞书推送】")
    send_to_feishu(content, report_type)

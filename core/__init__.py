"""
A 股龙头战法策略系统 - 核心模块

包含：
- 涨停池数据获取
- 龙头股评分
- 市场情绪判断
- 仓位管理
- 板块分析
- 止损/目标位计算
- 飞书推送
"""

from .limit_up_data import (
    get_limit_up_pool,
    get_limit_down_pool,
    get_zt_pool_strength,
    get_sector_limit_up_stats
)

from .leader_scorer import (
    calculate_leader_score,
    identify_sector_leaders,
    get_leader_level,
    filter_leaders_by_level
)

from .market_sentiment import (
    calculate_sentiment_score,
    judge_sentiment_stage,
    get_stage_advice,
    calculate_position_advice,
    get_market_sentiment_full,
    format_sentiment_report
)

from .position_manager import (
    calculate_position_allocation,
    get_single_stock_limit,
    adjust_position_for_risk,
    format_position_report
)

from .sector_analysis import (
    SectorAnalyzer,
    analyze_sectors_full,
    format_sector_report
)

from .price_targets import (
    calculate_stop_loss,
    calculate_price_targets,
    calculate_trade_plan,
    format_trade_plan
)

from .feishu_sender import (
    send_to_feishu,
    send_report_to_feishu,
    send_alert_to_feishu,
    send_daily_summary
)

__all__ = [
    # 数据
    'get_limit_up_pool',
    'get_limit_down_pool',
    'get_zt_pool_strength',
    'get_sector_limit_up_stats',
    
    # 评分
    'calculate_leader_score',
    'identify_sector_leaders',
    'get_leader_level',
    'filter_leaders_by_level',
    
    # 情绪
    'calculate_sentiment_score',
    'judge_sentiment_stage',
    'get_stage_advice',
    'calculate_position_advice',
    'get_market_sentiment_full',
    'format_sentiment_report',
    
    # 仓位
    'calculate_position_allocation',
    'get_single_stock_limit',
    'adjust_position_for_risk',
    'format_position_report',
    
    # 板块
    'SectorAnalyzer',
    'analyze_sectors_full',
    'format_sector_report',
    
    # 目标位
    'calculate_stop_loss',
    'calculate_price_targets',
    'calculate_trade_plan',
    'format_trade_plan',
    
    # 推送
    'send_to_feishu',
    'send_report_to_feishu',
    'send_alert_to_feishu',
    'send_daily_summary'
]

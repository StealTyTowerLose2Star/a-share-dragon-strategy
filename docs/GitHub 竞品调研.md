# 龙头股选股系统 - GitHub/ClawHub 调研报告

## 📊 调研时间

**日期**: 2026-04-01

---

## 🔍 GitHub 相关项目

### 1. 连板策略项目

#### 🌟 NekolovePepper/Quant-Strategy-for-Consecutive-Limit-Up-Stocks
**Stars**: 2  
**URL**: https://github.com/NekolovePepper/Quant-Strategy-for-Consecutive-Limit-Up-Stocks

**描述**: 
- 构建量化"打板"策略， targeting 连续涨停股票
- 目标：通过日频择时交易实现持续 alpha
- 市场：中国 A 股

**技术栈**: Python + 量化框架

**参考价值**: ⭐⭐⭐⭐
- 专注于连板股策略
- 有完整的回测框架

---

#### 🌟 Topps-2025/Quantitative-Reversal-Breakout-Strategy-Based-on-Multi-Bar-N-Shaped-Pattern
**Stars**: 2  
**URL**: https://github.com/Topps-2025/Quantitative-Reversal-Breakout-Strategy-Based-on-Multi-Bar-N-Shaped-Pattern

**描述**: 
- N 字形涨停突破策略
- 识别涨停后低开再涨停的形态
- 量化投资方法

**参考价值**: ⭐⭐⭐
- 关注特定 K 线形态
- 可作为补充策略

---

#### 🌟 icezerowjj/UpperLimitStock
**Stars**: 3  
**URL**: https://github.com/icezerowjj/UpperLimitStock

**描述**: 
- 计算股票涨幅达 9% 后涨停的概率
- 目标市场：中国 A 股（10% 涨停）

**参考价值**: ⭐⭐⭐
- 概率预测模型
- 可用于打板决策

---

### 2. 综合量化平台

#### 🌟 zhaoxusun/stock-quant ⭐⭐⭐⭐⭐ (127 stars)
**URL**: https://github.com/zhaoxusun/stock-quant

**描述**: 
K 线数据获取 - 量化回测 - 数据分析 - 策略选股（A 股、港股、美股）

**功能**:
- ✅ 多市场数据获取
- ✅ 量化回测框架
- ✅ 策略选股
- ✅ 数据分析

**技术栈**: Python + 多种数据源

**参考价值**: ⭐⭐⭐⭐⭐
- 完整的量化平台
- 高 star 数，社区活跃
- 可借鉴架构设计

---

#### 🌟 sjzsdu/EventTrader (6 stars)
**URL**: https://github.com/sjzsdu/EventTrader

**描述**: 
中国 A 股市场量化分析，基于策略的选股收益分析

**参考价值**: ⭐⭐⭐
- 事件驱动策略
- 收益分析框架

---

#### 🌟 wuyihao022/a-stock-quant-strategy (2 stars)
**URL**: https://github.com/wuyihao022/a-stock-quant-strategy

**描述**: 
A 股量化交易策略 - 基于 AkShare 数据

**参考价值**: ⭐⭐⭐
- 基于 AkShare（与我们相同）
- 可参考数据获取方式

---

### 3. 其他相关项目

| 项目 | Stars | 描述 | 参考价值 |
|------|-------|------|----------|
| ps2keeper/a-stock-strategy | 0 | 多因子确认 + 持仓风险管理 | ⭐⭐⭐ |
| aug369/cn-stock-fund-analyzer | 0 | 股票基金分析平台 | ⭐⭐⭐ |
| Yushcheng777/Haili-stock-style | 0 | 海利选股风格增强 | ⭐⭐ |

---

## 📦 ClawHub/OpenClaw 现有技能

### 已安装技能（工作区）

#### 1. stock-market-hotspots 🔥
**路径**: `skills/stock-market-hotspots/`

**功能**:
- ✅ 行业板块涨跌幅排名
- ✅ N 日强势行业识别（3 日/5 日/10 日）
- ✅ 概念题材排名
- ✅ 龙头股筛选（综合评分系统）

**龙头股评分**:
```python
评分 = 市值 (40%) + 涨幅 (30%) + 成交量 (30%)
```

**参考价值**: ⭐⭐⭐⭐⭐
- **可直接复用**行业分析功能
- 龙头股筛选逻辑可参考
- 数据源相同（AKShare）

---

#### 2. stock-sector-strategy 📈
**路径**: `skills/stock-sector-strategy/`

**功能**:
- ✅ 宏观策略分析（GDP/CPI/PMI）
- ✅ 板块诊断（走势/估值）
- ✅ 行业配置建议（超配/低配）
- ✅ 多智能体协同分析

**参考价值**: ⭐⭐⭐⭐
- 宏观分析可补充龙头战法
- 板块轮动逻辑可借鉴

---

#### 3. stock-main-force-analysis 💰
**路径**: `skills/stock-main-force-analysis/`

**功能**:
- ✅ 主力资金流向分析
- ✅ 主力净流入/流出统计
- ✅ 主力持仓变化

**参考价值**: ⭐⭐⭐⭐
- 主力数据可增强龙头识别
- 资金流向是重要指标

---

#### 4. stock-technical-analysis 📊
**路径**: `skills/stock-technical-analysis/`

**功能**:
- ✅ 技术指标计算（MA/MACD/RSI）
- ✅ 技术面分析
- ✅ 买卖点识别

**参考价值**: ⭐⭐⭐
- 技术指标可作为辅助判断

---

#### 5. stock-value-investment 📈
**路径**: `skills/stock-value-investment/`

**功能**:
- ✅ 价值投资选股
- ✅ 基本面分析
- ✅ 估值筛选

**参考价值**: ⭐⭐
- 更适合 80% 稳健仓位
- 龙头战法不太适用

---

## 🎯 可复用的现有代码

### 高优先级（直接复用）

#### 1. stock-market-hotspots/hotspots.py
**可复用功能**:
```python
- 行业涨幅排名获取
- N 日强势行业识别
- 概念板块分析
- 龙头股初步筛选
```

**集成方式**: 
- 直接导入模块
- 作为数据源使用

---

#### 2. stock-main-force-analysis/analyzer.py
**可复用功能**:
```python
- 主力资金流向计算
- 主力净流入统计
- 大单/中单/小单分析
```

**集成方式**:
- 调用分析函数
- 作为龙头评分因子

---

### 中优先级（参考逻辑）

#### 3. stock-sector-strategy/strategist.py
**可参考**:
- 宏观分析框架
- 板块轮动逻辑
- 多角色分析模式

---

#### 4. stock-technical-analysis/analyzer.py
**可参考**:
- 技术指标计算
- 技术面评分
- 买卖点识别

---

## 📊 竞品分析总结

### GitHub 项目特点

**优势**:
- ✅ 有完整的回测框架
- ✅ 部分项目专注于连板策略
- ✅ 开源可学习

**劣势**:
- ❌ star 数普遍较低（<10）
- ❌ 缺少龙头战法完整实现
- ❌ 大多侧重量化回测，非实盘

**结论**: 
- **没有发现成熟的龙头战法开源项目**
- 我们的规划是**领先的**
- 可借鉴量化框架设计

---

### OpenClaw 现有技能特点

**优势**:
- ✅ 已有行业分析、主力分析功能
- ✅ 数据源统一（AKShare）
- ✅ 可直接复用

**劣势**:
- ❌ 缺少连板数、涨停时间等龙头核心指标
- ❌ 缺少情绪周期判断
- ❌ 缺少仓位动态调整

**结论**:
- **在现有技能基础上增强**是最佳路径
- 避免重复造轮子

---

## 🚀 我们的差异化优势

### 与 GitHub 项目对比

| 维度 | GitHub 项目 | 我们的系统 |
|------|------------|-----------|
| **龙头识别** | 简单市值/涨幅评分 | 5 维综合评分（连板/时间/带动/抗跌） |
| **情绪周期** | 无 | 启动/发酵/高潮/退潮 |
| **仓位管理** | 固定仓位 | 动态仓位（根据情绪） |
| **主线判断** | 单日涨幅 | 连续 N 日强势 |
| **实盘指导** | 回测为主 | 每日实战报告 |

**优势**: 更贴近实战、更系统化

---

### 与 OpenClaw 现有技能对比

| 维度 | 现有技能 | 龙头战法系统 |
|------|---------|-------------|
| **核心指标** | 市值/涨幅/成交量 | 连板数/涨停时间/封单金额 |
| **数据源** | AKShare/pywencai | AKShare（涨停池） |
| **持仓周期** | 中线（1-3 月） | 短线（3-10 天） |
| **风险等级** | 中风险 | 高风险 |
| **仓位配置** | 80% 稳健仓位 | 20% 打板仓位 |

**定位**: 互补而非替代

---

## 💡 开发建议

### 策略：站在巨人肩膀上

**Phase 1（第 1 周）**: 复用现有代码
```python
# 直接导入
from skills.stock_market_hotspots import analyze as analyze_hotspots
from skills.stock_main_force_analysis import analyze as analyze_main_force

# 获取行业热点
hotspots = await analyze_hotspots(top_n=10, lookback_days=5)

# 获取主力流向
main_force = await analyze_main_force(date='2026-04-01')
```

**Phase 2（第 2 周）**: 增强龙头识别
```python
# 新增 AKShare 涨停池数据
import akshare as ak
zt_df = ak.stock_zt_pool_em(date='20260401')

# 计算连板数、涨停时间、封单金额
# 实现龙头评分模型
```

**Phase 3（第 3 周）**: 整合输出
```python
# 整合情绪判断 + 主线板块 + 龙头股 + 仓位建议
# 生成每日报告
```

---

## 📋 具体复用清单

### 可直接导入的模块

```python
# 1. 行业分析
from skills.stock_market_hotspots.hotspots import (
    get_industry_ranking,      # 行业排名
    get_concept_ranking,       # 概念排名
    get_industry_leaders       # 行业龙头
)

# 2. 主力分析
from skills.stock_main_force_analysis.analyzer import (
    get_main_force_flow,       # 主力流向
    calculate_net_inflow       # 净流入计算
)

# 3. 技术分析
from skills.stock_technical_analysis.analyzer import (
    calculate_ma,              # 均线
    calculate_macd,            # MACD
    calculate_rsi              # RSI
)
```

### 需要新增的功能

```python
# 1. 涨停池数据
def get_limit_up_pool(date):
    import akshare as ak
    return ak.stock_zt_pool_em(date=date)

# 2. 龙头评分
def calculate_leader_score(stock_data):
    # 连板高度 (40%)
    # 涨停时间 (25%)
    # 带动效应 (20%)
    # 抗跌性 (15%)
    pass

# 3. 情绪周期
def calculate_market_sentiment():
    # 涨停数、跌停数、连板高度
    # 情绪评分、阶段判断
    pass

# 4. 仓位建议
def calculate_position_advice(sentiment_score, stage):
    # 根据情绪阶段返回仓位使用比例
    pass
```

---

## 🎯 最终架构

```
a-share-dragon-strategy/
├── scripts/
│   ├── generate_report_v5.py    # 增强版报告生成
│   └── ...
├── core/
│   ├── sentiment.py             # 情绪周期（新增）
│   ├── leader_detector.py       # 龙头识别（新增）
│   ├── sector_analysis.py       # 板块分析（复用 hotspots）
│   └── position_manager.py      # 仓位管理（新增）
├── data/
│   ├── akshare_data.py          # AKShare 数据（新增）
│   └── state_manager.py         # 状态管理（新增）
├── utils/
│   ├── format_utils.py          # 格式化（新增）
│   └── ...
└── state/
    ├── dragon_leaders.json
    └── sectors_history.json
```

---

## ⚠️ 注意事项

### 1. 数据源依赖

**AKShare 接口稳定性**:
- 涨停池接口：`stock_zt_pool_em`
- 板块行情接口：`stock_board_industry_name_em`
- 需监控接口变化

### 2. 与现有技能隔离

**独立仓库**: 
- 保持 `a-share-dragon-strategy` 独立
- 通过 import 复用代码
- 避免循环依赖

### 3. 实盘风险

**风险提示**:
- 龙头战法高风险（20% 仓位）
- 严格止损
- 不盲目追高

---

## 📚 参考资料

### GitHub 项目
- https://github.com/zhaoxusun/stock-quant
- https://github.com/NekolovePepper/Quant-Strategy-for-Consecutive-Limit-Up-Stocks

### OpenClaw 技能
- `skills/stock-market-hotspots/`
- `skills/stock-main-force-analysis/`
- `skills/stock-sector-strategy/`

### 数据源
- AKShare: https://akshare.akfamily.xyz/
- pywencai（同花顺问财）

---

**调研完成时间**: 2026-04-01  
**版本**: v1.0  
**结论**: 无成熟竞品，我们的规划领先，建议快速推进

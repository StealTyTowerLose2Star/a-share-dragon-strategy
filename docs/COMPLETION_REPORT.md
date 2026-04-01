# 龙头战法仓库创建完成 - 总结报告

## ✅ 已完成任务

### 1. 创建独立 GitHub 仓库

**仓库信息**：
- **名称**: `a-share-dragon-strategy`
- **URL**: https://github.com/StealTyTowerLose2Star/a-share-dragon-strategy
- **描述**: A 股龙头战法策略系统 - 专业的龙头股识别与跟踪系统
- **可见性**: Public（公开）
- **主分支**: `main`

### 2. 仓库文件结构

```
a-share-dragon-strategy/
├── .gitignore                      # Git 忽略配置
├── README.md                       # 项目说明文档（6.5KB）
├── requirements.txt                # Python 依赖
├── scripts/
│   ├── generate_report_v4.py       # 核心报告生成脚本（22KB）
│   └── generate_word_report.py     # Word 报告生成（3.7KB）
├── docs/
│   ├── strategy.md                 # 龙头战法策略详解（5.2KB）
│   └── GITHUB_SETUP.md             # GitHub 部署指南（3.1KB）
├── config/
│   └── .gitkeep                    # 占位文件
└── state/
    └── .gitkeep                    # 占位文件
```

### 3. Git 提交历史

```
commit 3219542 - Add GitHub deployment guide
commit b7a6621 - Initial commit: A 股龙头战法策略系统 v1.0
```

---

## 📊 核心功能说明

### 主线板块识别

基于市场共识的板块周期判断：
- **启动期**: 1-2 日，前 10，2-3 只涨停 → 轻仓试错
- **发酵期**: 3-5 日，前 5，5-10 只涨停 → 加仓主线
- **高潮期**: 6-10 日，前 3，10+ 只涨停 → 持股待涨
- **退潮期**: 热度下降 2 日+，跌出前 20，<2 只涨停 → 清仓观望

**主线确认标准**：
- 连续 3 日板块涨幅前 10 → 确认为主线
- 连续 2 日跌出前 20 → 退潮信号

### 龙头股识别模型

**核心特征（权重排序）**：
1. **连板高度**（40%）：板块内连板数最高，至少 3 连板
2. **涨停时间**（25%）：9:30-9:35 最佳，封单金额>1 亿
3. **带动效应**（20%）：龙头涨停后板块跟风股上涨
4. **抗跌性**（15%）：板块调整日龙头横盘或微跌

**龙头等级划分**：
- **总龙头**: 7+ 板，市场标杆，持有到断板
- **主线龙头**: 5-6 板，主线核心，持有到 5 日线
- **板块龙头**: 3-4 板，板块领涨，持有到 3 日线
- **补涨龙**: 1-2 板，龙头调整后，快进快出

### 综合评分模型

```python
龙头评分 = (
    板块地位分 * 35 +      # 板块内排名
    连板高度分 * 25 +      # 连板数
    涨停时间分 * 20 +      # 涨停早晚
    带动效应分 * 15 +      # 跟风股数量
    抗跌性分 * 5           # 调整日表现
)
```

**等级判定**：
- >= 80 分 → 总龙头（7 板+）
- 60-79 分 → 主线龙头（5-6 板）
- 40-59 分 → 板块龙头（3-4 板）
- < 40 分 → 补涨龙（1-2 板）

### 动态仓位管理

| 情绪评分 | 情绪阶段 | 总仓位 | 操作策略 |
|----------|----------|--------|----------|
| 80-100 | 高潮期 | 50-60% | 持股待涨，不追高 |
| 60-80 | 发酵期 | 70-80% | 加仓主线，积极参与 |
| 40-60 | 分歧期 | 40-50% | 轻仓试错，等待确认 |
| 0-40 | 退潮期 | 0-20% | 空仓防守，等待信号 |

---

## 🔧 技术栈

- **Python 3.10+**
- **AKShare**: 市场数据（涨停池、连板数、板块行情）
- **pywencai**: 问财数据（主力资金、板块涨幅）
- **python-docx**: Word 报告生成
- **pandas**: 数据处理

---

## 📝 使用方式

### 安装依赖

```bash
/home/linuxbrew/.linuxbrew/bin/python3.10 -m pip install akshare pywencai python-docx pandas
```

### 运行报告生成

```bash
cd a-share-dragon-strategy

# 生成晚报
/home/linuxbrew/.linuxbrew/bin/python3.10 scripts/generate_report_v4.py evening

# 生成早报
/home/linuxbrew/.linuxbrew/bin/python3.10 scripts/generate_report_v4.py morning

# 生成周报
/home/linuxbrew/.linuxbrew/bin/python3.10 scripts/generate_report_v4.py weekly
```

---

## 🎯 后续规划

### 短期（1-2 周）
- [ ] 完善龙头股识别算法
- [ ] 增加回测功能
- [ ] 添加可视化图表

### 中期（1-2 月）
- [ ] **长期投资选股策略模块**
- [ ] **中长期趋势跟踪系统**
- [ ] 多策略组合管理

### 长期（3-6 月）
- [ ] 机器学习优化评分模型
- [ ] 实时行情接入
- [ ] 自动化交易接口

---

## 📧 仓库链接

**GitHub**: https://github.com/StealTyTowerLose2Star/a-share-dragon-strategy

**克隆仓库**:
```bash
git clone https://github.com/StealTyTowerLose2Star/a-share-dragon-strategy.git
```

---

## ⚠️ 风险提示

1. **数据延迟**：免费数据源可能有 15 分钟延迟
2. **市场风险**：极端行情下策略可能失效
3. **个体差异**：推荐股票需结合个人风险偏好
4. **仅供参考**：不构成投资建议，盈亏自负

### 风控红线
- 单只股票 ≤ 总仓位 20%
- 跌破 5 日线减仓，跌破 10 日线清仓
- 主线退潮信号出现时及时止盈
- 退潮期保持空仓或轻仓（≤20%）

---

**创建时间**: 2026-04-01  
**版本**: v1.0  
**状态**: ✅ 已完成并推送到 GitHub

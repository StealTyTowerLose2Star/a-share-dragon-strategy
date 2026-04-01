# GitHub 仓库部署指南

## 方式一：使用 GitHub CLI（推荐）

### 安装 gh CLI

```bash
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y

# 验证安装
gh --version
```

### 认证 GitHub

```bash
gh auth login
# 选择 GitHub.com
# 选择 HTTPS
# 选择 Login with a web browser
# 按提示完成认证
```

### 创建并推送仓库

```bash
cd /home/admin/.openclaw/workspace/a-share-dragon-strategy

# 创建仓库并推送
gh repo create a-share-dragon-strategy --public --source=. --remote=origin --push
```

---

## 方式二：使用 Git 命令行

### 1. 在 GitHub 上创建仓库

访问 https://github.com/new

- **Repository name**: `a-share-dragon-strategy`
- **Description**: A 股龙头战法策略系统 - 专业的龙头股识别与跟踪系统
- **Visibility**: Public（公开）
- **不要** 勾选 "Add a README file"
- **不要** 勾选 "Add .gitignore"
- **不要** 勾选 "Choose a license"

点击 "Create repository"

### 2. 推送代码到 GitHub

```bash
cd /home/admin/.openclaw/workspace/a-share-dragon-strategy

# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/a-share-dragon-strategy.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 3. 验证推送

访问：https://github.com/YOUR_USERNAME/a-share-dragon-strategy

确认代码已成功推送。

---

## 方式三：使用 GitHub Desktop

1. 下载并安装 GitHub Desktop: https://desktop.github.com/
2. 登录 GitHub 账号
3. File → Add Local Repository → 选择 `/home/admin/.openclaw/workspace/a-share-dragon-strategy`
4. File → Publish repository
5. 设置仓库名称为 `a-share-dragon-strategy`
6. 点击 "Publish repository"

---

## 推送完成后的操作

### 1. 设置 GitHub Pages（可选）

如果希望在线查看文档：

1. 进入仓库 Settings → Pages
2. Source 选择 "Deploy from a branch"
3. Branch 选择 "main"，文件夹选择 "/ (root)"
4. 点击 Save

访问：https://YOUR_USERNAME.github.io/a-share-dragon-strategy/

### 2. 添加 Topics

在仓库主页，点击 "Manage topics"，添加：

- `a-share`
- `dragon-strategy`
- `stock-analysis`
- `trading-system`
- `python`
- `quantitative-trading`

### 3. 保护主分支（推荐）

1. Settings → Branches → Add branch protection rule
2. Branch name pattern: `main`
3. 勾选 "Require a pull request before merging"
4. 点击 Create

---

## 仓库信息

### 仓库名称
`a-share-dragon-strategy`

### 仓库描述
```
A 股龙头战法策略系统 - 专业的龙头股识别与跟踪系统

核心功能：
- 主线板块识别（连续强势分析）
- 龙头股评分模型（连板高度/涨停时间/带动效应/抗跌性）
- 情绪周期判断（启动/发酵/高潮/退潮）
- 动态仓位建议
- 自动报告生成（早报/午报/晚报/周报）

基于市场共识和游资战法逻辑，科学识别龙头股，提供买卖点建议。
```

### 许可证
MIT License

---

## 当前仓库状态

```bash
cd /home/admin/.openclaw/workspace/a-share-dragon-strategy
git log --oneline
```

当前提交：
- Initial commit: A 股龙头战法策略系统 v1.0

文件结构：
```
a-share-dragon-strategy/
├── .gitignore
├── README.md
├── config/
│   └── .gitkeep
├── docs/
│   └── strategy.md
├── requirements.txt
├── scripts/
│   ├── generate_report_v4.py
│   └── generate_word_report.py
└── state/
    └── .gitkeep
```

---

## 后续步骤

1. **创建 GitHub 仓库**（按上述方式之一）
2. **推送代码**
3. **发送仓库链接给用户**

仓库 URL 格式：
```
https://github.com/YOUR_USERNAME/a-share-dragon-strategy
```

---

**创建时间**: 2026-04-01  
**版本**: v1.0

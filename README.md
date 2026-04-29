# 🌏 华域 AI · HuaYu Agent

**海外华人内容营销自动化平台 | Overseas Chinese Content Marketing Automation**

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![MoonshotAI](https://img.shields.io/badge/LLM-MoonshotAI-purple)](https://moonshot.cn)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 项目简介

华域 AI 是一套面向**海外华人市场**的 AI 驱动内容营销自动化系统，专为推广 CPS 平台（右豹、番茄小说、UC书城等）的短剧与小说内容而构建。

系统通过多 LLM API（MoonshotAI + Claude）自动生成适配 TikTok、YouTube、Instagram、小红书等平台的推广文案，并通过 n8n 工作流实现多账号矩阵分发。

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🤖 内容生成 Agent | 调用 MoonshotAI API，基于剧目信息+平台风格+受众画像生成文案 |
| 🌐 多平台适配 | 自动适配 TikTok / YouTube / Instagram / 小红书格式规范 |
| 🗺️ 地区受众定制 | 针对东南亚/北美/澳新/欧洲华人社群差异化内容策略 |
| 📊 批量生产 | 支持多剧目 × 多平台 × 多地区的矩阵式内容生产 |
| 🔁 数据回流优化 | 抓取互动数据，LLM 分析爆款规律，自动优化策略 |

## 🏗️ 系统架构

```
数据抓取层 (Scraper)
    ↓
CPS热榜数据 (右豹/番茄/UC)
    ↓
LLM内容生成层 (MoonshotAI + Claude API)
    ↓
多平台内容适配器
    ↓
n8n自动化工作流
    ↓
账号矩阵分发 (50+ 账号)
    ↓
数据回流 → 优化闭环
```

## 🚀 快速开始

```bash
git clone https://github.com/yourusername/huayu-agent
cd huayu-agent
pip install -r requirements.txt
export MOONSHOT_API_KEY="your_key_here"
python agent.py
```

## 📦 依赖

```
openai>=1.0.0        # Moonshot OpenAI-compatible API
anthropic>=0.20.0    # Claude API
python-dotenv>=1.0.0
requests>=2.31.0
n8n (workflow automation)
```

## 📊 运行指标

- 日均内容生成：**2,400+ 条**
- 月均 Token 消耗：**~1.2 亿 tokens**
- 覆盖账号矩阵：**50+ 账号**
- 月触达华人用户：**15 万+**
- 目标市场：东南亚、北美、澳新华人社区

## 🛠️ Tech Stack

- **LLM**: MoonshotAI `moonshot-v1-8k` + Anthropic Claude
- **Automation**: n8n + Dify
- **Backend**: Python 3.11
- **Database**: PostgreSQL + Redis
- **Infrastructure**: Docker + VPS

## 📁 项目结构

```
huayu-agent/
├── agent.py              # 核心 Agent 逻辑
├── scraper.py            # CPS 平台数据抓取
├── platforms/
│   ├── tiktok.py
│   ├── youtube.py
│   ├── instagram.py
│   └── xiaohongshu.py
├── workflow/
│   └── n8n_workflow.json # n8n 工作流配置
├── output/               # 生成内容输出
└── README.md
```

## 📄 License

MIT License

---

> 本项目用于合法 CPS 内容推广，遵守各平台服务条款。

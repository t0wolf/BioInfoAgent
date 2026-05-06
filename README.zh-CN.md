# BioInfo Agent

> AI 驱动的生物信息学分析平台

[English](README.md) | [中文](README.zh-CN.md)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Anthropic](https://img.shields.io/badge/Claude-API-D97706.svg)](https://anthropic.com)

BioInfo Agent 是一个基于 AI 的交互式生物信息学分析平台。它将对话式智能助手（Claude）与丰富的生物信息学工具相结合，通过直观的 Streamlit Web 界面，一站式完成转录组分析、序列分析、富集分析、数据库查询等任务。

---

## 功能特性

### 核心分析模块

| 模块 | 说明 |
|------|------|
| **智能对话** | 用自然语言描述分析需求，Agent 自动设计并解释分析流程 |
| **转录组分析** | 上传表达矩阵或生成示例数据 → PCA、热图、差异表达、火山图 |
| **序列分析** | GC 含量、ORF 查找、核苷酸组成、滑动窗口分析 |
| **富集分析** | GO / KEGG 通路富集分析，交互式气泡图 |
| **数据库查询** | 直接搜索 NCBI Gene、Ensembl、UniProt 数据库 |
| **格式转换** | 自动识别并解析 FASTA、FASTQ、BED、GTF、GFF、VCF 文件 |
| **可视化** | 交互式 Plotly 图表 — 火山图、热图、PCA、相关性矩阵 |
| **报告导出** | 一键生成 HTML 分析报告并下载 |

### 产品亮点

- **中英文双语界面** — 一键切换，所有 UI 文本完整覆盖
- **AI 智能驱动** — 集成 Claude API，智能解读分析结果、规划分析流程
- **无需数据即可体验** — 内置示例数据生成器，开箱即用
- **发表级图表** — 基于 Plotly 的交互式高质量可视化
- **模块化架构** — 易于扩展新的分析工具和流程

---

## 快速开始

### 环境要求

- Python 3.10+
- conda（推荐）或 pip

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/bioinfo-agent.git
cd bioinfo-agent

# 方式一：使用 conda（推荐）
conda create -n bioinfo-agent python=3.11 -y
conda activate bioinfo-agent
pip install -r requirements.txt

# 方式二：直接使用 pip
pip install -r requirements.txt
```

### 启动

```bash
# 激活环境（如果使用 conda）
conda activate bioinfo-agent

# 启动应用
streamlit run app.py
```

然后在浏览器中打开 **http://localhost:8501**。

---

## 使用指南

### 1. 智能对话

用自然语言描述你的分析需求：

> "我有肿瘤和正常样本的 paired-end RNA-seq 数据，想找到差异表达基因并做通路富集分析。"

Agent 会为你设计分析流程、解释每个步骤，并引导你完成分析。

### 2. 转录组分析

1. 在侧边栏进入 **转录组分析**
2. 上传表达矩阵（CSV/TSV）或点击 **生成示例数据**
3. 分配样本分组（对照 / 处理）
4. 运行差异表达分析
5. 查看火山图、Top 差异基因，运行 GO 富集分析

### 3. 序列分析

1. 进入 **序列分析**
2. 粘贴 DNA 序列或上传 FASTA 文件
3. 查看 GC 含量、ORF、核苷酸组成和滑动窗口 GC 分布图

### 4. 富集分析

1. 粘贴基因列表或从差异分析结果导入
2. 选择 GO 或 KEGG 数据库
3. 查看富集气泡图和详细结果表格
4. 使用 **AI 智能解读** 获取生物学背景信息

### 5. 数据库查询

无需离开应用，直接搜索 NCBI、Ensembl 或 UniProt 的基因/蛋白信息。

### 6. 格式转换

上传任意生物信息学文件 — 转换器自动识别格式、验证数据并解析内容。

---

## API 密钥（可选）

要启用 AI 对话助手和智能结果解读功能：

1. 从 [Anthropic 控制台](https://console.anthropic.com/) 或兼容的第三方服务商获取 API 密钥
2. 在侧边栏的 **设置** 区域输入密钥

### 支持的接口

| 提供商 | 配置方式 |
|--------|----------|
| **Anthropic 官方** | 选择「Anthropic 官方」预设，输入 API 密钥 |
| **小米 MiMo** | 选择「小米 MiMo」预设，输入 MiMo API 密钥 |
| **自定义** | 选择「自定义」预设，填入 Base URL 和模型名称 |

应用兼容所有遵循 [Anthropic Messages API](https://docs.anthropic.com/en/api/messages) 协议的接口。

即使没有 API 密钥，所有分析工具仍然可以正常使用 — 仅 AI 对话和智能解读功能受限。

---

## 项目结构

```
bioinfo-agent/
├── app.py                  # Streamlit 主应用
├── i18n.py                 # 国际化模块（中文 / 英文）
├── requirements.txt        # Python 依赖
│
├── agent/                  # AI Agent 核心
│   ├── core.py             # Agent 主循环（Claude API 集成）
│   ├── planner.py          # 流程规划（RNA-seq、ChIP-seq、Variant）
│   └── prompts.py          # Claude 系统提示词
│
├── tools/                  # 分析工具
│   ├── sequence.py         # 序列分析（GC、ORF、组成）
│   ├── rnaseq.py           # 转录组差异表达（类 DESeq2）
│   ├── enrichment.py       # GO / KEGG 富集分析
│   └── database.py         # NCBI、Ensembl、UniProt API 客户端
│
├── formats/                # 文件格式处理
│   ├── converter.py        # 格式自动检测与转换
│   └── validator.py        # 数据验证（FASTA、FASTQ、VCF）
│
├── report/                 # 报告生成
│   ├── plots.py            # Plotly 可视化引擎
│   └── generator.py        # HTML 报告构建器
│
└── examples/               # 示例数据
    ├── sample_counts.csv   # 示例表达矩阵
    └── sample.fasta        # 示例 FASTA 序列
```

---

## 技术栈

| 组件 | 技术 |
|------|------|
| Web 框架 | Streamlit |
| AI 引擎 | Claude API (Anthropic) |
| 可视化 | Plotly |
| 数据处理 | Pandas、NumPy、SciPy |
| 生物信息 | Biopython |
| 机器学习 | scikit-learn（PCA） |
| 统计分析 | statsmodels（多重检验校正） |

---

## 开发计划

- [ ] 导出 Snakemake / Nextflow 流程
- [ ] 单细胞转录组（scRNA-seq）分析
- [ ] ChIP-seq Peak Calling 工作流
- [ ] 变异注释（ANNOVAR / VEP 集成）
- [ ] 原始 FASTQ 上传与 QC 流程
- [ ] 多用户项目管理
- [ ] Docker 部署支持

---

## 参与贡献

欢迎参与贡献！步骤如下：

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m '添加某个功能'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 提交 Pull Request

请确保同步更新相关测试，并遵循现有代码风格。

---

## 开源许可

本项目基于 MIT 许可证开源 — 详见 [LICENSE](LICENSE) 文件。

---

## 致谢

- [Streamlit](https://streamlit.io/) — 优秀的 Web 框架
- [Anthropic](https://anthropic.com/) — Claude API
- [Biopython](https://biopython.org/) — 生物信息学工具库
- [Plotly](https://plotly.com/python/) — 交互式可视化

---

<p align="center">
  为生物信息学社区用心打造
</p>

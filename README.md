# BioInfo Agent

> AI-Powered Bioinformatics Analysis Platform

[English](README.md) | [中文](README.zh-CN.md)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Anthropic](https://img.shields.io/badge/Claude-API-D97706.svg)](https://anthropic.com)

BioInfo Agent is an interactive bioinformatics analysis platform powered by AI. It combines a conversational agent (Claude) with a rich set of bioinformatics tools, offering an intuitive Streamlit web interface for RNA-seq analysis, sequence analysis, enrichment analysis, database queries, and more — all in one place.

---

## Features

### Interactive Analysis

| Module | Description |
|--------|-------------|
| **Chat Agent** | Describe your analysis needs in natural language; the agent designs and explains pipelines for you |
| **RNA-seq Analysis** | Upload count matrices or generate demo data → PCA, heatmap, differential expression, volcano plots |
| **Sequence Analysis** | GC content, ORF finding, nucleotide composition, sliding window analysis |
| **Enrichment Analysis** | GO / KEGG pathway enrichment with interactive dot plots |
| **Database Query** | Search NCBI Gene, Ensembl, and UniProt databases directly |
| **Format Converter** | Auto-detect and parse FASTA, FASTQ, BED, GTF, GFF, VCF files |
| **Visualization** | Interactive Plotly charts — volcano, heatmap, PCA, correlation matrix |
| **Report Export** | One-click HTML report generation with download |

### Key Highlights

- **Bilingual UI** — Full Chinese / English support with one-click language switching
- **AI-Powered** — Integrates Claude API for intelligent result interpretation and pipeline planning
- **No Setup Required for Demo** — Built-in demo data generator lets you explore all features immediately
- **Publication-Quality Plots** — Plotly-based interactive visualizations
- **Modular Architecture** — Easy to extend with new analysis tools and pipelines

---

## Quick Start

### Prerequisites

- Python 3.10+
- conda (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bioinfo-agent.git
cd bioinfo-agent

# Option A: Using conda (recommended)
conda create -n bioinfo-agent python=3.11 -y
conda activate bioinfo-agent
pip install -r requirements.txt

# Option B: Using pip directly
pip install -r requirements.txt
```

### Run

```bash
# Activate environment (if using conda)
conda activate bioinfo-agent

# Start the application
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## Usage Guide

### 1. Chat Agent

Describe your analysis in natural language:

> "I have paired-end RNA-seq data from tumor and normal samples. I want to find differentially expressed genes and do pathway enrichment."

The agent will design a pipeline, explain each step, and guide you through the analysis.

### 2. RNA-seq Analysis

1. Go to **RNA-seq Analysis** in the sidebar
2. Upload a count matrix (CSV/TSV) or click **Generate Demo Data**
3. Assign sample groups (Control / Treatment)
4. Run differential expression analysis
5. Explore volcano plots, top DE genes, and run GO enrichment

### 3. Sequence Analysis

1. Go to **Sequence Analysis**
2. Paste a DNA sequence or upload a FASTA file
3. View GC content, ORFs, nucleotide composition, and sliding window GC plots

### 4. Enrichment Analysis

1. Paste a gene list or import from DE results
2. Select GO or KEGG database
3. View enrichment dot plots and detailed result tables
4. Use **AI Interpretation** for biological context

### 5. Database Query

Search NCBI, Ensembl, or UniProt for gene/protein information without leaving the app.

### 6. Format Converter

Upload any bioinformatics file — the converter auto-detects the format, validates it, and parses the content.

---

## API Key (Optional)

To enable the AI chat agent and intelligent result interpretation:

1. Get an API key from [Anthropic Console](https://console.anthropic.com/) or a compatible provider
2. Enter it in the **Settings** section of the sidebar

### Supported Providers

| Provider | Setup |
|----------|-------|
| **Anthropic Official** | Select "Anthropic Official" preset, enter your API key |
| **Xiaomi MiMo** | Select "Xiaomi MiMo" preset, enter your MiMo API key |
| **Custom** | Select "Custom" preset, enter the base URL and model name |

The app is compatible with any API endpoint that follows the [Anthropic Messages API](https://docs.anthropic.com/en/api/messages) protocol.

Without an API key, all analysis tools still work — only the AI chat and interpretation features are limited.

---

## Project Structure

```
bioinfo-agent/
├── app.py                  # Streamlit main application
├── i18n.py                 # Internationalization (Chinese / English)
├── requirements.txt        # Python dependencies
│
├── agent/                  # AI agent core
│   ├── core.py             # Agent main loop (Claude API integration)
│   ├── planner.py          # Pipeline planning (RNA-seq, ChIP-seq, Variant)
│   └── prompts.py          # System prompts for Claude
│
├── tools/                  # Analysis tools
│   ├── sequence.py         # Sequence analysis (GC, ORF, composition)
│   ├── rnaseq.py           # RNA-seq differential expression (DESeq2-like)
│   ├── enrichment.py       # GO / KEGG enrichment analysis
│   └── database.py         # NCBI, Ensembl, UniProt API clients
│
├── formats/                # File format handling
│   ├── converter.py        # Format auto-detection and conversion
│   └── validator.py        # Data validation (FASTA, FASTQ, VCF)
│
├── report/                 # Report generation
│   ├── plots.py            # Plotly visualization engine
│   └── generator.py        # HTML report builder
│
└── examples/               # Sample data files
    ├── sample_counts.csv   # Example count matrix
    └── sample.fasta        # Example FASTA sequences
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Web Framework | Streamlit |
| AI Engine | Claude API (Anthropic) |
| Visualization | Plotly |
| Data Processing | Pandas, NumPy, SciPy |
| Bioinformatics | Biopython |
| Machine Learning | scikit-learn (PCA) |
| Statistics | statsmodels (multiple testing correction) |

---

## Roadmap

- [ ] Snakemake / Nextflow pipeline export
- [ ] Single-cell RNA-seq (scRNA-seq) analysis
- [ ] ChIP-seq peak calling workflow
- [ ] Variant annotation (ANNOVAR / VEP integration)
- [ ] File upload for raw FASTQ with QC pipeline
- [ ] Multi-user project management
- [ ] Docker deployment support

---

## Contributing

Contributions are welcome! Here's how:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and follow the existing code style.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Streamlit](https://streamlit.io/) — for the amazing web framework
- [Anthropic](https://anthropic.com/) — for the Claude API
- [Biopython](https://biopython.org/) — for bioinformatics utilities
- [Plotly](https://plotly.com/python/) — for interactive visualizations

---

<p align="center">
  Made with care for the bioinformatics community
</p>

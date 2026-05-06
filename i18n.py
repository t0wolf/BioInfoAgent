"""Internationalization (i18n) support for BioInfo Agent."""

TRANSLATIONS = {
    # ── Header ──
    "app_title": {
        "zh": "🧬 生物信息智能分析平台",
        "en": "🧬 BioInfo Agent",
    },
    "app_subtitle": {
        "zh": "AI 驱动的生物信息学分析平台",
        "en": "AI-Powered Bioinformatics Analysis Platform",
    },

    # ── Sidebar ──
    "sidebar_title": {
        "zh": "🧬 生信智能助手",
        "en": "🧬 BioInfo Agent",
    },
    "settings": {
        "zh": "⚙️ 设置",
        "en": "⚙️ Settings",
    },
    "api_key_label": {
        "zh": "Anthropic API 密钥",
        "en": "Anthropic API Key",
    },
    "api_key_help": {
        "zh": "输入 API 密钥以启用 AI 智能分析功能",
        "en": "Enter your API key to enable AI-powered analysis",
    },
    "analysis_tools": {
        "zh": "📋 分析工具",
        "en": "📋 Analysis Tools",
    },
    "data_status": {
        "zh": "📊 数据状态",
        "en": "📊 Data Status",
    },
    "language_label": {
        "zh": "🌐 语言",
        "en": "🌐 Language",
    },
    "api_base_url_label": {
        "zh": "API Base URL（可选）",
        "en": "API Base URL (optional)",
    },
    "api_base_url_help": {
        "zh": "留空使用官方 Anthropic API，或填入第三方兼容接口地址（如 MiMo）",
        "en": "Leave empty for official Anthropic API, or enter a compatible endpoint (e.g. MiMo)",
    },
    "model_label": {
        "zh": "模型名称",
        "en": "Model Name",
    },
    "model_help": {
        "zh": "输入要使用的模型 ID，留空使用默认值",
        "en": "Enter the model ID to use, leave empty for default",
    },
    "provider_preset": {
        "zh": "接口预设",
        "en": "Provider Preset",
    },
    "provider_official": {
        "zh": "Anthropic 官方",
        "en": "Anthropic Official",
    },
    "provider_mimo": {
        "zh": "小米 MiMo",
        "en": "Xiaomi MiMo",
    },
    "provider_custom": {
        "zh": "自定义",
        "en": "Custom",
    },
    "provider_presets": {
        "zh": "接口预设",
        "en": "Provider Preset",
    },

    # ── Navigation ──
    "nav_chat": {
        "zh": "💬 智能对话",
        "en": "💬 Chat Agent",
    },
    "nav_rnaseq": {
        "zh": "📊 转录组分析",
        "en": "📊 RNA-seq Analysis",
    },
    "nav_sequence": {
        "zh": "🔬 序列分析",
        "en": "🔬 Sequence Analysis",
    },
    "nav_enrichment": {
        "zh": "🔍 富集分析",
        "en": "🔍 Enrichment Analysis",
    },
    "nav_database": {
        "zh": "🌐 数据库查询",
        "en": "🌐 Database Query",
    },
    "nav_converter": {
        "zh": "🔄 格式转换",
        "en": "🔄 Format Converter",
    },
    "nav_upload": {
        "zh": "📁 数据上传",
        "en": "📁 Data Upload",
    },
    "nav_visualization": {
        "zh": "📈 可视化",
        "en": "📈 Visualization",
    },
    "nav_report": {
        "zh": "📄 分析报告",
        "en": "📄 Report",
    },

    # ── Metrics ──
    "genes": {
        "zh": "基因数",
        "en": "Genes",
    },
    "samples": {
        "zh": "样本数",
        "en": "Samples",
    },
    "de_up": {
        "zh": "上调基因",
        "en": "DE Genes (UP)",
    },
    "de_down": {
        "zh": "下调基因",
        "en": "DE Genes (DOWN)",
    },
    "total_counts": {
        "zh": "总计数",
        "en": "Total Counts",
    },
    "genes_detected": {
        "zh": "检测到的基因",
        "en": "Genes Detected",
    },

    # ── Chat page ──
    "chat_title": {
        "zh": "## 💬 与生信智能助手对话",
        "en": "## 💬 Chat with BioInfo Agent",
    },
    "chat_subtitle": {
        "zh": "随时向我提问生物信息学分析相关的问题！",
        "en": "Ask me anything about bioinformatics analysis!",
    },
    "chat_placeholder": {
        "zh": "描述你的分析需求，例如：我有 RNA-seq 数据，想做差异表达分析...",
        "en": "Describe your analysis needs, e.g.: I have RNA-seq data and want to do differential expression analysis...",
    },
    "quick_actions": {
        "zh": "### 快捷操作",
        "en": "### Quick Actions",
    },
    "btn_rnaseq_pipeline": {
        "zh": "📋 RNA-seq 流程",
        "en": "📋 RNA-seq Pipeline",
    },
    "btn_chipseq_pipeline": {
        "zh": "📋 ChIP-seq 流程",
        "en": "📋 ChIP-seq Pipeline",
    },
    "btn_variant_pipeline": {
        "zh": "📋 变异检测流程",
        "en": "📋 Variant Calling",
    },

    # ── RNA-seq page ──
    "rnaseq_title": {
        "zh": "## 📊 转录组差异表达分析",
        "en": "## 📊 RNA-seq Differential Expression Analysis",
    },
    "data_source": {
        "zh": "数据来源",
        "en": "Data Source",
    },
    "upload_count_matrix": {
        "zh": "上传表达矩阵",
        "en": "Upload Count Matrix",
    },
    "generate_demo": {
        "zh": "生成示例数据",
        "en": "Generate Demo Data",
    },
    "n_genes": {
        "zh": "基因数量",
        "en": "Number of genes",
    },
    "n_samples": {
        "zh": "样本数量",
        "en": "Number of samples",
    },
    "btn_generate": {
        "zh": "生成数据",
        "en": "Generate Data",
    },
    "btn_upload_matrix": {
        "zh": "上传表达矩阵 (CSV/TSV)",
        "en": "Upload count matrix (CSV/TSV)",
    },
    "data_preview": {
        "zh": "📋 数据预览",
        "en": "📋 Data Preview",
    },
    "tab_distribution": {
        "zh": "📊 样本分布",
        "en": "📊 Distribution",
    },
    "tab_pca": {
        "zh": "🧬 PCA 分析",
        "en": "🧬 PCA",
    },
    "tab_heatmap": {
        "zh": "🔥 热图",
        "en": "🔥 Heatmap",
    },
    "assign_groups": {
        "zh": "### 分配样本分组",
        "en": "### Assign Sample Groups",
    },
    "control_samples": {
        "zh": "对照组样本",
        "en": "Control samples",
    },
    "treatment_samples": {
        "zh": "处理组样本",
        "en": "Treatment samples",
    },
    "btn_run_de": {
        "zh": "运行差异表达分析",
        "en": "Run DE Analysis",
    },
    "de_title": {
        "zh": "### 差异表达分析",
        "en": "### Differential Expression Analysis",
    },
    "upregulated": {
        "zh": "上调",
        "en": "Upregulated",
    },
    "downregulated": {
        "zh": "下调",
        "en": "Downregulated",
    },
    "total_de": {
        "zh": "总计 DE",
        "en": "Total DE",
    },
    "top_de_genes": {
        "zh": "### 差异表达基因 Top 列表",
        "en": "### Top DE Genes",
    },
    "btn_go_enrichment": {
        "zh": "运行 GO 富集分析",
        "en": "Run GO Enrichment",
    },
    "select_both_groups": {
        "zh": "请选择对照组和处理组样本",
        "en": "Please select both control and treatment samples",
    },
    "de_complete": {
        "zh": "差异表达分析完成！",
        "en": "DE analysis complete!",
    },
    "enrichment_complete": {
        "zh": "富集分析完成！",
        "en": "Enrichment analysis complete!",
    },

    # ── Sequence page ──
    "seq_title": {
        "zh": "## 🔬 序列分析",
        "en": "## 🔬 Sequence Analysis",
    },
    "tab_seq_input": {
        "zh": "📝 序列输入",
        "en": "📝 Sequence Input",
    },
    "tab_orf": {
        "zh": "🔍 ORF 查找",
        "en": "🔍 ORF Finder",
    },
    "tab_composition": {
        "zh": "📊 组成分析",
        "en": "📊 Composition",
    },
    "seq_input_label": {
        "zh": "输入 DNA/RNA 序列或上传 FASTA 文件：",
        "en": "Enter a DNA/RNA sequence or upload a FASTA file:",
    },
    "seq_placeholder": {
        "zh": "ATGCGATCGATCGATCG...",
        "en": "ATGCGATCGATCGATCG...",
    },
    "upload_fasta": {
        "zh": "或上传 FASTA 文件",
        "en": "Or upload FASTA",
    },
    "gc_content": {
        "zh": "GC 含量",
        "en": "GC Content",
    },
    "orfs_found": {
        "zh": "ORF 数",
        "en": "ORFs Found",
    },
    "length": {
        "zh": "长度",
        "en": "Length",
    },
    "found_orfs": {
        "zh": "### 发现 {n} 个 ORF",
        "en": "### Found {n} ORFs",
    },
    "no_orfs": {
        "zh": "未找到超过最小长度阈值的 ORF",
        "en": "No ORFs found above minimum length threshold",
    },
    "enter_seq_first": {
        "zh": "请先输入序列",
        "en": "Enter a sequence first",
    },
    "nucleotide_composition": {
        "zh": "核苷酸组成",
        "en": "Nucleotide Composition",
    },
    "gc_sliding_window": {
        "zh": "GC 含量分布（滑动窗口: {w}bp）",
        "en": "GC Content (sliding window: {w}bp)",
    },

    # ── Enrichment page ──
    "enrichment_title": {
        "zh": "## 🔍 富集分析",
        "en": "## 🔍 Enrichment Analysis",
    },
    "input_method": {
        "zh": "输入方式",
        "en": "Input Method",
    },
    "gene_list_input": {
        "zh": "基因列表",
        "en": "Gene List",
    },
    "from_de_results": {
        "zh": "从差异分析结果",
        "en": "From DE Results",
    },
    "enter_genes": {
        "zh": "输入基因名（每行一个或逗号分隔）",
        "en": "Enter gene names (one per line or comma-separated)",
    },
    "select_genes": {
        "zh": "选择基因集",
        "en": "Select genes",
    },
    "all_de": {
        "zh": "所有差异基因",
        "en": "All DE",
    },
    "using_n_genes": {
        "zh": "使用 {n} 个{type}基因",
        "en": "Using {n} {type} genes",
    },
    "no_de_warning": {
        "zh": "没有差异分析结果，请先运行转录组分析",
        "en": "No DE results available. Run RNA-seq analysis first.",
    },
    "genes_loaded": {
        "zh": "**{n} 个基因**已加载",
        "en": "**{n} genes** loaded",
    },
    "database_label": {
        "zh": "数据库",
        "en": "Database",
    },
    "btn_run_enrichment": {
        "zh": "运行富集分析",
        "en": "Run Enrichment",
    },
    "enrichment_found": {
        "zh": "发现 {n} 个富集通路",
        "en": "Found {n} enriched terms",
    },
    "no_enrichment": {
        "zh": "未发现显著富集",
        "en": "No significant enrichment found",
    },
    "total_terms": {
        "zh": "总通路数",
        "en": "Total Terms",
    },
    "significant_terms": {
        "zh": "显著 (p<0.05)",
        "en": "Significant (p<0.05)",
    },
    "top_enrichment": {
        "zh": "最高富集",
        "en": "Top Enrichment",
    },
    "enrichment_results": {
        "zh": "### 富集分析结果",
        "en": "### Enrichment Results",
    },
    "btn_ai_interpret": {
        "zh": "🤖 AI 智能解读",
        "en": "🤖 AI Interpretation",
    },

    # ── Database page ──
    "db_title": {
        "zh": "## 🌐 数据库查询",
        "en": "## 🌐 Database Query",
    },
    "search_ncbi": {
        "zh": "### 搜索 NCBI 基因数据库",
        "en": "### Search NCBI Gene Database",
    },
    "gene_name_placeholder": {
        "zh": "基因名或符号",
        "en": "Gene name or symbol",
    },
    "btn_search_ncbi": {
        "zh": "搜索 NCBI",
        "en": "Search NCBI",
    },
    "search_ensembl": {
        "zh": "### 搜索 Ensembl",
        "en": "### Search Ensembl",
    },
    "gene_symbol_placeholder": {
        "zh": "基因符号",
        "en": "Gene symbol",
    },
    "btn_search_ensembl": {
        "zh": "搜索 Ensembl",
        "en": "Search Ensembl",
    },
    "search_uniprot": {
        "zh": "### 搜索 UniProt",
        "en": "### Search UniProt",
    },
    "protein_placeholder": {
        "zh": "蛋白或基因名",
        "en": "Protein or gene name",
    },
    "btn_search_uniprot": {
        "zh": "搜索 UniProt",
        "en": "Search UniProt",
    },
    "searching": {
        "zh": "搜索中...",
        "en": "Searching...",
    },
    "no_results": {
        "zh": "未找到结果",
        "en": "No results found",
    },

    # ── Converter page ──
    "converter_title": {
        "zh": "## 🔄 格式转换与验证",
        "en": "## 🔄 Format Converter & Validator",
    },
    "upload_bio_file": {
        "zh": "上传生物信息学文件",
        "en": "Upload a bioinformatics file",
    },
    "detected_format": {
        "zh": "检测到格式：**{fmt}**",
        "en": "Detected format: **{fmt}**",
    },
    "format_valid": {
        "zh": "文件格式验证通过",
        "en": "File format is valid",
    },
    "validation_errors": {
        "zh": "验证错误：",
        "en": "Validation errors:",
    },
    "parsed_data": {
        "zh": "解析后的数据",
        "en": "Parsed Data",
    },

    # ── Upload page ──
    "upload_title": {
        "zh": "## 📁 数据上传",
        "en": "## 📁 Data Upload",
    },
    "upload_desc": {
        "zh": """
上传你的生物信息学数据文件进行分析。支持的格式：

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| FASTA | .fasta, .fa | 序列数据 |
| FASTQ | .fastq, .fq | 测序 reads |
| 表达矩阵 | .csv, .tsv | 基因表达计数 |
| BED | .bed | 基因组区域 |
| GTF/GFF | .gtf, .gff | 基因注释 |
| VCF | .vcf | 变异检测结果 |
""",
        "en": """
Upload your bioinformatics data files for analysis. Supported formats:

| Format | Extension | Description |
|--------|-----------|-------------|
| FASTA | .fasta, .fa | Sequence data |
| FASTQ | .fastq, .fq | Sequencing reads |
| Count Matrix | .csv, .tsv | Gene expression counts |
| BED | .bed | Genomic regions |
| GTF/GFF | .gtf, .gff | Gene annotations |
| VCF | .vcf | Variant calls |
""",
    },
    "upload_file": {
        "zh": "上传文件",
        "en": "Upload file",
    },
    "loaded_as_matrix": {
        "zh": "### 加载为表达矩阵：{genes} 个基因 x {samples} 个样本",
        "en": "### Loaded as count matrix: {genes} genes x {samples} samples",
    },
    "found_n_sequences": {
        "zh": "### 发现 {n} 条序列",
        "en": "### Found {n} sequences",
    },

    # ── Visualization page ──
    "viz_title": {
        "zh": "## 📈 可视化",
        "en": "## 📈 Visualization",
    },
    "no_data_warning": {
        "zh": "请先上传或生成数据（转录组分析页面）",
        "en": "Upload or generate data first (RNA-seq Analysis page)",
    },
    "chart_type": {
        "zh": "图表类型",
        "en": "Chart Type",
    },
    "chart_distribution": {
        "zh": "样本分布",
        "en": "Sample Distribution",
    },
    "chart_pca": {
        "zh": "PCA 图",
        "en": "PCA Plot",
    },
    "chart_heatmap": {
        "zh": "表达热图",
        "en": "Expression Heatmap",
    },
    "chart_correlation": {
        "zh": "相关性矩阵",
        "en": "Correlation Matrix",
    },
    "top_n_genes": {
        "zh": "按方差排序的 Top N 基因",
        "en": "Top N genes by variance",
    },
    "enrichment_viz": {
        "zh": "### 富集分析结果",
        "en": "### Enrichment Results",
    },
    "volcano_plot": {
        "zh": "### 火山图",
        "en": "### Volcano Plot",
    },

    # ── Report page ──
    "report_title": {
        "zh": "## 📄 分析报告",
        "en": "## 📄 Analysis Report",
    },
    "btn_generate_report": {
        "zh": "生成报告",
        "en": "Generate Report",
    },
    "btn_download_report": {
        "zh": "⬇️ 下载报告",
        "en": "⬇️ Download Report",
    },
    "no_results_warning": {
        "zh": "没有分析结果可生成报告，请先运行分析！",
        "en": "No analysis results to report. Run some analyses first!",
    },
    "report_data_summary": {
        "zh": "数据概览",
        "en": "Data Summary",
    },
    "report_de_results": {
        "zh": "差异表达结果",
        "en": "Differential Expression Results",
    },
    "report_enrichment": {
        "zh": "富集分析",
        "en": "Enrichment Analysis",
    },

    # ── Common ──
    "thinking": {
        "zh": "思考中...",
        "en": "Thinking...",
    },
    "generating": {
        "zh": "生成中...",
        "en": "Generating...",
    },
    "running": {
        "zh": "运行中...",
        "en": "Running...",
    },
    "success": {
        "zh": "成功！",
        "en": "Success!",
    },
    "error": {
        "zh": "错误",
        "en": "Error",
    },
    "warning": {
        "zh": "警告",
        "en": "Warning",
    },
    "control": {
        "zh": "对照",
        "en": "Control",
    },
    "treatment": {
        "zh": "处理",
        "en": "Treatment",
    },
    "description": {
        "zh": "描述",
        "en": "Description",
    },
    "chromosome": {
        "zh": "染色体",
        "en": "Chromosome",
    },
    "map_location": {
        "zh": "图谱位置",
        "en": "Map Location",
    },
    "organism": {
        "zh": "物种",
        "en": "Organism",
    },
    "warnings": {
        "zh": "警告信息",
        "en": "Warnings",
    },
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    """Translate a key to the specified language.

    Args:
        key: Translation key
        lang: Language code ('zh' or 'en')
        **kwargs: Format parameters for string interpolation

    Returns:
        Translated string
    """
    entry = TRANSLATIONS.get(key, {})
    text = entry.get(lang, entry.get("en", key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text

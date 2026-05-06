"""BioInfo Agent - Streamlit Visualization Interface with i18n support."""

import streamlit as st
import pandas as pd
import numpy as np
import json
import io
from datetime import datetime

from agent.core import BioInfoAgent
from agent.planner import PipelinePlanner
from tools.sequence import SequenceAnalyzer
from tools.rnaseq import RNASeqAnalyzer
from tools.enrichment import EnrichmentAnalyzer
from tools.database import DatabaseQuerier
from formats.converter import FormatConverter
from formats.validator import DataValidator
from report.plots import PlotGenerator
from report.generator import ReportGenerator
from i18n import t

# Page config
st.set_page_config(
    page_title="BioInfo Agent",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        padding: 8px 16px;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    defaults = {
        "agent": None,
        "chat_history": [],
        "count_matrix": None,
        "de_results": None,
        "enrichment_results": None,
        "current_pipeline": None,
        "lang": "zh",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def init_agent():
    """Return the current agent from session state, or a fallback."""
    if st.session_state.agent is not None:
        return st.session_state.agent
    return BioInfoAgent()  # No API key = fallback mode


def L(key, **kwargs):
    """Shorthand for translation."""
    return t(key, st.session_state.lang, **kwargs)


def render_sidebar():
    with st.sidebar:
        st.markdown(f"## {t('sidebar_title', st.session_state.lang)}")

        # Language switcher
        st.markdown("---")
        lang_choice = st.radio(
            t("language_label", st.session_state.lang),
            ["中文", "English"],
            index=0 if st.session_state.lang == "zh" else 1,
            horizontal=True,
            key="lang_radio",
        )
        new_lang = "zh" if lang_choice == "中文" else "en"
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun()

        st.markdown("---")

        # API Key
        st.markdown(f"### {t('settings', st.session_state.lang)}")
        api_key = st.text_input(
            t("api_key_label", st.session_state.lang),
            type="password",
            help=t("api_key_help", st.session_state.lang),
        )

        # Provider preset
        lang = st.session_state.lang
        provider_options = [
            t("provider_official", lang),
            t("provider_mimo", lang),
            t("provider_custom", lang),
        ]
        provider = st.selectbox(t("provider_presets", lang), provider_options)

        MIMO_BASE_URL = "https://token-plan-cn.xiaomimimo.com/anthropic"
        MIMO_MODELS = ["mimo-v2.5-pro", "MiMo-7B"]

        if provider == t("provider_official", lang):
            base_url = None
            model = st.text_input(
                t("model_label", lang),
                value="claude-sonnet-4-20250514",
                help=t("model_help", lang),
            )
        elif provider == t("provider_mimo", lang):
            base_url = MIMO_BASE_URL
            model = st.selectbox(t("model_label", lang), MIMO_MODELS)
            st.caption(f"Base URL: `{MIMO_BASE_URL}`")
        else:
            base_url = st.text_input(
                t("api_base_url_label", lang),
                help=t("api_base_url_help", lang),
            )
            model = st.text_input(
                t("model_label", lang),
                value="claude-sonnet-4-20250514",
                help=t("model_help", lang),
            )

        if api_key:
            # Always recreate agent to pick up latest settings
            st.session_state.agent = BioInfoAgent(
                api_key=api_key,
                model=model,
                base_url=base_url if base_url else None,
            )
        else:
            st.session_state.agent = None

        st.markdown("---")

        # Navigation
        lang = st.session_state.lang
        nav_options = [
            t("nav_chat", lang),
            t("nav_rnaseq", lang),
            t("nav_sequence", lang),
            t("nav_enrichment", lang),
            t("nav_database", lang),
            t("nav_converter", lang),
            t("nav_upload", lang),
            t("nav_visualization", lang),
            t("nav_report", lang),
        ]
        page = st.radio(
            t("analysis_tools", lang),
            nav_options,
            label_visibility="collapsed",
        )

        st.markdown("---")

        # Quick stats
        if st.session_state.count_matrix is not None:
            st.markdown(f"### {t('data_status', lang)}")
            cm = st.session_state.count_matrix
            st.metric(t("genes", lang), f"{len(cm):,}")
            st.metric(t("samples", lang), len(cm.columns))
            if st.session_state.de_results is not None:
                de = st.session_state.de_results
                st.metric(t("de_up", lang), len(de[de["regulation"] == "UP"]))
                st.metric(t("de_down", lang), len(de[de["regulation"] == "DOWN"]))

    return page


def render_chat_page():
    lang = st.session_state.lang
    st.markdown(t("chat_title", lang))
    st.markdown(t("chat_subtitle", lang))

    user_input = st.chat_input(t("chat_placeholder", lang))

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        agent = init_agent()
        with st.chat_message("assistant"):
            with st.spinner(t("thinking", lang)):
                if any(kw in user_input.lower() for kw in ["pipeline", "流程", "分析", "analysis", "rna-seq", "rnaseq"]):
                    pipeline = agent.plan_pipeline(user_input)
                    response = agent.get_pipeline_summary()
                    ai_response = agent.chat(user_input)
                    if "API error" not in ai_response and "API key" not in ai_response:
                        response = ai_response
                else:
                    response = agent.chat(user_input)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

    st.markdown("---")
    st.markdown(t("quick_actions", lang))
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(t("btn_rnaseq_pipeline", lang)):
            planner = PipelinePlanner()
            pipeline = planner.plan_from_request("RNA-seq differential expression")
            st.session_state.current_pipeline = pipeline
            st.session_state.chat_history.append({"role": "assistant", "content": planner.get_pipeline_summary(pipeline)})
            st.rerun()
    with col2:
        if st.button(t("btn_chipseq_pipeline", lang)):
            planner = PipelinePlanner()
            pipeline = planner.plan_from_request("ChIP-seq peak calling")
            st.session_state.current_pipeline = pipeline
            st.session_state.chat_history.append({"role": "assistant", "content": planner.get_pipeline_summary(pipeline)})
            st.rerun()
    with col3:
        if st.button(t("btn_variant_pipeline", lang)):
            planner = PipelinePlanner()
            pipeline = planner.plan_from_request("variant calling WGS")
            st.session_state.current_pipeline = pipeline
            st.session_state.chat_history.append({"role": "assistant", "content": planner.get_pipeline_summary(pipeline)})
            st.rerun()


def render_rnaseq_page():
    lang = st.session_state.lang
    st.markdown(t("rnaseq_title", lang))

    analyzer = RNASeqAnalyzer()
    plots = PlotGenerator()

    data_source = st.radio(t("data_source", lang), [t("upload_count_matrix", lang), t("generate_demo", lang)], horizontal=True)

    if data_source == t("generate_demo", lang):
        col1, col2 = st.columns(2)
        with col1:
            n_genes = st.number_input(t("n_genes", lang), 100, 10000, 1000)
        with col2:
            n_samples = st.number_input(t("n_samples", lang), 4, 20, 6)
        if st.button(t("btn_generate", lang), type="primary"):
            st.session_state.count_matrix = analyzer.create_sample_data(n_genes, n_samples)
            st.success(f"{t('success', lang)} {n_genes} genes x {n_samples} samples")

    elif data_source == t("upload_count_matrix", lang):
        uploaded = st.file_uploader(t("btn_upload_matrix", lang), type=["csv", "tsv"])
        if uploaded:
            sep = "\t" if uploaded.name.endswith(".tsv") else ","
            st.session_state.count_matrix = pd.read_csv(uploaded, index_col=0, sep=sep)
            cm = st.session_state.count_matrix
            st.success(f"{t('success', lang)} {len(cm)} genes x {len(cm.columns)} samples")

    if st.session_state.count_matrix is not None:
        cm = st.session_state.count_matrix

        with st.expander(t("data_preview", lang), expanded=True):
            st.dataframe(cm.head(10), use_container_width=True)

        stats = analyzer.summary_stats(cm)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(t("genes", lang), f"{stats['n_genes']:,}")
        col2.metric(t("samples", lang), stats["n_samples"])
        col3.metric(t("total_counts", lang), f"{stats['total_counts']:,}")
        col4.metric(t("genes_detected", lang), f"{stats['genes_detected']:,}")

        tab1, tab2, tab3 = st.tabs([t("tab_distribution", lang), t("tab_pca", lang), t("tab_heatmap", lang)])

        with tab1:
            fig = plots.sample_distribution(cm)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.markdown(t("assign_groups", lang))
            samples = list(cm.columns)
            groups = {}
            cols = st.columns(min(len(samples), 4))
            for i, sample in enumerate(samples):
                with cols[i % len(cols)]:
                    groups[sample] = st.selectbox(sample, [t("control", lang), t("treatment", lang)], key=f"group_{sample}")
            fig = plots.pca_plot(cm, groups)
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            fig = plots.heatmap(cm)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown(t("de_title", lang))

        control_samples = st.multiselect(
            t("control_samples", lang), list(cm.columns),
            default=[s for s in cm.columns if "Sample_0" in s or "Sample_1" in s or "Sample_2" in s][:3],
        )
        treatment_samples = st.multiselect(
            t("treatment_samples", lang), list(cm.columns),
            default=[s for s in cm.columns if "Sample_3" in s or "Sample_4" in s or "Sample_5" in s][:3],
        )

        if st.button(t("btn_run_de", lang), type="primary"):
            if not control_samples or not treatment_samples:
                st.error(t("select_both_groups", lang))
            else:
                with st.spinner(t("running", lang)):
                    st.session_state.de_results = analyzer.differential_expression(cm, control_samples, treatment_samples)
                st.success(t("de_complete", lang))

        if st.session_state.de_results is not None:
            de = st.session_state.de_results
            up_genes = de[de["regulation"] == "UP"]
            down_genes = de[de["regulation"] == "DOWN"]
            col1, col2, col3 = st.columns(3)
            col1.metric(t("upregulated", lang), len(up_genes))
            col2.metric(t("downregulated", lang), len(down_genes))
            col3.metric(t("total_de", lang), len(up_genes) + len(down_genes))

            fig = plots.volcano_plot(de)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(t("top_de_genes", lang))
            st.dataframe(
                de.head(50)[["gene", "baseMean", "log2FoldChange", "pvalue", "padj", "regulation"]].style.format({
                    "baseMean": "{:.1f}", "log2FoldChange": "{:.3f}", "pvalue": "{:.2e}", "padj": "{:.2e}",
                }),
                use_container_width=True,
            )

            if st.button(t("btn_go_enrichment", lang)):
                with st.spinner(t("running", lang)):
                    enrichment = EnrichmentAnalyzer()
                    sig_genes = de[de["regulation"] != "NS"]["gene"].tolist()
                    st.session_state.enrichment_results = enrichment.run_enrichment(sig_genes, database="go")
                st.success(t("enrichment_complete", lang))


def render_sequence_page():
    lang = st.session_state.lang
    st.markdown(t("seq_title", lang))

    analyzer = SequenceAnalyzer()
    plots = PlotGenerator()

    tab1, tab2, tab3 = st.tabs([t("tab_seq_input", lang), t("tab_orf", lang), t("tab_composition", lang)])

    with tab1:
        st.markdown(t("seq_input_label", lang))
        seq_input = st.text_area("Sequence", height=100, placeholder=t("seq_placeholder", lang))
        uploaded_fasta = st.file_uploader(t("upload_fasta", lang), type=["fasta", "fa", "fna"])

        sequence = ""
        if uploaded_fasta:
            content = uploaded_fasta.read().decode()
            records = analyzer.parse_fasta(content)
            if records:
                sequence = records[0]["sequence"]
                st.info(f"Loaded: {records[0]['id']} ({records[0]['length']} bp)")
        elif seq_input:
            sequence = seq_input.strip().replace("\n", "").replace(" ", "")

        if sequence:
            result = analyzer.analyze(sequence)
            col1, col2, col3, col4 = st.columns(4)
            gc = result["gc_content"]
            col1.metric(t("length", lang), f"{gc['length']} bp")
            col2.metric(t("gc_content", lang), f"{gc['gc_content']}%")
            col3.metric(t("orfs_found", lang), len(result["orfs"]))
            col4.metric("A/T", f"{gc['a_count']}/{gc['t_count']}")

    with tab2:
        if sequence:
            orfs = analyzer.find_orfs(sequence)
            if orfs:
                st.markdown(t("found_orfs", lang, n=len(orfs)))
                orf_df = pd.DataFrame(orfs)
                st.dataframe(orf_df[["frame", "start", "end", "length_nt", "length_aa"]], use_container_width=True)
            else:
                st.info(t("no_orfs", lang))
        else:
            st.info(t("enter_seq_first", lang))

    with tab3:
        if sequence:
            comp = analyzer.composition(sequence)
            comp_df = pd.DataFrame({"Base": list(comp.keys()), "Count": list(comp.values())})
            fig = plots.bar_plot(comp_df, "Base", "Count", t("nucleotide_composition", lang))
            st.plotly_chart(fig, use_container_width=True)

            window = min(100, len(sequence) // 10)
            if window > 10:
                gc_values, positions = [], []
                for i in range(0, len(sequence) - window, window // 2):
                    subseq = sequence[i:i + window]
                    gc_values.append(analyzer.gc_content(subseq)["gc_content"])
                    positions.append(i + window // 2)
                fig_gc = plots.bar_plot(
                    pd.DataFrame({"Position": positions, "GC%": gc_values}),
                    "Position", "GC%", t("gc_sliding_window", lang, w=window)
                )
                st.plotly_chart(fig_gc, use_container_width=True)
        else:
            st.info(t("enter_seq_first", lang))


def render_enrichment_page():
    lang = st.session_state.lang
    st.markdown(t("enrichment_title", lang))

    enrichment = EnrichmentAnalyzer()
    plots = PlotGenerator()

    input_method = st.radio(t("input_method", lang), [t("gene_list_input", lang), t("from_de_results", lang)], horizontal=True)

    gene_list = []
    if input_method == t("gene_list_input", lang):
        genes_text = st.text_area(t("enter_genes", lang), height=150, placeholder="TP53\nBRCA1\nMYC\nEGFR\n...")
        if genes_text:
            gene_list = [g.strip() for g in genes_text.replace(",", "\n").split("\n") if g.strip()]

    elif input_method == t("from_de_results", lang):
        if st.session_state.de_results is not None:
            de = st.session_state.de_results
            regulation = st.selectbox(t("select_genes", lang), [t("all_de", lang), t("upregulated", lang), t("downregulated", lang)])
            if regulation == t("all_de", lang):
                gene_list = de[de["regulation"] != "NS"]["gene"].tolist()
            elif regulation == t("upregulated", lang):
                gene_list = de[de["regulation"] == "UP"]["gene"].tolist()
            else:
                gene_list = de[de["regulation"] == "DOWN"]["gene"].tolist()
            st.info(t("using_n_genes", lang, n=len(gene_list), type=regulation))
        else:
            st.warning(t("no_de_warning", lang))

    if gene_list:
        st.markdown(t("genes_loaded", lang, n=len(gene_list)))
        database = st.selectbox(t("database_label", lang), ["GO (Gene Ontology)", "KEGG Pathways"])
        db_key = "go" if "GO" in database else "kegg"

        if st.button(t("btn_run_enrichment", lang), type="primary"):
            with st.spinner(t("running", lang)):
                results = enrichment.run_enrichment(gene_list, database=db_key)
                st.session_state.enrichment_results = results
            if not results.empty:
                st.success(t("enrichment_found", lang, n=len(results)))
            else:
                st.warning(t("no_enrichment", lang))

    if st.session_state.enrichment_results is not None:
        results = st.session_state.enrichment_results
        sig = results[results["padj"] < 0.05]
        col1, col2, col3 = st.columns(3)
        col1.metric(t("total_terms", lang), len(results))
        col2.metric(t("significant_terms", lang), len(sig))
        col3.metric(t("top_enrichment", lang), f"{results.iloc[0]['enrichment_factor']:.1f}x" if not results.empty else "N/A")

        fig = plots.dot_plot(results)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(t("enrichment_results", lang))
        st.dataframe(
            results[["term_name", "term_id", "overlap", "term_size", "enrichment_factor", "padj", "genes"]].style.format({
                "enrichment_factor": "{:.2f}", "padj": "{:.2e}",
            }),
            use_container_width=True,
        )

        agent = init_agent()
        if st.button(t("btn_ai_interpret", lang)):
            with st.spinner(t("thinking", lang)):
                interpretation = agent.interpret_results({
                    "enrichment_results": results.head(10).to_dict("records"),
                    "total_genes": len(gene_list) if gene_list else 0,
                })
            st.markdown(interpretation)


def render_database_page():
    lang = st.session_state.lang
    st.markdown(t("db_title", lang))

    db = DatabaseQuerier()
    tab1, tab2, tab3 = st.tabs(["NCBI Gene", "Ensembl", "UniProt"])

    with tab1:
        st.markdown(t("search_ncbi", lang))
        query = st.text_input(t("gene_name_placeholder", lang), placeholder="TP53")
        organism = st.selectbox(t("organism", lang), ["Homo sapiens", "Mus musculus", "Rattus norvegicus"])
        if st.button(t("btn_search_ncbi", lang)) and query:
            with st.spinner(t("searching", lang)):
                results = db.search_gene_ncbi(query, organism)
            if results and "error" not in results[0]:
                for r in results:
                    with st.expander(f"{r['name']} (ID: {r['gene_id']})"):
                        st.markdown(f"**{t('description', lang)}:** {r['description']}")
                        st.markdown(f"**{t('chromosome', lang)}:** {r['chromosome']}")
                        st.markdown(f"**{t('map_location', lang)}:** {r['map_location']}")
            else:
                st.warning(t("no_results", lang))

    with tab2:
        st.markdown(t("search_ensembl", lang))
        gene_name = st.text_input(t("gene_symbol_placeholder", lang), placeholder="BRCA1", key="ensembl_input")
        if st.button(t("btn_search_ensembl", lang)) and gene_name:
            with st.spinner(t("searching", lang)):
                results = db.search_ensembl(gene_name)
            if results and "error" not in results[0]:
                for r in results:
                    st.json(r)
            else:
                st.warning(t("no_results", lang))

    with tab3:
        st.markdown(t("search_uniprot", lang))
        protein_query = st.text_input(t("protein_placeholder", lang), placeholder="TP53", key="uniprot_input")
        if st.button(t("btn_search_uniprot", lang)) and protein_query:
            with st.spinner(t("searching", lang)):
                results = db.search_uniprot(protein_query)
            if results and "error" not in results[0]:
                for r in results:
                    with st.expander(f"{r['accession']} - {r['protein_name']}"):
                        st.markdown(f"**Gene:** {r['gene_name']}")
                        st.markdown(f"**{t('organism', lang)}:** {r['organism']}")
                        st.markdown(f"**{t('length', lang)}:** {r['length']} aa")
            else:
                st.warning(t("no_results", lang))


def render_converter_page():
    lang = st.session_state.lang
    st.markdown(t("converter_title", lang))

    converter = FormatConverter()
    validator = DataValidator()

    uploaded = st.file_uploader(t("upload_bio_file", lang), type=["fasta", "fa", "fastq", "fq", "bed", "gtf", "gff", "vcf", "csv", "tsv"])

    if uploaded:
        content = uploaded.read().decode()
        detected = converter.detect_format(content)
        st.info(t("detected_format", lang, fmt=detected.upper()))

        validation = validator.validate(content, detected)
        if validation["valid"]:
            st.success(t("format_valid", lang))
        else:
            st.error(t("validation_errors", lang))
            for err in validation["errors"]:
                st.markdown(f"- {err}")

        if validation.get("warnings"):
            with st.expander(t("warnings", lang)):
                for w in validation["warnings"]:
                    st.markdown(f"- {w}")

        if "sequence_count" in validation:
            st.metric("Sequences", validation["sequence_count"])
        if "read_count" in validation:
            st.metric("Reads", validation["read_count"])
        if "variant_count" in validation:
            st.metric("Variants", validation["variant_count"])

        with st.expander(t("parsed_data", lang)):
            parsed = converter.convert(content, detected)
            if isinstance(parsed, list):
                st.dataframe(pd.DataFrame(parsed).head(20), use_container_width=True)
            else:
                st.json(parsed)


def render_upload_page():
    lang = st.session_state.lang
    st.markdown(t("upload_title", lang))
    st.markdown(t("upload_desc", lang))

    uploaded = st.file_uploader(t("upload_file", lang), type=["fasta", "fa", "fastq", "fq", "csv", "tsv", "bed", "gtf", "gff", "vcf"])

    if uploaded:
        file_type = uploaded.name.split(".")[-1]
        st.success(f"{t('success', lang)} {uploaded.name} ({uploaded.size:,} bytes)")

        if file_type in ["csv", "tsv"]:
            sep = "\t" if file_type == "tsv" else ","
            try:
                df = pd.read_csv(uploaded, index_col=0, sep=sep)
                st.session_state.count_matrix = df
                st.markdown(t("loaded_as_matrix", lang, genes=len(df), samples=len(df.columns)))
                st.dataframe(df.head(10), use_container_width=True)
            except Exception as e:
                st.error(f"{t('error', lang)}: {e}")

        elif file_type in ["fasta", "fa"]:
            content = uploaded.read().decode()
            analyzer = SequenceAnalyzer()
            records = analyzer.parse_fasta(content)
            st.markdown(t("found_n_sequences", lang, n=len(records)))
            st.dataframe(pd.DataFrame(records)[["id", "length", "gc_content"]], use_container_width=True)

        else:
            content = uploaded.read().decode()
            st.code(content[:2000], language="text")


def render_visualization_page():
    lang = st.session_state.lang
    st.markdown(t("viz_title", lang))

    plots = PlotGenerator()

    if st.session_state.count_matrix is None:
        st.info(t("no_data_warning", lang))
        return

    cm = st.session_state.count_matrix
    chart_options = [
        t("chart_distribution", lang),
        t("chart_pca", lang),
        t("chart_heatmap", lang),
        t("chart_correlation", lang),
    ]
    chart_type = st.selectbox(t("chart_type", lang), chart_options)

    if chart_type == t("chart_distribution", lang):
        fig = plots.sample_distribution(cm)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == t("chart_pca", lang):
        fig = plots.pca_plot(cm)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == t("chart_heatmap", lang):
        top_n = st.slider(t("top_n_genes", lang), 10, 200, 50)
        var_genes = cm.var(axis=1).nlargest(top_n).index
        fig = plots.heatmap(cm, gene_list=list(var_genes))
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == t("chart_correlation", lang):
        corr = cm.corr()
        import plotly.graph_objects as go
        fig = go.Figure(data=go.Heatmap(z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(), colorscale="RdBu_r", zmid=0))
        fig.update_layout(title=t("chart_correlation", lang), height=500, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    if st.session_state.enrichment_results is not None:
        st.markdown("---")
        st.markdown(t("enrichment_viz", lang))
        fig = plots.dot_plot(st.session_state.enrichment_results)
        st.plotly_chart(fig, use_container_width=True)

    if st.session_state.de_results is not None:
        st.markdown("---")
        st.markdown(t("volcano_plot", lang))
        fig = plots.volcano_plot(st.session_state.de_results)
        st.plotly_chart(fig, use_container_width=True)


def render_report_page():
    lang = st.session_state.lang
    st.markdown(t("report_title", lang))

    reporter = ReportGenerator()

    if st.button(t("btn_generate_report", lang), type="primary"):
        sections = []

        if st.session_state.count_matrix is not None:
            cm = st.session_state.count_matrix
            sections.append({
                "title": t("report_data_summary", lang),
                "content": f"<p>Count matrix: {len(cm)} genes x {len(cm.columns)} samples</p>"
                           f"<p>Total counts: {cm.sum().sum():,}</p>",
            })

        if st.session_state.de_results is not None:
            sections.append({
                "title": t("report_de_results", lang),
                "content": reporter.format_de_results(st.session_state.de_results),
            })

        if st.session_state.enrichment_results is not None:
            sections.append({
                "title": t("report_enrichment", lang),
                "content": reporter.format_enrichment_results(st.session_state.enrichment_results),
            })

        if sections:
            html = reporter.generate_html_report("BioInfo Agent Analysis Report", sections)
            st.components.v1.html(html, height=800, scrolling=True)
            st.download_button(
                t("btn_download_report", lang),
                html,
                file_name=f"bioinfo_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html",
            )
        else:
            st.warning(t("no_results_warning", lang))


def main():
    init_session_state()

    lang = st.session_state.lang
    st.markdown(f"""
    <div class="main-header">
        <h1>{t('app_title', lang)}</h1>
        <p>{t('app_subtitle', lang)}</p>
    </div>
    """, unsafe_allow_html=True)

    page = render_sidebar()

    # Match page by checking which nav label was selected
    nav_map = {
        t("nav_chat", lang): render_chat_page,
        t("nav_rnaseq", lang): render_rnaseq_page,
        t("nav_sequence", lang): render_sequence_page,
        t("nav_enrichment", lang): render_enrichment_page,
        t("nav_database", lang): render_database_page,
        t("nav_converter", lang): render_converter_page,
        t("nav_upload", lang): render_upload_page,
        t("nav_visualization", lang): render_visualization_page,
        t("nav_report", lang): render_report_page,
    }
    render_fn = nav_map.get(page, render_chat_page)
    render_fn()


if __name__ == "__main__":
    main()

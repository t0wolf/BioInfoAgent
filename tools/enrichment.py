"""GO/KEGG enrichment analysis tools."""

import pandas as pd
import numpy as np
from typing import Any


class EnrichmentAnalyzer:
    """Tools for functional enrichment analysis."""

    # Simplified GO term database for demonstration
    GO_TERMS = {
        "GO:0006915": {"name": "apoptotic process", "category": "BP", "genes": ["TP53", "BAX", "CASP3", "BCL2", "FAS"]},
        "GO:0006954": {"name": "inflammatory response", "category": "BP", "genes": ["TNF", "IL6", "IL1B", "NFKB1", "CXCL8"]},
        "GO:0007049": {"name": "cell cycle", "category": "BP", "genes": ["CDK1", "CCNB1", "CDK2", "RB1", "E2F1"]},
        "GO:0008283": {"name": "cell proliferation", "category": "BP", "genes": ["EGF", "MYC", "PCNA", "MKI67", "CCND1"]},
        "GO:0006412": {"name": "translation", "category": "BP", "genes": ["RPS6", "RPL13A", "EEF1A1", "EIF4E", "RPLP0"]},
        "GO:0006281": {"name": "DNA repair", "category": "BP", "genes": ["BRCA1", "RAD51", "ATM", "XRCC1", "MLH1"]},
        "GO:0007155": {"name": "cell adhesion", "category": "BP", "genes": ["CDH1", "ITGB1", "VCAM1", "ICAM1", "FN1"]},
        "GO:0006468": {"name": "protein phosphorylation", "category": "BP", "genes": ["AKT1", "MAPK1", "EGFR", "SRC", "RAF1"]},
        "GO:0001525": {"name": "angiogenesis", "category": "BP", "genes": ["VEGFA", "KDR", "ANGPT1", "FLT1", "PECAM1"]},
        "GO:0045944": {"name": "positive regulation of transcription", "category": "BP", "genes": ["MYC", "JUN", "FOS", "SP1", "CREB1"]},
        "GO:0005737": {"name": "cytoplasm", "category": "CC", "genes": ["GAPDH", "ACTB", "TUBB", "RPS6", "EEF1A1"]},
        "GO:0005634": {"name": "nucleus", "category": "CC", "genes": ["TP53", "MYC", "HIST1H3A", "RB1", "BRCA1"]},
    }

    KEGG_PATHWAYS = {
    "hsa04110": {"name": "Cell cycle", "genes": ["CDK1", "CCNB1", "CDK2", "RB1", "TP53", "MAD2L1"]},
    "hsa04115": {"name": "p53 signaling pathway", "genes": ["TP53", "MDM2", "BAX", "CDKN1A", "GADD45A"]},
    "hsa04010": {"name": "MAPK signaling pathway", "genes": ["MAPK1", "MAPK3", "RAF1", "EGFR", "FGFR1"]},
    "hsa04150": {"name": "mTOR signaling pathway", "genes": ["MTOR", "RPTOR", "AKT1", "TSC1", "EIF4EBP1"]},
    "hsa04630": {"name": "JAK-STAT signaling pathway", "genes": ["JAK1", "STAT3", "STAT1", "IL6", "SOCS3"]},
    "hsa04064": {"name": "NF-kappa B signaling pathway", "genes": ["NFKB1", "RELA", "TNF", "IKBKB", "TRAF2"]},
    "hsa04210": {"name": "Apoptosis", "genes": ["CASP3", "CASP8", "BAX", "BCL2", "FAS"]},
    "hsa04510": {"name": "Focal adhesion", "genes": ["ITGB1", "FAK1", "SRC", "PXN", "VCL"]},
    "hsa04520": {"name": "Adherens junction", "genes": ["CDH1", "CTNNB1", "CTNNA1", "SRC", "EGFR"]},
    "hsa05200": {"name": "Pathways in cancer", "genes": ["TP53", "EGFR", "MYC", "VEGFA", "APC"]},
}

    def run_enrichment(
        self, gene_list: list[str], background_genes: list[str] | None = None, database: str = "go"
    ) -> pd.DataFrame:
        """Run enrichment analysis on a list of genes."""
        gene_set = set(gene_list)

        if database == "go":
            term_db = self.GO_TERMS
        else:
            term_db = self.KEGG_PATHWAYS

        results = []
        bg_size = len(background_genes) if background_genes else 20000

        for term_id, info in term_db.items():
            term_genes = set(info["genes"])
            overlap = gene_set & term_genes
            if not overlap:
                continue

            # Fisher's exact test (simplified)
            a = len(overlap)
            b = len(gene_set) - a
            c = len(term_genes) - a
            d = bg_size - a - b - c

            # Odds ratio and p-value
            from scipy.stats import fisher_exact

            table = [[a, b], [c, d]]
            odds_ratio, pvalue = fisher_exact(table, alternative="greater")

            # Enrichment factor
            expected = len(gene_set) * len(term_genes) / bg_size
            enrichment = a / expected if expected > 0 else 0

            results.append({
                "term_id": term_id,
                "term_name": info["name"],
                "category": info.get("category", "KEGG"),
                "overlap": a,
                "term_size": len(term_genes),
                "gene_set_size": len(gene_set),
                "enrichment_factor": round(enrichment, 2),
                "pvalue": pvalue,
                "genes": ", ".join(sorted(overlap)),
            })

        df = pd.DataFrame(results)
        if not df.empty:
            # Adjust p-values
            from statsmodels.stats.multitest import multipletests
            try:
                _, padj, _, _ = multipletests(df["pvalue"].values, method="fdr_bh")
                df["padj"] = padj
            except Exception:
                df["padj"] = df["pvalue"]
            df = df.sort_values("padj")

        return df

    def format_results(self, results: pd.DataFrame, top_n: int = 10) -> str:
        """Format enrichment results as a readable string."""
        if results.empty:
            return "No significant enrichment found."

        lines = ["## Enrichment Results\n"]
        for _, row in results.head(top_n).iterrows():
            sig = "***" if row["padj"] < 0.001 else "**" if row["padj"] < 0.01 else "*" if row["padj"] < 0.05 else ""
            lines.append(
                f"- **{row['term_name']}** ({row['term_id']}) {sig}\n"
                f"  - Overlap: {row['overlap']}/{row['term_size']} genes\n"
                f"  - Enrichment: {row['enrichment_factor']}x | p.adj = {row['padj']:.2e}\n"
                f"  - Genes: {row['genes']}\n"
            )
        return "\n".join(lines)

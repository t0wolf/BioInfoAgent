"""RNA-seq analysis tools."""

import pandas as pd
import numpy as np
from typing import Any


class RNASeqAnalyzer:
    """Tools for RNA-seq data analysis."""

    def create_sample_data(self, n_genes: int = 1000, n_samples: int = 6) -> pd.DataFrame:
        """Create sample count matrix for demonstration."""
        np.random.seed(42)
        gene_names = [f"Gene_{i}" for i in range(n_genes)]
        sample_names = [f"Sample_{i}" for i in range(n_samples)]

        # Base expression levels
        base_expr = np.random.lognormal(mean=3, sigma=1.5, size=n_genes)

        counts = np.zeros((n_genes, n_samples))
        for i in range(n_samples):
            noise = np.random.lognormal(mean=0, sigma=0.3, size=n_genes)
            if i < n_samples // 2:
                counts[:, i] = base_expr * noise
            else:
                # Treatment group: some genes are differentially expressed
                de_mask = np.random.random(n_genes) < 0.1
                de_factor = np.where(de_mask, np.random.choice([0.3, 3.0], size=n_genes), 1.0)
                counts[:, i] = base_expr * noise * de_factor

        counts = np.round(counts).astype(int)
        counts = np.maximum(counts, 0)

        return pd.DataFrame(counts, index=gene_names, columns=sample_names)

    def differential_expression(
        self, count_matrix: pd.DataFrame, control_samples: list[str], treatment_samples: list[str]
    ) -> pd.DataFrame:
        """Perform differential expression analysis (simplified DESeq2-like)."""
        control = count_matrix[control_samples]
        treatment = count_matrix[treatment_samples]

        # Normalize (simple CPM)
        control_cpm = control.div(control.sum(axis=0), axis=1) * 1e6
        treatment_cpm = treatment.div(treatment.sum(axis=0), axis=1) * 1e6

        # Log2 fold change
        control_mean = control_cpm.mean(axis=1) + 1
        treatment_mean = treatment_cpm.mean(axis=1) + 1
        log2fc = np.log2(treatment_mean / control_mean)

        # P-value (simplified t-test)
        from scipy import stats

        pvalues = []
        for gene in count_matrix.index:
            ctrl_vals = control_cpm.loc[gene].values
            treat_vals = treatment_cpm.loc[gene].values
            try:
                _, pval = stats.ttest_ind(treat_vals, ctrl_vals)
                pvalues.append(pval if not np.isnan(pval) else 1.0)
            except Exception:
                pvalues.append(1.0)

        pvalues = np.array(pvalues)

        # Multiple testing correction (Benjamini-Hochberg)
        from statsmodels.stats.multitest import multipletests

        try:
            _, padj, _, _ = multipletests(pvalues, method="fdr_bh")
        except Exception:
            padj = pvalues

        results = pd.DataFrame({
            "gene": count_matrix.index,
            "baseMean": count_matrix.mean(axis=1),
            "log2FoldChange": log2fc,
            "pvalue": pvalues,
            "padj": padj,
            "regulation": np.where(
                (padj < 0.05) & (log2fc > 1),
                "UP",
                np.where((padj < 0.05) & (log2fc < -1), "DOWN", "NS"),
            ),
        })

        return results.sort_values("padj")

    def summary_stats(self, count_matrix: pd.DataFrame) -> dict[str, Any]:
        """Get summary statistics for a count matrix."""
        return {
            "n_genes": len(count_matrix),
            "n_samples": len(count_matrix.columns),
            "total_counts": int(count_matrix.sum().sum()),
            "mean_counts_per_sample": round(count_matrix.sum(axis=0).mean(), 0),
            "median_gene_count": round(count_matrix.median(axis=1).median(), 0),
            "samples": list(count_matrix.columns),
            "genes_detected": int((count_matrix > 0).sum(axis=0).mean()),
        }

    def filter_low_counts(self, count_matrix: pd.DataFrame, min_count: int = 10, min_samples: int = 3) -> pd.DataFrame:
        """Filter out lowly expressed genes."""
        keep = (count_matrix >= min_count).sum(axis=1) >= min_samples
        return count_matrix[keep]

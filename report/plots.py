"""Visualization tools for bioinformatics data."""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


class PlotGenerator:
    """Generate publication-quality plots for bioinformatics data."""

    def volcano_plot(self, de_results: pd.DataFrame, title: str = "Volcano Plot") -> go.Figure:
        """Create a volcano plot from DE results."""
        df = de_results.copy()
        df["-log10(padj)"] = -np.log10(df["padj"].clip(lower=1e-300))
        df["color"] = df["regulation"].map({"UP": "#e74c3c", "DOWN": "#3498db", "NS": "#bdc3c7"})

        fig = go.Figure()

        for reg, color in [("NS", "#bdc3c7"), ("UP", "#e74c3c"), ("DOWN", "#3498db")]:
            subset = df[df["regulation"] == reg]
            fig.add_trace(go.Scatter(
                x=subset["log2FoldChange"],
                y=subset["-log10(padj)"],
                mode="markers",
                name=reg,
                marker=dict(color=color, size=6, opacity=0.7),
                text=subset["gene"],
                hovertemplate="<b>%{text}</b><br>log2FC: %{x:.2f}<br>-log10(padj): %{y:.2f}<extra></extra>",
            ))

        fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="gray", annotation_text="p=0.05")
        fig.add_vline(x=1, line_dash="dash", line_color="gray")
        fig.add_vline(x=-1, line_dash="dash", line_color="gray")

        fig.update_layout(
            title=title,
            xaxis_title="log2 Fold Change",
            yaxis_title="-log10(adjusted p-value)",
            template="plotly_white",
            height=500,
        )
        return fig

    def heatmap(
        self, count_matrix: pd.DataFrame, gene_list: list[str] | None = None, title: str = "Expression Heatmap"
    ) -> go.Figure:
        """Create an expression heatmap."""
        if gene_list:
            data = count_matrix.loc[count_matrix.index.isin(gene_list)]
        else:
            data = count_matrix.head(50)

        # Log transform
        log_data = np.log2(data + 1)
        # Z-score normalize per gene
        z_scores = (log_data.T - log_data.T.mean()) / log_data.T.std()
        z_scores = z_scores.T

        fig = go.Figure(data=go.Heatmap(
            z=z_scores.values,
            x=z_scores.columns.tolist(),
            y=z_scores.index.tolist(),
            colorscale="RdBu_r",
            zmid=0,
            hovertemplate="Gene: %{y}<br>Sample: %{x}<br>Z-score: %{z:.2f}<extra></extra>",
        ))

        fig.update_layout(
            title=title,
            height=max(400, len(z_scores) * 15),
            template="plotly_white",
        )
        return fig

    def pca_plot(self, count_matrix: pd.DataFrame, groups: dict[str, str] | None = None, title: str = "PCA Plot") -> go.Figure:
        """Create a PCA plot."""
        from sklearn.decomposition import PCA

        log_data = np.log2(count_matrix.T + 1)
        pca = PCA(n_components=2)
        pcs = pca.fit_transform(log_data)

        df = pd.DataFrame({
            "PC1": pcs[:, 0],
            "PC2": pcs[:, 1],
            "Sample": count_matrix.columns,
        })

        if groups:
            df["Group"] = [groups.get(s, "Unknown") for s in df["Sample"]]
            fig = px.scatter(df, x="PC1", y="PC2", color="Group", text="Sample", title=title)
        else:
            fig = px.scatter(df, x="PC1", y="PC2", text="Sample", title=title)

        fig.update_traces(textposition="top center", marker=dict(size=12))
        fig.update_layout(
            xaxis_title=f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)",
            yaxis_title=f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)",
            template="plotly_white",
            height=500,
        )
        return fig

    def bar_plot(self, data: pd.DataFrame, x: str, y: str, title: str = "Bar Plot", color: str | None = None) -> go.Figure:
        """Create a bar plot."""
        fig = px.bar(data.head(20), x=x, y=y, color=color, title=title, template="plotly_white")
        fig.update_layout(height=400)
        return fig

    def dot_plot(self, enrichment_results: pd.DataFrame, title: str = "Enrichment Dot Plot") -> go.Figure:
        """Create a dot plot for enrichment results."""
        df = enrichment_results.head(15).copy()
        df["-log10(padj)"] = -np.log10(df["padj"].clip(lower=1e-300))

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["enrichment_factor"],
            y=df["term_name"],
            mode="markers",
            marker=dict(
                size=df["overlap"] * 5,
                color=df["-log10(padj)"],
                colorscale="YlOrRd",
                showscale=True,
                colorbar=dict(title="-log10(padj)"),
            ),
            text=df.apply(lambda r: f"Genes: {r['genes']}", axis=1),
            hovertemplate="<b>%{y}</b><br>Enrichment: %{x:.1f}x<br>%{text}<extra></extra>",
        ))

        fig.update_layout(
            title=title,
            xaxis_title="Enrichment Factor",
            yaxis_title="",
            template="plotly_white",
            height=max(400, len(df) * 30),
            yaxis=dict(autorange="reversed"),
        )
        return fig

    def sample_distribution(self, count_matrix: pd.DataFrame, title: str = "Read Count Distribution") -> go.Figure:
        """Plot read count distribution per sample."""
        fig = go.Figure()
        for col in count_matrix.columns:
            counts = count_matrix[col]
            counts = counts[counts > 0]
            fig.add_trace(go.Box(
                y=np.log10(counts + 1),
                name=col,
                boxpoints=False,
            ))
        fig.update_layout(
            title=title,
            yaxis_title="log10(count + 1)",
            template="plotly_white",
            height=400,
        )
        return fig

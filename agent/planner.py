import json
from typing import Any, Dict, List


class PipelinePlanner:
    """Plans bioinformatics analysis pipelines from natural language descriptions."""

    PIPELINE_TEMPLATES = {
        "rnaseq": {
            "name": "RNA-seq Differential Expression",
            "steps": [
                {
                    "step_id": "qc",
                    "tool": "fastqc",
                    "command": "fastqc {input_files} -o {output_dir}/qc/",
                    "description": "Quality control of raw FASTQ files",
                    "output": "QC reports (HTML)",
                },
                {
                    "step_id": "trim",
                    "tool": "trim_galore",
                    "command": "trim_galore --paired {r1} {r2} -o {output_dir}/trimmed/",
                    "description": "Adapter trimming and quality filtering",
                    "output": "Trimmed FASTQ files",
                    "depends_on": ["qc"],
                },
                {
                    "step_id": "align",
                    "tool": "STAR",
                    "command": "STAR --genomeDir {genome_dir} --readFilesIn {r1} {r2} --outSAMtype BAM SortedByCoordinate --outFileNamePrefix {output_dir}/align/",
                    "description": "Align reads to reference genome",
                    "output": "Sorted BAM file",
                    "depends_on": ["trim"],
                },
                {
                    "step_id": "count",
                    "tool": "featureCounts",
                    "command": "featureCounts -a {gtf} -o {output_dir}/counts.txt {bam_file}",
                    "description": "Gene-level read counting",
                    "output": "Count matrix",
                    "depends_on": ["align"],
                },
                {
                    "step_id": "de_analysis",
                    "tool": "DESeq2",
                    "command": "python -c 'from tools.rnaseq import RNASeqAnalyzer; ...'",
                    "description": "Differential expression analysis",
                    "output": "DE results table, plots",
                    "depends_on": ["count"],
                },
                {
                    "step_id": "enrichment",
                    "tool": "clusterProfiler",
                    "command": "python -c 'from tools.enrichment import EnrichmentAnalyzer; ...'",
                    "description": "GO/KEGG enrichment analysis",
                    "output": "Enrichment results, dot plots",
                    "depends_on": ["de_analysis"],
                },
            ],
        },
        "chipseq": {
            "name": "ChIP-seq Peak Calling",
            "steps": [
                {
                    "step_id": "qc",
                    "tool": "fastqc",
                    "command": "fastqc {input_files} -o {output_dir}/qc/",
                    "description": "Quality control",
                    "output": "QC reports",
                },
                {
                    "step_id": "trim",
                    "tool": "trim_galore",
                    "command": "trim_galore {input_files} -o {output_dir}/trimmed/",
                    "description": "Adapter trimming",
                    "output": "Trimmed FASTQ",
                    "depends_on": ["qc"],
                },
                {
                    "step_id": "align",
                    "tool": "bowtie2",
                    "command": "bowtie2 -x {genome_index} -U {reads} -S {output_dir}/align.sam",
                    "description": "Align to reference genome",
                    "output": "SAM/BAM file",
                    "depends_on": ["trim"],
                },
                {
                    "step_id": "call_peaks",
                    "tool": "macs2",
                    "command": "macs2 callpeak -t {treatment_bam} -c {control_bam} -f BAM -g hs -n {output_dir}/peaks",
                    "description": "Peak calling",
                    "output": "Peak files (narrowPeak, broadPeak)",
                    "depends_on": ["align"],
                },
            ],
        },
        "variant_calling": {
            "name": "Variant Calling (WGS/WES)",
            "steps": [
                {
                    "step_id": "qc",
                    "tool": "fastqc",
                    "command": "fastqc {input_files} -o {output_dir}/qc/",
                    "description": "Quality control",
                    "output": "QC reports",
                },
                {
                    "step_id": "align",
                    "tool": "bwa-mem2",
                    "command": "bwa mem {genome_index} {r1} {r2} | samtools sort -o {output_dir}/aligned.bam",
                    "description": "Align reads",
                    "output": "Sorted BAM",
                    "depends_on": ["qc"],
                },
                {
                    "step_id": "mark_duplicates",
                    "tool": "picard",
                    "command": "picard MarkDuplicates I={bam} O={output_dir}/dedup.bam M={output_dir}/metrics.txt",
                    "description": "Mark PCR duplicates",
                    "output": "Deduplicated BAM",
                    "depends_on": ["align"],
                },
                {
                    "step_id": "call_variants",
                    "tool": "gatk HaplotypeCaller",
                    "command": "gatk HaplotypeCaller -R {reference} -I {bam} -O {output_dir}/variants.g.vcf.gz -ERC GVCF",
                    "description": "Variant calling",
                    "output": "GVCF file",
                    "depends_on": ["mark_duplicates"],
                },
            ],
        },
    }

    def plan_from_request(self, request: str) -> Dict[str, Any]:
        """Create a pipeline plan from a natural language request."""
        request_lower = request.lower()

        if any(kw in request_lower for kw in ["rna-seq", "rnaseq", "rna seq", "差异表达", "差异基因"]):
            return self.PIPELINE_TEMPLATES["rnaseq"]
        elif any(kw in request_lower for kw in ["chip-seq", "chipseq", "chip seq", "peak"]):
            return self.PIPELINE_TEMPLATES["chipseq"]
        elif any(kw in request_lower for kw in ["variant", "突变", "snp", "wgs", "wes", "变异"]):
            return self.PIPELINE_TEMPLATES["variant_calling"]
        else:
            return {
                "name": "Custom Analysis",
                "steps": [],
                "note": "Could not auto-detect pipeline type. Please specify your analysis type.",
            }

    def get_pipeline_summary(self, pipeline: dict) -> str:
        """Generate a human-readable summary of a pipeline plan."""
        lines = [f"## Pipeline: {pipeline['name']}\n"]
        for i, step in enumerate(pipeline.get("steps", []), 1):
            deps = step.get("depends_on", [])
            dep_str = f" (after: {', '.join(deps)})" if deps else ""
            lines.append(f"**Step {i}: {step['step_id']}**{dep_str}")
            lines.append(f"  - Tool: `{step['tool']}`")
            lines.append(f"  - {step['description']}")
            lines.append(f"  - Output: {step['output']}\n")
        return "\n".join(lines)

    def to_snakemake(self, pipeline: dict, config: dict) -> str:
        """Convert a pipeline plan to Snakemake format."""
        rules = []
        for step in pipeline.get("steps", []):
            rule_name = step["step_id"]
            tool = step["tool"]
            command = step["command"]
            deps = step.get("depends_on", [])

            input_str = ", ".join([f'rules.{d}.output' for d in deps]) if deps else "[]"
            rules.append(f"""
rule {rule_name}:
    input: {input_str}
    output: "results/{rule_name}/"
    shell:
        """
            + '"' + command + '"'
            + """
""")

        header = f"""# Auto-generated Snakemake pipeline: {pipeline['name']}
# Generated by BioInfo Agent

configfile: "config.yaml"

"""
        return header + "\n".join(rules)

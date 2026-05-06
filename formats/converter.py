"""Bioinformatics format conversion utilities."""

import io
from typing import Any


class FormatConverter:
    """Convert between bioinformatics file formats."""

    SUPPORTED_FORMATS = ["fasta", "fastq", "bed", "gff", "gtf", "vcf", "sam", "csv", "tsv"]

    def detect_format(self, content: str) -> str:
        """Auto-detect the format of file content."""
        first_line = content.strip().split("\n")[0]

        if first_line.startswith(">"):
            return "fasta"
        elif first_line.startswith("@"):
            return "fastq"
        elif first_line.startswith("##fileformat=VCF"):
            return "vcf"
        elif first_line.startswith("##gff") or first_line.startswith("##gff-version"):
            return "gff"
        elif "\t" in first_line:
            fields = first_line.split("\t")
            if len(fields) >= 3 and fields[1].isdigit() and fields[2].isdigit():
                return "bed"
            elif len(fields) >= 9 and fields[6] in ["+", "-", "."]:
                return "gtf"
            return "tsv"
        elif "," in first_line:
            return "csv"
        return "unknown"

    def fasta_to_dataframe(self, content: str) -> list[dict]:
        """Parse FASTA to structured data."""
        records = []
        current = None
        for line in content.strip().split("\n"):
            if line.startswith(">"):
                if current:
                    records.append(current)
                current = {"id": line[1:].split()[0], "description": line[1:], "sequence": ""}
            elif current:
                current["sequence"] += line.strip()
        if current:
            records.append(current)
        for r in records:
            r["length"] = len(r["sequence"])
        return records

    def bed_to_dataframe(self, content: str) -> list[dict]:
        """Parse BED format."""
        records = []
        for line in content.strip().split("\n"):
            if line.startswith("#") or line.startswith("track") or not line.strip():
                continue
            fields = line.split("\t")
            if len(fields) >= 3:
                rec = {
                    "chrom": fields[0],
                    "start": int(fields[1]),
                    "end": int(fields[2]),
                }
                if len(fields) > 3:
                    rec["name"] = fields[3]
                if len(fields) > 4:
                    rec["score"] = fields[4]
                if len(fields) > 5:
                    rec["strand"] = fields[5]
                records.append(rec)
        return records

    def gtf_to_dataframe(self, content: str) -> list[dict]:
        """Parse GTF/GFF format."""
        records = []
        for line in content.strip().split("\n"):
            if line.startswith("#") or not line.strip():
                continue
            fields = line.split("\t")
            if len(fields) >= 9:
                attrs = {}
                for item in fields[8].split(";"):
                    item = item.strip()
                    if item and " " in item:
                        key, val = item.split(" ", 1)
                        attrs[key] = val.strip('"')
                records.append({
                    "seqname": fields[0],
                    "source": fields[1],
                    "feature": fields[2],
                    "start": int(fields[3]),
                    "end": int(fields[4]),
                    "score": fields[5],
                    "strand": fields[6],
                    "frame": fields[7],
                    "attributes": attrs,
                })
        return records

    def convert(self, content: str, target_format: str) -> Any:
        """Convert content to target format."""
        source_format = self.detect_format(content)

        if source_format == "fasta":
            return self.fasta_to_dataframe(content)
        elif source_format == "bed":
            return self.bed_to_dataframe(content)
        elif source_format in ["gtf", "gff"]:
            return self.gtf_to_dataframe(content)
        else:
            return {"format": source_format, "raw": content[:1000]}

    def get_supported_formats(self) -> list[str]:
        return self.SUPPORTED_FORMATS

"""Data validation utilities."""

from typing import Any


class DataValidator:
    """Validate bioinformatics data files."""

    def validate_fasta(self, content: str) -> dict[str, Any]:
        """Validate FASTA format."""
        errors = []
        warnings = []
        sequence_count = 0
        total_length = 0

        lines = content.strip().split("\n")
        in_sequence = False

        for i, line in enumerate(lines, 1):
            if line.startswith(">"):
                sequence_count += 1
                in_sequence = True
                if len(line) == 1:
                    warnings.append(f"Line {i}: Empty sequence header")
            elif in_sequence:
                invalid_chars = set(line.strip()) - set("ACGTUNRYMKSWBDHVacgtunrymksbwdhv.-")
                if invalid_chars:
                    warnings.append(f"Line {i}: Non-standard characters: {invalid_chars}")
                total_length += len(line.strip())
            else:
                errors.append(f"Line {i}: Content before first header")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "sequence_count": sequence_count,
            "total_length": total_length,
        }

    def validate_fastq(self, content: str) -> dict[str, Any]:
        """Validate FASTQ format."""
        errors = []
        lines = content.strip().split("\n")
        read_count = 0

        i = 0
        while i < len(lines):
            if not lines[i].startswith("@"):
                errors.append(f"Line {i+1}: Expected '@' header, got: {lines[i][:50]}")
                i += 1
                continue

            if i + 3 >= len(lines):
                errors.append(f"Line {i+1}: Incomplete FASTQ record")
                break

            seq = lines[i + 1]
            qual = lines[i + 3]

            if lines[i + 2] != "+":
                errors.append(f"Line {i+3}: Expected '+' separator")

            if len(seq) != len(qual):
                errors.append(f"Line {i+1}: Sequence length ({len(seq)}) != Quality length ({len(qual)})")

            read_count += 1
            i += 4

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "read_count": read_count,
        }

    def validate_vcf(self, content: str) -> dict[str, Any]:
        """Validate VCF format."""
        errors = []
        warnings = []
        variant_count = 0
        header_found = False

        for i, line in enumerate(content.strip().split("\n"), 1):
            if line.startswith("##"):
                continue
            if line.startswith("#CHROM"):
                header_found = True
                continue
            if not header_found:
                errors.append(f"Line {i}: Data before #CHROM header")
                continue

            fields = line.split("\t")
            if len(fields) < 8:
                errors.append(f"Line {i}: Insufficient columns ({len(fields)}, need >= 8)")
            else:
                variant_count += 1
                try:
                    pos = int(fields[1])
                except ValueError:
                    errors.append(f"Line {i}: Invalid position: {fields[1]}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "variant_count": variant_count,
        }

    def validate(self, content: str, format_type: str) -> dict[str, Any]:
        """Validate content based on format type."""
        validators = {
            "fasta": self.validate_fasta,
            "fastq": self.validate_fastq,
            "vcf": self.validate_vcf,
        }
        validator = validators.get(format_type)
        if validator:
            return validator(content)
        return {"valid": True, "errors": [], "warnings": [f"No validator for format: {format_type}"]}

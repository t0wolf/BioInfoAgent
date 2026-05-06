"""Sequence analysis tools."""

from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
from Bio.Seq import Seq
from Bio.Blast import NCBIWWW, NCBIXML
import io
from typing import Any


class SequenceAnalyzer:
    """Tools for DNA/RNA/protein sequence analysis."""

    def gc_content(self, sequence: str) -> dict[str, float]:
        """Calculate GC content of a sequence."""
        seq = Seq(sequence.upper())
        gc = gc_fraction(seq) * 100
        return {
            "gc_content": round(gc, 2),
            "length": len(sequence),
            "g_count": sequence.upper().count("G"),
            "c_count": sequence.upper().count("C"),
            "a_count": sequence.upper().count("A"),
            "t_count": sequence.upper().count("T"),
        }

    def find_orfs(self, sequence: str, min_length: int = 30) -> list[dict]:
        """Find open reading frames in a DNA sequence."""
        seq = Seq(sequence.upper())
        orfs = []
        for frame in range(3):
            translated = seq[frame:].translate()
            aa_str = str(translated)
            start = 0
            while start < len(aa_str):
                if aa_str[start] == "M":
                    stop = aa_str.find("*", start)
                    if stop != -1 and (stop - start) * 3 >= min_length:
                        orfs.append({
                            "frame": frame + 1,
                            "start": frame + start * 3,
                            "end": frame + stop * 3 + 3,
                            "length_aa": stop - start,
                            "length_nt": (stop - start) * 3,
                            "sequence": str(seq[frame + start * 3: frame + stop * 3 + 3]),
                        })
                    start = stop + 1 if stop != -1 else len(aa_str)
                else:
                    start += 1
        return sorted(orfs, key=lambda x: x["length_nt"], reverse=True)

    def reverse_complement(self, sequence: str) -> str:
        """Get reverse complement of a DNA sequence."""
        return str(Seq(sequence.upper()).reverse_complement())

    def translate(self, sequence: str, frame: int = 0) -> str:
        """Translate DNA to protein."""
        seq = Seq(sequence.upper())
        return str(seq[frame:].translate())

    def parse_fasta(self, fasta_text: str) -> list[dict]:
        """Parse FASTA format text."""
        records = []
        for record in SeqIO.parse(io.StringIO(fasta_text), "fasta"):
            records.append({
                "id": record.id,
                "description": record.description,
                "sequence": str(record.seq),
                "length": len(record.seq),
                "gc_content": round(gc_fraction(record.seq) * 100, 2),
            })
        return records

    def composition(self, sequence: str) -> dict[str, int]:
        """Get nucleotide/amino acid composition."""
        seq = sequence.upper()
        comp = {}
        for char in seq:
            comp[char] = comp.get(char, 0) + 1
        return dict(sorted(comp.items()))

    def analyze(self, sequence: str) -> dict[str, Any]:
        """Run a full analysis on a sequence."""
        return {
            "gc_content": self.gc_content(sequence),
            "composition": self.composition(sequence),
            "orfs": self.find_orfs(sequence)[:5],  # Top 5 ORFs
            "reverse_complement": self.reverse_complement(sequence)[:100] + "...",
        }

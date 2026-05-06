"""Database query tools for NCBI, Ensembl, UniProt."""

import requests
import xml.etree.ElementTree as ET
from typing import Any


class DatabaseQuerier:
    """Query external bioinformatics databases."""

    NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    ENSEMBL_BASE = "https://rest.ensembl.org"
    UNIPROT_BASE = "https://rest.uniprot.org"

    def search_gene_ncbi(self, query: str, organism: str = "Homo sapiens", max_results: int = 5) -> list[dict]:
        """Search NCBI Gene database."""
        try:
            # Search for gene IDs
            search_url = f"{self.NCBI_BASE}/esearch.fcgi"
            params = {
                "db": "gene",
                "term": f"{query}[Gene Name] AND {organism}[Organism]",
                "retmax": max_results,
                "retmode": "json",
            }
            resp = requests.get(search_url, params=params, timeout=10)
            data = resp.json()
            ids = data.get("esearchresult", {}).get("idlist", [])

            if not ids:
                return []

            # Fetch gene summaries
            summary_url = f"{self.NCBI_BASE}/esummary.fcgi"
            params = {"db": "gene", "id": ",".join(ids), "retmode": "json"}
            resp = requests.get(summary_url, params=params, timeout=10)
            summary_data = resp.json()

            results = []
            for gid in ids:
                info = summary_data.get("result", {}).get(gid, {})
                if info:
                    results.append({
                        "gene_id": gid,
                        "name": info.get("name", ""),
                        "description": info.get("description", ""),
                        "organism": info.get("organism", {}).get("scientificname", ""),
                        "chromosome": info.get("chromosome", ""),
                        "map_location": info.get("maplocation", ""),
                    })
            return results
        except Exception as e:
            return [{"error": str(e)}]

    def get_sequence_ncbi(self, accession: str) -> dict[str, Any]:
        """Fetch a sequence from NCBI."""
        try:
            url = f"{self.NCBI_BASE}/efetch.fcgi"
            params = {"db": "nucleotide", "id": accession, "rettype": "fasta", "retmode": "text"}
            resp = requests.get(url, params=params, timeout=10)
            lines = resp.text.strip().split("\n")
            header = lines[0] if lines else ""
            sequence = "".join(lines[1:]) if len(lines) > 1 else ""
            return {
                "accession": accession,
                "header": header,
                "sequence": sequence,
                "length": len(sequence),
            }
        except Exception as e:
            return {"error": str(e)}

    def search_ensembl(self, gene_name: str, species: str = "human") -> list[dict]:
        """Search Ensembl for gene information."""
        try:
            url = f"{self.ENSEMBL_BASE}/lookup/symbol/{species}/{gene_name}"
            headers = {"Content-Type": "application/json"}
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return [{
                    "id": data.get("id"),
                    "display_name": data.get("display_name"),
                    "description": data.get("description"),
                    "biotype": data.get("biotype"),
                    "chromosome": data.get("seq_region_name"),
                    "start": data.get("start"),
                    "end": data.get("end"),
                    "strand": data.get("strand"),
                }]
            return [{"error": f"Not found: {gene_name}"}]
        except Exception as e:
            return [{"error": str(e)}]

    def search_uniprot(self, query: str, max_results: int = 5) -> list[dict]:
        """Search UniProt for protein information."""
        try:
            url = f"{self.UNIPROT_BASE}/uniprotkb/search"
            params = {"query": f"({query}) AND (organism_id:9606)", "format": "json", "size": max_results}
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()

            results = []
            for entry in data.get("results", []):
                results.append({
                    "accession": entry.get("primaryAccession"),
                    "protein_name": entry.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", ""),
                    "gene_name": entry.get("genes", [{}])[0].get("geneName", {}).get("value", "") if entry.get("genes") else "",
                    "organism": entry.get("organism", {}).get("scientificName", ""),
                    "length": entry.get("sequence", {}).get("length", 0),
                })
            return results
        except Exception as e:
            return [{"error": str(e)}]

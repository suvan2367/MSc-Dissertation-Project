# MSC DISSERTATION PROJECT

### TITLE: "Sequence and pharmacophore analysis of DNA recognition helices in the HTH family of proteins and their binding DNA"

## Overview 

The helix-turn-helix (HTH) motif is a highly conserved structural domain found in a wide range
of DNA-binding proteins across prokaryotes and eukaryotes. This project aims to investigate
the sequence and pharmacophore patterns of HTH motifs, particularly within the recognition
helices responsible for specific DNA interaction.



## Scripts

### 1. `conv_seq.py` - Sequence Converter
Converts protein sequences into pharmacophore representations by replacing standard amino acid codes with simplified pharmacophore groups.

**Features:**
- Takes a FASTA file as input
- Applies character-by-character replacement based on predefined mapping rules (e.g., hydrophobic residues like V, L, I, M → H)
- Outputs a new FASTA file with converted sequences while preserving headers
- Useful for reducing sequence complexity and focusing on functional properties rather than specific amino acids

**Usage:**
```bash
python conv_seq.py
```

---

### 2. `extract_dna_seqs.py` - DNA Sequence Extractor
Extracts DNA sequences from PDB structures that are homodimers.

**Features:**
- Reads PDB IDs from CSV files (`pdb_ids_cluster_*.csv`)
- Queries RCSB PDB to check stoichiometry (filters for "Homo 2-mer" structures)
- Downloads FASTA sequences and extracts only DNA chains
- Saves filtered DNA sequences to cluster-specific FASTA files (`dna_sequences_cluster_*.fasta`)
- Processes multiple cluster files automatically

**Usage:**
```bash
python extract_dna_seqs.py
```

---

### 3. `extract_pdbids.py` - PDB ID Extractor
Parses FASTA file headers to extract PDB identifiers.

**Features:**
- Reads FASTA files matching the pattern `cluster_*.fasta` (excluding consensus files)
- Uses regex to extract PDB IDs from headers (format: `>PDBID_...`)
- Exports extracted IDs to CSV files (`pdb_ids_cluster_*.csv`)
- Useful for creating ID lists for downstream processing

**Usage:**
```bash
python extract_pdbids.py
```

---

### 4. `extract_protein_seqs.py` - Protein Sequence Extractor
Extracts protein sequences from homodimeric PDB structures.

**Features:**
- Reads PDB IDs from a CSV file (`HTH_NAKB.csv`)
- Queries RCSB PDB to verify stoichiometry (filters for "Homo 2-mer")
- Downloads FASTA sequences and filters out DNA sequences using multiple pattern matching
- Saves only protein sequences to output FASTA file (`hth_homodimers.fasta`)
- Specifically designed for helix-turn-helix (HTH) protein analysis

**Usage:**
```bash
python extract_protein_seqs.py
```

---

### 5. `getpdb.py` - PDB File Downloader
Batch downloads PDB structure files from RCSB PDB.

**Features:**
- Reads a CSV file containing PDB IDs (column: `pdb_id`)
- Downloads corresponding `.pdb` files from RCSB PDB database
- Saves files to a specified output directory
- Provides download status feedback for each structure

**Usage:**
```bash
python getpdb.py
```

---

### 6. `matrix.py` - BLOSUM Matrix Calculator
Generates a custom BLOSUM-like substitution matrix from pharmacophore frequency data.

**Features:**
- Reads substitution frequency matrix from CSV (`pharmacophore_matrix.csv`)
- Calculates observed and expected frequencies based on pharmacophore groups
- Computes log-odds scores and converts to integer substitution scores
- Uses predefined amino acid frequencies and pharmacophore mappings (F, C, X, H, P, O, R, W, G)
- Outputs the resulting BLOSUM matrix to CSV (`blosum_matrix.csv`)

**Usage:**
```bash
python matrix.py
```

---

### 7. `score.py` - Consensus Sequence Scorer
Calculates consensus sequences and scores from multiple sequence alignments.

**Features:**
- Reads Clustal format alignment files (`.aln`)
- Determines the most frequent residue at each position
- Calculates position-specific consensus scores based on residue frequency
- Computes cumulative consensus score across the entire alignment
- Outputs consensus sequence, per-position scores, and total score to a text file
- Assigns zero score to gap positions

**Usage:**
```bash
python score.py
```

---

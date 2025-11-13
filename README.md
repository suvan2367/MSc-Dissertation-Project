# MSC DISSERTATION PROJECT

TITLE: "Sequence and pharmacophore analysis of DNA recognition helices in the HTH family of proteins and their binding DNA"

Overview: The helix-turn-helix (HTH) motif is a highly conserved structural domain found in a wide range
of DNA-binding proteins across prokaryotes and eukaryotes. This project aims to investigate
the sequence and pharmacophore patterns of HTH motifs, particularly within the recognition
helices responsible for specific DNA interaction.

# Project Scripts Documentation

## Overview
This repository contains a suite of Python scripts for analyzing protein-DNA complexes, extracting sequences from PDB structures, and generating custom substitution matrices based on pharmacophore representations.

---

## Scripts

### 1. `conv_seq.py` - Sequence Converter
Converts protein sequences into pharmacophore representations by replacing standard amino acid codes with simplified pharmacophore groups.

**Features:**
- Takes a FASTA file as input
- Applies character-by-character replacement based on predefined mapping rules (e.g., hydrophobic residues like V, L, I, M → H)
- Outputs a new FASTA file with converted sequences while preserving headers
- Useful for reducing sequence complexity and focusing on functional properties rather than specific amino acids


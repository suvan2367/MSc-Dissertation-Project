import csv
import subprocess
import os
import re

def get_stoichiometry(pdb_id):
    bash_command = f"curl -L -s https://www.rcsb.org/structure/{pdb_id} | grep -o -P '.{{0,0}}Stoich.{{0,30}}' | cut -c25-35"
    try:
        result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error fetching stoichiometry for {pdb_id}: {e}")
        return None

def get_protein_sequence(pdb_id):
    bash_command = f"curl -L -s https://www.rcsb.org/fasta/entry/{pdb_id}/display"
    try:
        result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, check=True)
        fasta_data = result.stdout.strip()

        # Extract only protein sequences (exclude DNA sequences)
        protein_sequences = []
        current_header = None
        current_sequence = []

        for line in fasta_data.split('\n'):
            if line.startswith('>'):
                if current_header:
                    header_text = current_header.lower()
                    # Avoid DNA sequences based on multiple patterns
                    if not (re.search(r'\bdna\b', header_text) or 
                            re.search(r"5'-d\(", header_text) or 
                            re.search(r"3'-d\(", header_text) or 
                            re.search(r'\b[acgtu]{5,}\b', current_sequence[0], re.IGNORECASE)):
                        protein_sequences.append((current_header, ''.join(current_sequence)))
                current_header = line
                current_sequence = []
            else:
                current_sequence.append(line)

        if current_header:
            header_text = current_header.lower()
            if not (re.search(r'\bdna\b', header_text) or 
                    re.search(r"5'-d\(", header_text) or 
                    re.search(r"3'-d\(", header_text) or 
                    re.search(r'\b[acgtu]{5,}\b', current_sequence[0], re.IGNORECASE)):
                protein_sequences.append((current_header, ''.join(current_sequence)))

        return protein_sequences

    except subprocess.CalledProcessError as e:
        print(f"Error fetching sequence for {pdb_id}: {e}")
        return []

def main():
    input_csv = "HTH_NAKB.csv"  # Your input CSV file
    output_fasta = "hth_homodimers.fasta"

    if not os.path.exists(input_csv):
        print(f"Input CSV file '{input_csv}' not found.")
        return

    with open(input_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        if 'ID' not in reader.fieldnames:
            print("CSV file must contain a column named 'ID'")
            return

        with open(output_fasta, 'w') as fasta_file:
            for row in reader:
                pdb_id = row['ID'].strip()
                if not pdb_id:
                    continue

                print(f"Processing PDB ID: {pdb_id}")
                stoichiometry = get_stoichiometry(pdb_id)

                if stoichiometry == "Homo 2-mer":
                    print(f"Homo 2-mer found for {pdb_id}. Fetching protein sequence...")
                    protein_sequences = get_protein_sequence(pdb_id)

                    for header, sequence in protein_sequences:
                        fasta_file.write(f"{header}\n{sequence}\n")

    print(f"Protein sequences saved to {output_fasta}")


if __name__ == "__main__":
    main()


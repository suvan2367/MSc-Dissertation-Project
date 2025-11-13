import csv
import subprocess
import os
import re
import glob

def get_stoichiometry(pdb_id):
    bash_command = f"curl -L -s https://www.rcsb.org/structure/{pdb_id} | grep -o -P '.{{0,0}}Stoich.{{0,30}}' | cut -c25-35"
    try:
        result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error fetching stoichiometry for {pdb_id}: {e}")
        return None

def get_dna_sequence(pdb_id):
    bash_command = f"curl -L -s https://www.rcsb.org/fasta/entry/{pdb_id}/display"
    try:
        result = subprocess.run(bash_command, shell=True, capture_output=True, text=True, check=True)
        fasta_data = result.stdout.strip()

        # Extract only DNA sequences
        dna_sequences = []
        current_header = None
        current_sequence = []

        for line in fasta_data.split('\n'):
            if line.startswith('>'):
                if current_header and re.search(r'\bDNA\b', current_header, re.IGNORECASE):  # Keep only DNA
                    dna_sequences.append((current_header, ''.join(current_sequence)))
                current_header = line
                current_sequence = []
            else:
                current_sequence.append(line)

        if current_header and re.search(r'\bDNA\b', current_header, re.IGNORECASE):  # Add last sequence
            dna_sequences.append((current_header, ''.join(current_sequence)))

        return dna_sequences

    except subprocess.CalledProcessError as e:
        print(f"Error fetching sequence for {pdb_id}: {e}")
        return []

def process_csv_file(csv_file):
    cluster_number = csv_file.split("_")[-1].split(".")[0]  # Extract the cluster number
    output_fasta = f"dna_sequences_cluster_{cluster_number}.fasta"

    if not os.path.exists(csv_file):
        print(f"CSV file '{csv_file}' not found.")
        return

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        if 'PDB_ID' not in reader.fieldnames:  # Ensure correct column name
            print(f"CSV file '{csv_file}' must contain a column named 'PDB_ID'")
            return

        with open(output_fasta, 'w') as fasta_file:
            for row in reader:
                pdb_id = row['PDB_ID'].strip()
                if not pdb_id:
                    continue

                print(f"Processing PDB ID: {pdb_id} from {csv_file}")
                stoichiometry = get_stoichiometry(pdb_id)

                if stoichiometry == "Homo 2-mer":
                    print(f"Homo 2-mer found for {pdb_id}. Fetching DNA sequence...")
                    dna_sequences = get_dna_sequence(pdb_id)

                    for header, sequence in dna_sequences:
                        fasta_file.write(f"{header}\n{sequence}\n")

    print(f"DNA sequences saved to {output_fasta}")

def main():
    csv_files = glob.glob("pdb_ids_cluster_*.csv")  # Get all matching CSV files
    if not csv_files:
        print("No input CSV files found.")
        return

    for csv_file in csv_files:
        process_csv_file(csv_file)

if __name__ == "__main__":
    main()


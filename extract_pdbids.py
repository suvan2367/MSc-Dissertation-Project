import re
import csv
import glob

def extract_pdb_ids(fasta_file, output_csv):
    pdb_ids = []

    with open(fasta_file, "r") as file:
        for line in file:
            if line.startswith(">"):  # Check if it's a header line
                match = re.match(r">(\w+)_", line)  # Extract PDB ID before "_"
                if match:
                    pdb_id = match.group(1)  # Get the matched PDB ID
                    pdb_ids.append([pdb_id])  # Store as a list for CSV writing

    # Write PDB IDs to CSV
    with open(output_csv, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["PDB_ID"])  # Write header
        writer.writerows(pdb_ids)  # Write extracted PDB IDs

    print(f"Extracted {len(pdb_ids)} PDB IDs from {fasta_file} and saved to {output_csv}")

# Process only the correct FASTA files
fasta_files = [file for file in glob.glob("cluster_*.fasta") if "_cons" not in file]  # Exclude *_cons.fasta

for fasta_file in fasta_files:
    cluster_number = fasta_file.split("_")[1].split(".")[0]  # Extract the cluster number
    output_csv = f"pdb_ids_cluster_{cluster_number}.csv"  # Create output filename
    extract_pdb_ids(fasta_file, output_csv)


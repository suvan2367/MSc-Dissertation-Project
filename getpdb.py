import os
import requests
import pandas as pd

def download_pdb(pdb_id, output_dir):
    pdb_url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
    response = requests.get(pdb_url)
    
    if response.status_code == 200:
        with open(os.path.join(output_dir, f'{pdb_id}.pdb'), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {pdb_id}")
    else:
        print(f"Failed to download: {pdb_id}")

def main(csv_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Assuming the CSV has a column named 'pdb_id'
    if 'pdb_id' not in df.columns:
        print("Error: 'pdb_id' column not found in CSV file.")
        return

    # Download each PDB file
    for pdb_id in df['pdb_id']:
        download_pdb(str(pdb_id).strip(), output_dir)

if __name__ == '__main__':
    csv_file = input("Enter the path to the CSV file containing PDB IDs: ")
    output_dir = input("Enter the output directory for downloaded PDB files: ")
    main(csv_file, output_dir)


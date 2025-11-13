import numpy as np
import csv

def read_substitution_frequencies(file_path):
    """Read a substitution frequency matrix from a CSV file."""
    with open(file_path, "r") as csvfile:
        reader = list(csv.reader(csvfile))
        amino_acids = reader[0][1:]  # Extract amino acid labels
        freq_matrix = np.array([list(map(float, row[1:])) for row in reader[1:]])
    return amino_acids, freq_matrix

def calculate_blosum_from_freq(freq_matrix, amino_acids, output_file, pseudocount=1e-10):
    """Calculate the BLOSUM matrix while ensuring no zero values appear."""
    total_pairs = np.sum(freq_matrix)
    
    # Convert to probabilities
    frequencies = freq_matrix / total_pairs  

    # Compute expected frequencies (outer product of individual AA frequencies)
    #aa_freqs = np.sum(frequencies, axis=1)
    #expected_freqs = np.outer(aa_freqs, aa_freqs)
    
    # Given amino acid frequencies
    aa_counts = {
    'A': 72060, 'R': 47671, 'N': 38063, 'D': 48555, 'C': 22533,
    'Q': 31697, 'E': 54594, 'G': 77275, 'H': 22870, 'I': 57132,
    'L': 84849, 'K': 51457, 'M': 22248, 'F': 40562, 'P': 39717,
    'S': 54328, 'T': 50667, 'W': 12772, 'Y': 31580, 'V': 66446}
    
    # Pharmacophore groups
    pharmacophore_mapping = {'F': {'N', 'Q', 'S', 'T'},'C': {'C'},
    'X': {'D', 'E'},'H': { 'A', 'V', 'L', 'I', 'M'},'P': {'P'},'O': {'H', 'K', 'R'},
    'R': {'F', 'Y'}, 'W': {'W'}, 'G': {'G'}
    }
    # Initialize an empty dictionary to store the pharmacophore frequencies
    pharmacophore_frequencies = {}
    
    # Sum the counts for each pharmacophore group
    for group, residues in pharmacophore_mapping.items():
    	pharmacophore_frequencies[group] = sum(aa_counts[res] for res in residues)
    
    print('AA Frequencies')
    
    # Print the results
    for key, value in pharmacophore_frequencies.items():
    	print(f"{key}: {value}")
    
    # Calculate total frequency
    total_frequency = sum(pharmacophore_frequencies.values())
    
    # Print the total
    print(f"Total Frequency: {total_frequency}")
    
    # Ensure consistent order by sorting keys
    sorted_pharmacophore_keys = sorted(pharmacophore_mapping.keys())
    
    # Recalculate frequencies with a sorted order
    pharmacophore_probabilities = {
    key: pharmacophore_frequencies[key] / total_frequency for key in sorted_pharmacophore_keys
    }
    
    # Print the probabilities
    print('\nProbabilities')                                                                                                                                           
    for key, value in pharmacophore_probabilities.items():
    	print(f"{key}: {value:.4f}")  # Rounded to 4 decimal places
    
    # Convert probabilities into a sorted list
    prob_values = np.array([pharmacophore_probabilities[key] for key in sorted_pharmacophore_keys])
    
    # Compute expected frequencies using the sorted list
    expected_frequencies = np.outer(prob_values, prob_values)
    
    # Convert to a nested list for matrix calculations
    expected_freqs = expected_frequencies.tolist()

    # Ensure no zero values in expected frequencies
    expected_freqs = np.where(expected_freqs == 0, pseudocount, expected_freqs)
    
    #Print the expected frequencies
    print('\nExpected frequencies')
    for row in expected_freqs:
    	print([round(val, 6) for val in row])
    
    # Compute log-odds scores
    log_odds = np.log2(frequencies / expected_freqs)
    
    print("Log odds:")
    print(log_odds)
    
    # Round off to the nearest integer
    blosum_matrix = np.rint(log_odds * 2).astype(int)  # Use np.rint() for nearest integer rounding

    # Save the matrix
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["AA"] + amino_acids)  # Header row
        for i, aa in enumerate(amino_acids):
            writer.writerow([aa] + list(blosum_matrix[i]))

    return blosum_matrix

def print_blosum(amino_acids, matrix):
    """Print the BLOSUM matrix."""
    print(f"{'AA':>3} {' '.join(f'{aa:>5}' for aa in amino_acids)}")
    for i, aa in enumerate(amino_acids):
        row = " ".join(f"{matrix[i, j]:5.2f}" for j in range(len(amino_acids)))
        print(f"{aa:>3} {row}")
        
# Main execution
if __name__ == "__main__":
    input_csv = "pharmacophore_matrix.csv"  # Provide the frequency matrix file
    output_csv = "blosum_matrix.csv"

    amino_acids, freq_matrix = read_substitution_frequencies(input_csv)
    blosum_matrix = calculate_blosum_from_freq(freq_matrix, amino_acids, output_csv)
    print_blosum(amino_acids, blosum_matrix)

    print(f"BLOSUM matrix has been saved to {output_csv}")


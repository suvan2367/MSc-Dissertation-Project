def replace_chars(input_str, to_replace, replace_with):
    
    result = ""
    for char in input_str:
        if char in to_replace:
            i = to_replace.index(char)
            result += replace_with[i]
        else:
            result += char
    return result

def process_fasta(input_file, output_file, to_replace, replace_with):
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith(">"):  # Header line
                outfile.write(line)
            else:  # Sequence line
                processed_sequence = replace_chars(line.strip(), to_replace, replace_with)
                outfile.write(processed_sequence + "\n")

# Define the replacement rules
to_replace = ['G', 'A', 'V', 'L', 'I', 'M', 'P', 'F', 'W', 'Y', 'S', 'T', 'C', 'N', 'Q', 'H', 'K', 'R', 'D', 'E']
replace_with = ['G', 'H', 'H', 'H', 'H', 'H', 'P', 'R', 'w', 'R', 'F', 'F', 'C', 'F', 'F', 'O', 'O', 'O', 'N', 'N']

# Input and output FASTA file paths
input_file = input("Enter the input FASTA file path: ")
output_file = input("Enter the output FASTA file path: ")

# Process the FASTA file
process_fasta(input_file, output_file, to_replace, replace_with)

print(f"Processed sequences have been saved to {output_file}.")


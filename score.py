from Bio import AlignIO
from collections import Counter

def calculate_consensus_score(alignment_file):
    # Read alignment
    alignment = AlignIO.read(alignment_file, "clustal")
    num_sequences = len(alignment)
    alignment_length = alignment.get_alignment_length()
    
    consensus_seq = ""
    consensus_scores = []
    
    for i in range(alignment_length):
        column = alignment[:, i]  # Extract column at position i
        freq_count = Counter(column)  # Count frequency of each residue
        
        # Get most frequent residue and its count
        most_common_residue, count = freq_count.most_common(1)[0]  
        consensus_seq += most_common_residue
        
        # If consensus is a gap, score it as zero
        if most_common_residue == "-":
            score = 0.0
        else:
            score = count  # Calculate consensus score
        
        consensus_scores.append(score)
    
    # Calculate cumulative consensus score
    cumulative_score = sum(consensus_scores)

    return consensus_seq, consensus_scores, cumulative_score


def write_output(consensus_seq, consensus_scores, cumulative_score, output_file):
    with open(output_file, "w") as f:
        f.write(">Consensus_Sequence\n")
        f.write(consensus_seq + "\n\n")
        
        f.write(">Consensus_Scores\n")
        f.write(" ".join(f"{score:.2f}" for score in consensus_scores) + "\n\n")
        
        f.write(f">Cumulative_Consensus_Score\n{cumulative_score:.2f}\n")


if __name__ == "__main__":
    input_file = "cluster_0.aln"  # Change this to your input .aln file
    output_file = "consensus_output_0.txt"
    
    consensus_seq, consensus_scores, cumulative_score = calculate_consensus_score(input_file)
    write_output(consensus_seq, consensus_scores, cumulative_score, output_file)
    
    print(f"Consensus sequence and scores saved in {output_file}")
    print(f"Cumulative Consensus Score: {cumulative_score:.2f}")


import pandas as pd
from Bio import SeqIO
from itertools import combinations
import gzip

import datetime

start = datetime.datetime.now()
print(start)

# Load uniprot matches
uniprot_matches = pd.read_excel("../data/defense_finder/refseq2uniprot_script/2025-06-24_RefSeq2Uniprot_mapping.xlsx", sheet_name="uniprot_matches")

# Load sequences from the FASTA file into a dictionary
fasta_file = "../data/uniprot_id_mapping_files/2025-06-24_bacterial_genomes_fasta_sequences-subset.fasta.gz"
seq_dict = {}

with gzip.open(fasta_file, "rt") as handle:
    for record in SeqIO.parse(handle, "fasta"):
        accession = record.id.split('|')[1] if '|' in record.id else record.id
        seq_dict[accession] = str(record.seq).upper()
        

# Group and compare as before
for refseq_id, group_df in uniprot_matches.groupby("RefSeq"):
    uniprot_ids = group_df["UniProtKB-AC"].dropna().unique()
    sequences = {uid: seq_dict.get(uid) for uid in uniprot_ids if uid in seq_dict}
    
    print(f"\nRefSeq ID: {refseq_id}")
    
    if len(sequences) < 2:
        print(f"  Not enough sequences found to compare (found {len(sequences)}).")
        continue
    
    all_same = True
    for acc1, acc2 in combinations(sequences, 2):
        if sequences[acc1] != sequences[acc2]:
            print(f" For {refseq_id}, {acc1} and {acc2} have DIFFERENT sequences.")
            all_same = False
        else:
            print(f" For {refseq_id}, {acc1} and {acc2} have SAME sequences.")
    
    if all_same:
        print(f"For {refseq_id}, All associated UniProtKB-AC accessions have the SAME sequence.")
    else:
        print(f"Not all sequences match for {refseq_id}.")

# Report missing accessions
missing = set(uniprot_matches["UniProtKB-AC"].dropna().unique()) - set(seq_dict.keys())
if missing:
    print("\nUniProtKB-AC accessions not found in FASTA file:")
    print(", ".join(missing))
    
    
print(missing)



end = datetime.datetime.now()
print(end)

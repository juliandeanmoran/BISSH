import pandas as pd
import re

import datetime

x = datetime.datetime.now()
print(x)

# Step 1: Load accessions into a set
accessions_df=pd.read_excel("../data/defense_finder/2025-06-24_df_refseq_clean_up.xlsx",sheet_name="uniq_accs_w_uniq_values_ranked")

print(f"There are {accessions_df.shape[0]} in the input file .../data/defense_finder/2025-06-24_df_refseq_clean_up.xlsx (sheet: uniq_accs_w_uniq_values_ranked)")


# Step 2: Load uniprot ID mapping file
input_file = "../data/uniprot_id_mapping_files/idmapping.RefSeq.clean.dat"
headers = [
    "UniProtKB-AC", "RefSeq"
]

uniprot_mapping_df=pd.read_csv(input_file,sep="\t", header=None, names=headers,dtype=str)
print(f"uniprot_mapping_df shape: {uniprot_mapping_df.shape}")

#uniprot_mapping_df = uniprot_mapping_df.dropna(subset=["RefSeq"])
#print(f"uniprot_mapping_df shape after dropping rows with NA: {uniprot_mapping_df.shape}")


#uniprot_mapping_df_expanded = uniprot_mapping_df.assign(
#    RefSeq=uniprot_mapping_df["RefSeq"].str.split(r"[;|, ]+")
#).explode("RefSeq")

#print(f"uniprot_mapping_df_expanded shape after splitting RefSeq IDs into separate rows: {uniprot_mapping_df_expanded.shape}")


# Step 3: Merge the dataframes
print("Merging the dataframes now")
merged_df=pd.merge(accessions_df,uniprot_mapping_df,left_on="accession_in_sys",right_on="RefSeq",how="left")

# Step 4: Write dataframe to TSV file
with pd.ExcelWriter('../data/defense_finder/refseq2uniprot_script/2025-06-24_refseq2uniprot-ALL.xlsx') as writer:   
    merged_df.to_excel(writer,index=False)

unmatched_df = merged_df[merged_df["RefSeq"].isna()]
matches_df = merged_df[merged_df["RefSeq"].notna()]


with pd.ExcelWriter('../data/defense_finder/refseq2uniprot_script/2025-06-24_RefSeq2Uniprot_mapping.xlsx') as writer:   
    unmatched_df[["accession_in_sys", "type", "subtype", "species","sys_id","sys_beg","sys_end","duplicate_count","rank"]].to_excel(writer, sheet_name="no_uniprot_matches", index=False)
    matches_df.to_excel(writer, sheet_name="uniprot_matches", index=False)
    

x = datetime.datetime.now()
print(x)
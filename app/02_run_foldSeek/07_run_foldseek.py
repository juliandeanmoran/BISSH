import pandas as pd
from ccm_benchmate.structure.structure import Structure
import subprocess
import argparse
from datetime import date

parser = argparse.ArgumentParser(description="Run foldseek.")
parser.add_argument("input_file", help="Path to input file with no annotations")
parser.add_argument("batch_num", help="Number of the batch, eg: batch_1")
args = parser.parse_args()

no_annots_df=pd.read_csv(f"../{args.input_file}")
#no_annots_df=pd.read_csv("../results/annotate_results/2025-07-14_results_batch2_no_annots.csv")
no_na=no_annots_df[~no_annots_df["protein_id"].isna()]

bacterial_proteins=set(no_na["defense_system_protein_id"].tolist())
human_proteins=set(no_na["protein_id"].tolist())

# Download structures

print(f"Downloading {len(bacterial_proteins)} bacterial proteins to ../data/structures/bacterial/{args.batch_num}")
for prot in bacterial_proteins:
    structure = Structure()
    try:
        structure.download(
            id=prot,           # PDB or UniProt ID
            source="AFDB",        # "PDB" or "AFDB" 
            destination=f"../data/structures/bacterial/{args.batch_num}", # Output directory
            load_after_download=False
        )
    except Exception as e:
        print(f"Caught exception: {e}")

print(f"Downloading {len(human_proteins)} human proteins to ../data/structures/human/{args.batch_num}")

no_struct_human=[]

for prot in human_proteins:
    structure = Structure()
    try:
        structure.download(
            id=prot,           # PDB or UniProt ID
            source="AFDB",        # "PDB" or "AFDB" 
            destination=f"../data/structures/human/{args.batch_num}", # Output directory
            load_after_download=False
        )
    except Exception as e:
        print(f"Caught exception: {e}")
        no_struct_human.append(prot)


print(f"Didn't find an associated structure for {len(no_struct_human)}: {no_struct_human}")

# Run foldseek: Use bacterial protein as query and human proteins as the target

foldseek_results_df=pd.DataFrame(columns=["protein_id","defense_system_protein_id","fident","alnlen","mismatch","gapopen","qstart","qend","tstart","tend","evalue_foldseek","bits"])

for bp in bacterial_proteins:
    print(bp)
    hp=no_na[no_na["defense_system_protein_id"]== bp]["protein_id"].tolist()
    # Constructing query string
    cmd=["/hpf/largeprojects/ccmbio/ajain/tools/foldseek/bin/foldseek","easy-search"]
    for i in hp:
        if i in no_struct_human:
            print(f"Skipping {i} as there is no structure available. Associated Bacterial Protein: {bp}")
            continue
        else:
            cmd.append(f"../data/structures/human/{args.batch_num}/{i}.pdb")
    cmd.append(f"../data/structures/bacterial/{args.batch_num}/{bp}.pdb")
    cmd.append(f"../results/acc_{args.batch_num}/foldseek/{bp}.tsv")
    cmd.append(f"temp/acc_{args.batch_num}")
    run_cmd=subprocess.run(cmd,capture_output=True, text=True)
    results=pd.read_csv(f"../results/acc_{args.batch_num}/foldseek/{bp}.tsv",sep="\t",names=["protein_id","defense_system_protein_id","fident","alnlen","mismatch","gapopen","qstart","qend","tstart","tend","evalue_foldseek","bits"])
    foldseek_results_df=pd.concat([foldseek_results_df,results])

today=date.today()

no_annots_df.merge(foldseek_results_df,on=["defense_system_protein_id","protein_id"],how="left").to_csv(f"../results/acc_{args.batch_num}/{today}_{args.batch_num}.no_annot.combined.foldseek.csv",index=False)

print("Done")

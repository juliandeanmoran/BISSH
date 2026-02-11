import pandas as pd
import argparse
from datetime import date

def add_domain_annotations(species, results_df):
    
    if species=="Human":
        start_col="qstart"
        end_col="qend"
        annot_df=pd.read_csv("../data/uniprotkb_human_annotations/uniprotkb_9606_domain_info_2025_07_22-cleaned.tsv.gz",sep="\t",compression='gzip')
        annot_df_indexed=annot_df.set_index("Entry")
        protein_acc_col="protein_id"
        type_name="Query"
        
    elif species=="Bacterial":
        start_col="tstart"
        end_col="tend"
        annot_df=pd.read_csv("../data/uniprotkb_bacterial_annotations/uniprotkb_bacterial_domain_info_2025_07_11-cleaned.tsv.gz",sep="\t",compression='gzip')
        annot_df_indexed=annot_df.set_index("Entry")
        protein_acc_col="defense_system_protein_id"
        type_name="Target"

    human_protein_id_list=[]
    bacterial_protein_id_list=[]
    #qt_length_list=[] # query or target length list
    qt_match_list=[] # query or target match list ['x..y']
    domain_match_list=[] # Matched domain list
    perc_of_domain_covered_list=[] #Percentage of the domain that is covered by the query/target
    perc_of_qt_covered_list=[] # Percentage of the query/target that is covered by the domain
    qt_wrt_total_prot_len_list=[] # Query/target wrt total human/bacterial protein length
    note_list=[]
    evidence_list=[]

    for row in results_df.itertuples(index=False):
        start = getattr(row, start_col) 
        end = getattr(row, end_col) 
        
        if pd.isna(start) or pd.isna(end):
            continue  # skip, no match

        try:
            domain_df_subset = annot_df_indexed.loc[[getattr(row, protein_acc_col)]]
        except KeyError:
            continue  # no domains for this protein ID

        for domain_row in domain_df_subset.itertuples(index=False):
            match_start = max(start, domain_row.domain_start)
            match_end = min(end, domain_row.domain_end)

            if match_start >= match_end:
                continue  # no overlap
                
            qt_length = getattr(row, f"{type_name}_length") 
            #qt_length = end - start + 1 # Query or target length
            per_of_domain_covered = ((match_end - match_start + 1) / domain_row.domain_length) * 100
            perc_of_qt_covered = ((match_end - match_start + 1) / qt_length) * 100
            qt_wrt_total_prot_len = ((qt_length)/ domain_row.Length)*100
                        
            # Append to list
            human_protein_id_list.append(row.protein_id)
            bacterial_protein_id_list.append(row.defense_system_protein_id)
            
            qt_match_list.append(f"{start}..{end}")
            domain_match_list.append(domain_row.DOMAIN)
            #qt_length_list.append(qt_length)
            
            # Metrics
            perc_of_domain_covered_list.append(f"{per_of_domain_covered:.2f}")
            perc_of_qt_covered_list.append(f"{perc_of_qt_covered:.2f}")
            qt_wrt_total_prot_len_list.append(f"{qt_wrt_total_prot_len:.2f}")
            note_list.append([domain_row.NOTE])
            evidence_list.append([domain_row.EVIDENCE])
            
    
    domain_annots=pd.DataFrame()
    domain_annots["defense_system_protein_id"]=bacterial_protein_id_list
    domain_annots["protein_id"]=human_protein_id_list
    domain_annots[f"{type_name}_range"]=qt_match_list
    #domain_annots[f"{type_name}_length"]=qt_length_list

    domain_annots[f"{species}_prot_domain_match"]=domain_match_list
    domain_annots[f"{species}_domain_percentage"]=perc_of_domain_covered_list
    domain_annots[f"{type_name}_percentage"]=perc_of_qt_covered_list
    domain_annots[f"{type_name}_overlap_w_{species}_protein"]=qt_wrt_total_prot_len_list
    domain_annots[f"{species}_domain_note"]=note_list
    domain_annots[f"{species}_domain_evidence"]=evidence_list
            
    return(domain_annots)

# Read arguments
parser = argparse.ArgumentParser(description="Add annotations to a file.")
parser.add_argument("input_file", help="Path to input file")
parser.add_argument("batch_num", help="Number of the batch, eg: batch_1")
args = parser.parse_args()

results=pd.read_csv(f"../{args.input_file}")
today=date.today()
output_file=f"../results/acc_{args.batch_num}/{today}_{args.batch_num}_annotated.xlsx"
print(f"Input file: {args.input_file}")
print(f"Expected output file: {output_file}\n")

# Add defense finder info
defense_finder_info=pd.read_excel("../data/defense_finder/refseq2uniprot_script/2025-06-24_RefSeq2Uniprot_mapping.xlsx",sheet_name="uniprot_matches")
result_w_df=defense_finder_info.merge(results,left_on="UniProtKB-AC",right_on="defense_system_protein_id",how="right")
result_w_df.drop(columns=['RefSeq'], inplace=True)

print("Successfully added Defense finder annotations")

## Add other UniProt annotations
uniprot_annot=pd.read_csv("../data/uniprotkb_human_annotations/uniprotkb_9606_2025_07_22.tsv.gz",sep="\t")
result_w_df_uniprot_annot=result_w_df.merge(uniprot_annot,left_on="protein_id",right_on="Entry",how="left")

result_w_df_uniprot_annot.drop(columns=['UniProtKB-AC', 'Entry'], inplace=True)

print("Successfully added UniProt annotations")

## Add domain annotation for humans

result_w_df_uniprot_annot["Query_range"]=(
    result_w_df_uniprot_annot["qstart"].astype(str) + 
    ".." + 
    result_w_df_uniprot_annot["qend"].astype(str)
)

result_w_df_uniprot_annot['Query_length']=result_w_df_uniprot_annot.apply(lambda row: row['qend']-row['qstart']+1, axis=1)

# Get the human protein lengths from a different file - should figure out another way but for now it shall suffice
human_prot_length_data=pd.read_csv("../data/uniprotkb_human_annotations/uniprotkb_9606_domain_info_2025_07_22.tsv.gz",sep="\t",compression='gzip')

result_w_df_uniprot_annot=result_w_df_uniprot_annot.merge(human_prot_length_data[["Entry","Length"]],left_on="protein_id",right_on="Entry",how="left").drop(columns=["Entry"]).rename(columns={"Length": "Human_prot_total_length"})

human_domain_annots=add_domain_annotations("Human", result_w_df_uniprot_annot)

result_w_df_uniprot_human_domain_annot=result_w_df_uniprot_annot.merge(human_domain_annots,on=["defense_system_protein_id","protein_id","Query_range"],how="left")

result_w_df_uniprot_human_domain_annot.to_excel(f"../results/acc_{args.batch_num}/{today}_{args.batch_num}_human_domain_annotated.xlsx",index=False)

print("Successfully added human domain annotations")

## Add domain annotation for defense systems

result_w_df_uniprot_human_domain_annot["Target_range"]=(
    result_w_df_uniprot_human_domain_annot["tstart"].astype(str) + 
    ".." + 
    result_w_df_uniprot_human_domain_annot["tend"].astype(str)
)

result_w_df_uniprot_human_domain_annot['Target_length']=result_w_df_uniprot_human_domain_annot.apply(lambda row: row['tend']-row['tstart']+1, axis=1)

# Get the bacterial protein lengths from a different file - should figure out another way but for now it shall suffice
bact_prot_length_data=pd.read_csv("../data/uniprotkb_bacterial_annotations/uniprotkb_bacterial_domain_info_2025_07_11-length.tsv",sep="\t")

result_w_df_uniprot_human_domain_annot=result_w_df_uniprot_human_domain_annot.merge(bact_prot_length_data,left_on="defense_system_protein_id",right_on="Entry",how="left").drop(columns=["Entry"]).rename(columns={"Length": "Bacterial_prot_total_length"})

bacterial_domain_annots=add_domain_annotations("Bacterial", result_w_df_uniprot_human_domain_annot)

print("Successfully added bacterial domain annotations")

result_w_df_uniprot_domain_annot=result_w_df_uniprot_human_domain_annot.merge(bacterial_domain_annots,on=["defense_system_protein_id","protein_id","Target_range"],how="left")

result_w_df_uniprot_domain_annot['Bacterial_Human_Len_Ratio'] =result_w_df_uniprot_domain_annot.apply(lambda row: row['Bacterial_prot_total_length']/row['Human_prot_total_length'], axis=1)

result_w_df_uniprot_domain_annot['Query_Target_Overlap_Length'] =result_w_df_uniprot_domain_annot.apply(lambda row: min(row['Target_length'],row['Query_length']), axis=1)

result_w_df_uniprot_domain_annot['Overlap_ratio'] =result_w_df_uniprot_domain_annot.apply(lambda row: row['Query_Target_Overlap_Length']/(min(row['Bacterial_prot_total_length'],row['Human_prot_total_length'])) , axis=1)


print(f"Writing output file to {output_file}")

result_w_df_uniprot_domain_annot.to_excel(output_file,index=False)

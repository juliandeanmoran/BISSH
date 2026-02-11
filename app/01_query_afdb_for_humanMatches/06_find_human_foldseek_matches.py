import argparse
import pandas as pd

####################################
### Parse command-line arguments ###
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("protein_id", type=str)
parser.add_argument("cluster_identity_filename", type=str)
parser.add_argument("cluster_similarity_filename", type=str)
parser.add_argument("output_file",type=str)
args = parser.parse_args()
#####################################

defense_system_protein_id=args.protein_id

# Find the defense system cluster id corresponding to the defense system protein id
cluster_identity_file = open(args.cluster_identity_filename)
defense_system_cluster_id = ""
for line in cluster_identity_file:
	cluster_id, protein_id = line.rstrip("\n").split("\t")[:2]
	if protein_id == defense_system_protein_id:
		defense_system_cluster_id = cluster_id
cluster_identity_file.close()

# Find all similar clusters to the defense_system_cluster_id

cluster_similarity_file = open(args.cluster_similarity_filename)
similar_clusters = {} # Key = cluster id, Value = evalue
for line in cluster_similarity_file:
	cluster_id1, cluster_id2, evalue = line.rstrip("\n").split("\t")
	if cluster_id1 == defense_system_cluster_id:
		similar_clusters[cluster_id2] = evalue
	elif cluster_id2 == defense_system_cluster_id:
		similar_clusters[cluster_id1] = evalue
cluster_similarity_file.close()

# Now look for proteins in each similar cluster that are in human
defense_system_protein_id_list=[]
defense_system_cluster_id_list=[]
cluster_id_list=[]
protein_id_list=[]
evalue_list=[]
cluFlag_list=[]

cluster_identity_file = open(args.cluster_identity_filename)
for line in cluster_identity_file:
	cluster_id, protein_id, cluFlag, taxID = line.rstrip("\n").split("\t")
	if cluster_id in similar_clusters and taxID == "9606":
		defense_system_protein_id_list.append(defense_system_protein_id)
		defense_system_cluster_id_list.append(defense_system_cluster_id)
		cluster_id_list.append(cluster_id)
		protein_id_list.append(protein_id)
		evalue_list.append(similar_clusters[cluster_id])
		cluFlag_list.append(cluFlag)

result=pd.DataFrame()
result["defense_system_protein_id"]=defense_system_protein_id_list
result["defense_system_cluster_id"]=defense_system_cluster_id_list
result["cluster_id"]=cluster_id_list
result["protein_id"]=protein_id_list
result["evalue"]=evalue_list
result["cluFlag"]=cluFlag_list

if (result.empty):
    result.loc[0,"defense_system_protein_id"]=defense_system_protein_id
    result.loc[0,"defense_system_cluster_id"]=defense_system_cluster_id
    result['protein_id'] = result['protein_id'].astype('object')

result.to_csv(args.output_file,index=False)
#result.to_csv(f"results/{defense_system_protein_id}.no_annot.csv",index=False)

## Add defense finder info
#defense_finder_info=pd.read_excel("data/defense_finder/refseq2uniprot_script/2025-06-24_RefSeq2Uniprot_mapping.xlsx",sheet_name="uniprot_matches")
#result_w_df=defense_finder_info.merge(result,left_on="UniProtKB-AC",right_on="defense_system_protein_id",how="right")

## Add annotation
#sprot_annot=pd.read_excel("data/swiss_prot/2025-06-27_UP000005640_9606_additional-subset.xlsx")
#result_w_df_sprot_annot=result_w_df.merge(sprot_annot,left_on="protein_id",right_on="Accession",how="left")

#result_w_df_sprot_annot.drop(columns=['RefSeq', 'UniProtKB-AC', 'Accession'], inplace=True)

#result_w_df_sprot_annot.to_excel(args.output_file,index=False)

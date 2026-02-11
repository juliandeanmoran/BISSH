#!/usr/bin/env bash

#for accession in $(cat data/01_first_100_acc.txt); do
#for accession in $(cat data/02_additional_accs.txt); do

for batch in data/accession_batches/*.txt
do 
    batch_number=$(basename $batch .txt)
    echo $batch_number
    
    output_dir="results/$batch_number"
    mkdir -p $output_dir
    
    for accession in $(cat $batch)
    do
        scripts/05_generate_slurm_file.py -m 16G --base-dir /hpf/projects/ddissanayake/GRIID/Chantel_foldseek/foldseek_AJ/ "scripts/06_find_human_foldseek_matches.py $accession data/afdb_cluster/5-allmembers-repId-entryId-cluFlag-taxId.tsv data/afdb_cluster/6-all-vs-all-similarity-queryId_targetId_eValue-Dec3_2024_updated.tsv $output_dir/$accession.no_annot.csv" uniprot_matches/$batch_number $accession
        
    done
        
done

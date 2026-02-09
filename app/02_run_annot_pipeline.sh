#!/usr/bin/env bash

TOTAL_BATCHES=177
today=($(date +"%Y-%m-%d"))

for ((batch_num=1; batch_num<=TOTAL_BATCHES; batch_num++))
do
   input_file="results/acc_batch_${batch_num}/*_batch_${batch_num}.no_annot.combined.foldseek.csv"
   echo $input_file
   # Submit python script to add domain annotations
   sbatch scripts/08_submit_add_annotations.sh ${input_file} batch_${batch_num}
 
done



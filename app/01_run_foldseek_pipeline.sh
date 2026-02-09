#!/usr/bin/env bash

TOTAL_BATCHES=177
today=($(date +"%Y-%m-%d"))

for ((batch_num=1; batch_num<=TOTAL_BATCHES; batch_num++))
do
   echo $batch_num
   # Create a combined CSV file for each batch
   head -n 1 "$(ls results/acc_batch_${batch_num}/*.csv | head -n 1)" > results/acc_batch_${batch_num}/${today}_batch_${batch_num}.no_annot.combined.csv
   tail -n +2 -q results/acc_batch_${batch_num}/*.csv >> results/acc_batch_${batch_num}/${today}_batch_${batch_num}.no_annot.combined.csv

   # Submit python script to run foldseek
   mkdir results/acc_batch_${batch_num}/foldseek
   #mkdir data/structures/bacterial/batch_${batch_num}
   #mkdir data/structures/human/batch_${batch_num}
   mkdir -p scripts/temp/acc_batch_${batch_num}

   # Run foldseek   
   sbatch scripts/07_submit_run_foldseek.sh results/acc_batch_${batch_num}/${today}_batch_${batch_num}.no_annot.combined.csv batch_${batch_num}
 
done



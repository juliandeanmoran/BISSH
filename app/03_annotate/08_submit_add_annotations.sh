#!/bin/bash
#SBATCH --job-name=add_uniprot_annots
#SBATCH --time=72:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --mem=100G
#SBATCH --output=logs/%x-%j.out

module load python
cd /hpf/projects/ddissanayake/GRIID/Chantel_foldseek/foldseek_AJ/scripts

input_file=$1
batch_num=$2

#python3 -u 08_add_annotations.py ../results/annotate_results/2025-07-14_results_batch2_no_annots_foldseek.csv
#python3 -u 08_add_annotations.py $input_file $batch_num
python3 -u 08_add_annotations-optimized-new_metrics.py $input_file $batch_num

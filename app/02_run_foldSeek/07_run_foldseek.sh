#!/bin/bash
#SBATCH --job-name=run_foldseek
#SBATCH --time=10:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --mem=60G
#SBATCH --output=logs/%x-%j.out

cd /hpf/projects/ddissanayake/GRIID/Chantel_foldseek/foldseek_AJ/scripts

source ~/.bashrc
conda_local

input_file=$1
batch_num=$2

mamba activate /hpf/largeprojects/ccmbio/ajain/tools/conda_envs/ccm_benchmate
python3 -u 07_run_foldseek.py $input_file $batch_num

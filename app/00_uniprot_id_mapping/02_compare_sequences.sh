#!/bin/bash
#SBATCH --job-name=submit_compare_sequences
#SBATCH --time=100:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --mem=60G
#SBATCH --output=logs/%x-%j.out

module load python

python3 -u 02_compare_sequences.py

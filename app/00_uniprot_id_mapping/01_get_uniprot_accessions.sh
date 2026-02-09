#!/bin/bash
#SBATCH --job-name=submit_python_script
#SBATCH --time=100:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --mem=60G
#SBATCH --output=logs/%x-%j.out

module load python

python3 -u 01_get_uniprot_accessions.py

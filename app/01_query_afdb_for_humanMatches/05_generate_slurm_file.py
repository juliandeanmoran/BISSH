#!/usr/bin/env python3

# Author: Brett Trost
# Modified by: Anjali Jain

import argparse
import os

description='''

Makes a slurm file with the specified resources and command.

Input: A string containing a command to be run via slurm, and optionally slurm resource requests (memory, number of nodes, number of cpus, etc.)

Output: a shell script that will execute the given command, and request the indicated resources.
'''

parser = argparse.ArgumentParser(description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-w", "--walltime", type=str, help="amount of time process will run", default="3:00:00")
parser.add_argument("-n", "--nodes", type=int, help="number of nodes", default=1)
parser.add_argument("-p", "--ppn", type=int, help="processors per node", default=1)
parser.add_argument("-m", "--mem", type=str, help="memory", default="16G")
parser.add_argument("-t", "--tmp", type=str, help="local disk space", default="100G")
parser.add_argument("-f", "--flags", type=str, default="")
parser.add_argument("--partition", type=str)
parser.add_argument("--reservation", type=str)
parser.add_argument("--constraint", type=str)
parser.add_argument("--qos", type=str)
parser.add_argument("--base-dir", type=str, nargs="?", default=os.getcwd())
parser.add_argument("cmd", type=str, help="the command you want to run")
parser.add_argument("slurm_dir_name", type=str, help="name of the slurm subdirectory")
parser.add_argument("slurm_job_name", type=str, help="name of the job")
args = parser.parse_args()


sbatch_options = []

if args.partition:
	sbatch_options.append("--partition={}".format(args.partition))

if args.reservation:
	sbatch_options.append("--reservation={}".format(args.reservation))
	
if args.constraint:
	sbatch_options.append("--constraint={}".format(args.constraint))
		
if args.qos:
	sbatch_options.append("--qos={}".format(args.qos))
	
if "G" not in args.mem and "M" not in args.mem and "T" not in args.mem:
	print("generate_slurm_file.py: Argument for --mem ({}) did not include a unit".format(args.mem))
	quit()
	

os.makedirs("scripts/pipeline_runs", exist_ok=True)
os.makedirs("scripts/pipeline_runs/{}".format(args.slurm_dir_name), exist_ok=True)

output_file = "scripts/pipeline_runs/{}/{}.out".format(args.slurm_dir_name, args.slurm_job_name)
log_file = "scripts/pipeline_runs/{}/{}.log".format(args.slurm_dir_name, args.slurm_job_name)
slurm_file = open("scripts/pipeline_runs/{}/{}.slurm".format(args.slurm_dir_name, args.slurm_job_name), "w")

if sbatch_options:
	sbatch_options_str = " ".join(sbatch_options) + " "
else:
	sbatch_options_str = ""

slurm_file.write('''
#!/bin/bash
#SBATCH {sbatch_options_str}--cpus-per-task={args.ppn} --mem={args.mem} --time={args.walltime} --tmp={args.tmp} --output={output_file} --chdir={args.base_dir} {args.flags}

#######################################################################
################### JOB SPECIFIC COMMANDS #############################
#######################################################################
cd {args.base_dir}

module load python
echo "Job start: $(date)" >> {log_file}
sdate=$(date '+%s')

CMD="python3 {args.cmd}"
eval $CMD

echo "Job end: $(date)" >> {log_file}
edate=$(date '+%s')
minutes=$(( (edate - sdate) / 60 ))
echo "Elapsed time: $minutes minutes" >> {log_file}

#######################################################################
################### END JOB SPECIFIC COMMANDS #########################
#######################################################################

if [ ! -s {output_file} ]; then rm {output_file}; fi

'''[1:-1].format(**vars()))
slurm_file.close()

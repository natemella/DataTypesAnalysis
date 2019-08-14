import sys

bash_args = {
    "numCommands": sys.argv[1],
}
out = """#!/bin/bash
#SBATCH -N 1 -n 2 --mem=64G -C rhel7
#SBATCH --array=0-{numCommands}
#SBATCH --mail-user=nathanmell@gmail.com   # email address
#SBATCH --mail-type=END
#SBATCH --time=36:00:00   # walltime

module load jdk/1.8

dockerCommandsFile=$1
    while read line; do
        $line &
    done < <(sed -n $(($SLURM_ARRAY_TASK_ID * 1 + 1)),$((($SLURM_ARRAY_TASK_ID + 1) * 1))p $dockerCommandsFile)
wait
""".format(**bash_args)
with open ("job_array.sh", 'w') as output:
    output.write(out)
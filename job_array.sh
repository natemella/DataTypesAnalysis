#!/bin/bash
#SBATCH -N 1 -n 1 --mem=16G -C rhel7
#SBATCH --array=0-490
#SBATCH --mail-user=nathanmell@gmail.com   # email address
#SBATCH --mail-type=END
#SBATCH --time=18:00:00   # walltime

dockerCommandsFile=$1
    while read line; do
        $line &
    done < <(sed -n $(($SLURM_ARRAY_TASK_ID * $SLURM_NTASKS + 1)),$((($SLURM_ARRAY_TASK_ID + 1) * $SLURM_NTASKS))p $dockerCommandsFile)
wait
echo DONE
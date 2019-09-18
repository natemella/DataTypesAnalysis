import sys
import os

if int(sys.argv[1]) > 1000:
    numCommands = "1000"
    remainder = (int(sys.argv[1]) - 1000)
else:
    numCommands = sys.argv[1]
    remainder = 0
bash_args = {
    "numCommands": numCommands,
}

out = """#!/bin/bash
#SBATCH -N 2 -n 1 --mem=120G -C rhel7
#SBATCH --array=0-{numCommands}
#SBATCH --mail-user=nathanmell@gmail.com   # email address
#SBATCH --mail-type=END
#SBATCH --time=80:00:00   # walltime

module load jdk/1.8

dockerCommandsFile=$1
    while read line; do
        $line &
    done < <(sed -n $(($SLURM_ARRAY_TASK_ID * 1 + 1)),$((($SLURM_ARRAY_TASK_ID + 1) * 1))p $dockerCommandsFile)
wait
""".format(**bash_args)
with open ("job_array.sh", 'w') as output:
    output.write(out)

# remove all additionaly job_arrays to avoid extras
j = 2
while os.path.isfile(f"job_array{j}.sh"):
    os.remove(f"job_array{j}.sh")
    j += 1

# exit before entering while loop
if remainder == 0:
    sys.exit(0)

thousands = "1000"
bash_args["thousands"] = thousands
i = 2
while True:
    if int(remainder) > 1000:
        numCommands = 1000
    else:
        numCommands = remainder

    bash_args["numCommands"] = numCommands
    out2 = ("#!/bin/bash\n"
            "#SBATCH -N 2 -n 1 --mem=120G -C rhel7\n"
            "#SBATCH --array=0-{numCommands}\n"
            "#SBATCH --mail-user=nathanmell@gmail.com   # email address\n"
            "#SBATCH --mail-type=END\n"
            "#SBATCH --time=80:00:00   # walltime\n"
            "\n"
            "module load jdk/1.8\n"
            "\n"
            "dockerCommandsFile=$1\n"
            "    while read line; do\n"
            "        $line &\n"
            "    done < <(sed -n $(($SLURM_ARRAY_TASK_ID * 1 + {thousands})),$((($SLURM_ARRAY_TASK_ID + {thousands}) * 1))p $dockerCommandsFile)\n"
            "wait\n"
            "    ").format(**bash_args)

    remainder = remainder - 1000
    with open (f"job_array{i}.sh", 'w') as output:
        output.write(out2)
    i +=1
    thousands = str(int(thousands) + 1000)
    bash_args["thousands"] = thousands
    if remainder < 0:
        break

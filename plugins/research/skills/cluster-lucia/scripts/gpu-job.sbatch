#!/bin/bash
# One full GPU node of Lucia (4 A100 40 GB), as in the Lucia docs, adapted to PyTorch DDP.
# Not tested on Lucia yet (the docs give no PyTorch or DDP example) [verify].
# Copy it next to the training script, then adapt the job name, the account, the time and the command.
#SBATCH --job-name=neptune-train
#SBATCH --account=bsmfc
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --gpus=4
#SBATCH --cpus-per-task=8              # at most 8 CPUs per GPU
#SBATCH --mem=240G                     # at most 60 GB per GPU
#SBATCH --time=48:00:00
#SBATCH --output=%j_%x.out

export MASTER_ADDR=$(scontrol show hostnames "$SLURM_JOB_NODELIST" | head -n 1)
export MASTER_PORT=$(expr 10000 + $(echo -n $SLURM_JOBID | tail -c 4))
export WORLD_SIZE=$SLURM_NTASKS

srun bash -c "RANK=\$SLURM_PROCID LOCAL_RANK=\$SLURM_LOCALID python train.py"

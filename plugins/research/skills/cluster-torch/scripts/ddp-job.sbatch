#!/bin/bash
# Multi-node DDP training on Torch: template from the `cluster-torch` skill (§ 9).
# Two full H200 nodes of Courant = the 16 GPUs allowed per user (`lzanna`, capped at 8 GPUs, cannot run it).
# More than 8 GPUs at once, or the preemption comment below: ask Victor first.
#
# Rules from the docs:
# - tasks = GPUs: --ntasks-per-node = --gres=gpu:N (not --ntasks);
# - fill whole nodes before going multi-node, never 1 GPU per node;
# - NCCL backend, local_rank = SLURM_PROCID % SLURM_GPUS_ON_NODE;
# - gradient_as_bucket_view=True saves ~1/3 of the memory;
# - optimize single-GPU first (dataloader workers = SLURM_CPUS_PER_TASK);
# - job arrays share SLURM_JOBID => add $SLURM_ARRAY_TASK_ID to MASTER_PORT.
#
#SBATCH --job-name=heimdall-ddp
#SBATCH --account=torch_pr_347_courant
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:8
#SBATCH --constraint=h200
#SBATCH --cpus-per-task=16                        # 128 cores / 8 GPUs
#SBATCH --mem=2000G                               # --mem=0 is refused on Torch
#SBATCH --time=48:00:00
#SBATCH --comment="preemption=yes;requeue=true"   # optional, needs auto-resume
#SBATCH --output=cluster/logs/%x-%j.out

export MASTER_ADDR=$(scontrol show hostnames "$SLURM_JOB_NODELIST" | head -n 1)
export MASTER_PORT=$(expr 10000 + $(echo -n $SLURM_JOBID | tail -c 4))   # job arrays share SLURM_JOBID: add $SLURM_ARRAY_TASK_ID
export WORLD_SIZE=$SLURM_NTASKS
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

srun apptainer exec --nv \
    --overlay $SCRATCH/env/heimdall.ext3:ro \
    --overlay $SCRATCH/data/dataset.sqf:ro \
    /share/apps/images/cuda13.0.1-cudnn9.13.0-ubuntu-24.04.3.sif \
    bash -c "source /ext3/env.sh; RANK=\$SLURM_PROCID LOCAL_RANK=\$SLURM_LOCALID python train.py"

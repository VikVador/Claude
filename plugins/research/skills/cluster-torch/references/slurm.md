# SLURM DETAILS

Part of the `cluster-torch` skill (§ 4): read it before a preemptible job or a B200 test, for the CPU QoS, or to look up a
Slurm command or a pending reason. The rules of § 4 still hold, and a preemptible job needs my approval first.

## CPU QoS

`show_slurm_qos` (the GPU QoS are in § 4):

| QoS           | Wall time | Max per user          | Used when       |
| ------------- | --------- | --------------------- | --------------- |
| `cpu48`       | 2 d       | 3000 CPUs, 6000 GB    | CPU jobs ≤ 48 h |
| `cpu168`      | 7 d       | 1000 CPUs, 2000 GB    | CPU jobs > 48 h |
| `interactive` | 6 h       | 16 CPUs, 60 GB        | –               |
| `cpu_short`   | 6 h       | 32 CPUs, 120 GB       | –               |
| `cpuprem`     | 2 d       | 30000 CPUs (preempt.) | –               |

## Pending reasons

| Reason                                                              | Meaning                                                      |
| ------------------------------------------------------------------- | ------------------------------------------------------------ |
| `QOSGrpGRES`                                                        | no free GPU in the partition (e.g. the 8 lab RTX all in use) |
| `QOSMaxGRESPerUser`, `QOSMaxMemoryPerUser`, `QOSMaxCpuPerUserLimit` | your personal limit                                          |

## Preemption

| Partitions                                                                 | Preempted?                       |
| -------------------------------------------------------------------------- | -------------------------------- |
| `*_lzanna`, `*_courant`, `*_public`, `cs`, `cpu_short` (`PreemptMode=OFF`) | **never**                        |
| `h200`, `l40s`, `rtx6000`, `b200_courant_prem`, … (with `preemption=yes`)  | yes, after 30 min, then requeued |

| `#SBATCH --comment=...`                                        | Effect                                                |
| -------------------------------------------------------------- | ----------------------------------------------------- |
| `"preemption=yes;requeue=true"`                                | normal + preemptible partitions (idle GPUs of others) |
| `"preemption=yes;preemption_partitions_only=yes;requeue=true"` | preemptible only (may allow more resources)           |
| `gpu_mps=yes`                                                  | several jobs share a GPU                              |
| `ram_disk=1GB`                                                 | RAM-backed directory `$SLURM_RAM_TMPDIR`              |

- Priority: stakeholder > public > preemptible partitions; GPU jobs preempt CPU jobs on GPU nodes.
- Requeued jobs restart from scratch ⇒ the training script must resume from its last checkpoint by itself.
- **B200 (191 GB)** are only reachable this way, e.g. `--account=torch_pr_347_courant --constraint=b200` →
  `b200_courant_prem` (12 nodes × 8 B200, open to every account): handy for short memory tests.

## Useful commands

| Need                                | Command                                                                        |
| ----------------------------------- | ------------------------------------------------------------------------------ |
| Start estimate, without submitting  | `sbatch --test-only job.sbatch` (also with other `--constraint`, `--gres`)     |
| GPU use of a running job            | `srun --jobid=<id> --overlap -n1 nvidia-smi` (array task: id from `squeue %A`) |
| Override the resources of an sbatch | `sbatch --array=5 --ntasks-per-node=2 --gres=gpu:2 --mem=128G job.sbatch`      |
| A whole H200 node                   | `--gres=gpu:8 --ntasks-per-node=8 --cpus-per-task=16 --mem=2000G`              |
| Short memory test on a big GPU      | `--constraint=b200 --comment="preemption=yes;preemption_partitions_only=yes"`  |
| Accounts, quotas, QoS               | `my_slurm_accounts`, `myquota`, `rpsquota`, `show_slurm_qos`                   |
| Efficiency of a finished job        | `seff <jobid>`                                                                 |
| GPU monitoring                      | `nvidia-smi -l 5`, `/share/apps/images/run-nvtop-3.2.0.bash nvtop`             |

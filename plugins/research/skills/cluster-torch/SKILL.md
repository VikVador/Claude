---
name: cluster-torch
description: "Use as soon as you work on Torch (not PyTorch), the HPC cluster of New York University (hostname torch-*, or a compute node gh*, gr*, gl*), before any Slurm job, choice of account or GPU, storage or quota operation, data transfer or Apptainer environment. Also for the Open Storage Network (S3-compatible object storage, pod nyu1.osn.mghpcc.org): endpoint, public and private buckets, reading and writing. Not for Lucia."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       NYU Torch cluster: access, GPUs, Slurm rules,
     ┌─┴───┴─┐       storage, OSN pod and software environment.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# CLUSTER TORCH (NYU)

How Torch works and what not to do there, so that jobs run and nothing gets lost.
**[verify]** = not in the docs or ambiguous: check before relying on it.

**Last checked: 2026-10-27** (NYU RTS docs; the cluster on 2026-10-14; the Heimdall datasets and encoder trainings,
2026-10-22 to 2026-10-27).

> **Keep this file up to date.** If the date above is **more than one month old**, before relying on this file:
> 1. launch an agent to re-read the [NYU RTS docs](https://services.rt.nyu.edu/docs/hpc/getting_started/intro/)
>    ([source](https://github.com/NYU-RTS/rts-docs)), and check your memory for what was learned on Torch since;
> 2. propose the changes to me; once I agree, make them in a clone of VikVador/Claude, on a branch, through a pull
>    request, with the new date. Never in `~/.claude/plugins/`: that copy is overwritten at the next update.

| File                               | Use      | When                                     |
| ---------------------------------- | -------- | ---------------------------------------- |
| `references/slurm.md`              | **Read** | preemption, CPU QoS, commands            |
| `references/osn.md`                | **Read** | when working with the OSN pod            |
| `references/environment.md`        | **Read** | when building or changing an environment |
| `references/access-and-billing.md` | **Read** | only when asked (SSH, RPS, …)            |
| `scripts/ddp-job.sbatch`           | **Copy** | a multi-GPU or multi-node training (§ 9) |

Related: the `cluster-lucia` skill for the other cluster (same section numbers).

**Contents**: 0. In short · 1. Access · 2. Hardware · 3. Our resources · 4. Slurm · 5. Allocations · 6. Storage ·
7. Data and transfers · 8. Software environment · 9. Job template · 10. Misc · 11. Open questions

---

## 0. IN SHORT

1. **`--account` is mandatory; `--partition`, `--mem=0` and `--exclude` are refused**: pick the GPU with
   `--constraint` (`h200`, `rtx6000`, …), ask for the memory explicitly, report a bad node to hpc@nyu.edu (§ 4).
2. **16 GPUs per user for jobs ≤ 48 h, 4 GPUs beyond**, counted over all the running jobs (§ 4).
3. **Underused GPUs are cancelled**: below 60 % on H200, 50 % on RTX / L40S / A100 (§ 4).
4. **Ask me first** before using `lzanna` (the 8 RTX GPUs of the whole lab) for long jobs, before more than 8 GPUs at
   once, and before a preemptible job (it needs auto-resume) (§ 4, § 5).
5. **Big trainings go on `courant`** (H200, L40S). It ends on **2026-12-10**: within 30 days of that date, remind me
   at the start of a session (§ 5).
6. **Scratch is purged after 60 days without access**; home has only 30 K files (§ 6).
7. **No transfer on login nodes** (DTN or Globus), no heavy work either (2 GB of memory per user) (§ 7).
8. **Jobs mount the environment overlay read-only** (`:ro`); install packages on a compute node (§ 8).

---

## 1. ACCESS

- **An *HPC account* and an *active allocation***: the NetID gives the login, an allocation on
  https://projects.hpc.nyu.edu gives a Slurm account `torch_pr_XXX_XXXXX`. No allocation → no jobs.
- **VPN mandatory off campus** (login, OOD, project portal, status dashboard). Linux: `sudo openconnect -b vpn.nyu.edu`.
- **No SSH keys**: password + Microsoft device-login 2FA (https://microsoft.com/devicelogin + Duo) ⇒ no
  non-interactive SSH from outside, automation runs *on* Torch.
- VSCode: `code-server` app in Open OnDemand (https://ood.torch.hpc.nyu.edu), or Remote-SSH. Cluster usage:
  https://stats.apps.cloud.rt.nyu.edu (VPN), or `vsinfo` (in `~/bin`).
- Support: hpc@nyu.edu (personal consultations, incl. deep-learning scaling).
- A reconnection can land on another login node (`torch-login-a-0`, `a-1`, `b-1`, `b-3`, …): processes started from
  the previous one keep running there (`ssh torch-login-b-3` from Torch to stop them).

---

## 2. HARDWARE

Infiniband NDR400. 4 login nodes, 2 DTN nodes (100 Gb/s to the research network). RTX nodes: gr101-106.

| Type          | Prefix (`sinfo`) |     Nodes × GPUs | GPU memory | CPUs, RAM / node    |
| ------------- | ---------------- | ---------------: | ---------: | ------------------- |
| H200          | `gh1*`           |     34 × 8 = 272 |     150 GB | 128, 2 TB           |
| L40S          | `gl*`            |     68 × 4 = 272 |          – | 128, 512 GB         |
| B200          | `gb*`            |     15 × 8 = 120 |     191 GB | 128, 3 TB           |
| RTX Pro 6000  | `gr*`            |       6 × 8 = 48 |     102 GB | 128, 1.5 TB         |
| H100          | `gh0*`           |      15 × 4 = 60 |          – | 96, 1.5 TB          |
| A100          | `ga*`            | (9+34) × 4 = 172 |          – | 64 / 80, 0.5 / 1 TB |
| CPU std / big | `cs*` / `cl*`    |    186 / 8 nodes |          – | 128, 512 GB / 3 TB  |

- **RTX Pro 6000** = Blackwell (driver 610, sm_120) ⇒ PyTorch built for **CUDA ≥ 12.8**. No NVLink (PCIe only) ⇒
  intra-node all-reduce slower than on H200 / B200 (general knowledge, not the docs).
- GPU memory: PyTorch `torch.cuda.get_device_properties(0).total_memory` (2026-10-25). H200 node:
  `RealMemory=2061000` MB (`scontrol show node gh110`).

---

## 3. OUR RESOURCES

Project **"Zanna Research"** (Laure Zanna, M²LInES) on https://projects.hpc.nyu.edu (verified 2026-10-14).

| Allocation        | Slurm account          | Reaches (no `--constraint`)                 | Ends                   |
| ----------------- | ---------------------- | ------------------------------------------- | ---------------------- |
| `torch` (Cluster) | `torch_pr_347_general` | CPUs, `l40s_public`, `h200_public`          | 2035-06-01             |
| `lzanna`          | `torch_pr_347_lzanna`  | `rtx6000_lzanna` + public GPUs              | 2027-07-14             |
| `courant`         | `torch_pr_347_courant` | `*_courant` (L40S, H200, RTX) + public GPUs | **2026-12-10** ⚠ renew |

Group caps, shared by **every member** of the group (`sacctmgr show qos`):

| Partition         |  GPUs | CPUs |  Memory | Shared by                      |
| ----------------- | ----: | ---: | ------: | ------------------------------ |
| `rtx6000_lzanna`  | **8** |  128 |  1400 G | the whole lab (= one RTX node) |
| `rtx6000_courant` |     8 |  128 |  1400 G | all of Courant                 |
| `l40s_courant`    |    52 | 1664 |  6500 G | all of Courant                 |
| `h200_courant`    |    88 | 1408 | 22000 G | all of Courant                 |
| `l40s_public`     |   208 | 6656 | 26000 G | everyone                       |
| `h200_public`     |    24 |  384 |  6000 G | everyone                       |

---

## 4. SLURM

| Rule                        | Details                                                                  |
| --------------------------- | ------------------------------------------------------------------------ |
| `--account=<slurm_account>` | mandatory on every `srun` / `sbatch` (§ 5)                               |
| **Never `--partition`**     | QoS views: Slurm uses every matching partition the account reaches       |
| `--constraint=<gpu>`        | `rtx6000`, `l40s`, `h200`, `h100`, `a100`, `b200`, `cuda`                |
| `--mem=0` refused           | "Please do not request memory 0": e.g. `--mem=1400G` per RTX node        |
| `--exclude=<node>` refused  | "Please do note --exclude … report back to hpc@nyu.edu": report the node |

Features: `sinfo -o "%P %f"`. Several GPU types at once: `--constraint='h200|l40s'`.

### Limits per user

`show_slurm_qos`. The QoS follows the wall time whatever the account; the group caps (§ 3) apply on top:

- **`gpu48`**: GPU jobs ≤ 48 h, **16 GPUs** per user. **`gpu168`**: GPU jobs > 48 h (up to 7 d, sbatch notice),
  **4 GPUs** per user. CPU jobs: `cpu48` (≤ 48 h) and `cpu168` (up to 7 d), limits in `references/slurm.md`.
- GPU caps are **per user, over all running jobs** (`MaxTRESPerUser`, no per-job cap): one job of 16 GPUs, or 2 of 8,
  the next ones waiting (`QOSMaxGRESPerUser`). The docs say 24 GPUs, `show_slurm_qos` gives 16 (2026-10-14).
- Queue: at most **500** (`gpu48`) or **50** (`gpu168`) GPU jobs, and **3000** CPU jobs (`cpu48`), **each task of an
  array counting** ⇒ submit big arrays in rolling batches.
- A busy cluster starts array tasks in slow batches (~15 min apart): `JobArrayTaskLimit` with no task running is slow,
  not stuck. Multi-node trainings: jobs ≤ 48 h, chained with checkpoint/restart.

### Cancellation of underused GPUs

Cancelled automatically ("Enforcement will be very aggressive"), after a delay not documented **[verify]**.

| Nodes                                 | Cancelled below | Warned below |
| ------------------------------------- | --------------: | -----------: |
| `gh*` (H200)                          |            60 % |         75 % |
| `gl*`, `ga*`, `gr*` (L40S, A100, RTX) |            50 % |         70 % |
| other                                 |            10 % |         50 % |

⇒ Long CPU-only phases in GPU jobs (data staging, validation on CPU, big evaluations) can get the job killed: keep the
GPU busy, stage the data in a CPU job beforehand, run notebooks on CPUs.

### Preemption and commands

- **Ask me first** before a preemptible job (`--comment="preemption=yes;…"`): it can be preempted after 30 min and
  requeued, and restarts from scratch, so the training script must resume from its last checkpoint by itself.
- Our partitions (`*_lzanna`, `*_courant`, `*_public`, `cs`, `cpu_short`) are never preempted. B200 GPUs are only
  reachable as preemptible. Options, B200 tests, other QoS (`interactive`, `cpu_short`, `cpuprem`),
  pending reasons, commands (`sbatch --test-only`, `seff`, `myquota`, …): `references/slurm.md`.
- A **whole H200 node** can wait **1–2 days** on `h200_courant`; partial requests start a bit sooner but run slower.
- Cancelling a pending job loses its place in the queue.
- Don't `watch squeue` / `sacct` (RPC throttling, `sdiag`); use `--mail-type` and job arrays.

---

## 5. ALLOCATIONS

Which account and constraint (verified with held jobs):

| Need                 | Flags                                                | Lands on                         |
| -------------------- | ---------------------------------------------------- | -------------------------------- |
| Lab RTX only         | `--account=torch_pr_347_lzanna --constraint=rtx6000` | `rtx6000_lzanna`                 |
| Courant H200         | `--account=torch_pr_347_courant --constraint=h200`   | `h200_courant` (+ `h200_public`) |
| Courant L40S         | `--account=torch_pr_347_courant --constraint=l40s`   | `l40s_courant` (+ `l40s_public`) |
| Any GPU we can reach | `--account=torch_pr_347_courant` (no constraint)     | first free partition             |
| CPU only             | `--account=torch_pr_347_general`                     | `cs`, `cpu_short`                |

- **`lzanna` is the whole lab**: its 8 RTX are **all** the lab's GPUs. Keep big trainings on `courant`, and `lzanna`
  for jobs needing the RTX or a guaranteed slot. **Ask me first** before a long job on it.
- **More than 8 GPUs at once**: ask me first (the § 9 template takes 16).
- **CPU-only jobs** land on the CPU partitions whatever the account ⇒ use `general` for them.
- **`courant` ends on 2026-12-10** (the PI renews it): within 30 days of that date, remind me at the start of a
  session.

---

## 6. STORAGE

| Path (variable)               | Quota (space / files) | Backup       | Purge             | Use                 |
| ----------------------------- | --------------------- | ------------ | ----------------- | ------------------- |
| `/home/$USER` (`$HOME`)       | 50 GB / **30 K**      | daily        | no                | code, configs       |
| `/scratch/$USER` (`$SCRATCH`) | 5 TB / 5 M            | **no**       | **unused ≥ 60 d** | jobs, all-flash     |
| `/archive/$USER` (`$ARCHIVE`) | 2 TB / 20 K           | daily        | no                | tar, **login only** |
| RPS (`/projects/…`?)          | paid                  | daily (30 d) | no                | shared lab space    |
| Node-local (`$SLURM_TMPDIR`)  | –                     | no           | end of job        | fast job I/O        |

- Node-local disk is also at `/state/partition1/$USER`.
- Faking access times (`touch` scripts) to dodge the purge = **account locked**.
- **Home inode trap**: no conda environments in `$HOME`; symlink `.vscode-server`, `.cursor-server` and conda `pkgs`
  to the scratch.
- RPS: paid, requested by the PI; ours is an open question (§ 11). **Never `chmod 777`**: share with NFSv4 ACLs or
  an IPA group. RPS price and sharing commands: `references/access-and-billing.md`.
- High-risk data (PII, PHI, CUI) is forbidden on HPC.

---

## 7. DATA AND TRANSFERS

- **Avoid millions of small files** (inodes, metadata): a few big files (Zarr with large chunks, HDF5, LMDB) or a
  **squashfs image** mounted read-only, shareable by several jobs:
  ```bash
  mksquashfs mydata mydata.sqf -keep-as-directory      # build on node-local disk
  apptainer exec --overlay mydata.sqf:ro …             # data appears at /mydata
  ```
- Fastest reads: stage a subset to `$SLURM_TMPDIR` or a RAM disk at the start of the job (mind the GPU cancellation
  while staging, § 4).
- **Internet on compute nodes works**, despite the docs: `api.wandb.ai`, PyPI, GitHub and `nyu1.osn.mghpcc.org`
  (2026-10-14).
- Public datasets (read-only): `/projects/work/public/ml-datasets/`.
- **Never transfer on login nodes**: the DTN `dtn.torch.hpc.nyu.edu` (rsync, scp, rclone), **Globus** `nyu#torch`
  (large volumes, automatic retries), or the Open OnDemand upload (small files only).
- `rclone`: on the DTN and as a module (`module load rclone/1.72.1`, the only version on 2026-10-22).
- **OSN pod** (S3 storage of M²LInES, `https://nyu1.osn.mghpcc.org`): Heimdall's datasets in the public bucket
  `m2lines-pubs/Datasets`, read anonymously; write only with the private rclone remote `osn-rw` or s3fs profile
  `osn`, keys never in a repository. Details: `references/osn.md`.

---

## 8. SOFTWARE ENVIRONMENT

Apptainer + overlay: the environment is a single file ⇒ no inode problem. Build: `references/environment.md`.

| Heimdall | Value                                                             |
| -------- | ----------------------------------------------------------------- |
| Overlay  | `$SCRATCH/env/heimdall.ext3` (15 GB, 500 K files)                 |
| Image    | `/share/apps/images/cuda13.0.1-cudnn9.13.0-ubuntu-24.04.3.sif`    |
| Env      | conda environment `heimdall` (Miniforge), PyTorch `cu130`         |
| Build    | `sbatch cluster/jobs/environment.sbatch` (creates or updates all) |
| Jupyter  | `sbatch cluster/jobs/jupyter.sbatch`                              |

- Jupyter: `--mem=96G` for a full day of GLORYS; then VSCode *Select Kernel → Existing Jupyter Server*,
  `http://<node>:8888/lab?token=…` (token in `cluster/logs/jupyter.log`).
- **Which image**: for Heimdall, always the Heimdall image above (its overlay goes with it); the generic
  `/share/apps/images/cuda-13.3.1-ubuntu-26.04.sif` only to build a new environment.
- No Docker, Apptainer only. Add `--nv` for GPUs.
- **Installs**: updating `albus` and `shaggy` as the `auto-update` skill says is pre-approved; any other install or
  upgrade in an environment, ask me first.
- **Install packages on a compute node**: login nodes cap memory at **2 GB/user** and run a *different OS*
  (`srun --account=<acct> -c4 --mem=16GB -t2:00:00 --pty bash`).
- **Jobs mount the overlay `:ro`**: a `:rw` mount locks the file (no other job may use it meanwhile).
- `/tmp` is local to each node: a file written there on a login node is invisible to the compute nodes.

---

## 9. JOB TEMPLATE

`scripts/ddp-job.sbatch`: DDP on two full H200 nodes of Courant (16 GPUs), with the DDP rules of the docs in its
header. Over 8 GPUs and preemptible: **ask me first** (§ 5).

Before a job:

- [ ] Account and constraint from § 5, no `--partition`, memory asked explicitly?
- [ ] GPUs busy: above 60 % (H200) / 50 % (others), data staged beforehand, workers = CPUs (§ 4)?
- [ ] Checkpointing: it resumes from its last checkpoint (48 h limit, requeue)?
- [ ] Output and logs in `$SCRATCH` or `cluster/logs/`, not `$HOME`?
- [ ] Quotas: `myquota` (home 30 K files), GPUs per user, queue limits for arrays (§ 4)?
- [ ] Every "ask me first" case (§ 0) cleared?

---

## 10. MISC

- **Compared to Lucia** (A100 40 GB, 4 per node, 48 GPUs per user): Torch has bigger GPUs but a tighter GPU limit per
  user (16 GPUs over 2 days, 4 over 7 days), and it cancels underused GPU jobs.
- Acknowledgement in publications: `references/access-and-billing.md`.

---

## 11. OPEN QUESTIONS

| #   | Question                                        | Status                    |
| --- | ----------------------------------------------- | ------------------------- |
| 1   | RPS volume of the group?                        | **open**                  |
| 2   | Delay before an underused GPU job is cancelled? | **open**, ask hpc@nyu.edu |
| 3   | Renewal of `courant` (ends 2026-12-10)          | **to do**, PI to renew it |

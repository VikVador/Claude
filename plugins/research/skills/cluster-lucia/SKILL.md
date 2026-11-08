---
name: cluster-lucia
description: "Use as soon as you work on Lucia, the CÉCI Tier-1 supercomputer of Cenaero (Wallonia) where Neptune runs (hostname frontal01 or frontal02, compute nodes cna, cni, cns), before any Slurm or dawgz job, choice of account, partition or GPU, BUh credit check, data transfer, storage or scratch operation, or install. Gives the rules so that jobs run and nothing gets lost. Not for Torch (NYU), which has its own skill."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Lucia cluster (Cenaero, Wallonia): access, GPUs,
     ┌─┴───┴─┐       Slurm, billing, storage and software environment.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# CLUSTER LUCIA (CENAERO)

How Lucia works, so that Neptune's jobs run and nothing gets lost. From the [Lucia docs](https://doc.lucia.cenaero.be),
the [CÉCI](https://www.ceci-hpc.be) pages (marked (CÉCI)) and Neptune. [verify] = missing or ambiguous.

**Last checked: 2026-11-01** (29 pages of the docs on 2026-10-27; the cluster on 2026-10-28 from `frontal02`, with
`sinfo`, `sacctmgr`, `scontrol`, `mmlsquota`, `sbatch --test-only`, no job run).

> **Keep this file up to date.** If the date above is more than one month old, before relying on this file:
> 1. launch **an agent with the model `sonnet`** to re-read the [Lucia docs](https://doc.lucia.cenaero.be) and the
>    [CÉCI pages](https://www.ceci-hpc.be/clusters/lucia/), and to list every value that differs from this file;
> 2. check your memory for anything useful learned on Lucia since then;
> 3. propose the changes to me; after my yes, make them in a clone of VikVador/Claude, on a branch, through a pull
>    request, never in `~/.claude/plugins/`.

| File                           | Use      | When                              |
| ------------------------------ | -------- | --------------------------------- |
| `scripts/gpu-job.sbatch`       | **Copy** | a job outside dawgz (§ 9)         |
| `references/access.md`         | **Read** | only when setting up access (§ 1) |
| `references/cpu-partitions.md` | **Read** | only for a CPU job (§ 4)          |
| `references/modules.md`        | **Read** | only for modules, CUDA, MPI       |
| `references/remote-session.md` | **Read** | only for a remote session (§ 10)  |

Related: the `cluster-torch` skill (same section numbers), the `cluster-remote` skill for a remote Claude session.

**Contents**

0. In short
1. Access
2. Hardware
3. Our resources
4. Slurm
5. Billing
6. Storage
7. Data and transfers
8. Software environment
9. Job template
10. Misc
11. Open questions

---

## 0. IN SHORT

1. **`--account=bsmfc` and `--partition=<name>`** in every job (unlike Torch, the partition is given). If `bsmfc`
   runs out of GPU credits, ask me before switching to `sail` (§ 3).
2. **GPU partition**: 4 A100 40 GB per node, at most 8 CPUs and 60 GB per GPU, 48 GPUs per user, **48 h** max (§ 4).
3. **No wall-time extension**: checkpoint and restart (§ 4).
4. **Every job costs credits** (BUh): a GPU node costs 512 BUh/h; a project out of credits cannot submit (§ 5).
5. **Scratch is wiped at the May and November maintenances**, without backup; next **2026-11-30**. If the next
   maintenance is less than 15 days away, warn me before writing to scratch (§ 6).
6. **Files in projects and scratch must belong to the project group**, otherwise "Disk quota exceeded" (§ 6).
7. **No computation on login nodes**; login through an SSH gateway (`gwceci.uliege.be`, ULiège VPN off campus).
8. **Installs**: updating `albus` and `shaggy` as the `auto-update` skill says is pre-approved; any other install,
   ask me first. Containers: Apptainer only (`--nv` for GPUs); software through Lmod / EasyBuild modules (§ 8).
9. **Neptune jobs go through dawgz**; go through the checklist of § 9 before submitting.

---

## 1. ACCESS

| Item     | Details                                                                                        |
| -------- | ---------------------------------------------------------------------------------------------- |
| Login    | `frontal.lucia.cenaero.be`, round robin over `frontal01` / `frontal02`, through an SSH gateway |
| Gateway  | ULiège: `gwceci.uliege.be`, ULiège VPN off campus (CÉCI)                                       |
| Password | valid 365 days, expired = no login even with a key: `passwd_days_left`                         |
| Support  | https://support.lucia.cenaero.be (Redmine, HPC credentials), or it@cenaero.be                  |

- Login nodes: light tasks and small compilations only. Each has 128 cores and 251 GB, shared by every user, with no
  per-user memory or CPU cap (cgroup and `ulimit` unlimited, 2026-10-28): keep it light (`nice`, 4 threads).
- A reconnection can land on the other login node: tmux sessions and processes started there keep running
  (`ssh frontal01` from Lucia to reach them).
- Support tickets: give job IDs, project, paths and error messages. Web access (Open OnDemand): `references/access.md`.

---

## 2. HARDWARE

AMD EPYC Milan (no hyperthreading), HDR InfiniBand fat tree, 10 Gb/s to Belnet. RHEL 8, Slurm 25.11.6. ~4 PFLOPS.

| Type           | Nodes (`sinfo`)      | GPUs / node            | CPUs | RAM / node (usable) |
| -------------- | -------------------- | ---------------------- | ---: | ------------------- |
| GPU            | `cna[001-050]` (50)  | **4× A100 40 GB**      |   32 | 256 GB (240 GB)     |
| AI             | `cni[001-002]` (2)   | **8× A100 SXM4 80 GB** |   64 | 2 TB (2000 GB)      |
| Visualization  | `cng[001-004]` (4)   | 4× T4 16 GB            |   32 | 512 GB (492 GB)     |
| Large / XLarge | `cnl`, `cnx` (7 + 1) | –                      |   64 | 2 TB / 4 TB         |

- No local disk, except 6.4 TB NVMe on the AI nodes.
- 200 A100 40 GB: `cna[001-048]` in `gpu`, `cna[049-050]` in `debug-gpu`. GRES: `gpu:A100:4` (`cna`), `gpu:A100:8`
  (`cni`), `gpu:T4:4` (`cng`). NVLink between the GPUs of a node: not documented [verify].
- Compared to Torch: more GPUs per user (48), but older and smaller GPUs (A100 40 GB vs H200 150 GB).

---

## 3. OUR RESOURCES

From the Neptune repository, from me (2026-10-27) and from the cluster (2026-10-28).

| What            | Value                                                                                            |
| --------------- | ------------------------------------------------------------------------------------------------ |
| Slurm accounts  | `bsmfc` (MAST group, Marilaure Grégoire): use it first; `sail` (SAIL lab, Gilles Louppe): backup |
| Partitions used | `gpu` (trainings), `ia` (fine-tuning), `debug-gpu`, `visu`, `large` (statistics)                 |
| Project space   | `/gpfs/projects/acad/bsmfc/` (NEMO simulation in `nemo4.2.0/`, datasets)                         |
| Scratch         | `/gpfs/scratch/acad/bsmfc/vmangele/` (group `bsmfc`)                                             |
| `sail` spaces   | `/gpfs/projects/acad/sail`, `/gpfs/scratch/acad/sail`                                            |
| Job submission  | [dawgz](https://github.com/francois-rozet/dawgz) 1.0.4 from Python, `schedule(...)` (§ 9)        |
| Environment     | micromamba `neptune` (`~/micromamba/envs/neptune`): PyTorch 2.5.1, ruff 0.4.8, wandb 0.26.1      |

Credits on 2026-10-28 (`get_slurm_quota`, both accounts), used of 40 000 000 BUh: `bsmfc` 31 443 476, 8.6 M left
(21 %), expires 2027-09-21; `sail` 36 640 950, 3.4 M left (8 %), expires **2027-02-22**.

- **`bsmfc` first.** When its GPU credits run low, ask me whether to switch to `sail`: never on your own.
- Both accounts reach the same partitions (§ 4, `references/cpu-partitions.md`).
- 8.6 M BUh = about 16 800 hours of full GPU nodes (512 BUh/h), e.g. 175 trainings of 48 h on one node.

---

## 4. SLURM

- **`--account` and `--partition`** in every job, as in all the examples of the docs.
- **At most 8 CPUs and 60 GB per GPU** on `gpu`: a full node = `--gpus=4 --cpus-per-task=8 --mem=240G`.
- **No wall-time extension**: checkpoint and restart.
- GPU syntax: `--gpus=N` (docs) or `--gres=gpu:N`, both accepted (`--test-only`).

GPU and big-memory partitions; the CPU ones are in `references/cpu-partitions.md`. Live values:
`sacctmgr show qos format=Name,MaxTRESPU%16,MaxJobsPU,MaxSubmitPU,MaxTRES%32,MaxWall`.

| Partition         | Nodes               | Max wall    | Limits                                     | Use            |
| ----------------- | ------------------- | ----------- | ------------------------------------------ | -------------- |
| `gpu`             | 48 × 4 A100 40 GB   | **48 h**    | **48 GPUs**, 12 nodes per user             | trainings      |
| `ia`              | 2 × 8 A100 80 GB    | **48 h**    | –                                          | big models     |
| `debug-gpu`       | 2 × 4 A100 40 GB    | **2 h**     | 2 nodes/job, 1 running, 10 queued per user | tests          |
| `visu`            | 4 × 4 T4            | 4 h         | exactly 1 GPU, ≤ 8 CPUs, ≤ 123 GB, 1 job   | light GPU work |
| `large`, `xlarge` | 7 × 2 TB / 1 × 4 TB | 168 / 336 h | ≥ 490 / 1000 GB per job, 4 / 1 nodes/user  | big memory     |

- **No preemption**: `PreemptMode=OFF` on `gpu`, `ia`, `debug-gpu` and `batch` (2026-10-28). Cancellation of
  underused GPUs and requeue: not documented, nothing seen in the configuration [verify]. Partitions do not overlap.
- GPU nodes are shared between jobs (`ExclusiveUser=NO`, `OverSubscribe=NO`): a 1-GPU job gets 8 CPUs of a node
  (`--test-only`). Default memory: 7.5 GB per CPU on `gpu` / `debug-gpu` (= 60 GB per GPU), 31 GB on `ia`.
- `xlarge`: the partition says 7 days, but its QoS overrides it with 14 days (`PartitionTimeLimit`).
- Interactive: `srun -p debug-gpu -A bsmfc --gpus=1 -t 60 --pty bash`.
- Arrays: `#SBATCH --array=0-19`, output `%A-%a_%x.out`, `$SLURM_ARRAY_TASK_ID`.

---

## 5. BILLING

In BUh: the largest of requested CPUs, memory and GPUs (in CPU equivalents) × weight of the node × hours. Weights
from `scontrol show partition`, per CPU / GB of memory / GPU:

| Partition     | Weights             |       1 GPU |        Full node |
| ------------- | ------------------- | ----------: | ---------------: |
| `gpu`         | 16 / 2.13 / 128     |   128 BUh/h |    **512 BUh/h** |
| `ia`          | 25.6 / 0.82 / 204.8 | 204.8 BUh/h | **1638.4 BUh/h** |
| `visu`        | 4 per CPU           |    32 BUh/h |        128 BUh/h |
| `batch` (CPU) | 1 per CPU           |           – |        128 BUh/h |

- **A project out of credits, or expired, cannot submit.** Top-up:
  https://login.ceci-hpc.be/init-project/#update_project.
- Usage: `get_slurm_quota`, or
  `sreport cluster AccountUtilizationByUser Accounts=bsmfc -t Hour -T billing Start=... End=...`.
- Fair share: 85 % for non-economic projects (70 % universities), shared equally between the projects of a category.

---

## 6. STORAGE

IBM Spectrum Scale (GPFS), about 3 PiB. Default quotas in space / files.

| Path                                | Default quota  | Backup                         | Use                          |
| ----------------------------------- | -------------- | ------------------------------ | ---------------------------- |
| `/gpfs/home/<org>/<user>` (`$HOME`) | 200 GB / ~1 M  | snapshots 7 days, tape 30 days | code, configs                |
| `/gpfs/projects/<org>/<project>`    | 1000 GB / ~1 M | snapshots 7 days, tape 30 days | shared data, long term       |
| `/gpfs/scratch/<org>/<project>`     | 1000 GB / ~1 M | **none**, wiped (below)        | fast I/O (NVMe burst buffer) |

Ours on 2026-10-28 (`mmlsquota`, soft quota / hard limit):

| Space                    | Used     | Space quota / limit | Files used | Files quota  |
| ------------------------ | -------- | ------------------- | ---------- | ------------ |
| home `vmangele`          | 109 GB   | 200 / 230 GB        | **940 K**  | **1.02 M** ⚠ |
| projects `bsmfc` (group) | 99.6 TB  | 150 / 195 TB        | 1.9 M      | 10.2 M       |
| scratch `bsmfc` (group)  | 121.5 TB | 150 / 195 TB        | 2.1 M      | 10.2 M       |

- **Scratch purge**: at the May and November maintenances (next **2026-11-30**, § 10), announced 15 days before.
  If the next maintenance is less than 15 days away, warn me before writing to scratch.
- **Home: 92 % of the files used** (environments, `.vscode-server`, caches): no new environments or many small files
  in `$HOME`. The default quotas of the docs (and CÉCI's 50 / 50 / 100 GB) do not apply to `bsmfc`.
- Check: `mmlsquota -g <project> --block-size g ess:projects` (or `ess:scratch`, `ess:home` with `-u <user>`).
- **Group trap**: files in projects and scratch must belong to the project group, otherwise "Disk quota exceeded".
  Use `newgrp <project>`, copy with `rsync -av --no-p --no-g --chmod=ug=rwX` or `cp` (not `mv`, not `scp`).
- Snapshots: `~/.snapshots/` (restore with `cp -p`); tape restores through a ticket.

---

## 7. DATA AND TRANSFERS

- I/O-heavy work goes to scratch (burst buffer, ~15× faster than projects); copy results elsewhere afterwards.
- Avoid millions of small files (file quotas). Only the AI nodes have a local disk (§ 2).
- Transfers: `rsync` / `scp` through the SSH gateway. No DTN, no Globus documented [verify].
- Internet: yes from the login nodes (GitHub, PyPI, `api.wandb.ai`, `claude.ai` reached on 2026-10-28;
  `apptainer pull docker://...` works there); from compute nodes [verify].

---

## 8. SOFTWARE ENVIRONMENT

- **Neptune environment**: activate it before running anything, in a shell and in a job (§ 3):
  `eval "$(micromamba shell hook -s bash)"; micromamba activate neptune`.
- **Installs**: updating `albus` and `shaggy` as the `auto-update` skill says is pre-approved; any other install or
  upgrade in an environment, ask me first.
- The [cybersecurity page](https://doc.lucia.cenaero.be/cyber/) asks to install nothing from unverified sources and
  to use only the modules and environments of the module managers: install only official releases (checksum
  verified). No documented policy for conda, pip or PyTorch [verify].
- Software through Lmod and EasyBuild modules (stacks, CUDA, Python, MPI, own builds: `references/modules.md`).
- Containers: Apptainer only (`ml containers/apptainer`), GPUs with `--nv`. Set `APPTAINER_CACHEDIR` to the project
  scratch (the default `~/.apptainer` grows large).

---

## 9. JOB TEMPLATE

- **Neptune jobs**: submit them with dawgz (`schedule(...)`), as the Neptune repository does.
- **Raw sbatch**: only outside Neptune's dawgz pipelines (a test, a one-off script): copy `scripts/gpu-job.sbatch`,
  one full GPU node from the docs, adapted to PyTorch DDP; not tested on Lucia yet [verify].

Before a job:

- [ ] `--account=bsmfc` (or `sail` after my yes) and the right `--partition` (§ 3, § 4)?
- [ ] `get_slurm_quota`: enough credits left (§ 5)?
- [ ] At most 8 CPUs and 60 GB per GPU on `gpu` (§ 4)?
- [ ] Can it run longer than 48 h: does it checkpoint and restart?
- [ ] Do the output files in projects or scratch belong to the project group (§ 6)?
- [ ] Scratch: is the next maintenance more than 15 days away, or did you warn me (§ 6)?

---

## 10. MISC

- **Acknowledgement** (required): *"The present research benefited from computational resources made available on
  Lucia, the Tier-1 supercomputer of the Walloon Region, infrastructure funded by the Walloon Region under the grant
  agreement n°1910247."*
- **Maintenance**: quarterly, Mondays 07:00–19:00. Next **Monday 2026-11-30** (scratch wiped; banner of the docs on
  2026-10-28), then planned 2027-02-22, 2027-05-10, 2027-09-13, 2027-11-29 [verify].
- Lucia is mainly meant for large jobs; short wall times favour the rotation of the jobs.
- Security: never share credentials or keys, report a lost key to support at once; Lucia is not a backup system.
- Remote Claude session: `references/remote-session.md`.

---

## 11. OPEN QUESTIONS

| #   | Question                                             | Status                          |
| --- | ---------------------------------------------------- | ------------------------------- |
| 1   | Internet from compute nodes (WandB, PyPI, GitHub)?   | **open**, test from a job       |
| 2   | Policy for conda / pip, recommended PyTorch install? | **open**, ask support (§ 8)     |
| 3   | Cancellation of underused GPUs?                      | **open**; no preemption (§ 4)   |
| 4   | Long, light processes on login nodes (tmux, Claude)? | **open**, ask support           |
| 5   | NVLink; DTN or Globus; 2FA, VSCode?                  | **open**, not documented        |
| 6   | Maintenance dates of 2027?                           | **open**, docs banner (§ 10)    |
| 7   | Does the GPU job template run?                       | **open**, try it on `debug-gpu` |

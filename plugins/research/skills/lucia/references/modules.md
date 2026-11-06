# Lucia: modules and builds

Read only when working outside the `neptune` micromamba environment: modules, CUDA, MPI, building software. From the
[Lucia docs](https://doc.lucia.cenaero.be) (read on 2026-10-27). Installs: the rules of SKILL.md § 8 apply.

| Tool       | Details                                                                                              |
| ---------- | ---------------------------------------------------------------------------------------------------- |
| Modules    | Lmod: `module avail`, `module spider`, `ml`; sticky modules need `module --force purge`              |
| Stacks     | `EasyBuild/2022a`, `2023a`, `2024a` (default): load one first, never mix them; updated each February |
| CUDA       | `CUDA/11.7.0` (2022a), `CUDA/12.2.0` (2023a), `CUDA/12.6.0` (2024a); A100 = `sm_80`                  |
| Python     | `devel/python/Anaconda3-2022.05`, `Python/3.11` and `3.12` + `virtualenv` (2023a)                    |
| MPI        | OpenMPI + UCX, CUDA-aware, e.g. `OpenMPI/5.0.3-NVHPC-25.1-CUDA-12.6.0` (2024a); not Intel MPI        |
| Own builds | EasyBuild in user space: `module load EasyBuild/2023a EasyBuild-user/4.9.0`, in `~/.local/easybuild` |

- UCX tuning: `UCX_NET_DEVICES=mlx5_0:1`, `UCX_TLS=rc,self,sm`, `UCX_MEMTYPE_CACHE=n`.
- The only PyTorch example of the docs is a container:
  `apptainer pull pytorch.sif docker://pytorch/pytorch:2.7.1-cuda11.8-cudnn9-runtime`.

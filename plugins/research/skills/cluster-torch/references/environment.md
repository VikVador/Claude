# BUILDING AN ENVIRONMENT ON TORCH

Part of the `cluster-torch` skill (§ 8): read it when building or changing an environment. The rules of § 8 still hold: any
install or upgrade needs my approval (except `albus` and `shaggy` through the `auto-update` skill), on a compute node,
never on a login node.

## Generic recipe

Apptainer + an ext3 overlay: the whole environment lives in a single file ⇒ no inode problem. For a **new**
environment, use the generic CUDA image below; Heimdall's overlay stays with its own image (§ 8).

1. Get a compute node (login nodes cap memory at 2 GB/user and run a different OS):
   `srun --account=<acct> -c4 --mem=16GB -t2:00:00 --pty bash`.
2. Copy an overlay template and open it read-write:

   ```bash
   cp /share/apps/overlay-fs-ext3/overlay-15GB-500K.ext3.gz $SCRATCH/env/ && gunzip $SCRATCH/env/overlay-15GB-500K.ext3.gz
   apptainer exec --fakeroot \
       --overlay $SCRATCH/env/overlay-15GB-500K.ext3:rw \
       /share/apps/images/cuda-13.3.1-ubuntu-26.04.sif bash
   ```

3. Inside: install Miniforge into `/ext3/miniforge3` (or uv into `/ext3/.uv` + venv `/ext3/.venv`), write
   `/ext3/env.sh`.
4. Jobs then mount the overlay `:ro` and run `source /ext3/env.sh` first.

`uv` variant: `UV_INSTALL_DIR=/ext3/.uv`, `UV_PYTHON_INSTALL_DIR=/ext3/.uv/python`, `UV_PROJECT_ENVIRONMENT=/ext3/.venv`,
then `uv sync` from the repository.

## Heimdall

`sbatch cluster/jobs/environment.sbatch` (in the Heimdall repository) creates or updates the overlay
`$SCRATCH/env/heimdall.ext3` and its conda environment `heimdall`.

## Good to know

- Images: `ls /share/apps/images/`; overlay templates: `ls /share/apps/overlay-fs-ext3/`.
- Lmod modules (`module avail`), e.g. `anaconda3/2024.02`, `openmpi/gcc/4.1.6`, `rclone`.
- Docker images work through Apptainer: `apptainer pull docker://…`.
- Optional: ext3 → squashfs (`mksquashfs /ext3 env.sqf -keep-as-directory`), ~2.5× smaller.
- No `conda init` block in `~/.bashrc` (it breaks overlays). Use `export PYTHONNOUSERSITE=True`.
- RTX Pro 6000 (Blackwell, sm_120) needs PyTorch built for **CUDA ≥ 12.8**.

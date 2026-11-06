# LIBRARIES

What each library contains, module by module. Read it before writing code that one of them could cover, or when you
need its API; then confirm in the docs or the installed source (§ 3 of `SKILL.md`), which win when they disagree.

**Contents**

1. azula: diffusion models
2. zuko: normalizing flows
3. shaggy: training tools and autoencoders (mine)
4. albus: metrics (mine)

---

## 1. AZULA: DIFFUSION MODELS

[GitHub](https://github.com/probabilists/azula) · [docs](https://azula.readthedocs.io)

One interface for diffusion models: a **noise schedule**, a **denoiser** and a **sampler**.

| Module           | Contents                                                                                            |
| ---------------- | --------------------------------------------------------------------------------------------------- |
| `azula.noise`    | `VPSchedule`, `VESchedule`, `CosineSchedule`, `RectifiedSchedule`, …                                |
| `azula.denoise`  | `GaussianDenoiser`, `KarrasDenoiser`, … (denoisers and training losses)                             |
| `azula.sample`   | `DDPMSampler`, `DDIMSampler`, `EulerSampler`, `HeunSampler`, `PCSampler`, …                         |
| `azula.guidance` | posterior sampling and guidance: `MMPSDenoiser`, `DPSSampler`, `CFGDenoiser`, …                     |
| `azula.nn`       | `DiT`, `ViT`, `UNet`, `MultiheadSelfAttention` with RoPE, `Patchify`, `RMSNorm`, `SwiGLU`, `ConvNd` |
| `azula.linalg`   | structured covariances, `cg`, `gmres`                                                               |
| `azula.plugins`  | pre-trained models (unstable)                                                                       |

---

## 2. ZUKO: NORMALIZING FLOWS

[GitHub](https://github.com/probabilists/zuko) · [docs](https://zuko.readthedocs.io)

Normalizing flows as `nn.Module`s on top of `torch.distributions`: `flow(context).log_prob(x)`, `.sample()`.

| Module                        | Contents                                                   |
| ----------------------------- | ---------------------------------------------------------- |
| `zuko.flows`, `zuko.mixtures` | `MAF`, `NSF`, `RealNVP`, `NICE`, `NAF`, `CNF`, … and `GMM` |
| `zuko.transforms`             | the transformations the flows are built from               |
| `zuko.distributions`          | `DiagNormal`, `BoxUniform`, …                              |
| `zuko.nn`                     | `MLP`, `MaskedMLP`, …                                      |

---

## 3. SHAGGY: TRAINING TOOLS AND AUTOENCODERS (MINE)

[GitHub](https://github.com/VikVador/Shaggy) · [documentation](https://shaggy.readthedocs.io) (tutorials) · tutorial
data on the [`master-demo`](https://github.com/VikVador/Shaggy/tree/master-demo) branch. The package is `shaggy`
(`import shaggy`).

| Module                | Contents                                                                                           |
| --------------------- | -------------------------------------------------------------------------------------------------- |
| `shaggy.models`       | `ConvEncoder`, `ConvDecoder`, `ConvAE`, `create_ConvAE`, `AutoEncoder`, `FusionAE`                 |
| `shaggy.layers`       | `BoundaryConv`, `FRMSNorm`, `ResidualBlock`, `ModulatedSequential`                                 |
| `shaggy.loss`         | `loss_reconstruction`, `loss_geometry_embedding` (GME), `loss_continuous_ranked_probability_score` |
| `shaggy.optimizers`   | `SOAP`, `Muon`, `HybridMA`, `safe_gradient_step`                                                   |
| `shaggy.schedulers`   | `warmup_cosine_decay`                                                                              |
| `shaggy.distributed`  | `setup_distributed`, `reduce_mean` (trainings under torchrun)                                      |
| `shaggy.dataloader`   | `infinite_dataloader`, `get_fixed_indices` (fixed validation samples)                              |
| `shaggy.training`     | `has_stagnated` (stopping), `save_state`, `load_state` (resume a training)                         |
| `shaggy.tools`        | `save`, `load`, `load_config`, `load_weights` (weights and configuration in one directory)         |

**Good to know**

- `ConvAE`: residual blocks per level, N spatial dimensions, stride per level and per axis, patching, boundaries per
  axis (`periodic=(-1,)`, `reflect=(...)`), optional modulation.

---

## 4. ALBUS: METRICS (MINE)

[GitHub](https://github.com/VikVador/Albus) · [documentation](https://albus-metrics.readthedocs.io) (one tutorial per
module). The package is `albus` (`import albus`).

| Module               | Contents                                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------ |
| `albus.metrics`      | all with masks: the functions are listed below                                             |
| `albus.ocean.oxygen` | `hypoxia` (detection scores, ROC and PR curves)                                            |
| `albus.visuals`      | per field, between two sets, on any features: the functions are listed below               |
| `albus.tools`        | `apply_mask`, `axes`, `drop` (named axes such as `"T C Y X"`, `names=`), `nanmean`         |

**Good to know**

- `albus.metrics`, all with masks: `mean_square_error`, `root_mean_square_error`, `skill`, `standard_deviation`,
  `spread`, `spread_skill_ratio`, `continuous_ranked_probability_score`, `power_spectrum`.
- `albus.visuals`: per field, `peak_signal_to_noise_ratio`, `structural_similarity`; between two sets,
  `frechet_inception_distance`, `kernel_inception_distance`; and on any features (latents), `frechet_distance`,
  `kernel_distance`.

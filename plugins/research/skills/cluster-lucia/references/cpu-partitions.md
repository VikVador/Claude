# Lucia: CPU partitions

Read only for a CPU job (no GPU). Checked on the cluster on 2026-10-28 (`sinfo`, `sacctmgr`, `scontrol`,
`sbatch --test-only`). The GPU partitions and `large` / `xlarge` are in SKILL.md (§ 4).

| Partition         | Nodes               | Max wall | Limits                                        | Use            |
| ----------------- | ------------------- | -------- | --------------------------------------------- | -------------- |
| `batch`, `medium` | 254 / 20 × 128 CPUs | 48 h     | whole nodes (ExclusiveUser), 2000 queued jobs | CPU jobs       |
| `batch` (`long`)  | 128 CPUs            | 168 h    | 4 nodes, 512 CPUs per user                    | long CPU jobs  |
| `shared`          | 10 × 128 CPUs       | 168 h    | 1 node per job, 500 queued                    | small CPU jobs |
| `debug`           | 10 × 128 CPUs       | 2 h      | 4 nodes, 4 running, 20 queued                 | CPU tests      |

CPU nodes (`sinfo`), no local disk:

| Type         | Nodes                | CPUs / node | RAM / node (usable) |
| ------------ | -------------------- | ----------: | ------------------- |
| CPU standard | `cns[001-270]` (270) |         128 | 256 GB (240 GB)     |
| CPU medium   | `cnm[001-030]` (30)  |         128 | 512 GB (492 GB)     |

- `long` QoS: `--partition=batch --qos=long` (accepted by `--test-only`). On `batch` / `medium`, the QoS is `normal`
  (default) or `long`.
- CPU nodes: `cns[002-255]` in `batch`, `cns[261-270]` in `debug`, `cns[256-260]` and `cns001` in the private
  partitions `sab` and `crm` (not reachable by our accounts); `cnm[001-020]` in `medium`, `cnm[021-030]` in `shared`.
- Interactive: `salloc -p batch -A bsmfc -N 1 -t 1:00:00`.
- Billing: weight 1 on `batch`, so 128 BUh/h for a full node.

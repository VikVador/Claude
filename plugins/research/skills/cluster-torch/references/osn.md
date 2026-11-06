# OSN POD

Open Storage Network, S3-compatible object storage of M²LInES. Part of the `cluster-torch` skill (§ 7): read it when working
with the OSN pod.

| Item       | Details                                                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Endpoint   | **`https://nyu1.osn.mghpcc.org`**                                                                                                    |
| Buckets    | **`m2lines-pubs`**, public: anonymous listing and reads since 2026-10-22. Others exist, e.g. `emulators`.                            |
| Heimdall   | datasets 2000-2025 in **`m2lines-pubs/Datasets`** (~12.4 TB, `README.md` at its root), paths in `heimdall/config`, read anonymously. |
| Writing    | only with the rclone remote **`osn-rw`** or the s3fs profile **`osn`**, set up privately by each user.                               |
| Access     | *open* buckets: anonymous read, keys to write; *protected*: keys for both, **two pairs RO / RW** → RO in jobs.                       |
| Naming     | lowercase, digits, `-_.`; no names differing only by case.                                                                           |
| Keys, help | https://coldfront.osn.mghpcc.org (keys), https://openstoragenetwork.github.io/docs/, help@osn.mghpcc.org                             |

## Read from Python (public bucket)

```python
ds = xr.open_zarr("s3://m2lines-pubs/Datasets/Glorys/cmems_glorys_2000-2025_daily_4320x2041x50.zarr",
                  storage_options={"anon": True, "client_kwargs": {"endpoint_url": "https://nyu1.osn.mghpcc.org"}})
```

## rclone

The remote is written privately: keys never in a repository, never displayed.

```text
[osn]
type = s3
provider = Ceph
access_key_id = <key>
secret_access_key = <secret>
endpoint = https://nyu1.osn.mghpcc.org
no_check_bucket = true
```

Then `rclone ls osn:/m2lines-pubs`, or `rclone copy --transfers=32 osn:/bucket/path $SCRATCH/path` (on the DTN).

## Good to know

- PyTorch `DataLoader` reading OSN with s3fs: **spawned** workers (`multiprocessing_context="spawn"`), forked ones hang.
- ~30 MB/s per S3 stream ⇒ speed comes from the dataloader workers, not the batch size; sharded zarr (one object per
  day) is ~2× faster to read than one object per chunk.
- `rclone about` is not supported; `rclone purge` prints a harmless "Failed to read versioning status". Listings
  (`rclone lsf`, `rclone size --fast-list`) are fine on a login node; big copies go on the DTN or in a job.
- Compute nodes reach `nyu1.osn.mghpcc.org` (2026-10-14).

# Lucia: remote Claude session

Read only when starting, checking or stopping a remote Claude session on a Lucia login node. The `claude-remote` skill
covers the setup; these are the Lucia facts, checked on 2026-10-28 and 2026-11-01.

- `frontal.lucia.cenaero.be` is a DNS round robin: an editor can reconnect to the other login node (`frontal01` /
  `frontal02`). Go to the node `claude-remote status` names with `ssh <node>` before stopping or attaching.
- Claude uses ~250 MB here; the `claude-remote` skill says ~350 MB [verify]. The login nodes have no per-user cap: the limit
  is ours, heavy work goes through Slurm.
- The docs allow "lightweight tasks" and say nothing on long, light processes such as tmux: ask support in case of
  doubt.
- `tmux` is `/usr/bin/tmux` 2.7 and `python3` is `/usr/bin/python3` 3.6.8 on both login nodes. The remote-session
  hooks (`phone-*.sh` of the `claude-remote` skill) are pure bash; the plugin hooks of `up-to-date` and `oral-recap` are
  Python and need `python3` ≥ 3.6, which 3.6.8 meets.
- A personal claude.ai account (Pro) allows Remote Control.
- The client needs neither the ULiège VPN nor the SSH gateway: the login node only makes outbound HTTPS requests.
- A maintenance reboots the login nodes: run `claude-remote` again afterwards.

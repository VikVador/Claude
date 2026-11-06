# ACCESS AND BILLING DETAILS

Part of the `torch` skill: read it only when I ask about client configuration, external collaborators, sharing
files, RPS pricing or the publication acknowledgement.

## External collaborators

A full-time NYU faculty sponsors an *affiliate* NetID, then the person requests the HPC account ("External
Collaborator"). It expires after **12 months** → yearly renewal.

## SSH client

`~/.ssh/config` (from the docs). Login has no SSH keys (password + Microsoft device-login 2FA), and the VPN is
mandatory off campus (§ 1).

```text
Host torch login.torch.hpc.nyu.edu
  Hostname login.torch.hpc.nyu.edu
  User <NetID>
  StrictHostKeyChecking no
  ServerAliveInterval 60
  ForwardAgent yes
  UserKnownHostsFile /dev/null
  LogLevel ERROR
Host dtn.torch.hpc.nyu.edu
  User <NetID>
  (same options)
Host cs* cl* gr* ga* gh* gl*          # compute nodes, through the login node
  User <NetID>
  ProxyCommand ssh -W %h:%p torch-login
  ForwardAgent yes
```

## VSCode Remote-SSH

- `Remote.SSH: Connect Timeout = 120`, "Lockfiles In Tmp" on, "Use Flock" off.
- `~/.vscode-server` symlinked to `$SCRATCH/.vscode-server` (home inode quota, § 6).
- Alternative: the `code-server` app in Open OnDemand (https://ood.torch.hpc.nyu.edu).

## Sharing files

NFSv4 ACLs (`nfs4_setfacl -a "A::<NetID>:RX" dir`, `-R -a "A:df:<NetID>:RWX" dir/share`), or an IPA group
`g-DEPT-LAB` (ask hpc@nyu.edu). Never `chmod 777`.

## RPS pricing

Research Project Space (shared lab space, daily backup kept 30 days, § 6):

- $100/TB/yr + $100 per 200 K inodes/yr, at least 1 TB + 200 K inodes;
- requested by the PI by email;
- stakeholder list: Google sheet linked in the docs. Whether the Zanna group has one is still open (§ 11).

## Acknowledgement in publications

*"This work was supported in part through the NYU IT High Performance Computing resources, services, and staff
expertise"*; add the papers and grants to the project in the portal (https://projects.hpc.nyu.edu).

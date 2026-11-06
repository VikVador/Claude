# Lucia: setting up access

Read only when setting up access to Lucia (account, gateway, SSH client, password): none of it is needed once logged
in. From the [Lucia docs](https://doc.lucia.cenaero.be) (read on 2026-10-27) and the
[CÉCI](https://www.ceci-hpc.be) pages (marked (CÉCI)).

| Item         | Details                                                                                             |
| ------------ | --------------------------------------------------------------------------------------------------- |
| Requirements | a CÉCI account and a project (CÉCI), see below                                                      |
| Login        | `frontal.lucia.cenaero.be` (round robin over `frontal01` / `frontal02`), through an SSH gateway     |
| ULiège       | gateway `gwceci.uliege.be`, with the CÉCI login and key; ULiège VPN off campus (CÉCI)               |
| Cenaero      | gateway `gateway.lucia.cenaero.be` (Cenaero and industry): no computation, 10 / 40 GB, own password |
| SSH config   | the CÉCI [ssh_config wizard](https://www.ceci-hpc.be/sshconfig.html), tick "Tier1"                  |
| SSH keys     | supported (ed25519 with passphrase)                                                                 |
| Password     | needed for Open OnDemand and support; valid 365 days, 12 characters min.                            |
| Web access   | Open OnDemand at https://hpcportal.lucia.cenaero.be: Jupyter, Linux desktop, ParaView, batch jobs   |
| Support      | https://support.lucia.cenaero.be (Redmine, HPC credentials), or it@cenaero.be                       |

## Account and project

A project is created by a permanent member of a CÉCI university (e.g. the supervisor) at
https://login.ceci-hpc.be/init-project/; projects last 3 years (CÉCI).

## Password

- An expired password means no login, even with a key.
- `passwd_days_left` (days left), `passwd` (change it), reset at https://ssp.lucia.cenaero.be.
- 5 wrong attempts lock the account for 10 min.
- The first SSH login changes the initial password and creates `$HOME`, needed before using Open OnDemand.

## SSH client

Academics use the CÉCI wizard. The `~/.ssh/config` of the docs, for the Cenaero gateway:

```text
Host gwlucia
    Hostname gateway.lucia.cenaero.be
    User <your_username>
    IdentityFile ~/.ssh/id_rsa
    ForwardAgent yes
Host lucia
    Hostname frontal.lucia.cenaero.be
    User <your_username>
    IdentityFile ~/.ssh/id_rsa
    ProxyJump gwlucia
```

Host-key warning: `ssh-keygen -f ~/.ssh/known_hosts -R frontal.lucia.cenaero.be`, then add the key given on the
[SSH page](https://doc.lucia.cenaero.be/connect/ssh/).

## Not documented

2FA, VSCode [verify].

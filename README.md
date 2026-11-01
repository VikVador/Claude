# claude

Victor's shared skills for Claude Code, used across projects (Heimdall, Neptune, …).

| Skill    | When Claude uses it                                   |
| -------- | ----------------------------------------------------- |
| `report` | before any report, analysis page or figure            |
| `torch`  | on the NYU Torch cluster: Slurm, storage, OSN pod     |
| `lucia`  | on the Lucia cluster (Cenaero, Neptune)               |
| `phone`  | driving Claude Code from the phone (Remote Control)   |

## Install (once per machine)

In Claude Code:

```
/plugin marketplace add VikVador/claude
/plugin install vikvador@vikvador
```

## Update

```
/plugin marketplace update vikvador
```

then restart Claude Code.

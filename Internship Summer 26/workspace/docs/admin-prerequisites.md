# Administrator prerequisites

These commands change shared host configuration and should be reviewed by the
machine administrator.

## Docker access

No administrator action is required. A rootless Docker daemon is installed for
this account and GPU 1 has passed a CUDA 12.2 CDI smoke test.

## Artifact storage

Provision an account-owned root on the large data disk:

```bash
sudo install -d -m 2775 -o julnk0207 -g julnk0207 /data/julnk0207
sudo install -d -m 2775 -o julnk0207 -g julnk0207 /data/julnk0207/vla
```

Afterward, the user can create datasets, checkpoints, assets, run outputs, and
caches beneath `/data/julnk0207/vla` without administrator privileges.

## Driver maintenance

Do not update the driver while other GPU jobs are active. The current driver is
535.161.07. Isaac Sim 6.0 documents 580.95.05 as its tested Linux version, and
the current GR00T dGPU container uses CUDA 12.8. Schedule the upgrade with the
server owner and validate all existing users' workloads afterward.

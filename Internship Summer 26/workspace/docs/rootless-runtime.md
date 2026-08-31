# Rootless GPU runtime

The account uses a rootless Docker daemon. It does not require access to the
system Docker socket or membership in the root-equivalent `docker` group.

## Installed components

| Component | Location |
|---|---|
| Docker user service | `~/.config/systemd/user/docker.service` |
| Docker socket | `/run/user/1017/docker.sock` |
| Docker context | `rootless` |
| Docker image data | `~/.local/share/docker` |
| Docker daemon config | `~/.config/docker/daemon.json` |
| NVIDIA CDI spec | `~/.config/cdi/nvidia.yaml` |
| Compose plugin | `~/.docker/cli-plugins/docker-compose` |
| slirp4netns | `~/.local/bin/slirp4netns` |
| uv | `~/.local/bin/uv` |

## Routine checks

```bash
systemctl --user status docker.service
docker context show
docker info --format '{{json .SecurityOptions}}'
cd ~/vla-workspace
./scripts/doctor.sh
docker compose --profile smoke run --rm gpu-smoke
```

The smoke profile selects physical GPU 1 using the CDI selector
`nvidia.com/gpu=1`. Inside the container it appears as GPU 0 because it is the
only visible device.

## After a host driver change

The CDI specification embeds driver library paths. Regenerate it after every
driver update, then restart the user daemon:

```bash
nvidia-ctk cdi generate --output="$HOME/.config/cdi/nvidia.yaml"
systemctl --user restart docker.service
cd ~/vla-workspace
docker compose --profile smoke run --rm gpu-smoke
```

## Storage limitation

Rootless Docker currently stores images on the root NVMe. Do not pull Isaac,
GR00T, or multiple large development images until an administrator provides a
writable directory on `/data`. When that exists, configure the rootless Docker
`data-root` and shared VLA cache paths there before downloading artifacts.


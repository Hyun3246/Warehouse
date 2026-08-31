FROM nvidia/cuda:12.2.2-base-ubuntu22.04@sha256:1a8a738e81d4adbef0c709241f5238cec5bb77186dcb5b2103db293315ed42d1

COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

ARG LIBERO_COMMIT=8f1084e3132a39270c3a13ebe37270a43ece2a01

ENV DEBIAN_FRONTEND=noninteractive \
    PATH=/opt/venv/bin:$PATH \
    PYTHONPATH=/opt/LIBERO \
    LIBERO_CONFIG_PATH=/opt/libero-config \
    MUJOCO_GL=egl \
    MUJOCO_EGL_DEVICE_ID=0 \
    PYOPENGL_PLATFORM=egl \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics \
    UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        clang \
        ffmpeg \
        g++ \
        git \
        libegl1 \
        libegl1-mesa-dev \
        libgl1 \
        libgl1-mesa-glx \
        libgles2-mesa-dev \
        libglew-dev \
        libglfw3-dev \
        libglib2.0-0 \
        libosmesa6-dev \
        libsm6 \
        libxext6 \
        libxrender1 \
        make \
    && rm -rf /var/lib/apt/lists/*

COPY containers/libero/requirements-sim.txt /tmp/requirements-sim.txt
RUN uv venv --python 3.8 /opt/venv \
    && uv pip install --python /opt/venv/bin/python --requirement /tmp/requirements-sim.txt

# The simulator stays model-agnostic and talks to policy servers through the
# lightweight OpenPI msgpack/WebSocket client protocol.
COPY projects/openpi/packages/openpi-client /opt/openpi-client
RUN uv pip install --python /opt/venv/bin/python --editable /opt/openpi-client

# LIBERO imports torch for benchmark metadata and initial-state loading. Keep
# this simulator client CPU-only; policy inference lives in a separate image.
RUN uv pip install --python /opt/venv/bin/python --no-deps \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==1.11.0+cpu

RUN git init /opt/LIBERO \
    && git -C /opt/LIBERO remote add origin https://github.com/Lifelong-Robot-Learning/LIBERO.git \
    && git -C /opt/LIBERO fetch --depth 1 origin ${LIBERO_COMMIT} \
    && git -C /opt/LIBERO checkout --detach FETCH_HEAD \
    && test "$(git -C /opt/LIBERO rev-parse HEAD)" = "${LIBERO_COMMIT}" \
    && uv pip install --python /opt/venv/bin/python --no-deps --editable /opt/LIBERO

COPY containers/libero/config.yaml /opt/libero-config/config.yaml
COPY scripts/sim /opt/smoke

RUN mkdir -p /artifacts/datasets/libero /artifacts/runs/sim-smoke

WORKDIR /workspace
CMD ["python", "/opt/smoke/libero_smoke.py"]

import json
from pathlib import Path

import imageio.v3 as iio
import numpy as np

from libero.libero import benchmark, get_libero_path
from libero.libero.envs import OffScreenRenderEnv


suite = benchmark.get_benchmark_dict()["libero_spatial"]()
task = suite.get_task(0)
bddl_file = Path(get_libero_path("bddl_files")) / task.problem_folder / task.bddl_file

env = OffScreenRenderEnv(
    bddl_file_name=str(bddl_file),
    camera_heights=128,
    camera_widths=128,
)

try:
    env.seed(7)
    observation = env.reset()
    image_keys = sorted(key for key in observation if key.endswith("_image"))
    assert "agentview_image" in observation, image_keys

    action = np.zeros(7, dtype=np.float32)
    action[-1] = -1.0
    observation, reward, done, info = env.step(action)

    frame = observation["agentview_image"][::-1]
    assert frame.shape == (128, 128, 3), frame.shape
    assert float(frame.std()) > 1.0, "LIBERO camera image is unexpectedly blank"

    output = Path("/artifacts/runs/sim-smoke/libero-spatial-task-0.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    iio.imwrite(output, frame)

    print(
        json.dumps(
            {
                "status": "ok",
                "suite": "libero_spatial",
                "task_id": 0,
                "language": task.language,
                "image_keys": image_keys,
                "reward": float(reward),
                "done": bool(done),
                "output": str(output),
            }
        )
    )
finally:
    env.close()

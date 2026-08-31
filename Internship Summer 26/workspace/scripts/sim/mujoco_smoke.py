import json
from pathlib import Path

import imageio.v3 as iio
import mujoco
import numpy as np


xml = """
<mujoco model="render-smoke">
  <worldbody>
    <light pos="0 0 3"/>
    <geom type="plane" size="2 2 0.1" rgba="0.15 0.2 0.25 1"/>
    <body pos="0 0 0.5">
      <joint type="free"/>
      <geom type="box" size="0.25 0.25 0.25" rgba="0.8 0.2 0.1 1"/>
    </body>
  </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)
mujoco.mj_step(model, data)

renderer = mujoco.Renderer(model, height=128, width=128)
renderer.update_scene(data)
frame = renderer.render()
renderer.close()

assert frame.shape == (128, 128, 3), frame.shape
assert frame.dtype == np.uint8, frame.dtype
assert float(frame.std()) > 1.0, "Rendered image is unexpectedly blank"

output = Path("/artifacts/runs/sim-smoke/mujoco.png")
output.parent.mkdir(parents=True, exist_ok=True)
iio.imwrite(output, frame)

print(json.dumps({"status": "ok", "renderer": "egl", "shape": list(frame.shape), "output": str(output)}))

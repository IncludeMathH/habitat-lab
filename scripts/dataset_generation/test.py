# Play a teaser video
from dataclasses import dataclass

from habitat.config.default import get_agent_config
from habitat.config.default_structured_configs import (
    MeasurementConfig,
    ThirdRGBSensorConfig,
)

try:
    from IPython.display import HTML

    HTML(
        '<iframe src="https://drive.google.com/file/d/1ltrse38i8pnJPGAXlThylcdy8PMjUMKh/preview" width="640" height="480" allow="autoplay"></iframe>'
    )
except Exception:
    pass

# @title Install Dependencies (if on Colab) { display-mode: "form" }
# @markdown (double click to show code)

import os
import gym
import numpy as np
from hydra.core.config_store import ConfigStore

import habitat
import habitat.gym
from habitat.core.embodied_task import Measure
from habitat.core.registry import registry
from habitat.tasks.rearrange.rearrange_sensors import RearrangeReward
from habitat.tasks.rearrange.rearrange_task import RearrangeTask
from habitat.utils.visualizations.utils import (
    observations_to_image,
    overlay_frame,
)
from habitat_sim.utils import viz_utils as vut

# Quiet the Habitat simulator logging
os.environ["MAGNUM_LOG"] = "quiet"
os.environ["HABITAT_SIM_LOG"] = "quiet"


def insert_render_options(config):
    # Added settings to make rendering higher resolution for better visualization
    with habitat.config.read_write(config):
        config.habitat.simulator.concur_render = False
        agent_config = get_agent_config(sim_config=config.habitat.simulator)
        agent_config.sim_sensors.update(
            {"third_rgb_sensor": ThirdRGBSensorConfig(height=512, width=512)}
        )
    return config


import importlib

# If the import block fails due to an error like "'PIL.TiffTags' has no attribute
# 'IFD'", then restart the Colab runtime instance and rerun this cell and the previous cell.
import PIL

importlib.reload(
    PIL.TiffTags  # type: ignore[attr-defined]
)  # To potentially avoid PIL problem

def main():
    with habitat.Env(
        config=insert_render_options(
            habitat.get_config(
                "benchmark/rearrange/skills/pick.yaml",
            )
        )
    ) as env:
        observations = env.reset()  # noqa: F841

        print("Agent acting inside environment.")
        count_steps = 0
        # To save the video
        video_file_path = "outputs/example_interact.mp4"
        video_writer = vut.get_fast_video_writer(video_file_path, fps=30)

        while not env.episode_over:
            observations = env.step(env.action_space.sample())  # noqa: F841
            info = env.get_metrics()

            render_obs = observations_to_image(observations, info)
            render_obs = overlay_frame(render_obs, info)

            video_writer.append_data(render_obs)

            count_steps += 1
        print("Episode finished after {} steps.".format(count_steps))

        video_writer.close()
        if vut.is_notebook():
            vut.display_video(video_file_path)

if __name__ == '__main__':
    main()

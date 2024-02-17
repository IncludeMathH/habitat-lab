import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='generate config file')

    parser.add_argument('--out', type=str, default='outputs/nav_pick_demo.yaml')

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    cfg_txt = """
    # @package _global_

    defaults:
    - /habitat: habitat_config_base
    - /habitat/simulator/agents@habitat.simulator.agents.main_agent: agent_base
    - /habitat/simulator/sim_sensors@habitat.simulator.agents.main_agent.sim_sensors.head_rgb_sensor: head_rgb_sensor
    - /habitat/task: task_config_base
    - /habitat/task/actions:
        - arm_action
        - base_velocity
    - /habitat/task/measurements:
        - articulated_agent_force
        - force_terminate
        - distance_to_target_object
        - nav_pick_reward
        - nav_pick_success
    - /habitat/task/lab_sensors:
        - target_start_sensor
        - joint_sensor
    - /habitat/dataset/rearrangement: replica_cad

    habitat:
    environment:
        # Number of steps within an episode.
        max_episode_steps: 2000
    task:
        type: RearrangeDemoNavPickTask-v0
        # Measurements
        measurements:
        distance_to_target_object:
            type: "DistanceToTargetObject"
        articulated_agent_force:
            type: "RobotForce"
            min_force: 20.0
        force_terminate:
            type: "ForceTerminate"
            # Maximum amount of allowed force in Newtons.
            max_accum_force: 5000.0
        nav_pick_reward:
            type: "NavPickReward"
            scaling_factor: 0.1
            # General Rearrange Reward config
            constraint_violate_pen: 10.0
            force_pen: 0.001
            max_force_pen: 1.0
            force_end_pen: 10.0
        nav_pick_success:
            type: "NavPickSuccess"
        actions:
        # Define the action space.
        arm_action:
            type: "ArmAction"
            arm_controller: "ArmRelPosAction"
            grip_controller: "MagicGraspAction"
            arm_joint_dimensionality: 7
            grasp_thresh_dist: 0.15
            disable_grip: False
            delta_pos_limit: 0.0125
            ee_ctrl_lim: 0.015
        base_velocity:
            type: "BaseVelAction"
            lin_speed: 12.0
            ang_speed: 12.0
            allow_dyn_slide: True
            allow_back: True
    simulator:
        type: RearrangeSim-v0
        additional_object_paths:
        - "data/objects/ycb/configs/"
        debug_render: False
        concur_render: False
        auto_sleep: False
        agents:
        main_agent:
            height: 1.5
            is_set_start_state: False
            radius: 0.1
            sim_sensors:
            head_rgb_sensor:
                height: 128
                width: 128
            start_position: [0, 0, 0]
            start_rotation: [0, 0, 0, 1]
            articulated_agent_urdf: ./data/robots/hab_fetch/robots/hab_fetch.urdf
            articulated_agent_type: "FetchRobot"

        # Agent setup
        # ARM_REST: [0.6, 0.0, 0.9]
        ctrl_freq: 120.0
        ac_freq_ratio: 4

        # Grasping
        hold_thresh: 0.09
        grasp_impulse: 1000.0

        habitat_sim_v0:
        allow_sliding: True
        enable_physics: True
        gpu_device_id: 0
        gpu_gpu: False
        physics_config_file: ./data/default.physics_config.json
    dataset:
        type: RearrangeDataset-v0
        split: train
        # The dataset to use. Later we will generate our own dataset.
        data_path: data/nav_pick.json.gz
        scenes_dir: "data/replica_cad/"
    """
    nav_pick_cfg_path = args.out
    with open(nav_pick_cfg_path, "w") as f:
        f.write(cfg_txt)

if __name__ == '__main__':
    main()

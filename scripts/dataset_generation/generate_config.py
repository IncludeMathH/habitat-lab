import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='generate config file')

    parser.add_argument('--out', type=str, default='outputs/nav_pick_dataset.yaml')

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    dataset_cfg_txt = """
    ---
    dataset_path: "examples/tutorials/colabs/data/replica_cad/replicaCAD.scene_dataset_config.json"
    additional_object_paths:
    - "examples/tutorials/colabs/data/objects/ycb/configs/"
    scene_sets:
    -
        name: "v3_sc"
        included_substrings:
        - "v3_sc"
        excluded_substrings: []
        comment: "This set (v3_sc) selects all 105 ReplicaCAD variations with static furniture."

    object_sets:
    -
        name: "kitchen"
        included_substrings:
        - "002_master_chef_can"
        - "003_cracker_box"
        excluded_substrings: []
        comment: "Leave included_substrings empty to select all objects."

    receptacle_sets:
    -
        name: "table"
        included_object_substrings:
        - "frl_apartment_table_01"
        excluded_object_substrings: []
        included_receptacle_substrings:
        - ""
        excluded_receptacle_substrings: []
        comment: "The empty substrings act like wildcards, selecting all receptacles for all objects."

    scene_sampler:
    type: "subset"
    params:
        scene_sets: ["v3_sc"]
    comment: "Samples from ReplicaCAD 105 variations with static furniture."


    object_samplers:
    -
        name: "kitchen_counter"
        type: "uniform"
        params:
        object_sets: ["kitchen"]
        receptacle_sets: ["table"]
        num_samples: [1, 1]
        orientation_sampling: "up"

    object_target_samplers:
    -
        name: "kitchen_counter_targets"
        type: "uniform"
        params:
        object_samplers: ["kitchen_counter"]
        receptacle_sets: ["table"]
        num_samples: [1, 1]
        orientation_sampling: "up"
    """
    nav_pick_cfg_path = args.out
    with open(nav_pick_cfg_path, "w") as f:
        f.write(dataset_cfg_txt)

if __name__ == '__main__':
    main()

import argparse
import os
import json
import time
import numpy as np
from timing_maze_game_simulation import TimingMazeGame
from collections import defaultdict
import tkinter as tk
import sys

sys.setrecursionlimit(10000)


def run_simulation(
    max_door_frequencies,
    radii,
    num_maps_per_config,
    wait_penalties,
    revisit_penalties,
    revisit_max_penalties,
    direction_vector_max_weights,
    direction_vector_multipliers,
    direction_vector_pov_radii,
):
    results = defaultdict(list)
    summary = []

    for max_door_frequency in max_door_frequencies:
        for radius in radii:
            for seed in range(num_maps_per_config):
                for wait_penalty in wait_penalties:
                    for revisit_penalty in revisit_penalties:
                        for revisit_max_penalty in revisit_max_penalties:
                            for (
                                direction_vector_max_weight
                            ) in direction_vector_max_weights:
                                for (
                                    direction_vector_multiplier
                                ) in direction_vector_multipliers:
                                    for (
                                        direction_vector_pov_radius
                                    ) in direction_vector_pov_radii:
                                        args = argparse.Namespace(
                                            max_door_frequency=max_door_frequency,
                                            radius=radius,
                                            seed=seed,
                                            maze=None,
                                            scale=9,
                                            no_gui=True,
                                            log_path=f"logs/mdf{max_door_frequency}_r{radius}_s{seed}.log",
                                            disable_logging=False,
                                            disable_timeout=True,
                                            player="1",
                                            wait_penalty=wait_penalty,
                                            revisit_penalty=revisit_penalty,
                                            revisit_max_penalty=revisit_max_penalty,
                                            direction_vector_max_weight=direction_vector_max_weight,
                                            direction_vector_multiplier=direction_vector_multiplier,
                                            direction_vector_pov_radius=direction_vector_pov_radius,
                                        )

                                        root = tk.Tk()
                                        game = TimingMazeGame(args, root)

                                        start_time = time.time()
                                        try:
                                            game.initialize(None)
                                        finally:
                                            end_time = time.time()
                                            result = {
                                                "turns": game.turns,
                                                "valid_moves": game.valid_moves,
                                                "time_taken": end_time - start_time,
                                                "goal_reached": game.cur_pos[0]
                                                == game.end_pos[0]
                                                and game.cur_pos[1] == game.end_pos[1],
                                            }
                                            # Convert tuple to string for JSON compatibility
                                            results[
                                                f"mdf_{max_door_frequency}_r_{radius}_s_{seed}_wp_{wait_penalty}_rp_{revisit_penalty}_rmp_{revisit_max_penalty}_dw_{direction_vector_max_weight}_dm_{direction_vector_multiplier}_dr_{direction_vector_pov_radius}"
                                            ].append(result)

                                            summary.append(
                                                {
                                                    "max_door_frequency": max_door_frequency,
                                                    "radius": radius,
                                                    "seed": seed,
                                                    "turns": game.turns,
                                                    "goal_reached": result[
                                                        "goal_reached"
                                                    ],
                                                    "wait_penalty": wait_penalty,
                                                    "revisit_penalty": revisit_penalty,
                                                    "revisit_max_penalty": revisit_max_penalty,
                                                    "direction_vector_max_weight": direction_vector_max_weight,
                                                    "direction_vector_multiplier": direction_vector_multiplier,
                                                    "direction_vector_pov_radius": direction_vector_pov_radius,
                                                }
                                            )

    return results, summary
    results = defaultdict(list)
    summary = []

    return results, summary


def save_results(results, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Convert the results to ensure all data is JSON serializable
    cleaned_results = convert_numpy_types(results)

    output_file = os.path.join(output_dir, f"results.json")
    with open(output_file, "w") as f:
        json.dump(cleaned_results, f, indent=2)


def save_summary(summary, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, "simulation_summary.csv")
    with open(output_file, "w") as f:
        f.write(
            "max_door_frequency,radius,seed,turns,goal_reached,wait_penalty,revisit_penalty,revisit_max_penalty,direction_vector_max_weight,direction_vector_multiplier,direction_vector_pov\n"
        )
        for entry in summary:
            f.write(
                f"{entry['max_door_frequency']},{entry['radius']},{entry['seed']},{entry['turns']},{entry['goal_reached']},{entry['wait_penalty']},{entry['revisit_penalty']},{entry['revisit_max_penalty']},{entry['direction_vector_max_weight']},{entry['direction_vector_multiplier']},{entry['direction_vector_pov_radius']}\n"
            )


def convert_numpy_types(data):
    if isinstance(data, np.bool_):
        return bool(data)
    elif isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, dict):
        return {k: convert_numpy_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_types(item) for item in data]
    return data


def main():
    max_door_frequencies = [3]
    radii = [30]
    num_maps_per_config = 1
    wait_penalties = [0.1, 0.15, 0.2, 0.3]
    revisit_penalties = [0.1, 0.15, 0.2, 0.3]
    revisit_max_penalties = [0.5, 0.75, 1, 2, 3]
    direction_vector_max_weights = [0.5, 1, 2, 3]
    direction_vector_multipliers = [0.01, 0.05, 0.1]
    direction_vector_pov_radii = [20, 30, 40]

    output_dir = "simulation_results"

    all_summary = []

    results, summary = run_simulation(
        max_door_frequencies,
        radii,
        num_maps_per_config,
        wait_penalties,
        revisit_penalties,
        revisit_max_penalties,
        direction_vector_max_weights,
        direction_vector_multipliers,
        direction_vector_pov_radii,
    )
    save_results(results, output_dir)
    all_summary.extend(summary)
    print(f"Simulation complete")

    save_summary(all_summary, output_dir)
    print(
        "All simulations completed. Results and summary saved in the 'simulation_results' directory."
    )


if __name__ == "__main__":
    main()

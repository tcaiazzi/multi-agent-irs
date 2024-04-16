import argparse
import json
import os.path
import sys

import numpy as np
from matplotlib import pyplot as plt


def chunk_list(l):
    ll = []
    for i in range(0, len(l), 10):
        sublist = l[i:i + 10]
        ll.append(sublist)

    return ll


def parse_results(path):
    parsed_results = {}
    for algorithm_result in os.listdir(path):
        algorithm = algorithm_result.split(".")[0]
        algorithm_result_path = os.path.join(path, algorithm_result)
        with open(algorithm_result_path, "r") as result_file:
            results = json.load(result_file)

        parsed_results[algorithm] = {}

        ra = results['attacker']
        parsed_results[algorithm]["attacker"] = {}
        for epoch, epoch_results in enumerate(chunk_list(ra)):
            parsed_results[algorithm]["attacker"][epoch] = epoch_results

        rd = results['defender']
        parsed_results[algorithm]["defender"] = {}
        for epoch, epoch_results in enumerate(chunk_list(rd)):
            parsed_results[algorithm]["defender"][epoch] = epoch_results

    return parsed_results


def plot_reward_on_epoch_figure(algorithm: str):
    def plot_reward_on_epoch_curve(role, color, marker):
        to_plot = {'x': [], 'y': [], 'dy': []}
        for epoch, epoch_results in parsed_results[role].items():
            rewards = list(map(lambda x: x[1], epoch_results))
            avg_reward = np.average(rewards)
            to_plot['x'].append(epoch + 1)
            to_plot['y'].append(avg_reward)

        plt.plot(
            to_plot['x'], to_plot['y'], label=role, linestyle='dashed', fillstyle='none', color=color, marker=marker
        )

    parsed_results = parse_results(results_directory)[algorithm]

    fig, ax = plt.subplots(layout='constrained')
    # ax.set_axisbelow(True)
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    # ax.tick_params(axis='both', labelsize=14)

    plot_reward_on_epoch_curve("attacker", "red", "o")
    plot_reward_on_epoch_curve("defender", "blue", "^")

    ax.set_ylabel('Reward', fontsize=14)
    ax.set_xlabel('Epoch', fontsize=14)
    ax.legend(fontsize=14)

    plt.title(f"{algorithm} Training", fontsize=14)
    plt.savefig(os.path.join(figures_directory, f"{algorithm}_reward_epoch.pdf"), format="pdf", bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run IRS training!',
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--training', action='store_true')
    group.add_argument('--evaluation', action='store_true')

    args = parser.parse_args(sys.argv[1:])

    if args.training:
        results_directory = os.path.join("results", "training")
        figures_directory = os.path.join("figures", "training")
    elif args.evaluation:
        results_directory = os.path.join("results", "evaluation")
        figures_directory = os.path.join("figures", "evaluation")

    os.makedirs(figures_directory, exist_ok=True)

    plot_reward_on_epoch_figure("DQN")
    # plot_reward_on_epoch_figure("PPO")
    # plot_reward_on_epoch_figure("PG")

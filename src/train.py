import argparse
import os
import sys

from training.run_training import run_training

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run IRS training!',
    )

    parser.add_argument(
        "--algorithm", "-a",
        required=True
    )

    parser.add_argument(
        "--epoch", "-e",
        type=int,
        required=True
    )

    parser.add_argument(
        "--gamma", "-g",
        type=float,
        required=True
    )

    parser.add_argument(
        "--agents",
        type=int,
        required=True
    )

    parser.add_argument(
        "--att-actions",
        type=int,
        required=True
    )

    parser.add_argument(
        "--k-att",
        type=float,
        required=True
    )

    parser.add_argument(
        "--def-actions",
        type=int,
        required=True
    )

    parser.add_argument(
        "--k-def",
        type=float,
        required=True
    )

    args = parser.parse_args(sys.argv[1:])

    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "results"), exist_ok=True)

    run_training(args.algorithm, args.epoch, args.gamma, args.agents, args.att_actions, args.k_att,
                 args.def_actions, args.k_def)

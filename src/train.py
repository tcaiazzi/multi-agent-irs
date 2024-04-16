import argparse
import os
import sys

from training.run_rsp_training import run_rsp_training

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

    args = parser.parse_args(sys.argv[1:])

    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "results"), exist_ok = True)

    run_rsp_training(args.algorithm, args.epoch, args.gamma)
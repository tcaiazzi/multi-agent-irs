import argparse
import os
import sys

from evaluation.evaluation import evaluate

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run IRS evaluation!',
    )

    parser.add_argument(
        "--algorithm", "-a",
        required=True
    )

    parser.add_argument(
        "--checkpoint", "-c",
        type=str,
        required=True
    )

    args = parser.parse_args(sys.argv[1:])

    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "results", "evaluation"), exist_ok = True)

    evaluate(args.algorithm, args.checkpoint)

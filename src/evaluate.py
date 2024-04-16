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

    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "results", "evaluation"), exist_ok = True)

    evaluate(args.algorithm, args.checkpoint, args.agents, args.att_actions, args.k_att,
                     args.def_actions, args.k_def)

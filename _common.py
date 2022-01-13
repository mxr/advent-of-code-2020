import sys
from argparse import ArgumentParser
from typing import Callable


def main(part1: Callable[[str], int], part2: Callable[[str], int]) -> int:
    parser = ArgumentParser()
    parser.add_argument("-p", "--part", type=int, default=0)
    parser.add_argument(
        "-f", "--filename", type=str, default=sys.argv[0].replace(".py", ".txt")
    )

    args = parser.parse_args()

    part: int = args.part
    filename: str = args.filename

    if (part or 1) == 1:
        print(f"part1: {part1(filename)}")
    if (part or 2) == 2:
        print(f"part2: {part2(filename)}")

    return 0
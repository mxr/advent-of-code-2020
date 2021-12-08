#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import Counter
from typing import List


def parse(filename: str) -> List[int]:
    with open(filename) as f:
        return [int(n) for n in f.read().split(",")]


def execute(filename: str, day: int) -> int:
    starting = parse(filename)

    turns = {n: i + 1 for i, n in enumerate(starting)}
    spoken = Counter(starting)

    prev, curr = starting[-1], -1
    curr = -1
    for i in range(len(starting) + 1, day + 1):
        curr = (i - 1) - turns[prev] if spoken[prev] > 1 else 0

        turns[prev] = i - 1
        spoken[curr] += 1
        prev = curr

    return curr


def part1(filename: str) -> int:
    return execute(filename, 2020)


def part2(filename: str) -> int:
    return execute(filename, 30000000)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("-p", "--part", type=int, default=0)
    parser.add_argument("-f", "--filename", type=str, required=True)

    args = parser.parse_args()

    part: int = args.part
    filename: str = args.filename

    if (part or 1) == 1:
        print(f"part1: {part1(filename)}")
    if (part or 2) == 2:
        print(f"part2: {part2(filename)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

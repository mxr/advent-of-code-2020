#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import Generator
from typing import List
from typing import Tuple


def parse(filename: str) -> Generator[int, None, None]:
    with open(filename) as f:
        for raw in f:
            yield int(raw)


def find(nums: List[int], target: int) -> Tuple[int, int]:
    mapping = {target - n: n for n in nums}
    for n1, n2 in mapping.items():
        if n2 in mapping:
            return n1, n2

    return 0, 0


def part1(filename: str) -> int:
    n1, n2 = find(list(parse(filename)), 2020)

    return n1 * n2


def part2(filename: str) -> int:
    nums = list(parse(filename))
    for i, n in enumerate(nums):
        n1 = 2020 - n
        n2, n3 = find(nums[:i] + nums[i + 1 :], n1)
        if n + n2 + n3 == 2020:
            return n * n2 * n3

    return -1


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

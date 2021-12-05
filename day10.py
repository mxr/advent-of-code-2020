#!/usr/bin/env python3
import functools
from argparse import ArgumentParser
from collections import Counter
from typing import Generator


def parse(filename: str) -> Generator[int, None, None]:
    with open(filename) as f:
        for line in f:
            yield int(line)


def part1(filename: str) -> int:
    nums = [0]  # outlet
    nums.extend(sorted(parse(filename)))
    nums.append(nums[-1] + 3)  # device

    diffs = (nums[i + 1] - nums[i] for i in range(len(nums) - 1))
    counts = Counter(diffs)

    return counts[1] * counts[3]


def part2(filename: str) -> int:
    nums = [0]  # outlet
    nums.extend(sorted(parse(filename)))
    nums.append(nums[-1] + 3)  # device

    @functools.lru_cache(len(nums))
    def count_ways(i: int) -> int:
        if i == len(nums) - 1:
            return 1
        return sum(
            count_ways(j)
            for j in (i + 1, i + 2, i + 3)
            if j < len(nums) and nums[j] - nums[i] <= 3
        )

    return count_ways(0)


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

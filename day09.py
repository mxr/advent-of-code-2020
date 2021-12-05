#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import deque
from typing import Generator
from typing import Iterable
from typing import Tuple


def parse(filename: str) -> Generator[int, None, None]:
    with open(filename) as f:
        for line in f:
            yield int(line)


def part1(filename: str) -> int:
    nums = list(parse(filename))
    preamble = deque(nums[:25])
    for i in range(26, len(nums)):
        n = nums[i]
        m, *_ = find(preamble, n)
        if not m:
            return n

        preamble.popleft()
        preamble.append(n)

    return -1


def find(nums: Iterable[int], target: int) -> Tuple[int, int]:
    mapping = {target - n: n for n in nums}
    for n1, n2 in mapping.items():
        if n2 in mapping:
            return n1, n2

    return 0, 0


def part2(filename: str) -> int:
    target = part1(filename)

    nums = list(parse(filename))

    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s > target:
                break
            elif s == target:
                return min(nums[i : j + 1]) + max(nums[i : j + 1])

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

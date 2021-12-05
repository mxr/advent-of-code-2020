#!/usr/bin/env python3
import functools
import re
from argparse import ArgumentParser
from typing import Generator
from typing import List
from typing import Tuple

RE = re.compile(r"(\d+) (\w+ \w+) bags?")


def parse(filename: str) -> Generator[Tuple[str, List[Tuple[int, str]]], None, None]:
    with open(filename) as f:
        for line in f.readlines():
            first, _, rest = line.partition(" contain ")
            outer = first[: -len(" bags")]
            inner = [(int(n), c) for (n, c) in RE.findall(rest)]
            yield outer, inner


def part1(filename: str) -> int:
    mapping = dict(parse(filename))
    can_contain = 0
    for start in mapping:
        q = [start]
        seen = set()
        while q:
            outer = q.pop()
            if outer in seen:
                continue
            seen.add(outer)
            if outer == "shiny gold":
                can_contain += 1
                break
            else:
                q.extend(color for _, color in mapping[outer])

    return can_contain - 1


def part2(filename: str) -> int:
    mapping = dict(parse(filename))

    @functools.lru_cache(len(mapping))
    def count_bags(color: str) -> int:
        if not mapping[color]:
            return 1
        return 1 + sum(n * count_bags(c) for n, c in mapping[color])

    return count_bags("shiny gold") - 1


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

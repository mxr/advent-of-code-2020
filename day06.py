#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import Generator
from typing import List
from typing import Set


def parse(filename: str) -> Generator[List[Set[str]], None, None]:
    with open(filename) as f:
        for chunk in f.read().split("\n\n"):
            yield [set(c) for c in chunk.split()]


def part1(filename: str) -> int:
    return sum(len(answers[0].union(*answers[1:])) for answers in parse(filename))


def part2(filename: str) -> int:
    return sum(
        len(answers[0].intersection(*answers[1:])) for answers in parse(filename)
    )


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

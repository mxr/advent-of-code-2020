#!/usr/bin/env python3
import re
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Generator
from typing import Tuple

RE = re.compile(r"(\d+)-(\d+)\s+(\w+):\s+(\w+)")


@dataclass
class Validator:
    left: int
    right: int
    char: str

    def valid_part1(self, password: str) -> bool:
        return self.left <= password.count(self.char) <= self.right

    def valid_part2(self, password: str) -> bool:
        # fmt: off
        return (
            (password[self.left - 1] == self.char) !=
            (password[self.right - 1] == self.char)
        )
        # fmt: on


def parse(filename: str) -> Generator[Tuple[Validator, str], None, None]:
    with open(filename) as f:
        for (left, right, char, pw) in RE.findall(f.read()):
            yield Validator(int(left), int(right), char), pw


def part1(filename: str) -> int:
    return sum(v.valid_part1(pw) for v, pw in parse(filename))


def part2(filename: str) -> int:
    return sum(v.valid_part2(pw) for v, pw in parse(filename))


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

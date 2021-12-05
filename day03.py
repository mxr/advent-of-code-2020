#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import List
from typing import NamedTuple


class Land(NamedTuple):
    tree: bool


class Map:
    def __init__(self, grid: List[List[Land]]) -> None:
        self.grid = grid
        self.width, self.height = len(grid[0]), len(grid)

    def traverse(self, col_step: int = 3, row_step: int = 1) -> int:
        i, j, num_trees = 0, 0, 0
        while i < self.height - 1:
            i, j = i + row_step, (j + col_step) % self.width
            num_trees += self.grid[i][j].tree

        return num_trees


def parse(filename: str) -> Map:
    with open(filename) as f:
        grid = [[Land(c == "#") for c in line.strip()] for line in f.readlines()]

    return Map(grid)


def part1(filename: str) -> int:
    return parse(filename).traverse()


def part2(filename: str) -> int:
    m = parse(filename)

    prod = 1
    for cs, rs in (
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ):
        prod *= m.traverse(cs, rs)

    return prod


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

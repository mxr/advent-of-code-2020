#!/usr/bin/env python3
from argparse import ArgumentParser
from typing import Generator
from typing import Tuple


DIRS = ["N", "E", "S", "W"]


class Ship:
    def __init__(self) -> None:
        self.direction = "E"
        self.x, self.y = 0, 0

    def move(self, direction: str, dist: int) -> None:
        if direction == "N":
            self.y -= dist
        elif direction == "S":
            self.y += dist
        elif direction == "W":
            self.x -= dist
        elif direction == "E":
            self.x += dist
        elif direction == "F":
            self.move(self.direction, dist)
        else:
            steps = (-1) ** (direction == "L") * dist // 90
            dir_index = DIRS.index(self.direction)
            new_index = (dir_index + steps) % len(DIRS)
            self.direction = DIRS[new_index]

    def dist(self) -> int:
        return abs(self.x) + abs(self.y)


class ShipWithWaypoint:
    def __init__(self) -> None:
        self.direction = "E"
        self.x, self.y = 0, 0
        self.wx, self.wy = 10, -1  # relative coords

    def move(self, direction: str, dist: int) -> None:
        if direction == "N":
            self.wy -= dist
        elif direction == "S":
            self.wy += dist
        elif direction == "W":
            self.wx -= dist
        elif direction == "E":
            self.wx += dist
        elif direction == "F":
            self.x += self.wx * dist
            self.y += self.wy * dist
        else:
            steps = ((-1) ** (direction == "L") * dist // 90) % len(DIRS)
            if steps == 1 or steps == -3:
                self.wx, self.wy = -self.wy, self.wx
            elif steps == 2 or steps == -2:
                self.wx, self.wy = -self.wx, -self.wy
            elif steps == 3 or steps == -1:
                self.wx, self.wy = self.wy, -self.wx
            else:
                # no movement
                pass

    def dist(self) -> int:
        return abs(self.x) + abs(self.y)


def parse(filename: str) -> Generator[Tuple[str, int], None, None]:
    with open(filename) as f:
        for line in f:
            yield line[0], int(line[1:])


def part1(filename: str) -> int:
    s = Ship()
    for (direction, dist) in parse(filename):
        s.move(direction, dist)

    return s.dist()


def part2(filename: str) -> int:
    s = ShipWithWaypoint()
    for (direction, dist) in parse(filename):
        s.move(direction, dist)

    return s.dist()


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

from __future__ import annotations

from collections import defaultdict
from itertools import product
from typing import Generator
from typing import TypeVar

T = TypeVar("T", "Cubes", "Cubes4D")


class Cubes:
    DELTAS = frozenset(product((-1, 0, 1), repeat=3)) - {(0, 0, 0)}

    def __init__(self, section: list[str]) -> None:
        self.cubes: dict[tuple[int, int, int], str] = defaultdict(lambda: ".")

        self.height, self.width, self.depth = len(section), len(section[0]), 0
        for i, line in enumerate(section):
            for j, c in enumerate(line):
                self.cubes[i, j, 0] = c

    def cycle(self) -> None:
        new_cubes = self.cubes.copy()

        # "all cubes simultaneously change their state"
        # but because state depends on neighbors we can look at a bit
        # beyond the known cubes
        for x in range(self.width // 2 - self.width, self.width // 2 + self.width + 1):
            for y in range(
                self.height // 2 - self.height, self.height // 2 + self.height + 1
            ):
                for z in range(-self.depth - 2, self.depth + 2 + 1):
                    active = self.cubes[x, y, z] == "#"
                    num_active = 0
                    for neighbor in self._neighbors(x, y, z):
                        if neighbor == "#":
                            num_active += 1
                        if num_active > 3:
                            break
                    if active and (num_active != 2 and num_active != 3):
                        new_cubes[x, y, z] = "."
                    elif not active and num_active == 3:
                        new_cubes[x, y, z] = "#"

        self.width += 2
        self.height += 2
        self.depth += 2

        self.cubes = new_cubes

    def count(self) -> int:
        return sum(c == "#" for c in self.cubes.values())

    def _neighbors(self, x: int, y: int, z: int) -> Generator[str, None, None]:
        for xd, yd, zd in self.DELTAS:
            yield self.cubes[x + xd, y + yd, z + zd]


# TODO make Cubes generic instead of copy-pasting
class Cubes4D:
    DELTAS = frozenset(product((-1, 0, 1), repeat=4)) - {(0, 0, 0, 0)}

    def __init__(self, section: list[str]) -> None:
        self.cubes: dict[tuple[int, int, int, int], str] = defaultdict(lambda: ".")

        self.height, self.width, self.depth, self.spiss = (
            len(section),
            len(section[0]),
            0,
            0,
        )
        for i, line in enumerate(section):
            for j, c in enumerate(line):
                self.cubes[i, j, 0, 0] = c

    def cycle(self) -> None:
        new_cubes = self.cubes.copy()

        # "all cubes simultaneously change their state"
        # but because state depends on neighbors we can look at a bit
        # beyond the known cubes
        for x in range(self.width // 2 - self.width, self.width // 2 + self.width + 1):
            for y in range(
                self.height // 2 - self.height, self.height // 2 + self.height + 1
            ):
                for z in range(-self.depth - 2, self.depth + 2 + 1):
                    for w in range(-self.spiss - 2, self.spiss + 2 + 1):
                        active = self.cubes[x, y, z, w] == "#"
                        num_active = 0
                        for neighbor in self._neighbors(x, y, z, w):
                            if neighbor == "#":
                                num_active += 1
                            if num_active > 3:
                                break
                        if active and (num_active != 2 and num_active != 3):
                            new_cubes[x, y, z, w] = "."
                        elif not active and num_active == 3:
                            new_cubes[x, y, z, w] = "#"

        self.width += 2
        self.height += 2
        self.depth += 2
        self.spiss += 2

        self.cubes = new_cubes

    def count(self) -> int:
        return sum(c == "#" for c in self.cubes.values())

    def _neighbors(self, x: int, y: int, z: int, w: int) -> Generator[str, None, None]:
        for xd, yd, zd, wd in self.DELTAS:
            yield self.cubes[x + xd, y + yd, z + zd, w + wd]


def parse(filename: str, cube_type: type[T]) -> T:
    with open(filename) as f:
        cubes = cube_type(f.read().splitlines())

    return cubes


def part1(filename: str) -> int:
    cubes = parse(filename, Cubes)
    for _ in range(6):
        cubes.cycle()
    return cubes.count()


def part2(filename: str) -> int:
    cubes = parse(filename, Cubes4D)
    for _ in range(6):
        cubes.cycle()
    return cubes.count()


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))

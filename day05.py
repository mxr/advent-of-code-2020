#!/usr/bin/env python3
from argparse import ArgumentParser
from itertools import tee
from typing import Generator
from typing import Iterable
from typing import Tuple
from typing import TypeVar

T = TypeVar("T")


def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def parse(filename: str) -> Generator[Tuple[str, str], None, None]:
    with open(filename) as f:
        for raw in f:
            line = raw.strip()
            yield line[:-3], line[-3:]


def part1(filename: str) -> int:
    return max(seat_ids(filename))


def seat_ids(filename: str) -> Generator[int, None, None]:
    return (seat_id(row_enc, col_enc) for row_enc, col_enc in parse(filename))


def seat_id(row_enc: str, col_enc: str) -> int:
    row = binsearch(row_enc, "F")
    col = binsearch(col_enc, "L")

    return row * 8 + col


def binsearch(enc: str, cap_char: str) -> int:
    lo, hi = 0, 2 ** len(enc) - 1
    for c in enc:
        if c == cap_char:
            hi = lo + (hi - lo) // 2
        else:
            lo = lo + (hi - lo) // 2 + 1

    return lo


def part2(filename: str) -> int:
    sids = sorted(seat_ids(filename))
    for c, n in pairwise(sids):
        if n - c == 2:
            return c + 1

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

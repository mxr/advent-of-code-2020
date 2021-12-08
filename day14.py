#!/usr/bin/env python3
import re
from argparse import ArgumentParser
from typing import Generator
from typing import List
from typing import NamedTuple


RE = re.compile(r"mem\[(\d+)\] = (\d+)")


class Command(NamedTuple):
    address: int
    value: int


class MaskCommands(NamedTuple):
    mask: str
    mask0: int
    mask1: int
    commands: List[Command]


def parse(filename: str) -> Generator[MaskCommands, None, None]:
    with open(filename) as f:
        chunks = iter(f.read().strip().split("mask"))
        next(chunks)  # blank line

        for chunk in chunks:
            raw_mask, raw_mems = chunk.split("\n", 1)

            _, _, mask = raw_mask.partition(" = ")
            mask0 = int(mask.translate({ord("X"): "0"}), 2)
            mask1 = int(mask.translate({ord("X"): "1"}), 2)

            commands = [Command(int(a), int(v)) for a, v in RE.findall(raw_mems)]

            yield MaskCommands(mask, mask0, mask1, commands)


def part1(filename: str) -> int:
    memory = {}
    for mc in parse(filename):
        for c in mc.commands:
            memory[c.address] = mc.mask0 | c.value & mc.mask1

    return sum(memory.values())


def part2(filename: str) -> int:
    memory = {}
    for mc in parse(filename):
        for c in mc.commands:
            for addr in gen_addrs(apply(mc.mask, c.address)):
                memory[addr] = c.value

    return sum(memory.values())


def apply(mask: str, address: int) -> str:
    return "".join(
        a if m == "0" else "1" if m == "1" else "X"
        for (m, a) in zip(mask, format(address, "036b"))
    )


def gen_addrs(mask: str) -> Generator[int, None, None]:
    if "X" in mask:
        yield from gen_addrs(mask.replace("X", "0", 1))
        yield from gen_addrs(mask.replace("X", "1", 1))
    else:
        yield int(mask, 2)


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

#!/usr/bin/env python3
import itertools
from argparse import ArgumentParser
from typing import Generator
from typing import List
from typing import NamedTuple
from typing import Tuple


class Instruction(NamedTuple):
    cmd: str
    val: int


def parse(filename: str) -> Generator[Instruction, None, None]:
    with open(filename) as f:
        for line in f:
            name, _, val = line.partition(" ")
            yield Instruction(name, int(val))


def part1(filename: str) -> int:
    instructions = list(parse(filename))
    return execute(instructions)[1]


def execute(instructions: List[Instruction]) -> Tuple[bool, int]:
    seen = set()
    ip, acc = 0, 0
    while ip < len(instructions):
        if ip in seen:
            return True, acc
        seen.add(ip)

        instr = instructions[ip]
        if instr.cmd == "acc":
            acc += instr.val
            ip += 1
        elif instr.cmd == "jmp":
            ip += instr.val
        else:
            ip += 1

    return False, acc


def part2(filename: str) -> int:
    instructions = list(parse(filename))
    for i, instr in enumerate(instructions):
        if instr.cmd == "nop":
            new_cmd = "jmp"
        elif instr.cmd == "jmp":
            new_cmd = "nop"
        else:
            continue

        new_instructions = list(
            itertools.chain(
                instructions[:i],
                (Instruction(new_cmd, instr.val),),
                instructions[i + 1 :],
            )
        )
        dup, acc = execute(new_instructions)
        if not dup:
            return acc

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

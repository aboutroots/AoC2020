from common import file_to_lines
from collections import namedtuple
import itertools


class Decoder:
    def __init__(self, mode=0):
        """Mode 0: decode value, 1: decode addresses"""
        self.mask_one = "".zfill(36)
        self.mask_two = "".zfill(36)
        self.mem = {}
        self.mode = mode

    @staticmethod
    def _parse_row(row):
        Parsed = namedtuple("ParsedRow", "is_mask, value, addr")
        if "mask" in row:
            _, value = row.strip().split(" = ")
            return Parsed(True, value, None)

        mem, value = row.strip().split(" = ")
        mem = mem.strip("mem[]")
        return Parsed(False, value, mem)

    def _decode_value(self, value):
        with_or_mask = value | self.mask_one
        return with_or_mask & self.mask_two

    def _decode_addresses(self, addr):
        with_mask = addr | self.mask_one

        # convert to zero-padded string
        with_mask_as_bits = str(bin(with_mask)).lstrip("0b").zfill(36)
        addresses = []
        x_bit_ids = [index for index, char in enumerate(self.mask_two) if char == "X"]
        # get possible bits combinations
        bit_combinations = list(itertools.product(["0", "1"], repeat=len(x_bit_ids)))

        for comb in bit_combinations:
            a = with_mask_as_bits
            for bit, target_index in zip(comb, x_bit_ids):
                # just a string replacement
                a = a[:target_index] + bit + a[target_index + 1 :]
            addresses.append(a)

        return [int(a, 2) for a in addresses]

    def _compute_value(self, value):
        if self.mode == 0:
            return self._decode_value(value)
        return value

    def _compute_addresses(self, addr):
        if self.mode == 0:
            return [addr]
        return self._decode_addresses(addr)

    def _compute_masks(self, value):
        mask_one = int(value.replace("X", "0"), 2)
        if self.mode == 0:
            mask_two = int(value.replace("X", "1"), 2)
        else:
            mask_two = value
        return mask_one, mask_two

    def compute(self, rows):
        for row in rows:
            parsed = self._parse_row(row)
            if parsed.is_mask:
                mask_one, mask_two = self._compute_masks(parsed.value)
                self.mask_one = mask_one
                self.mask_two = mask_two
            else:
                value = self._compute_value(int(parsed.value))
                addresses = self._compute_addresses(int(parsed.addr))
                for target_addr in addresses:
                    self.mem[target_addr] = value


def first(rows):
    decoder = Decoder(mode=0)
    decoder.compute(rows)
    return sum(decoder.mem.values())


def second(rows):
    decoder = Decoder(mode=1)
    decoder.compute(rows)
    return sum(decoder.mem.values())


def main():
    rows = file_to_lines("inputs/day14.txt")
    print(first(rows))
    print(second(rows))


if __name__ == "__main__":
    main()

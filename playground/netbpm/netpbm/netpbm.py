from collections.abc import Sequence
from enum import IntEnum
from io import TextIOWrapper
from typing import Optional, Tuple


class MagicNumber(IntEnum):
    P1 = 1
    P2 = 2
    P3 = 3


class Netpbm:
    def __init__(
        self,
        magic_number: MagicNumber,
        file: str,
        data: Sequence,
        dimensions: Tuple[int, int],
        max_value: Optional[int] = None,
    ) -> None:
        self.magic_number = magic_number
        self.file = file
        self.data = data
        self.dimensions = dimensions
        self.max_value = max_value

    def write(self) -> Optional[Exception]:
        try:
            with open(self.file, "w") as f:
                self._write_header(f)
                self._write_data(f)
        except Exception as e:
            return e

    def _write_header(self, file: TextIOWrapper) -> None:
        file.write("P%d\n" % self.magic_number)
        file.write("%d %d\n" % self.dimensions)
        match self.magic_number:
            case MagicNumber.P2 | MagicNumber.P3:
                file.write("%d\n" % self.max_value)

    def _write_data(self, file: TextIOWrapper):
        match self.magic_number:
            case MagicNumber.P1 | MagicNumber.P2:
                self._write_matrix(file)
            case MagicNumber.P3:
                self._write_rgb_sequence(file)

    def _write_matrix(self, file: TextIOWrapper):
        _, h = self.dimensions
        for i in range(h):
            file.write("%s\n" % " ".join(str(n) for n in self.data[i]))

    def _write_rgb_sequence(self, file: TextIOWrapper):
        for color in self.data:
            file.write("%d %d %d\n" % color)

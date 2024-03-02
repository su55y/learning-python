from collections.abc import Sequence
from enum import IntEnum
from typing import IO, Any, Optional, Tuple

from .utils import is_onedimensional


class MagicNumber(IntEnum):
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4
    P6 = 6


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
        mode = "w" if self.magic_number < 4 else "wb"
        try:
            with open(self.file, mode) as f:
                if mode == "w":
                    self._write_header(f)
                else:
                    self._write_header_bin(f)
                self._write_data(f)
        except Exception as e:
            return e

    def _write_header(self, file: IO[Any]) -> None:
        file.write("P%d\n" % self.magic_number)
        file.write("%d %d\n" % self.dimensions)
        match self.magic_number:
            case MagicNumber.P2 | MagicNumber.P3:
                file.write("%d\n" % self.max_value)

    def _write_header_bin(self, file: IO[Any]) -> None:
        file.write(("P%d\n" % self.magic_number).encode("ascii"))
        file.write(("%d %d\n" % self.dimensions).encode("ascii"))
        match self.magic_number:
            case MagicNumber.P2 | MagicNumber.P3 | MagicNumber.P6:
                file.write(("%d\n" % self.max_value).encode("ascii"))

    def _write_data(self, file: IO[Any]):
        match self.magic_number:
            case MagicNumber.P1 | MagicNumber.P2:
                self._write_matrix(file)
            case MagicNumber.P3:
                self._write_rgb_sequence(file)
            case MagicNumber.P4:
                self._write_sequence_bin(file)
            case MagicNumber.P6:
                self._write_rgb_sequence_bin(file)

    def _write_matrix(self, file: IO[Any]):
        for row in self.data:
            file.write("%s\n" % " ".join(str(n) for n in row))

    def _write_rgb_sequence(self, file: IO[Any]):
        for color in self.data:
            file.write("%d %d %d\n" % color)

    def _write_rgb_sequence_bin(self, file: IO[Any]):
        file.write(self.data)
        # for color in self.data:
        #     file.write(color)

    def _write_sequence_bin(self, file: IO[Any]):
        if isinstance(self.data, bytearray):
            file.write(self.data)
            return
        assert isinstance(self.data, Sequence), "data should be sequence"
        assert (
            is_onedimensional(self.data) == True
        ), "only singledimensional sequence allowed"
        assert max(self.data) == 1, "max value allowed is 1"
        assert min(self.data) == 0, "min value allowed is 0"
        byte_groups = (self.data[i : i + 8] for i in range(0, len(self.data), 8))
        data = bytearray()
        for group in byte_groups:
            byte = 0
            for i, bit in enumerate(group):
                byte |= bit << (7 - i)
            data.append(byte)
        file.write(data)

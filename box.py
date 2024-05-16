from typing import List, Optional, Tuple

class Box:
    ALL_BOXES: List["Box"] = []
    BOXES_DONE = 0

    def __init__(self, y: int, x: int):
        self.idx: Tuple[int, int] = (y, x)
        self._top: Optional[str] = None
        self._bottom: Optional[str] = None
        self._left: Optional[str] = None
        self._right: Optional[str] = None
        self.sides: int = 0
        self.color: Optional[str] = None

        Box.ALL_BOXES.append(self)

    def top_idx(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.idx, (self.idx[0], self.idx[1] + 1)

    def bottom_idx(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return (self.idx[0] + 1, self.idx[1]), (self.idx[0] + 1, self.idx[1] + 1)

    def left_idx(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.idx, (self.idx[0] + 1, self.idx[1])

    def right_idx(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return (self.idx[0], self.idx[1] + 1), (self.idx[0] + 1, self.idx[1] + 1)

    @property
    def top(self) -> Optional[str]:
        return self._top

    @top.setter
    def top(self, top: str):
        self._top = top
        self.sides += 1
        if self.sides == 4:
            self.color = top
            Box.BOXES_DONE += 1

    @property
    def bottom(self) -> Optional[str]:
        return self._bottom

    @bottom.setter
    def bottom(self, bottom: str):
        self._bottom = bottom
        self.sides += 1
        if self.sides == 4:
            self.color = bottom
            Box.BOXES_DONE += 1

    @property
    def left(self) -> Optional[str]:
        return self._left

    @left.setter
    def left(self, left: str):
        self._left = left
        self.sides += 1
        if self.sides == 4:
            self.color = left
            Box.BOXES_DONE += 1

    @property
    def right(self) -> Optional[str]:
        return self._right

    @right.setter
    def right(self, right: str):
        self._right = right
        self.sides += 1
        if self.sides == 4:
            self.color = right
            Box.BOXES_DONE += 1

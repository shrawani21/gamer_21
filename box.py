from typing import List

class Box:
    # Class variable to store all instances of Box
    ALL_BOXES: List["Box"] = []
    # Class variable to keep track of the number of completed boxes
    BOXES_DONE = 0

    def __init__(self, y, x):
        # Initialize the box with its coordinates (y, x)
        self.idx = y, x
        # Initialize the surrounding edges of the box
        self._top = None
        self._bottom = None
        self._left = None
        self._right = None
        # Initialize the number of sides completed (edges drawn)
        self.sides = 0
        # Initialize the color of the completed box (None if incomplete)
        self.color = None

        # Add the newly created box instance to the list of all boxes
        Box.ALL_BOXES.append(self)

    # Method to get the indices of the top edge of the box
    def top_idx(self):
        return self.idx, (self.idx[0], self.idx[1] + 1)

    # Method to get the indices of the bottom edge of the box
    def bottom_idx(self):
        return (self.idx[0] + 1, self.idx[1]), (self.idx[0] + 1, self.idx[1] + 1)

    # Method to get the indices of the left edge of the box
    def left_idx(self):
        return self.idx, (self.idx[0] + 1, self.idx[1])

    # Method to get the indices of the right edge of the box
    def right_idx(self):
        return (self.idx[0], self.idx[1] + 1), (self.idx[0] + 1, self.idx[1] + 1)

    # Getter method for the top edge of the box
    @property
    def top(self):
        return self._top

    # Setter method for the top edge of the box
    @top.setter
    def top(self, top):
        self._top = top
        # Increment the number of completed sides
        self.sides += 1
        # If all sides are completed, set the color of the box and increment the completed boxes count
        if self.sides == 4:
            self.color = top
            Box.BOXES_DONE += 1

    # Getter method for the bottom edge of the box
    @property
    def bottom(self):
        return self._bottom

    # Setter method for the bottom edge of the box
    @bottom.setter
    def bottom(self, bottom):
        self._bottom = bottom
        # Increment the number of completed sides
        self.sides += 1
        # If all sides are completed, set the color of the box and increment the completed boxes count
        if self.sides == 4:
            self.color = bottom
            Box.BOXES_DONE += 1

    # Getter method for the left edge of the box
    @property
    def left(self):
        return self._left

    # Setter method for the left edge of the box
    @left.setter
    def left(self, left):
        self._left = left
        # Increment the number of completed sides
        self.sides += 1
        # If all sides are completed, set the color of the box and increment the completed boxes count
        if self.sides == 4:
            self.color = left
            Box.BOXES_DONE += 1

    # Getter method for the right edge of the box
    @property
    def right(self):
        return self._right

    # Setter method for the right edge of the box
    @right.setter
    def right(self, right):
        self._right = right
        # Increment the number of completed sides
        self.sides += 1
        # If all sides are completed, set the color of the box and increment the completed boxes count
        if self.sides == 4:
            self.color = right
            Box.BOXES_DONE += 1

# Importing required modules
import random
from box import Box
from typing import List

# Function to determine boxes affected by a line
def line_boxes(mat, line) -> List[Box]:
    # Taking the endpoints of the line
    p1, p2 = line
    boxes = []
    # Checking if the line is horizontal
    if p1[0] == p2[0]:
        pos1 = min(p1, p2, key=lambda x: x[1])
        if pos1[0] > 0:
            box_top = mat[pos1[0] - 1][pos1[1]]
            boxes.append(box_top)
        if pos1[0] < len(mat):
            box_bottom = mat[pos1[0]][pos1[1]]
            boxes.append(box_bottom)
    else:
        pos1 = min(p1, p2, key=lambda x: x[0])
        if pos1[1] > 0:
            box_left = mat[pos1[0]][pos1[1] - 1]
            boxes.append(box_left)
        if pos1[1] < len(mat[0]):
            box_right = mat[pos1[0]][pos1[1]]
            boxes.append(box_right)
    return boxes

# Function to get the surrounding boxes of the given box
def get_boxes_around(box_mat, box: Box):
    boxes = {'top': None, 'bottom': None, 'left': None, 'right': None}
    if box.idx[0] > 0:
        boxes['top'] = box_mat[box.idx[0] - 1][box.idx[1]]
    if box.idx[0] < len(box_mat) - 1:
        boxes['bottom'] = box_mat[box.idx[0] + 1][box.idx[1]]
    if box.idx[1] > 0:
        boxes['left'] = box_mat[box.idx[0]][box.idx[1] - 1]
    if box.idx[1] < len(box_mat[0]) - 1:
        boxes['right'] = box_mat[box.idx[0]][box.idx[1] + 1]
    return boxes

# Function to count surrounding boxes of the given box
def num_boxes_around(box_mat, box: Box):
    count = 0
    if box.idx[0] > 0:
        count += 1
    if box.idx[0] < len(box_mat) - 1:
        count += 1
    if box.idx[1] > 0:
        count += 1
    if box.idx[1] < len(box_mat[0]) - 1:
        count += 1
    return count

# Function to get an empty side of a box
def get_empty(box):
    if box.top is None:
        return box.top_idx()
    elif box.bottom is None:
        return box.bottom_idx()
    elif box.left is None:
        return box.left_idx()
    else:
        return box.right_idx()

# Function to get a random empty side of a box, excluding a specific index
def get_rand_empty(box, exclude=None):
    choices = []
    if box.top is None:
        if exclude is None or box.top_idx() != exclude:
            choices.append(box.top_idx())
    if box.bottom is None:
        if exclude is None or box.bottom_idx() != exclude:
            choices.append(box.bottom_idx())
    if box.left is None:
        if exclude is None or box.left_idx() != exclude:
            choices.append(box.left_idx())
    if box.right is None:
        if exclude is None or box.right_idx() != exclude:
            choices.append(box.right_idx())
    return random.choice(choices)

# Function to get the sides of surrounding boxes of the given box
def get_sides_box(box_mat, box: Box):
    sides = {'top': None, 'bottom': None, 'left': None, 'right': None}
    if box.idx[0] > 0:
        sides['top'] = box_mat[box.idx[0] - 1][box.idx[1]].sides
    if box.idx[0] < len(box_mat) - 1:
        sides['bottom'] = box_mat[box.idx[0] + 1][box.idx[1]].sides
    if box.idx[1] > 0:
        sides['left'] = box_mat[box.idx[0]][box.idx[1] - 1].sides
    if box.idx[1] < len(box_mat[0]) - 1:
        sides['right'] = box_mat[box.idx[0]][box.idx[1] + 1].sides
    return sides

# Function to check if a box has less than a certain number of sides for a given side
def less_than_sides(box_mat, box: Box, side, num):
    sides = get_sides_box(box_mat, box)[side]
    if side == 'top' and box.top is not None:
        return False
    if side == 'bottom' and box.bottom is not None:
        return False
    if side == 'left' and box.left is not None:
        return False
    if side == 'right' and box.right is not None:
        return False
    if sides is None:
        return True
    return sides < num

# Function to check if a box is facing outward
def facing_out(box_mat, box: Box):
    if box.idx[0] == 0 and box.top is None:
        return True
    if box.idx[0] == len(box_mat) - 1 and box.bottom is None:
        return True
    if box.idx[1] == 0 and box.left is None:
        return True
    if box.idx[1] == len(box_mat[0]) - 1 and box.right is None:
        return True
    return False

# Function to determine the AI's move in the game for the difficulty level "easy" 
def easy(box_mat, prev_line):
    if prev_line is not None:
        prev_boxes = line_boxes(box_mat, prev_line)
        for prev_box in prev_boxes:
            if prev_box.sides == 3:
                return get_rand_empty(prev_box)
    boxes = Box.ALL_BOXES
    box0 = list(filter(lambda x: x.sides == 0, boxes))
    box1 = list(filter(lambda x: x.sides == 1, boxes))
    box2 = list(filter(lambda x: x.sides == 2, boxes))
    box3 = list(filter(lambda x: x.sides == 3, boxes))
    if box3:
        return get_rand_empty(random.choice(box3))
    if box0:
        return get_rand_empty(random.choice(box0))
    if box1:
        return get_rand_empty(random.choice(box1))
    if box2:
        return get_rand_empty(random.choice(box2))

# Function to determine the AI's move in the game for the difficulty level "medium" 
def medium(box_mat, prev_line):
    if prev_line is not None:
        prev_boxes = line_boxes(box_mat, prev_line)
        for prev_box in prev

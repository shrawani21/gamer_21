import random
from typing import List, Dict, Optional
from box import Box

def get_line_boxes(matrix: List[List[Box]], line: List[tuple[int, int]]) -> List[Box]:
    """Returns the boxes adjacent to a given line."""
    p1, p2 = line
    boxes = []
    if p1[0] == p2[0]:  # horizontal
        pos1 = min(p1, p2, key=lambda x: x[1])
        if pos1[0] > 0:
            box_top = matrix[pos1[0] - 1][pos1[1]]
            boxes.append(box_top)
        if pos1[0] < len(matrix):
            box_bottom = matrix[pos1[0]][pos1[1]]
            boxes.append(box_bottom)
    else:  # vertical
        pos1 = min(p1, p2, key=lambda x: x[0])
        if pos1[1] > 0:
            box_left = matrix[pos1[0]][pos1[1] - 1]
            boxes.append(box_left)
        if pos1[1] < len(matrix[0]):
            box_right = matrix[pos1[0]][pos1[1]]
            boxes.append(box_right)
    return boxes

def get_adjacent_boxes(matrix: List[List[Box]], box: Box) -> Dict[str, Optional[Box]]:
    """Returns the boxes adjacent to a given box."""
    boxes = {'top': None, 'bottom': None, 'left': None, 'right': None}
    if box.idx[0] > 0:
        boxes['top'] = matrix[box.idx[0] - 1][box.idx[1]]
    if box.idx[0] < len(matrix) - 1:
        boxes['bottom'] = matrix[box.idx[0] + 1][box.idx[1]]
    if box.idx[1] > 0:
        boxes['left'] = matrix[box.idx[0]][box.idx[1] - 1]
    if box.idx[1] < len(matrix[0]) - 1:
        boxes['right'] = matrix[box.idx[0]][box.idx[1] + 1]
    return boxes

def count_adjacent_boxes(matrix: List[List[Box]], box: Box) -> int:
    """Returns the number of adjacent boxes around a given box."""
    count = 0
    if box.idx[0] > 0:
        count += 1
    if box.idx[0] < len(matrix) - 1:
        count += 1
    if box.idx[1] > 0:
        count += 1
    if box.idx[1] < len(matrix[0]) - 1:
        count += 1
    return count

def get_random_empty_side(box: Box, exclude: Optional[tuple[int, int]] = None) -> Optional[tuple[int, int]]:
    """Returns a random empty side of a given box."""
    choices = []
    if box.top is None and (exclude is None or box.top_idx() != exclude):
        choices.append(box.top_idx())
    if box.bottom is None and (exclude is None or box.bottom_idx() != exclude):
        choices.append(box.bottom_idx())
    if box.left is None and (exclude is None or box.left_idx() != exclude):
        choices.append(box.left_idx())
    if box.right is None and (exclude is None or box.right_idx() != exclude):
        choices.append(box.right_idx())
    return random.choice(choices) if choices else None

def get_side_counts(matrix: List[List[Box]], box: Box) -> Dict[str, Optional[int]]:
    """Returns the number of sides occupied around a given box."""
    sides = {'top': None, 'bottom': None, 'left': None, 'right': None}
    if box.idx[0] > 0:
        sides['top'] = matrix[box.idx[0] - 1][box.idx[1]].sides
    if box.idx[0] < len(matrix) - 1:
        sides['bottom'] = matrix[box.idx[0] + 1][box.idx[1]].sides
    if box.idx[1] > 0:
        sides['left'] = matrix[box.idx[0]][box.idx[1] - 1].sides
    if box.idx[1] < len(matrix[0]) - 1:
        sides['right'] = matrix[box.idx[0]][box.idx[1] + 1].sides
    return sides

def is_side_less_than(matrix: List[List[Box]], box: Box, side: str, num: int) -> bool:
    """Checks if the sides around a given box are less than a specified number."""
    sides = get_side_counts(matrix, box)[side]
    return sides is None or sides < num

def is_facing_outside(matrix: List[List[Box]], box: Box) -> bool:
    """Checks if a given box is facing the outside of the matrix."""
    if box.idx[0] == 0 and box.top is None:
        return True
    if box.idx[0] == len(matrix) - 1 and box.bottom is None:
        return True
    if box.idx[1] == 0 and box.left is None:
        return True
    if box.idx[1] == len(matrix[0]) - 1 and box.right is None:
        return True
    return False

def easy_strategy(matrix: List[List[Box]], prev_line: Optional[List[tuple[int, int]]]) -> Optional[tuple[int, int]]:
    """Returns a move for easy difficulty."""
    if prev_line:
        for prev_box in get_line_boxes(matrix, prev_line):
            if prev_box.sides == 3:
                return get_random_empty_side(prev_box)

    boxes = Box.ALL_BOXES
    box0 = [box for box in boxes if box.sides == 0]
    box1 = [box for box in boxes if box.sides == 1]
    box2 = [box for box in boxes if box.sides == 2]
    box3 = [box for box in boxes if box.sides == 3]

    if box3:
        return get_random_empty_side(random.choice(box3))
    if box0:
        return get_random_empty_side(random.choice(box0))
    if box1:
        return get_random_empty_side(random.choice(box1))
    if box2:
        return get_random_empty_side(random.choice(box2))

def medium_strategy(matrix: List[List[Box]], prev_line: Optional[List[tuple[int, int]]]) -> Optional[tuple[int, int]]:
    """Returns a move for medium difficulty."""
    if prev_line:
        for prev_box in get_line_boxes(matrix, prev_line):
            if prev_box.sides == 3:
                return get_random_empty_side(prev_box)

    boxes = Box.ALL_BOXES
    box0 = [box for box in boxes if box.sides == 0]
    box1 = [box for box in boxes if box.sides == 1]
    box2 = [box for box in boxes if box.sides == 2]
    box3 = [box for box in boxes if box.sides == 3]

    box_less2 = box0 + box1

    if box3:
        return get_random_empty_side(random.choice(box3))

    sides_to_check = ['top', 'bottom', 'left', 'right']
    choices = []
    for side in sides_to_check:
        choices.extend([
            getattr(box, f"{side}_idx")()
            for box in box_less2 if is_side_less_than(matrix, box, side, 2)
        ])
    if choices:
        return random.choice(choices)

    if box0:
        return get_random_empty_side(random.choice(box0))
    if box1:
        return get_random_empty_side(random.choice(box1))
    if box2:
        return get_random_empty_side(random.choice(box2))

def hard_strategy(matrix: List[List[Box]], prev_line: Optional[List[tuple[int, int]]]) -> Optional[tuple[int, int]]:
    """Returns a move for hard difficulty."""
    if prev_line:
        for prev_box in get_line_boxes(matrix, prev_line):
            if prev_box.sides == 3:
                return get_random_empty_side(prev_box)

    boxes = Box.ALL_BOXES
    box0 = [box for box in boxes if box.sides == 0]
    box1 = [box for box in boxes if box.sides == 1]
    box3 = [box for box in boxes if box.sides == 3]

    if box3:
        return get_random_empty_side(random.choice(box3))

    box_less2 = box0 + box1

    sides_to_check = ['top', 'bottom', 'left', 'right']
    choices = []
    for side in sides_to_check:
        choices.extend([
            getattr(box, f"{side}_idx")()
            for box in box_less2 if is_side_less_than(matrix, box, side, 2)
        ])
    if choices:
        return random.choice(choices)

    chains = []
    checked = []
    crosses = []
    options = boxes.copy()
    while len(checked) < len(boxes):
        current = [options[0]]
        if current[0].color is not None:
            checked.append(current[0])
            options.remove(current[0])
            continue
        if current[0].sides < 2:
            crosses.append(current[0])
            checked.append(current[0])
            options.remove(current[0])
            continue
        new_chain = []
        chain = []
        while current:
            for box in current:
                checked.append(box)
                chain.append(box)
                options.remove(box)
                for direction in ['top', 'bottom', 'left', 'right']:
                    adj_box = get_adjacent_boxes(matrix, box)[direction]
                    if getattr(box, direction) is None and adj_box and adj_box not in new_chain and adj_box not in chain:
                        if adj_box.sides >= 2:
                            new_chain.append(adj_box)
            current = new_chain
            new_chain = []
        chains.append(chain)

    sorted_chains = sorted(chains, key=len)
    if sorted_chains:
        return get_random_empty_side(random.choice(sorted_chains[0]))

    return get_random_empty_side(random.choice(crosses))

def extreme_strategy(matrix: List[List[Box]], prev_line: Optional[List[tuple[int, int]]]) -> Optional[tuple[int, int]]:
    """Returns a move for extreme difficulty."""
    boxes = Box.ALL_BOXES
    box0 = [box for box in boxes if box.sides == 0]
    box1 = [box for box in boxes if box.sides == 1]
    box3 = [box for box in boxes if box.sides == 3]

    box_less2 = box0 + box1

    sides_to_check = ['top', 'bottom', 'left', 'right']
    choices = []
    for side in sides_to_check:
        choices.extend([
            getattr(box, f"{side}_idx")()
            for box in box_less2 if is_side_less_than(matrix, box, side, 2)
        ])

    chains = []
    checked = []
    crosses = []
    options = boxes.copy()
    while len(checked) < len(boxes):
        current = [options[0]]
        if current[0].color is not None:
            checked.append(current[0])
            options.remove(current[0])
            continue
        if current[0].sides < 2:
            crosses.append(current[0])
            checked.append(current[0])
            options.remove(current[0])
            continue
        new_chain = []
        chain = []
        while current:
            for box in current:
                checked.append(box)
                chain.append(box)
                options.remove(box)
                for direction in ['top', 'bottom', 'left', 'right']:
                    adj_box = get_adjacent_boxes(matrix, box)[direction]
                    if getattr(box, direction) is None and adj_box and adj_box not in new_chain and adj_box not in chain:
                        if adj_box.sides >= 2:
                            new_chain.append(adj_box)
            current = new_chain
            new_chain = []
        chains.append(chain)

    sorted_chains = sorted(chains, key=len)

    if prev_line:
        for prev_box in get_line_boxes(matrix, prev_line):
            if prev_box.sides == 3:
                side = get_random_empty_side(prev_box)
                if not choices and len(sorted_chains) > 1:
                    if len(sorted_chains[1]) > 2 and len(box3) < 2:
                        side_boxes = get_line_boxes(matrix, side)
                        for box in side_boxes:
                            if box != prev_box and count_adjacent_boxes(matrix, box) < 4 and is_facing_outside(matrix, box):
                                return get_random_empty_side(box, exclude=side)
                return side

    if box3:
        selected_box = random.choice(box3)
        side = get_random_empty_side(selected_box)
        if not choices and len(sorted_chains) > 1:
            if len(sorted_chains[1]) > 2 and len(box3) < 2:
                side_boxes = get_line_boxes(matrix, side)
                for box in side_boxes:
                    if box != selected_box and count_adjacent_boxes(matrix, box) < 4 and is_facing_outside(matrix, box):
                        return get_random_empty_side(box, exclude=side)
        return side

    if choices:
        return random.choice(choices)

    if sorted_chains:
        return get_random_empty_side(random.choice(sorted_chains[0]))

    return get_random_empty_side(random.choice(crosses))

def expert_strategy(matrix: List[List[Box]], prev_line: Optional[List[tuple[int, int]]]) -> Optional[tuple[int, int]]:
    """Returns a move for expert difficulty. (To be implemented)"""
    pass

class Player:
    def __init__(self, player_type: str, color: str, difficulty: int = 1):
        self.player_type = player_type
        self.score = 0
        self.color = color
        self.move = None
        self.difficulty = difficulty

    def get_move(self, matrix: List[List[Box]], prev_line: Optional[List[tuple[int, int]]]) -> Optional[tuple[int, int]]:
        if self.player_type == 'human':
            move = self.move
            self.move = None
            return move

        strategy_funcs = {
            1: easy_strategy,
            2: medium_strategy,
            3: hard_strategy,
            4: extreme_strategy,
            5: expert_strategy  # Placeholder for future implementation
        }
        return strategy_funcs[self.difficulty](matrix, prev_line)

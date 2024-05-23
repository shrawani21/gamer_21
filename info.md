# GAME FUNCTION INFORMATION

### Grid Initialization:
A matrix of Box objects is created, each with properties for its sides and color.

### Drawing the Grid:
draw_grid function renders the grid of boxes with their current state (sides and color).

### Handling Box Clicks:
get_clicked_box function determines which box was clicked based on mouse position.
increment_side function increments the sides of the box and the adjacent box.

### Player Class:
Represents a player (human or AI) with properties for player type, color, and difficulty.
make_move method for making a move; human players make moves based on mouse clicks, while AI players can be extended with different strategies.

### Main Game Loop:
Handles player turns, updates the grid based on moves, and switches to the next player.


### Future Enhancements
Implement AI strategies in make_move method.
Add more sides and capturing logic.
Improve player customization and menu interfaces.
Enhance the visual representation and animations.

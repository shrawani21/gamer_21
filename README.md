Here's the corrected and updated README.md:

**"Dots and Boxes"** or **"The Dot Game"**

**Objective:**

Drawing lines on a grid to conquer it is the aim of the game. Players must draw one line at each turn. If after these four, a square is completed, a player gets an extra point and takes another turn. The participant having accumulated the highest number of squares wins.

**Components:**

1. Grid: This game is played with dots in rows and columns. Every dot represents where one can end up with their line.

2. Lines: A player has to link dots using lines to make their sides of squares. These strokes run either horizontally or vertically but connect two adjoining dots.

3. Squares: On drawing the fourth side of a square by making a line complete it, that square gets “captured” by a player who puts his sign (X or O) there.

4. Scoreboard: It records players' scores at different times, usually on one side of the grid.

**Gameplay:**

1. Starting the Game: The grid begins empty and without any dots.

2. Taking Turns: As participants take their turns they do this by drawing lines between two adjacent dots that don’t share a pre-existing line and are straight(either vertical or horizontal)

3. Completing Squares: When a player draws a line and this makes the fourth side of a square, they have captured that square. The symbol inside this square shows that it belongs to them.

4. Earning Points: A player earns one point and takes an additional turn when he/she captures a square. The process continues until all squares are captured.

5. Ending the Game: The game ends as soon as all possible lines have been drawn and no more squares can be claimed by any player. It is important to note that the winner has the most number of squares (points).

**Implementation:**

There are dots on a grid; players take turns drawing lines on it. Once a player completes a square, their symbol is put in it, and they have earned one point. The game concludes after every square has been taken, with the highest scorer being declared as the overall winner.

**Additional Features:**

- Pygame should provide a graphical representation of grids and lines in your implementation
- It keeps track of each player’s score which is displayed on the screen
- There should be a resetting option for restarting the game and quitting
- Visual feedback is provided whenever a player's owns a box

**Some Potential Enhancements:**

- We may improve our AI for single-player mode.
- For a more interesting user experience, we could put in sound effects or animations.
- Additionally, one can add a multiplayer mode where players can compete locally or online.
- Moreover, the game can be made more engaging by allowing customization of grid size and difficulty levels.


**Installation:**
1. Clone the repository to your local machine:
   ```
   git clone https://github.com/shrawani21/gamer_21.git
   ```
2. Navigate to the project directory:
   ```
   cd gamer_21
   ```
3. Install dependencies/requirements:
   ```
   pip install -r requirements.txt
   ```
   or
   ```
   pip install pygame
   ```
4. Run the Game:
   ```
   python main.py
   ```
   This will launch the game!

**Credits:**
- This project is based on the classic Dot and Boxes game.
- Developed using Python only.

**Contributing:**
1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure the tests pass.
4. Submit a pull request for review.

**License:**
- This project is licensed under the MIT License - see the LICENSE file for details.
```


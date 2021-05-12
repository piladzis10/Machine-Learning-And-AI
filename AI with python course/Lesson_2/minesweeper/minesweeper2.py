import itertools
import random

class Minesweeper:

    def __init__(self, height = 8, width = 8, mines = 8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly

        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i,j))
                self.board[i][j] = True

        # Player have not found any mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self,cell):
        i,j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0]- 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i,j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = cells
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        self.cells.remove(cell)
        self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.cells.remove(cell)

class MinesweeperAI:

    def __init__(self, height = 8, width = 8):
        self.height = 8
        self.width = 8

        # Keep track of cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mine
        self.mines = set()
        self.safes = set()

        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """

        self.mines.add(cell)
        if self.knowledge is not None:
            for sentence in self.knowledge:
                sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        if self.knowledge is not None:
            for sentence in self.knowledge:
                sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        self.moves_made.add(cell)

        self.safes.add(cell)

        cells = set()
        for i in range(-1,2):
            for j in range(-1,2):
                if 0 <= cell[0] + i < self.height and 0 <= cell[1] + j < self.width:
                    if not all([i == 0, j == 0]) and (i,j) not in self.mines and (i,j) not in self.safes and  not in self.moves_made:
                        cells.add((cell[0] + i,cell[1] + j))
        sentence = Sentence(cells, count)

        self.knowledge.append(sentence)

        # Check if can mark cells as safe or mines
        for sentance in self.knowledge:
            if len(sentance.cells) == sentance.count:
                for cell in sentance.cells:
                    self.mines.add(cell)
            elif sentance.count == 0:
                for cell in sentance.cells:
                    self.safes.add(cell)

        # Check if can conclude new sentances

        for sentance in self.knowledge:
            for sentance2 in self.knowledge:
                if sentance.cells != sentance2.cells:
                    if sentance2.cells in sentance.cells:
                        cells = set()
                        for c in sentance.cells:
                            if c not in sentance2.cells:
                                cells.add(c)
                        count = sentance.count - sentance2.count
                        self.knowledge.append(Sentence(cells, count))    


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) != 0:
            for cell in self.safes:
                if cell not in self.moves_made:
                    return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.width):
            for j in range(self.height):
                while True:
                    h = random.randint(0, self.width)
                    w = random.randint(0, self.height)
                    if (h,w) not in self.moves_made and (h,w) not in self.mines:
                        return (h,w)

        
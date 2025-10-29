import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

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
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
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

    def is_mine(self, cell):
        i, j = cell
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
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
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
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def empty(self):
        if len(self.cells) < 1:
            return True
        return False

    def known_mines(self):
        if self.count == len(self.cells):
                return copy.deepcopy(self.cells)
        return set()
        # selfMines = set()
        # for cell in self.cells:
        #     if cell in mines:
        #         selfMines.add(cell)
        #         self.count -= 1
        # self.cells.difference_update(selfMines)
        
        """
        Returns the set of all cells in self.cells known to be mines.
        """
       # raise NotImplementedError

    def known_safes(self):
        if self.count == 0:
            return copy.deepcopy(self.cells)
        return set()
        # knownSafes = set()
        # if self.count == 0:
        #     for cell in list(self.cells):
        #         knownSafes.add(cell)
        # return knownSafes
        # selfSafes = set()
        # for cell in self.cells :
        #     if cell in safes:
        #         selfSafes.add(cell)
        # self.cells.difference_update(selfSafes)
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #raise NotImplementedError

    def mark_mine(self, cell):
        #self.cells.remove(cell)
        # newcells = copy.deepcopy(cells)
        # sentenceSize = len(self.cells)
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1

        # if len(self.cells) < sentenceSize:
        #     self.count -= (sentenceSize - len(self.cells))

        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

    def mark_safe(self, cell):
        #self.cells.remove(cell)
        # newcells = copy.deepcopy(cells)
        if cell in self.cells:
            self.cells.remove(cell)
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    # def cellCount(self,cell):
    #     i,j = cell
    #     count = 0
    #     for r in range(-1,2):
    #         for c in range(-1,2):
    #             if r==0 and c==0 :
    #                 continue
    #             else:
    #                 if (i+r,j+c) in self.mines:
    #                     count+=1
    #     return count

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        # try:
        if not cell in self.mines:
            self.mines.add(cell)
        # except(TypeError):
        #     self.mines.update(cell)

        for sentence in list(self.knowledge):
            if cell in sentence.cells:
                sentence.mark_mine(cell)
            # if sentence.empty():
            #     self.knowledge.remove(sentence)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # try:
        if not cell in self.safes:
            self.safes.add(cell)
        # except(TypeError):
        #     self.safes.update(cell)

        for sentence in list(self.knowledge):
            if cell in sentence.cells:
                sentence.mark_safe(cell)
            # if sentence.empty():
            #     self.knowledge.remove(sentence)
        

    def add_knowledge(self, cell, count):


        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        neighbors = set()
        i, j = cell
        for r in range(-1, 2):
            for c in range(-1, 2):
                if r == 0 and c == 0:
                    continue
                ni, nj = i + r, j + c
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    neighbors.add((ni, nj))

        # Remove known mines and safes from neighbors
        new_cells = neighbors.copy()
        new_count = count
        for ncell in neighbors:
            if ncell in self.mines:
                new_cells.remove(ncell)
                new_count -= 1
            elif ncell in self.safes:
                new_cells.remove(ncell)

        # Add new sentence if it has unknown cells
        if len(new_cells) > 0:
            new_sentence = Sentence(new_cells, new_count)
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)

        # 4 & 5) Keep applying inference until no new information is found
        updated = True
        while updated:
            updated = False

            # Mark known mines and safes
            for sentence in list(self.knowledge):
                for cell in sentence.known_mines():
                    if cell not in self.mines:
                        self.mark_mine(cell)
                        updated = True
                for cell in sentence.known_safes():
                    if cell not in self.safes:
                        self.mark_safe(cell)
                        updated = True

            # Remove empty sentences
            self.knowledge = [s for s in self.knowledge if not s.empty()]

            # Infer new sentences from subsets
            new_sentences = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 != s2 and s2.cells.issubset(s1.cells):
                        inferred = Sentence(s1.cells - s2.cells, s1.count - s2.count)
                        if inferred not in self.knowledge and not inferred.empty():
                            new_sentences.append(inferred)
                            updated = True
            self.knowledge.extend(new_sentences)

                        


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if not cell in self.moves_made:
                # self.add_knowledge(cell,count)
                return cell
        
        return None


        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        cells = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    cells.add((i,j))

        for cell in cells:
            # self.add_knowledge(cell,self.cellCount(cell))
            return random.choice(list(cells))
        
        return None
        raise NotImplementedError

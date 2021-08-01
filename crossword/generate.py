import sys
import pdb

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        copy_domains = self.domains.copy()
        for domain in copy_domains.items():
            values = domain[1].copy()
            for value in values:
                if domain[0].length != len(value):
                    self.domains[domain[0]].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlaps = self.crossword.overlaps[x,y]

        revised = False
        if overlaps is None:
            return revised

        var_x_index = overlaps[0]
        var_y_index = overlaps[1]
        var_x_values = self.domains[x].copy()
        var_y_values = self.domains[y].copy()
        
        for x_value in var_x_values:
            var_x_char = x_value[var_x_index]

            match_found = False
            for y_value in var_y_values:
                var_y_char = y_value[var_y_index]

                if var_y_char == var_x_char:
                    match_found = True

            if not match_found:
                self.domains[x].remove(x_value)
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.

        queue = all arcs in csp
        while queue not empty
        (X,Y) = DEQUEUE(queue)
        if REVISE(csp, X,Y):
            if size of X.domain == 0:
                return False
            for each Z in X.neighbors - {Y}:
                ENQUEUE(queue, (Z,X))
        return True
        """
        if arcs is None:
            arcs = list({ k:v for k,v in self.crossword.overlaps.items() if v is not None }.keys())

        while arcs:
            arc = arcs.pop(0)
            X = arc[0]
            Y = arc[1]
            if self.revise(X, Y):
                if self.domains[X] == 0:
                    return False
                for Z in self.crossword.neighbors(X) - {Y}:
                    arcs.append((Z, X))

            return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check for duplicates
        values = assignment.values()
        if len(values) != len(set(values)):
            return False
        
        for item in assignment.items():
            variable = item[0]
            value = item[1]
            
            # Check lengths
            if variable.length != len(value):
                return False

            # Check overlaps are valid
            neighbors = self.crossword.neighbors(variable)
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[variable, neighbor]
                if neighbor in assignment:
                    if value[overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False

        return True

    def order_domain_values(self, variable, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.

        get values of var
        get neighbors of var
        filter out already assigned neighbors

        func(value, neighbors, variable)
            n = 0
            for each neighbor of var:
                get overlap between neighbor and var
                for each value of neighbor:
                    get char at index of overlap for var
                    get char at index of overlap for neighbor
                    if != increment n by 1

            return n
        """
        def sort_by_lcv(value, neighbors, variable):
            n = 0
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[variable, neighbor]
                neighbor_values = self.domains[neighbor]
                for neighbor_value in neighbor_values:
                    if value[overlap[0]] != neighbor_value[overlap[1]]:
                        n += 1
        
            return n

        values = self.domains[variable]
        neighbors = self.crossword.neighbors(variable)
        assignment_copy = assignment.copy()
        unassigned_neighbors = neighbors - set(assignment_copy)
        return sorted(values, key=lambda value: sort_by_lcv(value, unassigned_neighbors, variable))


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        remaining = self.crossword.variables - set(assignment)
        return remaining.pop()

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.

        function BACKTRACK(assignment):
            if assignment complete: return assignment
            var = SELECT-UNASSIGNED-VAR(assignment)
            for value in DOMAIN-VALUE(var, assignment)
            if value consistent with assignment:
                add { var = value } to assignment
                result = BACKTRACK(assignment)
                if result != failure: return result
            remove { var = value } from assignment
        return failure
        """
        if self.assignment_complete(assignment):
            return assignment
        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            assignment[variable] = value

            # neighbors = self.crossword.neighbors(variable)
            # arcs = []
            # for neighbor in neighbors:
            #     arcs.append((neighbor, variable))
            # self.ac3(arcs=arcs)

            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result: 
                    return result
            del assignment[variable]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

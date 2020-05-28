from random import randrange
import re
import math
import string

BOARD_SIZE = 4
class Game:
    def __init__(self):
        self.fields = []
        for x in range(BOARD_SIZE):
            self.fields.append([])
            for y in range(BOARD_SIZE):
                self.fields[x].append(Field(x, y, randrange(1, 6)))

    def play(self):
        fromField = get_field_input("Enter the gem you want to move (e.g A1): ")
        toField = get_field_input("Enter a new destination for the gem: ")

        self.move(fromField, toField)

    def move(self, fromField, toField):
        if self.check_move(fromField, toField):
            if self.check_board(fromField, toField):
                print(f"Valid move from {fromField} to {toField}")
            else:
                print(f"Invalid move from {fromField} to {toField}")
        else:
            print(f"Invalid move from {fromField} to {toField}")

    def check_move(self, fromField, toField):
        if fromField == toField:
            print("The fields to be exchanged cannot be identical")
            return False
        
        fromCol = convert_str_to_int(fromField[0])
        fromRow = int(fromField[1])

        toCol = convert_str_to_int(toField[0])
        toRow = int(toField[1])

        if math.fabs(fromCol - toCol) > 1 or math.fabs(fromRow - toRow) > 1:
            print("The two fields to be exchanged have to be adjacent")
            return False
        elif math.fabs(fromCol - toCol) == 1 and math.fabs(fromRow - toRow) == 1:
            print("The fields to be exchanged have to be vertically or horizontally adjacent")
            return False
        else:
            return True

    def check_row(self, toField, fromField):
        # Check row
        legalRow = True
        inARow = 0
        col = toField.x
        rows =[]
        for field in self.fields[col]:

            if not field.y == toField.y:
                if field.color == fromField.color:
                    rows.append(field.y)
                    inARow += 1
                elif not field.color == fromField.color and inARow < 2:
                    inARow = 0

        if inARow < 2:
            rows = []
            legalRow = False

        return [legalRow, rows]

    def check_col(self, fromField, toField):
        row = toField.y
        #Check col
        legalCol = True
        inARow = 0

        cols = []
        for col in self.fields:
            field = col[row]

            if not field.x == toField.x:
                if field.color == fromField.color:
                    cols.append(field.x)
                    inARow += 1
                elif not field.color == fromField.color and inARow < 2:
                    inARow = 0
                    
        if inARow < 2:
            legalCol = False
            cols = []
        
        return [legalCol, cols]

    def check_board(self, fromCoords, toCoords):
        fromField = convert_coords_to_field(self, fromCoords)
        toField = convert_coords_to_field(self, toCoords)
        if fromField.color == toField.color:
            print("You cannot exchange two identical gems")
            return False
        
        row = toField.y
        col = toField.x

        tmp = self.check_row(toField, fromField)
        legalRow = tmp[0]
        rows = tmp[1]

        tmp = self.check_col(fromField, toField)
        legalCol = tmp[0]
        cols = tmp[1]

        for i in rows:
            self.check_row()

        if legalCol and legalRow:
            print("Bomb found")

        return legalCol or legalRow

    def __repr__(self):
        title_row = "    "
        divider = "  |"
        for i in range(BOARD_SIZE):
            title_row += f"{string.ascii_uppercase[i]}   "
            divider += "----"
        divider = divider[:-1]
        divider += "|\n"
        title_row += "\n"
        board = title_row + divider
        for i in reversed(range(BOARD_SIZE)):
            row = f"{i+1} |"
            for j in range(BOARD_SIZE):
                row += f" {self.fields[j][i].color} |"
            row += "\n"
            board += row
            board += divider
        return board
class Field:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.coords = f"{string.ascii_uppercase[x]}{y+1}"

    def __repr__(self):
        return f"({self.x}, {self.y}): {self.color}"



def get_field_input(question):
    field = input(question)

    if (field[0] in string.ascii_uppercase[:BOARD_SIZE] or field[0] in string.ascii_lowercase[:BOARD_SIZE]) and int(field[1]) in range(1, BOARD_SIZE+1):
        return field
    else:
        print(f"Please enter a valid field (A1 - {string.ascii_uppercase[BOARD_SIZE-1]}{BOARD_SIZE})")
        return get_field_input(question)

def convert_str_to_int(str):
    fields = {}
    for i in range(BOARD_SIZE):
        fields[string.ascii_lowercase[i]] = i+1
    
    return fields[str.lower()]

def convert_coords_to_field(board, coords):
    x = int(convert_str_to_int(coords[0]))
    y = int(coords[1])
    return board.fields[x-1][y-1]

if __name__ == "__main__":
    game = Game()
    print(game)
    game.play()
    
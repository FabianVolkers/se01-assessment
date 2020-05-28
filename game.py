from random import randrange
import re
import math

class Game:
    def __init__(self):
        self.fields = []
        for x in range(3):
            self.fields.append([])
            for y in range(3):
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
        
    def check_board(self, fromCoords, toCoords):
        fromField = convert_coords_to_field(self, fromCoords)
        toField = convert_coords_to_field(self, toCoords)
        if fromField.color == toField.color:
            print("You cannnot exchange two identical gems")
            return False
        
        row = toField.y
        col = toField.x

        # Check row
        legalRow = True

        for field in self.fields[col]:
            if not field.y == toField.y:
                if field.color == fromField.color:
                    continue
                else:
                    legalRow = False

        #Check col
        legalCol = True
        
        for col in self.fields:
            field = col[row]
            if not field.x == toField.x:
                if field.color == fromField.color:
                    continue
                else:
                    legalCol = False

        return legalCol or legalRow

    def __repr__(self):
        return f"""
    A   B   C 
  |-----------|
3 | {self.fields[0][2].color} | {self.fields[1][2].color} | {self.fields[2][2].color} |
  |-----------|
2 | {self.fields[0][1].color} | {self.fields[1][1].color} | {self.fields[2][1].color} |
  |-----------|
1 | {self.fields[0][0].color} | {self.fields[1][0].color} | {self.fields[2][0].color} |
  |-----------|
        """
class Field:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        return f"({self.x}, {self.y}): {self.color}"



def get_field_input(question):
    field = input(question)
    field_regex = r"^[A-Ca-c]{1}[1-3]{1}$"
    if re.search(field_regex, field):
        return field
    else:
        print("Please enter a valid field (A1 - C3)")
        return get_field_input(question)

def convert_str_to_int(str):
    fields = {
        "a": 1,
        "b": 2,
        "c": 3
    }
    return fields[str.lower()]

def convert_coords_to_field(board, coords):
    x = int(convert_str_to_int(coords[0]))
    y = int(coords[1])
    return board.fields[x-1][y-1]

if __name__ == "__main__":
    game = Game()
    print(game)
    game.play()
    
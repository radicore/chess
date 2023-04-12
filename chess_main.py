import json
import re
import os

posA = [1, 2, 3, 4, 5, 6, 7, 8]
posB = ["a", "b", "c", "d", "e", "f", "g", "h"]
metadata = {}
for num in posA:
    for letter in posB:
        if (num == 1 or num == 8) and (letter == "a" or letter == "h"):
            t = ["Castle"]
            if num == 8:
                t.append("Black")
            else:
                t.append("White")
            t.append(5)
            metadata[(letter + str(num))] = t
        elif (num == 1 or num == 8) and (letter == "b" or letter == "g"):
            t = ["Horse"]
            if num == 8:
                t.append("Black")
            else:
                t.append("White")
            t.append(3)
            metadata[(letter + str(num))] = t
        elif (num == 1 or num == 8) and (letter == "c" or letter == "f"):
            t = ["Bishop"]
            if num == 8:
                t.append("Black")
            else:
                t.append("White")
            t.append(3)
            metadata[(letter + str(num))] = t
        elif (num == 1 or num == 8) and (letter == "d"):
            t = ["Queen"]
            if num == 8:
                t.append("Black")
            else:
                t.append("White")
            t.append(9)
            metadata[(letter + str(num))] = t
        elif (num == 1 or num == 8) and (letter == "e"):
            t = ["King"]
            if num == 8:
                t.append("Black")
            else:
                t.append("White")
            t.append(None)
            metadata[(letter + str(num))] = t
        elif num == 2 or num == 7:
            t = ["Pawn"]
            if num == 7:
                t.append("Black")
            else:
                t.append("White")
            t.append(True)
            t.append(1)
            metadata[(letter + str(num))] = t
        else:
            metadata[(letter + str(num))] = [None, "Neutral"]


# print(metadata)


class Chess:
    def __init__(self):
        self.can_flip = False
        self.metadata = metadata
        self.PawnDoubleMove = True
        self.Checkmate = False
        self.Play_AI = False
        self.loaded = False
        self.flip = False
        self.ThrowawayBool = True
        self.game_name = ""

    def meta_to_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        for pos, data in self.metadata.items():
            x = ord(pos[0]) - ord('a')
            y = int(pos[1]) - 1
            board[y][x] = data
        if not self.flip:
            chess_board = board[::-1]
        else:
            chess_board = board
        for i in range(8):
            row = ""
            for j in range(8):
                if chess_board[i][j][0]:
                    row += f"{chess_board[i][j][1][0]}{chess_board[i][j][0][0]} "
                else:
                    row += "〇 "  # 〇
            row = row.replace("WC", "♜").replace("WH", "♞").replace("WB", "♝").replace("WQ", "♛").replace("WK",
                                                                                                          "♚").replace(
                "WP", "♟")
            row = row.replace("BC", "♖").replace("BH", "♘").replace("BB", "♗").replace("BQ", "♕").replace("BK",
                                                                                                          "♔").replace(
                "BP", "♙")
            print(row)

    @staticmethod
    def colour_switch(z):
        return z[0] + str(list(reversed(posA)).index(int(z[1])) + 1)

    def start_game(self):
        # self.evaluateMoves()
        while not self.loaded:
            file_name = input("Type file name or 'new' for a NEW game: ")
            file_name = file_name.lower()
            if file_name != "new":
                try:
                    self.metadata = self.load_game(file_name)
                    self.loaded = True
                    self.game_name = file_name
                except FileNotFoundError or AttributeError:
                    print("\nIncorrect file name / attr error!\n")
            else:
                print("\nCreated game!\n")
                self.game_name = f"saved_{self.check_number()}"
                open(f"cache/saved_{self.check_number()}.json", "w").write(json.dumps(self.metadata))
                self.loaded = True

        """
        ai = input("Play an AI (y/n): ")
        ai = ai.lower()
        if ai in ["yes", "y"]:
            self.Play_AI = True
        """

        if self.ThrowawayBool:
            self.meta_to_board()
            self.ThrowawayBool = False

        position = input("Move: ")  # input("Move pos to pos (e.g. A1 A4): ")
        try:
            if position == "b":
                self.meta_to_board()
            elif position == "q":
                self.save_game(self.game_name)
                quit()
            else:
                e = position.lower()
                print(len(e))
                e = re.sub("[^\w ]", "", e)
                e = e.split(" ")
                if len(position) == 2:
                    try:
                        print(self.metadata[e[0]])
                    except KeyError:
                        print("Invalid Position!")
                elif len(position) > 5:
                    print("There can only be 2 pairs of a VALID length of 2 when grid referencing!")
                else:
                    c = e[0]
                    d = e[1]
                    if not self.flip and self.can_flip:
                        print("Board flipped")
                        self.flip = True
                        self.can_flip = False
                        c, d = self.colour_switch(e[0]), self.colour_switch(e[1])
                        print(c, d)
                        (a, b) = self.rule_check(c, d)
                    else:
                        (a, b) = self.rule_check(e[0], e[1])
                    if a:
                        self.move(c, d)
                        self.meta_to_board()
                        self.save_game(self.game_name)
        except KeyError:
            print("IndexError occurred - incorrect key")

    def save_game(self, file_name):  # code to save the game state in a json file
        open(f"cache/{file_name}.json", "w").write(json.dumps(self.metadata))
        print("\nCache saved!\n")

    def load_game(self, file_name):  # code to load a previously saved game in a json file
        try:
            self.game_name = file_name
            print("\nCache loaded!\n")
            return json.load(open(f"cache/{file_name}.json", "r"))
        except AttributeError:
            print("Invalid filename!")
            return False

    @staticmethod
    def check_number():
        files = str(len([entry for entry in os.listdir("cache") if os.path.isfile(os.path.join("cache", entry))]))
        with open("GAME_NUMBER.txt", "w") as f:
            if open("GAME_NUMBER.txt", "r").read() != files:
                f.write(files)

        return files

    def move(self, old, new):  # move the specified piece if rule check has been satisfied
        print(self.item_check(old), "moved to position", new)
        self.metadata[new] = self.metadata[old]
        self.metadata[old] = [None, "Neutral"]

    def colour_check(self, old, new):  # code to check if a colour is valid
        if self.metadata[old][1] != self.metadata[new][1]:
            return True
        else:
            return False

    def item_check(self, pos):  # code to check the items name
        # try:
        return self.metadata[pos][0]
        # except IndexError:  # keyError

        # print("KeyError: Invalid position.")

    @staticmethod
    def distance_check(x, y):  # code to check the distance between two items
        if x >= y:
            result = x - y
        else:
            result = y - x
        return result

    def capture_piece(self, old, new):
        def new_not_neutral(name):
            if self.item_check(new) is not None:
                return True, f"{name} took " + self.item_check(new)
            else:
                return False, None

        if self.item_check(old) == "Pawn":
            if new_not_neutral("Pawn")[0]:
                return new_not_neutral("Pawn")
        elif self.item_check(old) == "Castle":
            if new_not_neutral("Castle")[0]:
                return new_not_neutral("Castle")
        elif self.item_check(old) == "Horse":
            if new_not_neutral("Horse")[0]:
                return new_not_neutral("Horse")
        elif self.item_check(old) == "Bishop":
            if new_not_neutral("Bishop")[0]:
                return new_not_neutral("Bishop")

        elif self.item_check(old) == "Queen":
            if new_not_neutral("Queen")[0]:
                return
        elif self.item_check(old) == "King":
            if new_not_neutral("Pawn")[0]:
                return new_not_neutral("Pawn")

    def rule_check(self, old, new):  # code to check if a move is within the games parameters
        rv, item = False, None
        if old == new:
            rv, item = False, self.item_check(old)
            print("Tried to move to the same position!")
            return rv, item
        if self.item_check(old) == "Pawn" and self.colour_check(old, new):
            if old[0] == new[0] and int(new[1]) > 0:  # checks if position (e.g. a1 a3) have the same letters
                if self.metadata[old][2] and self.distance_check(int(old[1]), int(new[1])) in (1, 2):
                    rv, item = True, "Pawn"
                    self.metadata[old][2] = False
                elif not self.metadata[old][2] and self.distance_check(int(old[1]), int(new[1])) == 1:
                    rv, item = True, "Pawn"
                    self.metadata[old][2] = False
                else:
                    print("Pawn attempted to move more than 1 or 2 spaces!")
                    rv, item = False, "Pawn"
            else:
                print("Pawn cannot move diagonally!")
                rv, item = False, "Pawn"

        elif self.item_check(old) == "Castle" and self.colour_check(old, new):
            # Check if move is horizontal
            if old[0] == new[0]:
                # Check for obstructions and occupied squares
                m = self.distance_check(int(old[1]), int(new[1]))
                for n in range(1, m):
                    if (int(old[1])) < 9 and self.item_check((old[0] + str(int(old[1])))) is not None:
                        print("MOVE ERROR: Obstruction!")
                        return False, "Castle"
                if self.item_check(new) is None:
                    return True, "Castle"
                else:
                    print("MOVE ERROR: position occupied!")
                    return False, "Castle"
            # Check if move is vertical
            elif old[1] == new[1]:
                # Check for obstructions and occupied squares
                m = self.distance_check((posB.index(old[0])), posB.index(new[0]))
                for n in range(1, m):
                    if self.item_check((posB[n - 1 + posB.index(old[0])] + str(old[1]))) is not None:
                        print("MOVE ERROR: Obstruction!")
                        return False, "Castle"
                if self.item_check(new) is None:
                    return True, "Castle"
                else:
                    print("MOVE ERROR: position occupied!")
                    return False, "Castle"
            else:
                print("MOVE ERROR: illegal move!")
                return False, "Castle"

            # castle in a1 moving to a5 - check for only empty cells between
        elif self.item_check(old) == "Horse" and self.colour_check(old, new):

            x_distance = self.distance_check(posB.index(old[0]), posB.index(new[0]))
            y_distance = self.distance_check(int(old[1]), int(new[1]))

            if x_distance == 2 and y_distance == 1:
                rv, item = True, "Horse"
            elif x_distance == 1 and y_distance == 2:
                rv, item = True, "Horse"
            else:
                rv, item = False, "Horse"

        elif self.item_check(old) == "Bishop" and self.colour_check(old, new):
            x_distance = self.distance_check(posB.index(old[0]), posB.index(new[0]))
            y_distance = self.distance_check(int(old[1]), int(new[1]))
            i = 0
            if x_distance == y_distance:
                for n in range(x_distance):
                    if posB.index(old[0]) < posB.index(new[0]):
                        if (int(old[1]) + n) < 9:
                            if self.item_check((posB[posB.index(old[0]) + n] + str(int(old[1]) + n))) is None:
                                i += 1
                    else:
                        if n <= posB.index(old[0]) and (int(old[1]) - n) > 0:
                            print(str(int(old[1]) - n))
                            if self.item_check((posB[posB.index(old[0]) - n] + str(int(old[1]) - n))) is None:
                                i += 1
                if i == x_distance:
                    rv, item = True, "Bishop"
                else:
                    print("MOVE ERROR: Obstruction!")
                    rv, item = False, "Bishop"
            else:
                print("MOVE ERROR: Bishop can only move diagonally!")
                rv, item = False, "Bishop"

        elif self.item_check(old) == "Queen" and self.colour_check(old, new):
            x_distance = self.distance_check(posB.index(old[0]), posB.index(new[0]))
            y_distance = self.distance_check(int(old[1]), int(new[1]))
            if x_distance == y_distance:
                i = 0
                for n in range(x_distance):
                    if posB.index(old[0]) < posB.index(new[0]):
                        if (int(old[1]) + n) < 9:
                            if self.item_check((posB[posB.index(old[0]) + n] + str(int(old[1]) + n))) is None:
                                i += 1
                    else:
                        if n <= posB.index(old[0]) and (int(old[1]) - n) > 0:
                            if self.item_check((posB[posB.index(old[0]) - n] + str(int(old[1]) - n))) is None:
                                i += 1
                if i == x_distance:
                    rv, item = True, "Queen"
                else:
                    print("MOVE ERROR: Obstruction!")
                    rv, item = False, "Queen"
            elif old[0] == new[0] or old[1] == new[1]:
                i = 0
                if old[0] == new[0]:
                    m = self.distance_check(int(old[1]), int(new[1]))
                    for n in range(m + 1):
                        if self.item_check((old[0] + str(n + 1))) is None:
                            i += 1
                else:
                    m = self.distance_check((posB.index(old[0])), posB.index(new[0]))
                    for n in range(m + 1):
                        if self.item_check((posB[n] + str(old[1]))) is None:
                            i += 1
                if i == m:
                    rv, item = True, "Queen"
                else:
                    print("MOVE ERROR: Obstruction!")
                    rv, item = False, "Queen"
            else:
                print("MOVE ERROR: Queen can only move diagonally or in a straight line!")
                rv, item = False, "Queen"
        elif self.item_check(old) == "King" and self.colour_check(old, new):
            x_distance = self.distance_check(posB.index(old[0]), posB.index(new[0]))
            y_distance = self.distance_check(int(old[1]), int(new[1]))

            if x_distance <= 1 and y_distance <= 1:
                rv, item = True, "King"
            else:
                print("MOVE ERROR: King can only move one square in any direction!")
                rv, item = False, "King"

        elif self.item_check(old) is None:
            print("Attempted to move an empty cell?!")
        else:
            print("Error: position is incorrect OR/AND occupied by the same colour!")
        self.can_flip, self.flip = rv, not rv
        return rv, item

    def evaluateMoves(self):
        possible_moves = []
        occupied_positions = []
        all_positions = [i2+str(i) for i in posA for i2 in posB]

        for i in posA:
            for i2 in posB:
                if self.item_check(i2 + str(i)) is not None:
                    occupied_positions.append((i2 + str(i)))

        for old in occupied_positions:
            for new in all_positions:
                if self.rule_check(old, new)[0]:
                    possible_moves.append(f"{old} {new}")

        print(possible_moves)


        """
                        for i3 in posA:
                    for i4 in posB:
                        old = i2 + str(i)
                        new = i4 + str(i3)
                        if old != new:
                            print(old, new)
                            if self.rule_check(old, new)[0]:
                                possible_moves.append(new)
                                """

        """if self.item_check(old) == "Pawn":
            pass
        elif self.item_check(old) == "Castle":
            pass
        elif self.item_check(old) == "Horse":
            pass
        elif self.item_check(old) == "Bishop":
            pass
        elif self.item_check(old) == "Queen":
            pass
        elif self.item_check(old) == "King":
            pass"""

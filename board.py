from pieces import PieceInfo


class Board:
    def __init__(self, fen):
        self.board = [[PieceInfo.empty for _ in range(8)] for _ in range(8)]

        sections = fen.split(" ")
        x = 0
        y = 0
        for c in sections[0]:
            if c == "/":
                y += 1
                x = 0
            elif c.isdigit():
                x += int(c)
            else:
                piece = PieceInfo.symbol_to_type(c) + PieceInfo.symbol_to_color(c)
                self.board[x][y] = piece
                x += 1

    def move_piece(self, start, target):
        piece = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = PieceInfo.empty
        self.board[target[0]][target[1]] = piece
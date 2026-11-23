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

        self.white_to_move = (sections[1] == "w")
        self.move_color = PieceInfo.white if self.white_to_move else PieceInfo.black

        self.white_castle_kingside = "K" in sections[2]
        self.white_castle_queenside = "Q" in sections[2]
        self.black_castle_kingside = "k" in sections[2]
        self.black_castle_queenside = "q" in sections[2]

    def move_piece(self, piece, start, target):
        self.board[start[0]][start[1]] = PieceInfo.empty
        self.board[target[0]][target[1]] = piece

    def make_move(self, start_pos, target_pos):
        piece = self.board[start_pos[0]][start_pos[1]]

        target_x, target_y = target_pos

        self.move_piece(piece, start_pos, target_pos)

        if PieceInfo.get_type(piece) == PieceInfo.king and abs(self.start_pos[0] - self.target_pos[0]) >= 2:
            kingside = target_x == 6
            rook_start = (target_x + 1, target_y) if kingside else (target_x - 2, target_y)
            rook_target = (target_x - 1, target_y) if kingside else (target_x + 1, target_y)

            rook = self.board[rook_start[0]][rook_start[1]]
            self.move_piece(rook, rook_start, rook_target)

        self.update_castling_rights(piece, start_pos, target_pos)

        self.white_to_move = not self.white_to_move
        self.move_color = PieceInfo.white if self.white_to_move else PieceInfo.black

    def update_castling_rights(self, piece, start_pos, target_pos):
        if PieceInfo.get_type(piece) == PieceInfo.king:
            if self.white_to_move:
                self.white_castle_kingside = False
                self.white_castle_queenside = False
            else:
                self.black_castle_kingside = False
                self.black_castle_queenside = False

        h1 = (7, 7)
        a1 = (0, 7)
        h8 = (7, 0)
        a8 = (0, 0)
        if target_pos == h1 or start_pos == h1:
            self.white_castle_kingside = False
        if target_pos == a1 or start_pos == a1:
            self.white_castle_queenside = False
        if target_pos == h8 or start_pos == h8:
            self.black_castle_kingside = False
        if target_pos == a8 or start_pos == a8:
            self.black_castle_queenside = False
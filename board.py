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

        captured_piece = self.board[target_x][target_y]
        self.move_piece(piece, start_pos, target_pos)

        if PieceInfo.get_type(piece) == PieceInfo.king and abs(start_pos[0] - target_pos[0]) >= 2:
            kingside = target_x == 6
            rook_start = (target_x + 1, target_y) if kingside else (target_x - 2, target_y)
            rook_target = (target_x - 1, target_y) if kingside else (target_x + 1, target_y)

            rook = self.board[rook_start[0]][rook_start[1]]
            self.move_piece(rook, rook_start, rook_target)

        return captured_piece

    def unmake_move(self, start_pos, target_pos, captured_piece):
        moved_piece = self.board[target_pos[0]][target_pos[1]]

        self.move_piece(moved_piece, target_pos, start_pos)

        capture_square_x, capture_square_y = target_pos

        self.board[capture_square_x][capture_square_y] = captured_piece

        if PieceInfo.get_type(moved_piece) == PieceInfo.king and abs(start_pos[0] - target_pos[0]) >= 2:
            target_x, target_y = target_pos
            kingside = target_x == 6
            rook_start = (target_x + 1, target_y) if kingside else (target_x - 2, target_y)
            rook_target = (target_x - 1, target_y) if kingside else (target_x + 1, target_y)
            rook = self.board[rook_target[0]][rook_target[1]]
            self.move_piece(rook, rook_target, rook_start)

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

    def change_turn(self):
        self.white_to_move = not self.white_to_move
        self.move_color = PieceInfo.white if self.white_to_move else PieceInfo.black

    def get_threats(self):
        enemy_moves = []
        color = PieceInfo.opponent_color(self.move_color)

        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if PieceInfo.get_color(piece) == color:
                    enemy_moves += PieceInfo.get_valid_moves(piece, self.board, x, y)

        return enemy_moves

    def search_king(self):
        piece = PieceInfo.king + self.move_color
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == piece:
                    return (x, y)
        return None

    def get_piece_moves(self, x, y):
        piece = self.board[x][y]

        if PieceInfo.get_color(piece) != self.move_color:
            return []

        valid_targets = PieceInfo.get_valid_moves(piece, self.board, x, y)

        valid_moves = []
        for target in valid_targets:
            captured_piece = self.make_move((x, y), target)

            king_pos = self.search_king()
            if king_pos not in self.get_threats():
                valid_moves.append(target)

            self.unmake_move((x, y), target, captured_piece)


        if PieceInfo.get_type(piece) == PieceInfo.king:
            enemy_threats = self.get_threats()
            if (x, y) not in enemy_threats:
                castle_kingside = (self.move_color == PieceInfo.white and self.white_castle_kingside) or (self.move_color == PieceInfo.black and self.black_castle_kingside)
                if castle_kingside:
                    if not any((self.board[col][y] != PieceInfo.empty or (col, y) in enemy_threats) for col in range(x + 1, 7)):
                        valid_moves.append((6, y))

                castle_queenside = (self.move_color == PieceInfo.white and self.white_castle_queenside) or (self.move_color == PieceInfo.black and self.black_castle_queenside)
                if castle_queenside:
                    if not any((self.board[col][y] != PieceInfo.empty or (col, y) in enemy_threats) for col in range(x - 1, 1, -1)) and self.board[1][y] == PieceInfo.empty:
                        valid_moves.append((2, y))

        return valid_moves
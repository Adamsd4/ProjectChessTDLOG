from board import Board
from pieces import PieceInfo


def draw(plt, moves = None):
    for x in range(8):
        for y in range(8):
            piece = plt[y][x]
            if moves is not None and (y, x) in moves:
                print(".", end=" ")
            else:
                print(PieceInfo.get_symbol(piece), end=" ")
        print()


if __name__ == "__main__":
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq")

    while True:
        draw(board.board)

        x1 = int(input("start_pos x : "))
        y1 = int(input("start_pos y : "))
        while PieceInfo.get_color(board.board[x1][y1]) != board.move_color:
            x1 = int(input("start_pos x : "))
            y1 = int(input("start_pos y : "))

        valid_moves = board.get_piece_moves(x1, y1)

        draw(board.board, valid_moves)

        x2 = int(input("target_pos x : "))
        y2 = int(input("target_pos y : "))
        while (x2, y2) not in valid_moves:
            x2 = int(input("target_pos x : "))
            y2 = int(input("target_pos y : "))

        board.make_move((x1, y1), (x2, y2))
        board.update_castling_rights(board.board[x2][y2], (x1, y1), (x2, y2))
        board.change_turn()

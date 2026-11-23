from board import Board
from pieces import PieceInfo


def draw(plt):
    for x in range(8):
        for y in range(8):
            piece = plt[y][x]
            print(PieceInfo.get_symbol(piece), end=" ")
        print()


if __name__ == "__main__":
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

    while True:
        draw(board.board)

        x1 = int(input("start_pos x : "))
        y1 = int(input("start_pos y : "))

        x2 = int(input("target_pos x : "))
        y2 = int(input("target_pos y : "))

        board.move_piece((x1, y1), (x2, y2))

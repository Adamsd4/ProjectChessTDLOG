class PieceInfo:
    white = 8
    black = 16

    empty =  0
    pawn = 1
    knight = 2
    bishop = 3
    rook = 4
    queen = 5
    king = 6

    symbol_to_type_dict = {"p": pawn, "n": knight, "b": bishop, "r": rook, "q": queen, "k": king, "_": empty}
    type_to_symbol_dict = {pawn: "p", knight: "n", bishop: "b", rook: "r", queen: "q", king: "k", empty: "_"}

    @staticmethod
    def get_color(piece:int):
        return piece - (piece % 8)

    @staticmethod
    def get_type(piece: int):
        return piece % 8

    @staticmethod
    def symbol_to_color(piece:str) -> int:
        return PieceInfo.white if piece.isupper() else PieceInfo.black

    @staticmethod
    def symbol_to_type(piece:str) -> int:
        return PieceInfo.symbol_to_type_dict[piece.lower()]

    @staticmethod
    def get_symbol(piece: int) -> str:
        piece_char = PieceInfo.type_to_symbol_dict[PieceInfo.get_type(piece)]
        return piece_char if PieceInfo.get_color(piece) == PieceInfo.black else piece_char.upper()
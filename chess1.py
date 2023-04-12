from chess_handler import Chess

chess = Chess()

checkmate = chess.Checkmate

while not checkmate:
    chess.start_game()

from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)


def minimax(position, depth, alpha, beta, max_player, game):
    #base case
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position

    if max_player:
        # Maximizing player moves to maximize score
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            # Recursively call minimax for the child node
            evaluation = minimax(move, depth - 1, alpha, beta, False, game)[0]
            # Update maxEval with the maximum score found
            maxEval = max(maxEval, evaluation)
            # Update alpha (the best score the maximizer can guarantee at that level or above)
            alpha = max(alpha, evaluation)
            # Update best_move if a new maximum evaluation is found
            if best_move is None or maxEval == evaluation:
                best_move = move
            # Alpha-Beta Pruning: If alpha is greater or equal to beta, prune the remaining branches
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth - 1, alpha, beta, True, game)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if best_move is None or minEval == evaluation:
                best_move = move
            if beta <= alpha:
                break
        return minEval, best_move

#Simulate a move on the board
def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

#Get all possible moves for a given color
def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves


#draw the moves on the board
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(100)

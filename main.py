# Using ANSI escape codes for new colors
class Colors:
    RESET = '\033[0m'
    # PLAYER1 = '\033[94m'  # Blue
    # PLAYER2 = '\033[92m'  # Green
    PLAYER1 = '\033[48;5;21m'  # Blue background
    PLAYER2 = '\033[48;5;28m'  # Green background


class SequenceBoard:
    def __init__(self):
        self.suits = ['♠', '♦', '♣', '♥']
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
        self.board_cards = [(value, suit) for _ in range(2) 
                            for suit in self.suits for value in self.values]
        self.board = [["" for _ in range(10)] for _ in range(10)]
        
        self.N_SPACES = (5*8) + (4*2)
        self.FREE_MARKER = "??"
        self.free_spaces_xy = [(0,0), (9,0), (0,9), (9,9)]
        self.marked_positions = {}  # {(x, y): "PLAYER1" or "PLAYER2"}

        self.fill_free_spaces()
        self.fill_board()


    def fill_free_spaces(self):
        for x, y in self.free_spaces_xy:
            self.board[x][y] = self.FREE_MARKER


    def fill_board(self):    
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        current_steps, stride_length, stride_counter = 0, 9, -1
        x, y = 0, 0
        card_counter = 0

        for _i in range(10*10 - 1):
                    
            x, y = x + directions[0][0], y + directions[0][1]
            current_steps += 1

            if (x,y) not in self.free_spaces_xy:
                self.board[x][y] = self.board_cards[card_counter]
                card_counter += 1
            
            if current_steps >= stride_length:
                directions.append(directions.pop(0))
                current_steps = 0
                stride_counter += 1
                if (stride_counter == 2):
                    stride_counter = 0
                    stride_length -= 1
    
    def mark_position(self, x, y, player):
        """Marks the given position with the player's color"""
        if (x, y) not in self.marked_positions and self.board[x][y] != self.FREE_MARKER:
            self.marked_positions[(x, y)] = player

    def display(self):
        for i, row in enumerate(self.board):
            row_display = []
            for j, card in enumerate(row):
                card_str = f"{card[0]}{card[1]}"
                if (i, j) in self.marked_positions:
                    if self.marked_positions[(i, j)] == "PLAYER1":
                        card_str = Colors.PLAYER1 + card_str + Colors.RESET
                    else:
                        card_str = Colors.PLAYER2 + card_str + Colors.RESET
                row_display.append(card_str)
            print(' | '.join(row_display))
            print('-' * self.N_SPACES)

    # def display(self):
    #     for row in self.board:
    #         print(' | '.join([f"{card[0]}{card[1]}" for card in row]))
    #         print('-' * self.N_SPACES)


if __name__ == '__main__':
    game_board = SequenceBoard()
    game_board.mark_position(1, 1, "PLAYER1")
    game_board.mark_position(2, 2, "PLAYER1")
    game_board.mark_position(3, 3, "PLAYER2")
    game_board.mark_position(4, 4, "PLAYER2")
    game_board.display()

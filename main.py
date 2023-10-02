import random

def leftpad(s):
    if len(s) == 1: return f" {s}"
    else: return s

# coord <tuple> (x, y) : (row, col) | 0-9, 0-9
# alpha <string>       : (col, row) | a-j, 0-9

def coord_to_alpha(coord):
    return chr(97 + coord[1]) + str(coord[0])

def alpha_to_coord(alpha):
    return (int(alpha[1:]), ord(alpha[0]) - 97,)

class Colors:
    RESET = '\033[0m'
    # PLAYER1 = '\033[94m'      # Blue Font
    # PLAYER2 = '\033[92m'      # Green Font
    PLAYER1 = '\033[48;5;21m'   # Blue background
    PLAYER2 = '\033[48;5;28m'   # Green background


class CardDeck:
    
    def __init__(self):
        self.suits = ['♠', '♦', '♣', '♥']
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.cards = [(value, suit) for _ in range(2) 
                      for suit in self.suits for value in self.values]
        random.shuffle(self.cards)
    
    def draw_card(self):
        return self.cards.pop()


class SequenceBoard:
    
    def __init__(self):
        self.suits = ['♠', '♦', '♣', '♥']
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']  # No Jacks
        self.board_cards = [(value, suit) for _ in range(2) 
                            for suit in self.suits for value in self.values]
        self.board = [["" for _ in range(10)] for _ in range(10)]
        
        self.N_SPACES = (5*8) + (4*2) + 4
        self.FREE_MARKER = "##"
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
        if (x, y) not in self.marked_positions and self.board[x][y] != self.FREE_MARKER:
            self.marked_positions[(x, y)] = player

    def get_card_positions(self, value_suit_tuple):
        positions = []
        for i, row in enumerate(self.board):
            for j, card in enumerate(row):
                if card == value_suit_tuple:
                    positions.append((i, j))
        return positions

    def display(self):

        column_headers = ' '.join([' ' * 4] + [chr(97 + i).upper() + "   " for i in range(10)])
        print(column_headers)
        print('-' * self.N_SPACES)

        for i, row in enumerate(self.board):
            row_display = [str(i)]  # Row header
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


class SequenceGame:
    def __init__(self):
        self.board = SequenceBoard()
        self.current_player = "PLAYER1"
        self.card_deck = CardDeck()
        self.hands = {
            "PLAYER1": [self.card_deck.draw_card() for _ in range(7)],
            "PLAYER2": [self.card_deck.draw_card() for _ in range(7)]
        }
        
    def switch_player(self):
        """Switches the current player."""
        if self.current_player == "PLAYER1":
            self.current_player = "PLAYER2"
        else:
            self.current_player = "PLAYER1"

        
    def play_card(self):
        while True:
            try:
                raw_user_input = input("Enter coords to mark (e.g. c3) or cardnumber (1-8): ")
                user_input = raw_user_input.strip().lower()
                
                if user_input == "exit":
                    return False
                
                if (len(user_input) == 1 and user_input.isdigit()):
                    
                    card_number = int(user_input)
                    if (1 <= card_number <= 8):
                        selected_card = self.hands[self.current_player][card_number-1]

                        if selected_card[0] == 'J':
                            print("j-johhny-jack")
                            # TODO
                        
                        # find postions of card on board
                        candidate_coords = self.board.get_card_positions(selected_card)

                        # eliminate positions already filled
                        candidate_coords = [coord for coord in candidate_coords
                                            if coord not in self.board.marked_positions]
                        
                        candidate_coords = [coord_to_alpha(coord) 
                                            for coord in candidate_coords]

                        cc_msg = f"{''.join(selected_card)} choose which position:\n"
                        cc_msg += "==========================\n"
                        for i, coord in enumerate(candidate_coords):
                            cc_msg += f"{i+1}) {coord}\n"
                        cc_msg += "input number > "
                        
                        ret = input(cc_msg)

                        selected_ind_position = int(ret) - 1
                        # TODO - validate input

                        x, y = alpha_to_coord(candidate_coords[selected_ind_position])

                        break

                    else:
                        print("Invalid card number. Please try again.")
                elif ((len(user_input) == 2) 
                      and user_input[0].isalpha() and user_input[1].isdigit()
                      ):
                    
                    x, y = alpha_to_coord(user_input)
                    
                    if ((0 <= x < 10 and 0 <= y < 10)
                        and (x, y) not in self.board.marked_positions
                        and self.board.board[x][y] != self.board.FREE_MARKER
                        ):
                        # TODO - check if you have card
                        # TODO - refactor
                        break   # valid choice
                    else:
                        print("Invalid coordinates. Please try again.")
                else:
                    print("Invalid input; neither coords, nor cardnumber. Please try again.")
        
            except ValueError:
                print("Invalid format. Please use comma-separated values (e.g., 1,2).")

        # handle jacks
        # one-eyed: spades,hearts | two-eyed: clubs, hearts
            
        self.hands[self.current_player].remove(selected_card)

        return x, y
        

    def play_turn(self):
        print(f"\n{self.current_player}'s Turn")

        drawn_card = self.card_deck.draw_card()
        self.hands[self.current_player].append(drawn_card)
        print(f"Drawn card: {drawn_card[0]}{drawn_card[1]}")

        self.display_hand(self.hands[self.current_player])
        
        x, y = self.play_card()

        self.board.mark_position(x, y, self.current_player)
        print('')
        self.board.display()
        self.switch_player()
        return True
    
    def display_hand(self, hand):
        row_display = []
        for card in hand:
            card_str = f"{card[0]}{card[1]}"
            row_display.append(card_str)

        n_spaces = (((len(hand)-2)*5) + (2*4))
        print('-' * n_spaces )
        print(' | '.join(row_display))
        print('-' * n_spaces )
        print(' | '.join([leftpad(str(e)) for e in range(1, len(hand)+1)]))
        print('-' * n_spaces )
    
    def play(self):
        """Main game loop."""
        print("Welcome to Sequence!\n")
        self.board.display()
        while True:
            b_continue = self.play_turn()
            if not(b_continue):
                print("game exited by user, goodbye")
                break


if __name__ == '__main__':
    game = SequenceGame()
    game.play()
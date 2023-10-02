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

    def unmark_position(self, x, y, player):
        if (x, y) in self.marked_positions and self.board[x][y] != self.FREE_MARKER:
            _ = self.marked_positions.pop((x,y))

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
        if self.current_player == "PLAYER1":
            self.current_player = "PLAYER2"
        else:
            self.current_player = "PLAYER1"

        
    def play_card(self):
        while True:
            try:
                num_cards = len(self.hands[self.current_player])
                raw_user_input = input(f"Enter coords to mark (e.g. c3) or cardnumber (1-{num_cards}): ")
                user_input = raw_user_input.strip().lower()
                
                if user_input == "exit":
                    return False
                
                if (len(user_input) == 1 and user_input.isdigit()):
                    
                    card_number = int(user_input)
                    if (1 <= card_number <= num_cards):
                        selected_card = self.hands[self.current_player][card_number-1]

                        if selected_card[0] == 'J':
                            break
                        
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
                    
                    if not((0 <= x < 10 and 0 <= y < 10)
                        and (x, y) not in self.board.marked_positions
                        and self.board.board[x][y] != self.board.FREE_MARKER
                        ):
                        print("Invalid coordinates. Please try again.")
                        continue
                        
                    selected_card = self.board.board[x][y]
                    
                    if selected_card not in self.hands[self.current_player]:
                        print(f"You chose tile {user_input} with {selected_card} but don't have it in your hand.")
                        continue
                    
                    # if you're here it's a valid choice, break loop and finish function
                    break   
                    
                else:
                    print("Invalid input; neither coords, nor cardnumber. Please try again.")
        
            except ValueError:
                print("Invalid input formart.")

        # jack played: handle one-eye vs two-eye behavior and user selection of spot
        if selected_card[0] == 'J':
        
            one_eyed, two_eyed = ['♠', '♥'], ['♦', '♣']
            is_one_eyed = True if selected_card[1] in one_eyed else False

            j_msg =  f"You are playing a {'one' if is_one_eyed else 'two'}-eyed jack\n"
            if is_one_eyed:
                j_msg += f"Remove a tile by entering the coords (e.g. c3) >"
            else:
                j_msg += f"Add a tile (to unmarked sq) by entering the coords (e.g. c3) >"

            while True:

                ret = input(j_msg)        
                ret = ret.strip().lower()

                if not((len(ret) == 2) 
                      and ret[0].isalpha() and ret[1].isdigit()
                    ):
                    print(f"coord {ret} not recognized, try again")
                    continue

                x, y = alpha_to_coord(ret)

                # validation
                if not((0 <= x < 10 and 0 <= y < 10)
                    and self.board.board[x][y] != self.board.FREE_MARKER
                    ):
                    print("Invalid spot chosen, try again.")
                    continue
                    
                if is_one_eyed:
                    if (x, y) not in self.board.marked_positions:
                        print("Chose a marked spot to remove with one eyed jack")
                        continue
                    self.board.unmark_position(x, y, self.current_player)
                    x, y = None, None   # will not mark
                else:
                    if (x, y) in self.board.marked_positions:
                        print("Chose an unmarked spot to remove with one eyed jack")
                        continue
                
                break
            
        # finish up routine
        self.hands[self.current_player].remove(selected_card)

        return x, y
        

    def play_turn(self):
        print(f"\n{self.current_player}'s Turn")

        drawn_card = self.card_deck.draw_card()
        self.hands[self.current_player].append(drawn_card)
        print(f"Drawn card: {drawn_card[0]}{drawn_card[1]}")

        self.display_hand(self.hands[self.current_player])
        
        x, y = self.play_card()

        if x is not None and y is not None:
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
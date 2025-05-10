import random
import sys
import os
import time # For computer 'thinking' delay

# --- Constants ---
NUM_PLAYERS_MIN = 2
NUM_PLAYERS_MAX = 4
TOKENS_PER_PLAYER = 4
HOME_POSITION_INDEX = 57 # Index representing the final home square
START_POSITION_INDEX = 1 # Index representing the first square on the board after leaving base
BASE_POSITION_INDEX = 0  # Index representing the starting base
MAIN_PATH_END_INDEX = 51 # Last index on the shared path before home stretch

PLAYER_COLORS = ["YELLOW", "BLUE", "RED", "GREEN"]
PLAYER_CHARS = ["Y", "B", "R", "G"]

# Player Types
PLAYER_TYPE_HUMAN = "Human"
PLAYER_TYPE_COMPUTER = "Computer"

COMPUTER_THINK_DELAY = 0.5 # Seconds for computer 'thinking'

# Ludo paths array (0-indexed for players)
LUDO_PATHS = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 101, 102, 103, 104, 105, 106], # Yellow Path
    [0, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 201, 202, 203, 204, 205, 206], # Blue Path
    [0, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 301, 302, 303, 304, 305, 306], # Red Path
    [0, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 401, 402, 403, 404, 405, 406]  # Green Path
]

# Board layout for printing
DISPLAY_LAYOUT = [
    [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500],
    [502, 502, 502, 502, 502, 502, 501, 24,  25,  26,  501, 502, 502, 502, 502, 502, 502],
    [502, 58,  502, 502, 59,  502, 501, 23, 301,  27, 501, 502, 61,  502, 502, 62,  502],
    [502, 502, 502, 502, 502, 502, 501, 22, 302,  28, 501, 502, 502, 502, 502, 502, 502],
    [502, 502, 502, 502, 502, 502, 501, 21, 303,  29, 501, 502, 502, 502, 502, 502, 502],
    [502, 57,  502, 502, 60,  502, 501, 20, 304,  30, 501, 502, 64,  502, 502, 63,  502],
    [502, 502, 502, 502, 502, 502, 501, 19, 305,  31, 501, 502, 502, 502, 502, 502, 502],
    [500, 500, 500, 500, 500, 500, 501, 500, 500, 500, 501, 500, 500, 500, 500, 500, 500],
    [13,  14,  15,  16,  17,  18, 501, 502, 306, 502, 501, 32,  33,  34,  35,  36,  37 ],
    [12, 201, 202, 203, 204, 205, 501, 206, 502, 406, 501, 405, 404, 403, 402, 401, 38 ],
    [11,  10,   9,   8,   7,   6, 501, 502, 106, 502, 501, 44,  43,  42,  41,  40,  39 ],
    [500, 500, 500, 500, 500, 500, 501, 500, 500, 500, 501, 500, 500, 500, 500, 500, 500],
    [502, 502, 502, 502, 502, 502, 501,  5, 105,  45, 501, 502, 502, 502, 502, 502, 502],
    [502, 55,  502, 502, 56,  502, 501,  4, 104,  46, 501, 502, 68,  502, 502, 65,  502],
    [502, 502, 502, 502, 502, 502, 501,  3, 103,  47, 501, 502, 502, 502, 502, 502, 502],
    [502, 502, 502, 502, 502, 502, 501,  2, 102,  48, 501, 502, 502, 502, 502, 502, 502],
    [502, 54,  502, 502, 53,  502, 501,  1, 101,  49, 501, 502, 67,  502, 502, 66,  502],
    [502, 502, 502, 502, 502, 502, 501, 52,  51,  50, 501, 502, 502, 502, 502, 502, 502],
    [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
]

# Map player index to their base square numbers in DISPLAY_LAYOUT
BASE_SQUARES = {
    0: [53, 54, 55, 56],  # Yellow
    1: [57, 58, 59, 60],  # Blue
    2: [61, 62, 63, 64],  # Red
    3: [65, 66, 67, 68]   # Green
}

# --- Safe Squares Definition ---
SAFE_SQUARES = {
    1, 9, 14, 22, 27, 35, 40, 48 # Standard safe squares including starting points
}
SAFE_SQUARE_MARKER = " # "
REGULAR_SQUARE_MARKER = " * "

# --- Functions ---

def clear_screen():
    """Clears the terminal screen."""
    # os.system('cls' if os.name == 'nt' else 'clear') # Uncomment if desired
    print("\n" * 3)

def roll_dice():
    """Simulates rolling a 6-sided die."""
    return random.randint(1, 6)

def get_int_input(prompt, min_val=None, max_val=None):
    """Gets integer input from the user with validation."""
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Input must be at least {min_val}.")
            elif max_val is not None and value > max_val:
                print(f"Input must be at most {max_val}.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_player_setup():
    """Gets the number of players and their types/names."""
    while True:
        num_players = get_int_input(
            f"Enter total number of players ({NUM_PLAYERS_MIN}-{NUM_PLAYERS_MAX}): ",
            NUM_PLAYERS_MIN,
            NUM_PLAYERS_MAX
        )
        if NUM_PLAYERS_MIN <= num_players <= NUM_PLAYERS_MAX:
            break
        else:
            print(f"Please enter a number between {NUM_PLAYERS_MIN} and {NUM_PLAYERS_MAX}.")

    player_names = []
    player_types = []
    print("\n--- Player Setup ---")
    for i in range(num_players):
        while True:
            p_type_input = input(f"Is Player {i+1} ({PLAYER_COLORS[i]}) Human (H) or Computer (C)? ").strip().upper()
            if p_type_input == 'H':
                player_types.append(PLAYER_TYPE_HUMAN)
                name = input(f"  Enter name for Human Player {i+1}: ").strip()
                if not name: # Handle empty name
                    name = f"Human {i+1}"
                player_names.append(f"{PLAYER_COLORS[i]} {name}")
                break
            elif p_type_input == 'C':
                player_types.append(PLAYER_TYPE_COMPUTER)
                name = f"Computer {i+1}" # Default computer name
                player_names.append(f"{PLAYER_COLORS[i]} {name}")
                print(f"  Player {i+1} is {player_names[-1]}")
                break
            else:
                print("Invalid input. Please enter 'H' or 'C'.")

    return num_players, player_names, player_types


def display_board(token_positions):
    """Prints the current state of the Ludo board with safe squares marked."""
    clear_screen()
    print("--- LUDO BOARD ('#' denotes a safe square) ---")
    max_row_len = max(len(row) for row in DISPLAY_LAYOUT) * 3 + 5 # Estimate width

    for r in range(len(DISPLAY_LAYOUT)):
        row_str = ""
        for c in range(len(DISPLAY_LAYOUT[r])):
            cell_val = DISPLAY_LAYOUT[r][c]
            token_found = False
            printed_char = "" # Store what to print for this cell

            # Check for tokens on the path or home stretch
            tokens_on_cell = []
            for p_idx, tokens in token_positions.items():
                for t_idx, pos_idx in enumerate(tokens):
                    if pos_idx != BASE_POSITION_INDEX: # Token is on the board
                        try:
                             abs_pos = LUDO_PATHS[p_idx][pos_idx]
                             if abs_pos == cell_val:
                                 tokens_on_cell.append(f"{PLAYER_CHARS[p_idx]}{t_idx+1}")
                        except IndexError:
                             # This indicates an error in game logic if it happens
                             print(f"Error: Invalid pos_idx {pos_idx} for player {p_idx} in display")
                             continue

            if tokens_on_cell:
                 printed_char = f" {tokens_on_cell[0]}" # Show first token found
                 # Advanced: Handle stacking display here if needed
                 token_found = True

            # Check for tokens in base if nothing else was found on path
            if not token_found:
                for p_idx, base_sq_list in BASE_SQUARES.items():
                    if p_idx in token_positions and cell_val in base_sq_list:
                        try:
                           base_index = base_sq_list.index(cell_val)
                           if token_positions[p_idx][base_index] == BASE_POSITION_INDEX:
                               printed_char = f" {PLAYER_CHARS[p_idx]}{base_index+1}"
                               token_found = True
                               break
                        except (ValueError, IndexError):
                            pass # Should not happen with correct BASE_SQUARES

            # If still no token, print board element or path marker
            if not token_found:
                if cell_val == 500:
                    printed_char = "---"
                elif cell_val == 501:
                    printed_char = " | "
                elif cell_val == 502:
                    printed_char = "   "
                # Check if it's a path/home square value potentially
                # Values > 100 represent home stretches
                elif 1 <= cell_val <= 52 or (100 < cell_val < 500 and cell_val % 100 <= 6):
                     if cell_val in SAFE_SQUARES:
                         printed_char = SAFE_SQUARE_MARKER
                     else:
                         printed_char = REGULAR_SQUARE_MARKER
                else:
                     # Fallback for base square numbers or unexpected values
                     printed_char = "   " # Assume empty space if it's a base number etc.


            row_str += printed_char

        print(row_str)

    print("-" * max_row_len) # Separator line


def check_capture(moving_player_idx, moved_token_idx, token_positions):
    """
    Checks if the moved token captures an opponent's token.
    Captures do NOT happen on SAFE_SQUARES.
    Returns the updated token_positions.
    """
    try:
        moved_token_pos_idx = token_positions[moving_player_idx][moved_token_idx]
    except IndexError:
        print(f"Error: Invalid token index {moved_token_idx} for player {moving_player_idx} in capture check.")
        return token_positions

    # Cannot capture from base or if the move ended in the home stretch/home
    if moved_token_pos_idx == BASE_POSITION_INDEX or moved_token_pos_idx > MAIN_PATH_END_INDEX:
         return token_positions

    # Get the absolute board position where the token landed
    try:
        moved_token_abs_pos = LUDO_PATHS[moving_player_idx][moved_token_pos_idx]
    except IndexError:
         print(f"Error: Invalid move index {moved_token_pos_idx} for capture check.")
         return token_positions

    # Check if the landing square is safe
    if moved_token_abs_pos in SAFE_SQUARES:
        return token_positions # No capture on safe squares

    # Proceed with capture check if landing square is not safe
    capture_made = False
    for p_idx, tokens in token_positions.items():
        if p_idx == moving_player_idx:
            continue # Don't capture your own tokens

        for t_idx, pos_idx in enumerate(tokens):
            # Check if the opponent token is on the main path
            if pos_idx != BASE_POSITION_INDEX and pos_idx <= MAIN_PATH_END_INDEX:
                try:
                    opponent_abs_pos = LUDO_PATHS[p_idx][pos_idx]
                    if opponent_abs_pos == moved_token_abs_pos:
                        # Capture!
                        print(f"!!! {PLAYER_COLORS[moving_player_idx]}'s token {moved_token_idx+1} captured {PLAYER_COLORS[p_idx]}'s token {t_idx+1} on square {moved_token_abs_pos} !!!")
                        token_positions[p_idx][t_idx] = BASE_POSITION_INDEX # Send opponent home
                        capture_made = True
                        # Optional: Break inner loop if only one capture per square allowed
                        # break
                except IndexError:
                     # Error in opponent's position data?
                     print(f"Error: Invalid pos_idx {pos_idx} for opponent player {p_idx} during capture check.")
                     continue

        # Optional: If multiple tokens from *different* players could be captured,
        # this loop structure continues checking. Standard Ludo usually clears the square.
        # If a capture was made, maybe break the outer loop too?
        # if capture_made: break

    return token_positions


def computer_choose_move(player_idx, token_positions, dice_roll, movable_tokens):
    """
    AI logic for choosing a move. Enhanced to consider safe squares.
    Simple Strategy:
    1. Prioritize moving out of base if possible (roll is 6).
    2. Prioritize moving a token that can reach home exactly.
    3. Prioritize moving onto a safe square if possible.
    4. Prioritize moving the token furthest along the path.
    5. Fallback: Random choice among movable tokens.
    Returns the chosen token number (1-4).
    """
    print("Computer is thinking...")
    time.sleep(COMPUTER_THINK_DELAY)

    current_player_tokens = token_positions[player_idx]

    # 1. Prioritize moving out of base if roll is 6
    if dice_roll == 6:
        base_tokens_movable = [
            t_num for t_num in movable_tokens
            if current_player_tokens[t_num - 1] == BASE_POSITION_INDEX
        ]
        if base_tokens_movable:
            chosen_token = random.choice(base_tokens_movable) # Pick one randomly if multiple
            print(f"Computer chooses to move Token {chosen_token} out of base.")
            return chosen_token

    # 2. Prioritize exact move to home
    home_bound_tokens = [
        t_num for t_num in movable_tokens
        # Ensure token is actually on the home stretch before checking exact move
        if MAIN_PATH_END_INDEX < current_player_tokens[t_num - 1] < HOME_POSITION_INDEX and
           current_player_tokens[t_num - 1] + dice_roll == HOME_POSITION_INDEX
    ]
    if home_bound_tokens:
         chosen_token = random.choice(home_bound_tokens)
         print(f"Computer chooses Token {chosen_token} to move exactly to home.")
         return chosen_token

    # 3. Prioritize moving onto a safe square (Ludo Mix Powerup)
    safe_landing_tokens = []
    for t_num in movable_tokens:
         current_pos_idx = current_player_tokens[t_num-1]
         if current_pos_idx != BASE_POSITION_INDEX: # Only consider tokens already on board
             new_pos_idx = current_pos_idx + dice_roll
             if new_pos_idx <= HOME_POSITION_INDEX: # Ensure valid move index
                 try:
                     new_abs_pos = LUDO_PATHS[player_idx][new_pos_idx]
                     if new_abs_pos in SAFE_SQUARES and new_pos_idx < HOME_POSITION_INDEX: # Check if landing is safe (and not home itself)
                         safe_landing_tokens.append(t_num)
                 except IndexError:
                     continue # Skip if new_pos_idx is somehow invalid

    if safe_landing_tokens:
         # Maybe prioritize furthest among safe options? For now, random safe landing.
         chosen_token = random.choice(safe_landing_tokens)
         print(f"Computer chooses Token {chosen_token} to land on a safe square.")
         return chosen_token


    # 4. Prioritize moving the furthest token (that is movable and not already covered by above)
    best_token = -1
    max_pos = -1
    non_base_movable = [
        t_num for t_num in movable_tokens
        if current_player_tokens[t_num - 1] != BASE_POSITION_INDEX
    ]

    if non_base_movable:
        # Prefer tokens not already on the final home stretch unless it's the only option
        main_path_tokens = [t for t in non_base_movable if current_player_tokens[t-1] <= MAIN_PATH_END_INDEX]
        home_stretch_tokens = [t for t in non_base_movable if current_player_tokens[t-1] > MAIN_PATH_END_INDEX]

        tokens_to_consider = main_path_tokens if main_path_tokens else home_stretch_tokens

        for token_num in tokens_to_consider:
            pos_idx = current_player_tokens[token_num - 1]
            # Simple distance metric (higher index is further)
            if pos_idx > max_pos:
                max_pos = pos_idx
                best_token = token_num

        if best_token != -1:
             print(f"Computer chooses to move furthest token: Token {best_token}.")
             return best_token

    # 5. Fallback: Random choice among all movable tokens
    if not movable_tokens: # Should not happen if logic above is correct, but safeguard
         print("Error: No movable tokens found in computer AI fallback.")
         return -1 # Indicate error
    chosen_token = random.choice(movable_tokens)
    print(f"Computer randomly chooses to move Token {chosen_token}.")
    return chosen_token


def play_turn(player_idx, player_name, player_type, token_positions, num_players):
    """Handles a single player's turn, differentiating between Human and Computer."""
    print("\n" + "="*60)
    print(f"\nPlayer {player_idx+1}'s Turn: {player_name} ({player_type})")

    current_token_positions = token_positions[player_idx]
    print("\nToken Positions:")
    for i, pos in enumerate(current_token_positions):
        position_str = ""
        if pos == BASE_POSITION_INDEX:
            position_str = "Base"
        elif pos == HOME_POSITION_INDEX:
            position_str = "Home"
        else:
            try:
                abs_pos = LUDO_PATHS[player_idx][pos]
                position_str = f"Square {abs_pos}"
                if abs_pos in SAFE_SQUARES:
                     position_str += " (Safe)"
            except IndexError:
                 position_str = "Invalid Position!"
        print(f"  Token {i+1}: {position_str}", end="\t")
    print("\n")

    # Dice roll for both Human and Computer
    if player_type == PLAYER_TYPE_HUMAN:
        input("Press ENTER to roll the dice...")
    else:
        print("Computer rolling dice...")
        time.sleep(COMPUTER_THINK_DELAY / 2)

    dice_roll = roll_dice()
    print(f"!!.. Rolled a {dice_roll} ..!!")

    # --- Determine valid moves (same for Human and Computer) ---
    movable_tokens = [] # List of token numbers (1-4)
    can_move_from_base = (dice_roll == 6)
    all_tokens_at_base = all(pos == BASE_POSITION_INDEX for pos in current_token_positions)

    if all_tokens_at_base and not can_move_from_base:
        print("\nNo tokens can move. You need a 6 to leave base.")
        return token_positions, False

    for i, pos_idx in enumerate(current_token_positions):
        token_num = i + 1
        if pos_idx == BASE_POSITION_INDEX:
            if can_move_from_base:
                movable_tokens.append(token_num)
        elif pos_idx == HOME_POSITION_INDEX:
            continue # Cannot move token already home
        else:
            # Check if move is possible without overshooting
            if pos_idx + dice_roll <= HOME_POSITION_INDEX:
                 movable_tokens.append(token_num)

    if not movable_tokens:
        print("\nNo valid moves possible with this roll.")
        # Provide specific reasons if possible
        if any(pos == BASE_POSITION_INDEX for pos in current_token_positions) and not can_move_from_base:
             print("(Need a 6 to move a token from base)")
        elif any(0 < pos <= HOME_POSITION_INDEX and pos + dice_roll > HOME_POSITION_INDEX for pos in current_token_positions):
            print("(Cannot overshoot the home square - requires exact roll)")
        return token_positions, False

    # --- Player chooses token (Human vs Computer) ---
    token_choice = -1
    if player_type == PLAYER_TYPE_HUMAN:
        while True:
            prompt = f"\nWhich token do you want to move? ({', '.join(map(str, movable_tokens))}): "
            token_choice_input = get_int_input(prompt)
            if token_choice_input in movable_tokens:
                token_choice = token_choice_input
                break
            else:
                print(f"Invalid choice. Please choose one of: {', '.join(map(str, movable_tokens))}")
    else: # Computer's turn
        token_choice = computer_choose_move(player_idx, token_positions, dice_roll, movable_tokens)
        if token_choice == -1: # Error in AI logic
             return token_positions, False # End turn


    # --- Execute Move (same logic for Human and Computer choice) ---
    token_idx_to_move = token_choice - 1
    current_pos_idx = current_token_positions[token_idx_to_move]
    new_pos_idx = -1
    new_abs_pos = -1 # Store the landing square absolute position

    if current_pos_idx == BASE_POSITION_INDEX: # Moving from base
        if dice_roll == 6:
            new_pos_idx = START_POSITION_INDEX
            token_positions[player_idx][token_idx_to_move] = new_pos_idx
            new_abs_pos = LUDO_PATHS[player_idx][new_pos_idx] # Store abs pos
            print(f"\nToken {token_choice} moved to the start square ({new_abs_pos}).")
            # Capture check (Start squares are safe)
            token_positions = check_capture(player_idx, token_idx_to_move, token_positions)
        else:
             print("Error: Logic flaw - tried to move from base without a 6.") # Should not happen
             return token_positions, False # End turn due to error

    else: # Moving token already on board
        proposed_new_pos_idx = current_pos_idx + dice_roll
        if proposed_new_pos_idx <= HOME_POSITION_INDEX:
            new_pos_idx = proposed_new_pos_idx
            token_positions[player_idx][token_idx_to_move] = new_pos_idx
            new_abs_pos = LUDO_PATHS[player_idx][new_pos_idx] # Store abs pos
            if new_pos_idx == HOME_POSITION_INDEX:
                print(f"\nToken {token_choice} reached HOME!")
            else:
                position_type = "(Safe)" if new_abs_pos in SAFE_SQUARES else ""
                print(f"\nToken {token_choice} moved to square {new_abs_pos} {position_type}.")
            # Check for captures
            if new_pos_idx < HOME_POSITION_INDEX:
                 token_positions = check_capture(player_idx, token_idx_to_move, token_positions)
        else:
            # This case should be prevented by movable_tokens logic
             print(f"Error: Logic flaw - tried to overshoot home for Token {token_choice}.")
             return token_positions, False # End turn due to error

    # --- Check for Extra Turn ---
    extra_turn = False
    # Check in order of priority: Roll 6 > Reach Home > Land on Safe
    if dice_roll == 6:
        print("\n!!.. Rolled a 6, get an extra turn! ..!!")
        extra_turn = True
    elif new_pos_idx == HOME_POSITION_INDEX:
         print("\n!!.. Token reached home, get an extra turn! ..!!")
         extra_turn = True
    # NEW: Check if landed on a safe square (and didn't get bonus for above reasons)
    elif new_abs_pos != -1 and new_abs_pos in SAFE_SQUARES and new_pos_idx != HOME_POSITION_INDEX:
         print("\n!!.. Ludo Mix Powerup! Landed on a safe square, get an extra turn! ..!!")
         extra_turn = True
    # Add capture bonus rule here if desired using 'elif not extra_turn and capture_made:'

    return token_positions, extra_turn


def check_win(player_idx, token_positions):
    """Checks if the given player has won."""
    if player_idx not in token_positions:
        return False
    return all(pos == HOME_POSITION_INDEX for pos in token_positions[player_idx])

# --- Main Game Logic ---

def main():
    """Main function to run the Ludo game."""
    # display_board({i: [0]*TOKENS_PER_PLAYER for i in range(4)}) # Optional: Show initial empty board

    num_players, player_names, player_types = get_player_setup()

    # Initialize token positions
    token_positions = {i: [BASE_POSITION_INDEX] * TOKENS_PER_PLAYER for i in range(num_players)}

    print("\n--- Ludo Mix Powerup Active: Landing on '#' gives an extra turn! ---") # Announce rule
    print("\nEnter 1 to PLAY or 0 to Exit.")
    choice = get_int_input("Enter your choice: ", 0, 1)


    if choice == 0:
        print("\nThanks for setting up. Exiting.")
        sys.exit()

    current_player_idx = 0
    game_over = False
    winner_idx = -1

    while not game_over:
        display_board(token_positions)

        # Check if the current player has already won
        active_players_left = [p for p in range(num_players) if not check_win(p, token_positions)]
        if not active_players_left:
             print("\nAll active players have finished!")
             game_over = True
             continue # Skip to game over sequence

        # Skip turn if player already won
        if check_win(current_player_idx, token_positions):
             # print(f"\n{player_names[current_player_idx]} has already won. Skipping turn.") # Can be verbose
             current_player_idx = (current_player_idx + 1) % num_players
             continue # Move to the next player index check


        player_name = player_names[current_player_idx]
        player_type = player_types[current_player_idx]

        # Play the turn
        token_positions, gets_extra_turn = play_turn(
            current_player_idx, player_name, player_type, token_positions, num_players
        )

        # Check for win condition AFTER the move
        if check_win(current_player_idx, token_positions):
            print(f"\n**** {player_name} has finished! ****")
            # Check if this win ends the game (e.g., only one player left or first player wins mode)
            active_players_left_after_move = [p for p in range(num_players) if not check_win(p, token_positions)]
            if len(active_players_left_after_move) <= 1: # Or check if winner_idx == -1 for "first wins"
                 game_over = True
                 if winner_idx == -1: # Record the first winner
                     winner_idx = current_player_idx
            # Don't break yet, let the loop handle the next turn or game over sequence


        # Determine the next player index
        next_player_idx = current_player_idx # Assume extra turn initially
        if not gets_extra_turn:
            next_player_idx = (current_player_idx + 1) % num_players

        # -- End-of-Turn Pause --
        if not game_over:
            if gets_extra_turn:
                # Message indicating who gets the extra turn
                print(f"\n{player_name} gets another turn.")
            else:
                # Message indicating whose turn is next
                print(f"\nTurn complete. Next player: {player_names[next_player_idx]}")

            # Always ask for ENTER before the next turn starts
            input("\nPress ENTER to continue...")

        # Update current player index for the next loop iteration
        current_player_idx = next_player_idx


    # --- Game Over ---
    display_board(token_positions) # Show final board
    print("\n==================== GAME OVER ====================")

    # Determine winner(s) based on game rules (e.g., first to finish, or last player standing)
    winners = [player_names[p] for p in range(num_players) if check_win(p, token_positions)]

    if winner_idx != -1: # If we tracked the first winner
         print(f"\n!!!!!!!! CONGRATULATIONS {player_names[winner_idx]} !!!!!!!!")
         print("!!!!!!!! YOU ARE THE WINNER (First to finish) !!!!!!!!")
    elif winners:
         print(f"\nGame ended! Finished players: {', '.join(winners)}")
         # Declare the last active player if that's the rule, or just list finishers
    else:
         print("\nGame ended.") # Fallback

    print("\nThanks for playing Ludo Mix!")

if __name__ == "__main__":
    main()
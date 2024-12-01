import random

# Cluedo Cards
murderers = ["Miss Scarlet", "Professor Plum", "Mrs. Peacock", "Colonel Mustard", "Dr. Orchid", "Mr. Green"]
rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billiard Room", "Library", "Lounge", "Hall", "Study"]
weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]


# Select a random murder solution
solution = {
    "murderer": random.choice(murderers),
    "weapon": random.choice(weapons),
    "room": random.choice(rooms)
}

# Game board layout
game_board = rooms
tunnels = {
    "Kitchen": ["Study", "Dining Room"],
    "Study": ["Kitchen"],
    "Dining Room": ["Kitchen"],
    "Conservatory": ["Lounge"],
    "Lounge": ["Conservatory"],
}

# Initialize players
players = {}
n = 6
for i in range(n):
    players["Player " + str(i + 1)] = {"accusation": False, "cards": [], "player_name": murderers[i], "position": random.choice(game_board), "suggestion_cards": []}

# Distribute cards to players
def distribute_cards():
    all_cards = murderers + weapons + rooms
    solution_cards = [solution["murderer"], solution["weapon"], solution["room"]]
    deck = []
    for card in all_cards:
        if card not in solution_cards:
            deck.append(card)
    
    # Shuffle the deck
    random.shuffle(deck)

    for i, card in enumerate(deck):
        players[f"Player {i % len(players) + 1}"]["cards"].append(card)

# Move player to a different room
def move_player(player, position):
    current_index = game_board.index(position)
    
    print("\nWhere would you like to move?")

    # Possible destinations
    options = []

    # Add rooms to left & right of current room
    if current_index > 0:
        options.append(game_board[current_index - 1])
    if current_index < len(game_board) - 1:
        options.append(game_board[current_index + 1])
    
    # Include tunnels / shortcuts
    if position in tunnels:
        for path in tunnels[position]:
            options.append(path)
    
    print(f"Possible Destinations: {', '.join(options)}")

    # Check for valid inputs
    while True:
        new_position = input("Enter desired destination: ").strip()
        if new_position in options:
            return new_position
        print("Invalid destination.")

# Function for player guesses
def player_guess(current_room, suggestion=False):
    print(f"\nYou are in {current_room}.")

    if suggestion:
        print("Make a suggestion!")
    else:
        print("Make an accusation!")
    
    guess_murderer = input(f"Choose a murderer ({', '.join(murderers)}): ").strip()
    guess_room = current_room
    guess_weapon = input(f"Choose a weapon ({', '.join(weapons)}): ").strip()


    return guess_murderer, guess_weapon, guess_room

# Handle Suggestions
def handle_suggestion(guess, current_player):
    print(f"{current_player} suggests: {guess[0]} with the {guess[1]} in the {guess[2]}")

    # Move the suggested player (if applicable) to the suggested room
    for player, data in players.items():
        if data['player_name'] == guess[0]:
            data["position"] = guess[2]

    # Get the list of players
    player_names = list(players.keys())
    current_index = player_names.index(current_player)
    matching_cards = []

    # Start at the next player and loop around
    for i in range(1, len(player_names)):
        next_player = player_names[(current_index + i) % len(player_names)]
        
        if next_player != current_player:
            # Check if the next player has any of the guessed cards
            for card in players[next_player]["cards"]:
                if card in guess:
                    matching_cards.append(card)
            
            print(matching_cards)
            if len(matching_cards) > 0:
                match_card = random.choice(matching_cards)
                print(f"{next_player} shows {match_card} to you")

                # Add the card shown to the player's knowledge base
                players[current_player].setdefault("suggestion_cards", []).append(match_card)
                print("Suggestion Cards: ", players[current_player]["suggestion_cards"])
                return

    # If no one can disprove
    print("No one has cards for the suggestion")

# Check guesses against the solution
def check_guess(guess, solution):
    feedback = []
    if guess[0] != solution["murderer"]:
        feedback.append("Murderer is incorrect.")
    if guess[1] != solution["weapon"]:
        feedback.append("Weapon is incorrect.")
    if guess[2] != solution["room"]:
        feedback.append("Room is incorrect.")
    return feedback

# Main game
def play_cluedo():
    print("Welcome to Cluedo!")
    print("Here is solution: ", solution)

    distribute_cards()

    turn = 0
    player_names = list(players.keys())

    while True:
        # Current player
        turn = turn % len(player_names)

        # Turn player property
        current_player = player_names[turn % len(player_names)]
        game_name = players[current_player]["player_name"]
        current_position = players[current_player]["position"]

        print(f"\n{current_player}'s ({game_name}) turn. You are currently in the {current_position}.")
        print("\nYour hand: ", players[current_player]["cards"])
        move_decision = input("Would you like to move to another room? (yes/no): ").strip().lower()

        # Player decided to move
        if move_decision == "yes":
            new_position = move_player(current_player, current_position)
            players[current_player]["position"] = new_position
            current_position = new_position
            print(f"You moved to the {current_position}.")
        
        # Prompt player for action
        action = input("Would you like to make a suggestion or accusation? (suggestion/accusation/none): ").strip().lower()

        # Player decided to propose a suggestion
        if action == "suggestion":
            guess = player_guess(current_position, suggestion=True)
            handle_suggestion(guess, current_player)
            turn += 1

        # Player decided to propose an accusation
        elif action == "accusation":
            guess = player_guess(current_position)
            feedback = check_guess(guess, solution)

            # No feedback means the guess is correct and the game is stopped
            if not feedback:
                print("\nYou solved the solution!")
                print(f"The case was: {solution['murderer']} in the {solution['room']} with the {solution['weapon']}.")
                break
            
            # Remove player from the game, but not from showing cards
            else:
                print("Your accusation was incorrect. You're out of the game!")

                player_names.remove(current_player)
                # print(player_names, turn)

                if len(player_names) == 1:  # Only one player left
                    print(f"\n{player_names[0]} is the last player remaining!")
                    break

        else:
            turn += 1

# Run the game
if __name__ == "__main__":
    play_cluedo()

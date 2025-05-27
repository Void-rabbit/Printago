from game_world import world, items

# Player state
current_room = 'entrance_hall'
inventory = []

def parse_input(user_input):
    """
    Parses user input into a command and an optional argument.
    Handles empty or whitespace-only input by returning (None, None).
    """
    parts = user_input.lower().split()
    command = parts[0] if parts else None
    argument = parts[1] if len(parts) > 1 else None
    return command, argument

def check_win_condition():
    """
    Checks if the player has met the win condition.
    """
    if current_room == 'chamber_of_riddles' and 'glowing_orb' in inventory:
        return True
    return False

def handle_movement(command, argument):
    """
    Handles player movement between rooms.
    Returns True if movement was successful, False otherwise.
    """
    global current_room
    if command == 'go':
        if argument is None:
            print("Where do you want to go?")
            return False
        if argument in world[current_room]['exits']:
            current_room = world[current_room]['exits'][argument]
            print(world[current_room]['description'])
            room_items = world[current_room]['items']
            if room_items:
                print("Items here: " + ", ".join(room_items))
            else:
                print("There are no items in this room.")
            return True # Movement successful
        else:
            print("You can't go that way.")
            return False
    return False

def handle_look(command, argument):
    """
    Handles looking around the room or at specific items.
    """
    if command == 'look':
        if argument is None:
            print(world[current_room]['description'])
            room_items = world[current_room]['items']
            if room_items:
                print("Items here: " + ", ".join(room_items))
            else:
                print("There are no items in this room.")
            return True
        elif argument in world[current_room]['items'] or argument in inventory:
            if argument in items:
                print(items[argument]['description'])
                return True
            else: # Should not happen if data is consistent
                print("You see nothing special about it.")
                return False
        else:
            print("You don't see that here.")
            return False
    return False

def handle_take(command, argument):
    """
    Handles taking items from a room.
    Returns True if item was taken successfully, False otherwise.
    """
    global inventory
    if command == 'take':
        if argument is None:
            print("What do you want to take?")
            return False
        if argument in world[current_room]['items']:
            inventory.append(argument)
            world[current_room]['items'].remove(argument)
            print(f"You took the {argument}.")
            return True # Item taken successfully
        else:
            print("That item is not here.")
            return False
    return False

def handle_inventory(command):
    """
    Handles displaying the player's inventory.
    """
    if command == 'inventory':
        if not inventory:
            print("Your inventory is empty.")
        else:
            print("You are carrying:")
            for item_name in inventory:
                print(f"- {item_name}")
        return True
    return False

def main_game_loop():
    """
    Main loop for the game.
    """
    print("Welcome to The Whispering Library!")
    print(world[current_room]['description'])
    room_items = world[current_room]['items']
    if room_items:
        print("Items here: " + ", ".join(room_items))
    else:
        print("There are no items in this room.")

    while True:
        user_input = input("> ").strip()
        
        command, argument = parse_input(user_input)

        if command is None: 
            continue

        action_taken = False
        if command == 'quit':
            print("Thank you for visiting The Whispering Library. Goodbye!")
            break
        elif command == 'go':
            action_taken = handle_movement(command, argument)
        elif command == 'look':
            handle_look(command, argument) # Look doesn't change state for win condition
        elif command == 'take':
            action_taken = handle_take(command, argument)
        elif command == 'inventory':
            handle_inventory(command) # Inventory doesn't change state for win condition
        else:
            print("Unknown command. Try 'go', 'look', 'take', 'inventory', or 'quit'.")

        # Check for win condition after relevant actions
        if command in ['go', 'take'] and action_taken: # Only check if action was successful
            if check_win_condition():
                print("Congratulations! You have found the Glowing Orb in the Chamber of Riddles and unlocked its secrets! You win!")
                break
        # For the specific case where the player is already in the chamber and takes the orb.
        # The above check handles it, but if we wanted to be extremely explicit, we could add another check_win_condition() call
        # specifically within handle_take if the item taken is 'glowing_orb' and current_room is 'chamber_of_riddles'.
        # However, the current placement after the command block is sufficient.

if __name__ == "__main__":
    main_game_loop()

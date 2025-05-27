import unittest
import io
import sys
import copy

# Import game logic and world data
import game
from game_world import world as original_world, items as original_items

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        # Reset game state for each test
        game.current_room = 'entrance_hall'
        game.inventory = []
        # Deep copy world and items to prevent tests from interfering with each other
        game.world = copy.deepcopy(original_world)
        game.items = copy.deepcopy(original_items)

        # Redirect stdout to capture print statements
        self.held_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    # --- Test parse_input ---
    def test_parse_input_valid_command_with_arg(self):
        self.assertEqual(game.parse_input("go north"), ('go', 'north'))

    def test_parse_input_valid_command_no_arg(self):
        self.assertEqual(game.parse_input("inventory"), ('inventory', None))

    def test_parse_input_extra_args(self):
        # parse_input should only take the first two words
        self.assertEqual(game.parse_input("go north fast"), ('go', 'north'))

    def test_parse_input_empty(self):
        self.assertEqual(game.parse_input(""), (None, None))

    def test_parse_input_spaces_only(self):
        self.assertEqual(game.parse_input("   "), (None, None))

    # --- Test handle_movement ---
    def test_handle_movement_valid(self):
        initial_room = game.current_room
        self.assertTrue(game.handle_movement('go', 'east'))
        self.assertNotEqual(game.current_room, initial_room)
        self.assertEqual(game.current_room, 'hall_of_scrolls')
        output = sys.stdout.getvalue()
        self.assertIn(game.world['hall_of_scrolls']['description'], output)

    def test_handle_movement_invalid_direction(self):
        initial_room = game.current_room
        self.assertFalse(game.handle_movement('go', 'south'))
        self.assertEqual(game.current_room, initial_room) # Should not change room
        self.assertIn("You can't go that way.", sys.stdout.getvalue())

    def test_handle_movement_no_direction(self):
        initial_room = game.current_room
        self.assertFalse(game.handle_movement('go', None))
        self.assertEqual(game.current_room, initial_room)
        self.assertIn("Where do you want to go?", sys.stdout.getvalue())

    # --- Test handle_look ---
    def test_handle_look_room(self):
        game.handle_look('look', None)
        output = sys.stdout.getvalue()
        self.assertIn(game.world[game.current_room]['description'], output)
        if game.world[game.current_room]['items']:
            self.assertIn("Items here:", output)
        else:
            self.assertIn("There are no items in this room.", output)

    def test_handle_look_item_in_room(self):
        # Place an item in the current room for testing
        game.current_room = 'hall_of_scrolls' # This room has 'strange_scroll'
        game.handle_look('look', 'strange_scroll')
        self.assertIn(game.items['strange_scroll']['description'], sys.stdout.getvalue())

    def test_handle_look_item_in_inventory(self):
        game.inventory.append('dusty_tome')
        game.handle_look('look', 'dusty_tome')
        self.assertIn(game.items['dusty_tome']['description'], sys.stdout.getvalue())

    def test_handle_look_item_not_found(self):
        game.handle_look('look', 'non_existent_item')
        self.assertIn("You don't see that here.", sys.stdout.getvalue())

    # --- Test handle_take ---
    def test_handle_take_valid_item(self):
        game.current_room = 'hall_of_scrolls' # This room has 'strange_scroll'
        item_to_take = 'strange_scroll'
        self.assertTrue(game.handle_take('take', item_to_take))
        self.assertIn(item_to_take, game.inventory)
        self.assertNotIn(item_to_take, game.world[game.current_room]['items'])
        self.assertIn(f"You took the {item_to_take}.", sys.stdout.getvalue())

    def test_handle_take_item_not_in_room(self):
        game.current_room = 'entrance_hall' # This room has no items initially
        self.assertFalse(game.handle_take('take', 'strange_scroll'))
        self.assertNotIn('strange_scroll', game.inventory)
        self.assertIn("That item is not here.", sys.stdout.getvalue())

    def test_handle_take_no_argument(self):
        self.assertFalse(game.handle_take('take', None))
        self.assertIn("What do you want to take?", sys.stdout.getvalue())

    # --- Test handle_inventory ---
    def test_handle_inventory_empty(self):
        game.handle_inventory('inventory')
        self.assertIn("Your inventory is empty.", sys.stdout.getvalue())

    def test_handle_inventory_with_items(self):
        game.inventory.append('strange_scroll')
        game.inventory.append('dusty_tome')
        game.handle_inventory('inventory')
        output = sys.stdout.getvalue()
        self.assertIn("You are carrying:", output)
        self.assertIn("- strange_scroll", output)
        self.assertIn("- dusty_tome", output)

    # --- Test check_win_condition ---
    def test_check_win_condition_false_wrong_room(self):
        game.current_room = 'entrance_hall'
        game.inventory.append('glowing_orb')
        self.assertFalse(game.check_win_condition())

    def test_check_win_condition_false_no_item(self):
        game.current_room = 'chamber_of_riddles'
        self.assertFalse(game.check_win_condition()) # glowing_orb not in inventory

    def test_check_win_condition_false_item_not_orb(self):
        game.current_room = 'chamber_of_riddles'
        game.inventory.append('strange_scroll')
        self.assertFalse(game.check_win_condition())

    def test_check_win_condition_true(self):
        game.current_room = 'chamber_of_riddles'
        game.inventory.append('glowing_orb')
        self.assertTrue(game.check_win_condition())

if __name__ == '__main__':
    unittest.main()

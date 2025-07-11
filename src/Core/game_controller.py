from typing import Dict
import pygame
from typing import Callable, Any
from src.Core.event_dispatcher import EventDispatcher
from src.Core.chip import Chip
from src.GameUI.dragging_chip import DraggingChip
from src.Core.players import Player 
from src.GameUI.game_ui import GameUI
from src.Core.chip_tracker import ChipTracker
from src.Grids.board_grid import BoardGrid
from src.Grids.tray_grid import TrayGrid
from src.Core.game_rules import GameRules
from src.Core.chip_validator import ChipValidator
from src.GameUI.player_interaction import PlayerInteraction
from src.Core.move_manager import MoveManager
from src.GameUI.drag_manager import DragManager
from collections import Counter
import random

class GameController:
    sprites: dict[str, pygame.Surface]
    board_grid: BoardGrid
    dragging_chip: DraggingChip
    dispatcher: EventDispatcher
    players: list[Player]
    current_player_index: int
    current_player: Player
    chip_tracker: ChipTracker
    drag_manager: DragManager
    chip_validator: ChipValidator
    move_manager: MoveManager
    game_rules: GameRules
    player_interaction: PlayerInteraction
    game_ui: GameUI

    def __init__(self, sprites: Dict[str, pygame.Surface], dispatcher: EventDispatcher, players: int):
        self.sprites = sprites
        self.board_grid = BoardGrid()
        self.dragging_chip = DraggingChip()
        self.dispatcher = dispatcher
        self.players = self.create_players(players)
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]

        self.chip_tracker = ChipTracker(
            self.board_grid,
            self.players[self.current_player_index].tray_grid,
            self.dispatcher)
        self.generate_and_shuffle_hidden_chips()
        self.deal_initial_chips()
        self.subscribe_events()

        self.drag_manager = DragManager(
            self.chip_tracker, 
            self.dragging_chip, 
            self.dispatcher)  
       
        self.chip_validator = ChipValidator(
            self.chip_tracker, 
            self.drag_manager, 
            self.dispatcher)
       
        self.move_manager = MoveManager(
            self.chip_tracker, 
            self.chip_validator, 
            self.dispatcher)
        
        self.game_rules = GameRules(
            self.current_player, 
            self.chip_tracker, 
            self.chip_validator, 
            self.move_manager, 
            self.dispatcher)
        
        self.player_interaction = PlayerInteraction(
            self.chip_tracker,
            self.dispatcher,
            self.drag_manager)
        
        self.game_ui = GameUI(
            self.chip_tracker,
            self.chip_validator,
            self.dispatcher,
            self.player_interaction,
            self.drag_manager)

        self.first_player_initiated()



    def run(self) -> None:
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                self.player_interaction.handle_event(event) #testing stage
           
            self.draw()
            clock.tick(60)  


    def draw(self) -> None:
        self.game_ui.draw()  
        pygame.display.flip()  


    def create_players(self, number_of_players: int) -> list[Player]:
        players = []
        for player in range(1, number_of_players + 1):
            players.append(Player(f"Player {player}", TrayGrid()))

        return players


    def next_turn(self) -> None:
        self.game_rules.on_turn_end(self)
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        self.game_rules.current_player = self.current_player
        self.chip_tracker.tray_grid = self.current_player.tray_grid
        self.game_ui.current_player = self.current_player
        self.current_player.end_turn()
        self.move_manager.end_turn()
        self.player_interaction.next_player_turn_wait = True


    def generate_and_shuffle_hidden_chips(self) -> None:
        colors = ["red", "blue", "orange", "black"]
        numbers = range(1, 14)
        hidden_chips = []

        for color in colors:
            for number in numbers:
                for copy in range(2):  # Two of each chip
                    chip = Chip(self.sprites[f"{color}_{number}"], color=color, number=number, is_joker= False, copy=copy)
                    hidden_chips.append(chip)

        for i in range(2):
            chip = Chip(self.sprites['joker'], 'purple', None, True, copy=i) 
            hidden_chips.append(chip)

        random.shuffle(hidden_chips)
        self.chip_tracker.hidden_chips = hidden_chips


    def deal_initial_chips(self) -> None:
        for _ in range(14):
            for player in self.players:
                self.chip_tracker.tray_grid = player.tray_grid
                self.chip_tracker.place_chip_in_tray_from_hidden()
    

    def sort_chips_in_tray(self) -> None:
        for chip in self.chip_tracker.tray_grid.slots.values():
            if chip is not None:
        # if self.current_player.turn >= 3:
                (from_slots, from_chips, to_coordinates) = self.current_player.tray_grid.sort_chips_in_tray()
                if from_slots:
                    self.move_manager.move_history.append({
                        'action': f'chips_sorted',
                        'chip': from_chips,
                        'from': from_slots,
                        'to': to_coordinates})

                    return
        self.dispatcher.dispatch('error', message='No chips to sort')
# ...existing code...

    def check_chip_duplicates_and_missing(self, **kwargs: Callable[..., Any]) -> None:
        # Gather all chips from hidden, board, trays, and dragging
        all_chips = []
        all_chips.extend(self.chip_tracker.hidden_chips)
        all_chips.extend([chip for chip in self.chip_tracker.board_grid.slots.values() if chip is not None])
        for player in self.players:
            all_chips.extend([chip for chip in player.tray_grid.slots.values() if chip is not None])
        all_chips.extend([chip for chip in self.drag_manager.dragging_chip.chips if chip is not None])

        # Count chips by (color, number, is_joker)
        def chip_key(chip):
            return (chip.color, chip.number, chip.is_joker)

        chip_counts = Counter([chip_key(chip) for chip in all_chips])

        # Build expected set of chips
        expected_keys = []
        colors = ["red", "blue", "orange", "black"]
        numbers = range(1, 14)
        for color in colors:
            for number in numbers:
                expected_keys.append((color, number, False))
        expected_keys.append(("purple", None, True))  # Joker

        duplicates = []
        missing = []

        # Check for duplicates and missing chips
        for key in expected_keys:
            count = chip_counts.get(key, 0)
            if key[2]:  # is_joker
                expected = 2
            else:
                expected = 2
            if count > expected:
                duplicates.append((key, count))
            elif count < expected:
                missing.append((key, count))

        if duplicates:
            print("Duplicated chips found (more than 2):")
            for (color, number, is_joker), count in duplicates:
                if is_joker:
                    print(f"Joker (count: {count})")
                else:
                    print(f"{color} {number} (count: {count})")
        else:
            print("No duplicated chips found.")

        if missing:
            print("Missing chips (less than 2):")
            for (color, number, is_joker), count in missing:
                if is_joker:
                    print(f"Joker (count: {count})")
                else:
                    print(f"{color} {number} (count: {count})")
        else:
            print("No missing chips. All chips are present in correct quantity.")

    def error_manager(self, **kwargs: Callable[..., Any]) -> None:
        total_chips = 0
        hidden_chips = len(self.chip_tracker.hidden_chips)
        total_chips += hidden_chips
        chips_on_board = 0
        for chip in self.chip_tracker.board_grid.slots.values():
            if chip is not None:
                chips_on_board += 1
        total_chips += chips_on_board
        chip_in_trays = 0
        for player in self.players:
            for chip in player.tray_grid.slots.values():
                if chip is not None:
                    chip_in_trays += 1
        total_chips += chip_in_trays
        dragging_chip = len([chip for chip in self.drag_manager.dragging_chip.chips if chip != None])
        total_chips += dragging_chip
        print('error message')
        print(f"total chips: {total_chips} should be 106")
        print(f'hidden chips: {hidden_chips}')
        print(f'chip on board: {chips_on_board}')
        print(f'chips in trays: {chip_in_trays}')
        print(f'dragging_chip: {dragging_chip}')


    def subscribe_events(self) -> None:
        self.dispatcher.subscribe('next player turn', self.next_turn)
        self.dispatcher.subscribe('button Sort Chips pressed', self.sort_chips_in_tray)
        self.dispatcher.subscribe('Exit Game', self.exit_game)
        
        # self.dispatcher.subscribe('chip placed on slot' , self.check_chip_duplicates_and_missing) # for debugging
        # self.dispatcher.subscribe('multiple chips placed', self.check_chip_duplicates_and_missing)


    def exit_game(self) -> None:
        print('exited')
        pygame.quit()
        exit()


    def first_player_initiated(self) -> None:
        self.game_rules.on_turn_end(self)
        self.current_player = self.players[0]
        self.game_rules.current_player = self.current_player
        self.chip_tracker.tray_grid = self.current_player.tray_grid
        self.game_ui.current_player = self.current_player
        self.current_player.end_turn()
        self.move_manager.end_turn()



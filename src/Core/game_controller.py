from typing import Dict
import pygame
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
import random

class GameController:
    def __init__(self, sprites: Dict[str, pygame.Surface], dispathcer, players: int):
        self.sprites = sprites
        self.board_grid = BoardGrid()
        self.dragging_chip = DraggingChip()
        self.dispatcher = dispathcer
        self.players = self.create_players(players)
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]

        self.chip_tracker = ChipTracker(
            self.board_grid,
            self.players[self.current_player_index].tray_grid,
            self.dragging_chip,
            self.dispatcher
        )
        self.generate_and_shuffle_hidden_chips()
        self.deal_initial_chips()
        self.subscribe_events()

        self.drag_manager = DragManager(
            self.chip_tracker, 
            self.dragging_chip, 
            self.dispatcher)  # 
       
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

 
    

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                self.player_interaction.handle_event(event) #testing stage
            
           

            self.draw()
            clock.tick(60)  


    def draw(self):
        self.game_ui.draw()  
        pygame.display.flip()  


    def create_players(self, number_of_players):
        players = []
        for player in range(1, number_of_players + 1):
            players.append(Player(f"Player {player}", TrayGrid()))

        return players


    def next_turn(self):
        self.game_rules.on_turn_end(self)
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        self.game_rules.current_player = self.current_player
        self.chip_tracker.tray_grid = self.current_player.tray_grid
        self.game_ui.current_player = self.current_player
        self.current_player.end_turn()
        self.move_manager.end_turn()
        self.player_interaction.next_player_turn_wait = True
        print(f"Switched to {self.current_player.name}")


    def generate_and_shuffle_hidden_chips(self):
        colors = ["red", "blue", "orange", "black"]
        numbers = range(1, 14)
        hidden_chips = []

        for color in colors:
            for number in numbers:
                for copy in range(2):  # Two of each chip
                    chip = Chip(self.sprites[f"{color}_{number}_1"], color=color, number=number, is_joker= False, copy=copy)
                    hidden_chips.append(chip)

        for i in range(2):
            chip = Chip(self.sprites['joker'], 'purple', None, True, copy=i) 
            hidden_chips.append(chip)

        random.shuffle(hidden_chips)
        self.chip_tracker.hidden_chips = hidden_chips


    def deal_initial_chips(self):
        for _ in range(14):
            for player in self.players:
                # Temporarily set the tray_grid to the current player
                self.chip_tracker.tray_grid = player.tray_grid
                self.chip_tracker.place_chip_in_tray_from_hidden()
    
    def sort_chips_in_tray(self):
        if self.current_player.turn >= 3:
            (from_slots, from_chips, to_coordinates) = self.current_player.tray_grid.sort_chips_in_tray()
            if len(from_slots) > 0:
                self.move_manager.move_history.append({
                    'action': f'chips_sorted',
                    'chip': from_chips,
                    'from': from_slots,
                    'to': to_coordinates
                })
            
            return
        self.dispatcher.dispatch('error', message='Can only sort tray after 3 moves')

    def subscribe_events(self):
        self.dispatcher.subscribe('next player turn', self.next_turn)
        self.dispatcher.subscribe('button Sort Chips pressed', self.sort_chips_in_tray)
        self.dispatcher.subscribe('Exit Game', self.exit_game)
        
    def exit_game(self):
        print('exited')
        pygame.quit()
        exit()

    def first_player_initiated(self):
        self.game_rules.on_turn_end(self)
        self.current_player = self.players[0]
        self.game_rules.current_player = self.current_player
        self.chip_tracker.tray_grid = self.current_player.tray_grid
        self.game_ui.current_player = self.current_player
        self.current_player.end_turn()
        self.move_manager.end_turn()



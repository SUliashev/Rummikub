import pygame
from src.Core.chip import Chip
from src.Config.config import C
import random
import math

class GameUI:
    def __init__(self, chip_tracker, chip_validator, dispatcher, player_interaction, drag_manager):
        self.window = C.window 
        print('size', self.window.get_size())
        pygame.display.set_caption("Rummikub")
        self.chip_tracker = chip_tracker  # Use ChipTracker for chip management
        self.drag_manager = drag_manager
        self.chip_validator = chip_validator
        self.dispatcher = dispatcher
        self.player_interaction = player_interaction
        self.message = ""
        self.message_timer = 0 
        self.fireworks = []
        self.next_firework_time = pygame.time.get_ticks() + random.randint(500, 600)
    
        self.subscribe_events()

    def schedule_fireworks(self):
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_firework_time:
            self.launch_firework()
            self.next_firework_time = current_time + random.randint(500, 600)  # 1–3s until next firework

    def launch_firework(self):
        launch_x = random.randint(100, self.window.get_width() - 100)
        launch_y = self.window.get_height()
        pop_time = pygame.time.get_ticks() + random.randint(700, 1200)  # Time in air before pop
        color = random.choice([(255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 50)])
        self.fireworks.append({
            "x": launch_x,
            "y": launch_y,
            "vx": 0,
            "vy": -random.uniform(4, 7),
            "color": color,
            "popped": False,
            "pop_time": pop_time,
            "particles": []
        })

    def update_fireworks(self):
        current_time = pygame.time.get_ticks()
        for fw in self.fireworks:
            if not fw["popped"]:
                fw["y"] += fw["vy"]
                if current_time >= fw["pop_time"]:
                    fw["popped"] = True
                    for _ in range(50):  # more particles
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(2, 7)  # wider spread
                        fw["particles"].append({
                            "x": fw["x"],
                            "y": fw["y"],
                            "vx": math.cos(angle) * speed,
                            "vy": math.sin(angle) * speed,
                            "life": 60,
                            "color": fw["color"]
                        })
            else:
                for p in fw["particles"]:
                    p["x"] += p["vx"]
                    p["y"] += p["vy"]
                    p["vy"] += 0.12  # gravity
                    p["life"] -= 1
        self.fireworks = [fw for fw in self.fireworks if any(p["life"] > 0 for p in fw["particles"]) or not fw["popped"]]



    def draw_fireworks(self):
        for fw in self.fireworks:
            if not fw["popped"]:
                pygame.draw.circle(self.window, fw["color"], (int(fw["x"]), int(fw["y"])), 3)
            else:
                for p in fw["particles"]:
                    if p["life"] > 0:
                        alpha = max(0, min(255, p["life"] * 4))
                        particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
                        pygame.draw.circle(particle_surface, (*p["color"], alpha), (2, 2), 2)
                        self.window.blit(particle_surface, (p["x"], p["y"]))






    def write_current_player(self):
        if hasattr(self, "current_player"):
            player_name = self.current_player.name
        elif hasattr(self.chip_tracker, "current_player"):
            player_name = self.chip_tracker.current_player.name
        else:
            player_name = "Player"

        white = pygame.Rect(C.current_player_background_w)
        blue = pygame.Rect(C.current_player_background_b)
        pygame.draw.rect(self.window, (255,255,255), white, border_radius=5) 
        pygame.draw.rect(self.window, (50,100,100), blue, border_radius=5)  

        font_size = int(C.window_height * 0.05)
        font = pygame.font.SysFont(None, font_size)
        text = font.render(player_name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(C.window_width // 2, int(C.window_height * 0.06)))
        self.window.blit(text, C.current_player_xy)

    def draw_next_player_ready_overlay(self):
        if self.player_interaction.next_player_turn_wait == True:
            overlay = pygame.Surface((C.window_width, C.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))  # RGBA, alpha=120 for shade
            self.window.blit(overlay, (0, 0))


            button_rect = pygame.Rect(C.next_player_ready_button)
            pygame.draw.rect(self.window, (69, 69, 69), button_rect, border_radius=20)

            # Draw button text
            font_size = int(C.next_player_ready_button[3] * 0.5)
            font = pygame.font.SysFont(None, font_size)
            text = font.render("Next Player Ready", True, (255, 255, 255))
            text_rect = text.get_rect(center=button_rect.center)
            self.window.blit(text, text_rect)

            # Optionally, save the rect for click detection
            self.next_player_ready_rect = button_rect

    def subscribe_events(self):
        self.dispatcher.subscribe('error', self.set_message)
 
    def set_message(self, message):
        self.message = message
        self.message_timer = 120

    def draw_message(self):
        behind = pygame.Rect(C.error_message_behind)
        error_rect = pygame.Rect(C.error_message_rect)
        pygame.draw.rect(self.window, (255,255,255), behind, border_radius=5)  
        pygame.draw.rect(self.window, (50,100,100), error_rect, border_radius=5)
        
        if self.message and self.message_timer > 0:
            font = pygame.font.SysFont(None, int(C.error_message_rect[3]*0.8))
            text = font.render(self.message, True, (255, 255, 255))
            self.window.blit(text, C.error_message_coord)
            self.message_timer -= 1
        elif self.message_timer <= 0:
            self.message = ""


    def draw_selection_rectangle(self):
        if self.drag_manager.selection_start:
            x1, y1 = self.drag_manager.selection_start
            x2 = self.player_interaction.mouse_x
            y2 = self.player_interaction.mouse_y
            rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill((0, 120, 255, 60))  
            self.window.blit(s, rect.topleft)
            pygame.draw.rect(self.window, (0, 120, 255), rect, 2)


    def draw(self):
        self.window.fill((39,105,127))  # Clear the screen

        self.draw_tray_background()
        self.draw_tray_grid()

        self.draw_next_player_button()
        self.draw_message()
        self.write_current_player()
        
        self.draw_board_slots()
        self.draw_side_rectangle()
        self.draw_right_side_buttons()
        self.draw_incorrect_chip_combination()      # shows which combinations on the board are not valid
        self.draw_hovering_slot()
        self.draw_moving_chip()

        self.draw_selection_rectangle()
        self.show_selected_chips()
        self.draw_undo_all_confirmation()
        self.draw_next_player_ready_overlay()
        self.draw_tray_arrows()
        # self.schedule_fireworks()
        # self.update_fireworks()
        # self.draw_fireworks()
        


    def show_selected_chips(self):
        if self.drag_manager.selected_chips:
            if not self.drag_manager.dragging_multiple_chips:
            
                if self.drag_manager.selected_chips[0] == 'tray':
                    slots_to_highlight = C.tray_slot_coordinates
                else:
                    slots_to_highlight = C.board_slot_coordinates
                (row_type, chip_positions, chips_in_row) = self.drag_manager.selected_chips
                for indx, chip in enumerate(chips_in_row):
                    if chip is not None:
                        self.draw_chip_hue(*slots_to_highlight[chip_positions[indx]])
        
    def draw_side_rectangle(self):
        pygame.draw.rect(
            self.window,
            (200, 200, 200),  # Rectangle color
            (C.right_rect),
            border_radius=12
        )

    def draw_right_side_buttons(self):
        for button_name, rect in C.right_buttons.items():
            pygame.draw.rect(
                self.window,
                (69, 69, 69),  # Button color
                rect,
                border_radius=8
        )
            font_size = C.right_buttons_font_size[button_name]
            font = pygame.font.SysFont(None, font_size)
            text = font.render(button_name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))

            self.window.blit(text, text_rect)



    def draw_board_slots(self):
        draw_numbers_next_to_slots = True       # testing stage, adds numbers next to the slots on the board
        font = pygame.font.SysFont(None, 18)

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():
            x , y = C.board_slot_coordinates[row, col]
            if item_in_slot is None:
                    self.draw_empty_slot(x, y)
            else:
                self.draw_chip(item_in_slot, x, y)
            
            if draw_numbers_next_to_slots:
                col_text = font.render(str(col + 1), True, (200, 200, 0))
                self.window.blit(col_text, (x + 4, y + 2))


    def draw_chip(self, chip, x, y):
        chip_drawing = self.window.blit(chip.sprite, (x, y))
        return chip_drawing
    
    
    def draw_empty_slot(self, x: int, y: int):
        border_radius = 9
        thickness = 2
        pygame.draw.rect(
        self.window, (255, 255, 255),
        (x, y, C.chip_width, C.chip_height),
        thickness, border_radius=border_radius)
        
        
    def draw_hovering_slot(self):
        if not self.drag_manager.hovering_slot:
            return
        
        if len(self.drag_manager.dragging_chip.chips) == 1:
            grid_type, slot = self.drag_manager.hovering_slot 
            if slot is None:
                return      
            grid_coord = C.tray_slot_coordinates if grid_type == 'tray' else C.board_slot_coordinates
            x, y = grid_coord[slot]
   

            border_radius = 9
            rect = pygame.draw.rect(
                    self.window, (0, 30, 140),
                    (x, y, C.chip_width, C.chip_height),
                    3, border_radius=border_radius)
    
        if self.drag_manager.dragging_multiple_chips:
            self.draw_multiple_hovering_slots()
        

    def draw_multiple_hovering_slots(self):
        if self.drag_manager.multiple_hovering_slots:
            slot_type , slots = self.drag_manager.multiple_hovering_slots
            if slot_type == 'tray':
                slot_coordinates = C.tray_slot_coordinates
            else:
                slot_coordinates = C.board_slot_coordinates
            border_radius = 9
            for row, col in slots:
                x,y = slot_coordinates[row, col]
                rect = pygame.draw.rect(
                    self.window, (0, 30, 140),
                    (x, y, C.chip_width, C.chip_height),
                    3, border_radius=border_radius)
        
        
    def draw_incorrect_chip_combination(self):
        for (row, col), correct in self.chip_validator.slots_on_board.items():
            if not correct:
                self.draw_invalid_placed_chip_border(*C.board_slot_coordinates[row, col])
                

    def draw_invalid_placed_chip_border(self, x, y):       
        thickness = 5
        border_radius = 15
        pygame.draw.rect(
        self.window, (255, 0, 0),
        (x - thickness , y - thickness , C.chip_width + thickness * 2, C.chip_height  + thickness * 2),
        thickness, border_radius=border_radius)
        
            
    def draw_chip_hue(self, x, y, width=None, height=None, outline_thickness=10, border_radius=10):
        if width is None:
            width = C.chip_width
        if height is None:
            height = C.chip_height

        rect_x = x - outline_thickness // 2
        rect_y = y - outline_thickness // 2
        rect_w = width + outline_thickness
        rect_h = height + outline_thickness

        outline_surface = pygame.Surface((rect_w, rect_h), pygame.SRCALPHA)
        pygame.draw.rect(
            outline_surface,
            (255, 255, 255, 120),  # White with alpha for soft glow
            (0, 0, rect_w, rect_h),
            border_radius=border_radius
        )
        self.window.blit(outline_surface, (rect_x, rect_y))


    def draw_moving_chip(self):
        if self.drag_manager.dragging_chip.main_chip:
            chips = self.drag_manager.dragging_chip.chips
            if len(chips) == 1 or chips is None:
                chip = self.drag_manager.dragging_chip.main_chip
                x = self.player_interaction.mouse_x - C.chip_width / 2
                y = self.player_interaction.mouse_y - C.chip_height / 2

                # Draw the hue behind the chip
                self.draw_chip_hue(x, y)

                # Draw the chip itself
                self.draw_chip(chip, x, y)
                return
            else:
                self.draw_multiple_moving_chips()
        

    def draw_multiple_moving_chips(self):
        dc = self.drag_manager.dragging_chip
        if not hasattr(dc, "main_chip") or dc.main_chip is None:
            return

        chip_w = C.chip_width
        chip_h = C.chip_height
        spacing = C.slot_horizontal_spacing

        mouse_x = self.player_interaction.mouse_x
        mouse_y = self.player_interaction.mouse_y

        for i, chip in enumerate(reversed(dc.chips_to_left)):
            if chip is None:
                continue
            x = mouse_x - chip_w // 2 - (chip_w + spacing) * (i + 1)
            y = mouse_y - chip_h // 2
            self.draw_chip_hue(x, y)
            self.draw_chip(chip, x, y)

        x_main = mouse_x - chip_w // 2
        y_main = mouse_y - chip_h // 2
        self.draw_chip_hue(x_main, y_main)
        self.draw_chip(dc.main_chip, x_main, y_main)

        for i, chip in enumerate(dc.chips_to_right):
            if chip is None:
                continue
            x = mouse_x + (chip_w + spacing) * (i + 1) - chip_w // 2
            y = mouse_y - chip_h // 2
            self.draw_chip_hue(x, y)
            self.draw_chip(chip, x, y)          
         
        
    def draw_next_player_button(self): #to update later with config data
        button_rect = pygame.Rect(C.next_player_button[0])
        font_size = int(C.next_player_button[1])
        pygame.draw.rect(self.window, C.draw_button_color, button_rect, border_radius=12)
        font = pygame.font.SysFont(None, font_size)
        text = font.render("Next Player", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.window.blit(text, text_rect)


    def draw_tray_background(self):
        pygame.draw.rect(
            self.window,
            (69, 69, 69), 
            (C.tray_background_x, C.tray_background_y , C.tray_background_width ,  C.tray_background_height ),
            border_radius=20)
        

    def draw_tray_grid(self): 
        if self.player_interaction.next_player_turn_wait == False:
            tray_grid = self.chip_tracker.tray_grid
            start_row = tray_grid.visible_row_start
            end_row = start_row + 2
            for (row, col), (x, y) in C.tray_slot_coordinates.items():
                if start_row <= row < end_row:
                    item_in_slot = tray_grid.slots[(row, col)]
                    if item_in_slot is None:
                        self.draw_empty_slot(x, y)
                    elif isinstance(item_in_slot, Chip):
                        self.draw_chip(item_in_slot, x, y)       
    

    def draw_tray_arrows(self):
        arrow_width = C.tray_down_button[2]
        arrow_height = C.tray_down_button[3]
        x = C.tray_down_button[0]
        y_up = C.tray_up_button[1]
        y_down = C.tray_down_button[1]

        # Draw up arrow
        up_rect = pygame.Rect(x, y_up, arrow_width, arrow_height)
        pygame.draw.polygon(self.window, (200, 200, 200), [
            (x + arrow_width // 2, y_up),
            (x, y_up + arrow_height),
            (x + arrow_width, y_up + arrow_height)
        ])
        # Draw down arrow
        down_rect = pygame.Rect(x, y_down, arrow_width, arrow_height)
        pygame.draw.polygon(self.window, (200, 200, 200), [
            (x, y_down),
            (x + arrow_width, y_down),
            (x + arrow_width // 2, y_down + arrow_height)
        ])
        # Save rects for click detection
        self.tray_arrow_up_rect = up_rect
        self.tray_arrow_down_rect = down_rect

    def draw_undo_all_confirmation(self):
        if self.player_interaction.warning_window == True:
            overlay = pygame.Surface((C.window_width, C.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120)) 
            self.window.blit(overlay, (0, 0))

            width = C.window_width // 3
            height = C.window_height // 3
            x = (C.window_width - width) // 2
            y = (C.window_height - height) // 2
            pygame.draw.rect(self.window, (240, 240, 240), C.undo_all_white_rect, border_radius=15)
            pygame.draw.rect(self.window, (0, 0, 0), C.undo_all_black_rect, 3, border_radius=15)

        
            font = pygame.font.SysFont(None, int(C.undo_all_main_text_fontsize))
            text = font.render("Are you sure you want to undo all the moves?", True, (0, 0, 0))
            self.window.blit(text, (x + 60, y + 40))

            yes_rect = pygame.Rect(C.undo_cofirmation_button)
            pygame.draw.rect(self.window, (0, 200, 0), yes_rect, border_radius=10)
            yes_text = font.render("Yes", True, (255, 255, 255))
            self.window.blit(yes_text, (yes_rect.x + 25, yes_rect.y + 5))

            # No button (red)
            no_rect = pygame.Rect(x + width - 150, y + int(height* 0.8 ), 100, 40)
            pygame.draw.rect(self.window, (200, 0, 0), no_rect, border_radius=10)
            no_text = font.render("No", True, (255, 255, 255))
            self.window.blit(no_text, (no_rect.x + 30, no_rect.y + 5))

            # Save button rects for click detection
            self.undo_all_yes_rect = yes_rect
            self.undo_all_no_rect = no_rect
                





        









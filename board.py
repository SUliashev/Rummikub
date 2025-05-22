import pygame
from chip import Chip
from game_logic import GameLogic

class Board:
    chip_image = pygame.image.load("chips/red_1_1.png")  # Load a sample chip image
    chip_width = chip_image.get_width()
    chip_height = chip_image.get_height()

    def __init__(self, window):
        self.window = window  # Initialize the window
        self.game_logic = GameLogic()  # Initialize game logic
        self.row1 = {}  # 29 slots
        self.row2 = {}
        self.row3 = {}
        self.row4 = {}
        self.row5 = {}
        self.all_rows = [self.row1, self.row2, self.row3, self.row4, self.row5]
        self.is_dragging = False
        self.last_chip = None  # Track the last chip placed
        self.placed_chips = []  # Track chips placed on the board
        self.bottom_row_positions = []  # Track positions in the bottom row

        self.create_coordinates()

        # Initialize black chips numbered 1-7 for testing
        self.chips = []
        for i in range(7):
            x = 100 + i * Board.chip_width  # Separate chips by their width
            y = 800
            self.chips.append(Chip(x, y, f"chips/black_{i + 1}_1.png"))
            self.bottom_row_positions.append((x, y))  # Add initial positions to the bottom row tracker

    def create_coordinates(self):
        for i in range(29):
            self.row1[i] = (Board.chip_width * i, 0)
            self.row2[i] = (Board.chip_width * i, (Board.chip_height * 2))
            self.row3[i] = (Board.chip_width * i, Board.chip_height * 4)
            self.row4[i] = (Board.chip_width * i, Board.chip_height * 6)
            self.row5[i] = (Board.chip_width * i, Board.chip_height * 8)

    def draw_lines(self):
        for row in self.all_rows:
            for i in range(29):
                pygame.draw.rect(self.window, (255, 255, 255), (row[i][0], row[i][1], Board.chip_width, Board.chip_height), 2)

    def drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for chip in self.chips:
                if chip.x_line[0] <= mouse_pos[0] <= chip.x_line[1] and chip.y_line[0] <= mouse_pos[1] <= chip.y_line[1]:
                    self.is_dragging = chip  # Set the chip being dragged
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False

    def drag_to_slot(self):
        if self.is_dragging:
            # Update chip position while dragging
            mouse_pos = pygame.mouse.get_pos()
            self.is_dragging.x = mouse_pos[0] - self.is_dragging.width / 2
            self.is_dragging.y = mouse_pos[1] - self.is_dragging.height / 2
            self.is_dragging.update_boundaries()
        else:
            # Snap chip to the nearest slot when dragging stops
            for chip in self.chips:
                nearest_slot = None
                min_distance = float('inf')

                for row in self.all_rows:
                    for i in range(29):
                        slot_x, slot_y = row[i]
                        distance = ((chip.x - slot_x) ** 2 + (chip.y - slot_y) ** 2) ** 0.5

                        if distance < min_distance:
                            min_distance = distance
                            nearest_slot = (slot_x, slot_y)

                if nearest_slot:
                    chip.x, chip.y = nearest_slot
                    chip.update_boundaries()

                    # Track placed chips
                    self.placed_chips.append(chip)

                    # Inform GameLogic about the placement
                    slot_id = self.get_slot_id(nearest_slot)
                    self.game_logic.place_chip(chip, slot_id)

                    # Validate the combination if 3 chips are placed
                    if len(self.placed_chips) == 3:
                        if not self.game_logic.validate_combination(slot_id):
                            # If invalid, return all 3 chips to the bottom row
                            for placed_chip in self.placed_chips:
                                self.return_to_bottom_row(placed_chip)
                            self.placed_chips.clear()  # Clear the placed chips list

    def return_to_bottom_row(self, chip):
        """
        Return a chip to the next available position in the bottom row.
        """
        for x, y in self.bottom_row_positions:
            # Check if the position is already occupied
            if not any(c.x == x and c.y == y for c in self.chips):
                chip.x = x
                chip.y = y
                chip.update_boundaries()
                return

    def get_slot_id(self, slot_coordinates):
        """
        Convert slot coordinates to a unique slot ID.
        """
        # Implement logic to map (x, y) coordinates to a slot ID
        pass

    def draw(self):
        # Draw all chips and lines
        self.window.fill((0, 0, 0))  # Clear the screen
        self.draw_lines()
        for chip in self.chips:
            self.window.blit(chip.sprite, (chip.x, chip.y))


pygame.init()
window = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

board = Board(window)


for keys, value in board.row2.items():
    print(f"key: {keys}, values: {value}")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        board.drag(event)

    window.fill((0, 0, 0))
    board.draw()

    board.drag_to_slot()

    pygame.display.flip()
    clock.tick(60)



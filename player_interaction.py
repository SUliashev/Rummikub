import pygame

class PlayerInteraction:
    def __init__(self,  chip_tracker, tray):
        self.chip_tracker = chip_tracker
        self.tray = tray
        self.dragging_chip = False

    def is_mouse_over_tray(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tray_rect = pygame.Rect(self.tray.x, self.tray.y, self.tray.width, self.tray.height)
        return tray_rect.collidepoint(mouse_x, mouse_y)
    
    def pick_up_chip(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_mouse_over_tray():
                # Check tray chips only
                for chip in self.chip_tracker.chips:
                    if chip and chip.x_line[0] <= mouse_pos[0] <= chip.x_line[1] and chip.y_line[0] <= mouse_pos[1] <= chip.y_line[1]:
                        self.chip_tracker.remove_chip(chip)
                        self.dragging_chip = True

        print("cannot pick up chip, error 'pick_up_chip' in PI")
    
    def drag_chip(self, event):
        if self.dragging_chip:
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.chip_tracker.drag_chip(mouse_x, mouse_y)

    def release_chip(self, event):
        if self.dragging_chip:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.is_mouse_over_tray():
                    tray_slot = self.chip_tracker.choose_next_tray_slot(mouse_x, mouse_y)
                    if tray_slot:
                        self.chip_tracker.snap_chip_to_tray_slot(tray_slot)
                else:
                    board_slot = self.chip_tracker.choose_next_slot(mouse_x, mouse_y)
                    if board_slot:
                        self.chip_tracker.snap_chip_to_board_slot(board_slot)
                self.dragging_chip = False

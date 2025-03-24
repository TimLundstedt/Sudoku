import pygame
import time

# Properties
WIDTH, HEIGHT = 900, 900
GREY = (25, 39, 52)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
DARK_RED = (150, 0, 0)
DARK_GREEN = (0, 150, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
DARK_BLUE = (0, 0, 150)

sudoku_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

selected_cell = None
message = None
message_time = 0

def draw_buttons(screen, font, buttons, mouse_pos):
    for text, rect in buttons.items():
        color = (
            DARK_BLUE if rect.collidepoint(mouse_pos) else BLUE
        )
        pygame.draw.rect(screen, color, rect, border_radius=10)
                    
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

def event_handle(game_state, buttons):
    global selected_cell
    global sudoku_grid
    global message, message_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = "quit"
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = False
            if game_state == "sudoku":
                clicked = get_clicked_cell(event.pos, 225, 150, 50)
            if clicked:
                row, col = clicked
                if sudoku_grid[row][col] == 0:
                    selected_cell = (row, col)
            for button in buttons.items():
                if(buttons[button[0]].collidepoint(event.pos)):
                    game_state = button[0].lower()
                    selected_cell = None

        if event.type == pygame.KEYDOWN and selected_cell:
            if pygame.K_1 <= event.key <= pygame.K_9:
                num = event.key - pygame.K_0
                row, col = selected_cell
                if ctl_num_row(row, num) and ctl_num_col(col, num) and ctl_num_box(selected_cell, num):
                    sudoku_grid[row][col] = num
                    selected_cell = None
                else:
                    message = "Invalid Move!"
                    message_time = pygame.time.get_ticks()
        
    if game_state == "tips":
        game_state = "menu"

    return game_state

def ctl_num_row(row, num):
    global sudoku_grid
    size = len(sudoku_grid[row])
    for col in range(size):
        if sudoku_grid[row][col] == num:
            return False
        
    return True

def ctl_num_col(col, num):
    global sudoku_grid
    size = len(sudoku_grid)
    for row in range(size):
        if sudoku_grid[row][col] == num:
            return False
        
    return True

def ctl_num_box(selected_cell, num):
    global sudoku_grid
    grid_size = 3 
    sel_row, sel_col = selected_cell
    box_row = int(sel_row / grid_size) * grid_size
    box_col = int(sel_col / grid_size) * grid_size
    for i in range(grid_size):
        for j in range(grid_size):
            if sudoku_grid[box_row+i][box_col+j] == num:
                return False
            
    return True
    # print(f"row: {sel_row}, col: {sel_col}, the grid top_left corner is row: {row}, col: {col}")
    

def draw_sudoku_grid(screen):
    for i in range(10):
        length_box = 50
        length_line = length_box * 9
        width = 2
        padding_x = 225
        padding_y = 150

        if i % 3 == 0:
            width = 4

        pygame.draw.line(
            screen, BLACK,
            (padding_x + length_box * i, padding_y),
            (padding_x + length_box * i, padding_y + length_line),
            width
        )

        pygame.draw.line(
            screen, BLACK,
            (padding_x, padding_y + length_box * i),
            (padding_x + length_line, padding_y + length_box * i),
            width
        )

def draw_numbers(screen, font, sudoku_grid):
    length_box = 50
    padding_x = 225
    padding_y = 150

    for row in range(9):
        for col in range(9):
            num = sudoku_grid[row][col]
            if num != 0:
                text_surface = font.render(str(num), True, BLACK)
                text_rect = text_surface.get_rect(center=(
                    padding_x + col * length_box + length_box // 2,  
                    padding_y + row * length_box + length_box // 2  
                ))
                screen.blit(text_surface, text_rect)

def get_clicked_cell(mouse_pos, padding_x, padding_y, length_box):
    x, y = mouse_pos
    col = (x - padding_x) // length_box
    row = (y - padding_y) // length_box

    if 0 <= row < 9 and 0 <= col < 9:
        return row, col
    return None

def highlight_selected_cell(screen, selected_cell, padding_x, padding_y, length_box):
    if selected_cell:
        row, col = selected_cell
        pygame.draw.rect(
            screen, RED,
            (padding_x + col * length_box, padding_y + row * length_box, length_box, length_box),
            3
        )
def show_message(screen, text, font, color, position):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def show_message_timed(screen, font):
    global message, message_time
    if message:
        show_message(screen, message, font, RED, (WIDTH / 2, 50))
        if pygame.time.get_ticks() - message_time > 2000:
            message = None


def main():
    pygame.init()

    game_state = "menu"
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    button_width, button_height = 200, 60

    menu_buttons = {
        "Sudoku": pygame.Rect((WIDTH/2)-(button_width/2), 150, button_width, button_height),
        "Highscore": pygame.Rect((WIDTH/2)-(button_width/2), 250, button_width, button_height),
        "Quit": pygame.Rect((WIDTH/2)-(button_width/2), 350, button_width, button_height)
    }

    sudoku_buttons = {
        "Tips": pygame.Rect(100, (HEIGHT-(button_height*2)), button_width, button_height),
        "Menu": pygame.Rect(600, (HEIGHT-(button_height*2)), button_width, button_height)
    }

    font = pygame.font.Font(None, 40)

    running = True
    while running:

        if game_state == "menu":

            screen.fill(WHITE)

            mouse_pos = pygame.mouse.get_pos()

            draw_buttons(screen, font, menu_buttons, mouse_pos)
            game_state = event_handle(game_state, menu_buttons)

        elif game_state == "highscore":
            screen.fill(WHITE)

            mouse_pos = pygame.mouse.get_pos()

            draw_buttons(screen, font, menu_buttons, mouse_pos)
            game_state = event_handle(game_state, menu_buttons)
        
        elif game_state == "sudoku":
            screen.fill(WHITE)
            mouse_pos = pygame.mouse.get_pos()
            
            draw_sudoku_grid(screen)
            draw_numbers(screen, font, sudoku_grid)
            draw_buttons(screen, font, sudoku_buttons, mouse_pos)
            highlight_selected_cell(screen, selected_cell, 225, 150, 50)
            show_message_timed(screen, font)

            game_state = event_handle(game_state, sudoku_buttons)

        elif game_state == "quit":
            running = False

        pygame.display.flip()
        pygame.display.set_caption(game_state.capitalize())

    pygame.quit()

if __name__ == "__main__":
    main()
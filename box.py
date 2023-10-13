import pygame
import random
from pygame import mixer
import sys

# Initialize Pygame
pygame.init()

# Initialize the Pygame mixer
pygame.mixer.init()

WIDTH, HEIGHT = 900, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BoXeS")
clock = pygame.time.Clock()
run = True

# Define some constants
FPS = 60
GREY = (128, 128, 128)
DARKGREY = (65, 65, 65)
GRADIENT_START = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
COLOUR = GRADIENT_START
WIDTH_OF_LINE = 5
inc_or_dec_up_down = -1
inc_or_dec_left_right = 1
inc_value = HEIGHT / 100
x_pos = 0.2 * WIDTH + 2 * WIDTH_OF_LINE
y_pos = 0.8 * HEIGHT
counter = 10

color_inc_or_dec = [1, 1, 1]

# Slider properties
SLIDER_X = 50
SLIDER_Y = 50
SLIDER_WIDTH = 200
SLIDER_HEIGHT = 10
SLIDER_HANDLE_RADIUS = 15
SLIDER_COLOR = (0, 0, 0)
SLIDER_HANDLE_COLOR = (255, 0, 0)
slider_value = 0.5  # Initial volume value

# Flag to indicate slider dragging
slider_dragging = False

# List to store box positions and colors
box_data = []

# Function to update volume based on the slider position
def update_volume():
    volume = slider_value
    mixer.music.set_volume(volume)

def new_colour(colour):
    global color_inc_or_dec
    colour = list(colour)
    index = random.randint(0, 2)
    if (colour[index] >= 230) or (colour[index] <= 0):
        color_inc_or_dec[index] *= -1
    colour[index] = (colour[index] + counter * color_inc_or_dec[index])
    return tuple(colour)

def draw_window():
    global x_pos, y_pos, inc_or_dec_left_right, inc_or_dec_up_down, COLOUR

    outer_box = pygame.Rect(0.2 * WIDTH + WIDTH_OF_LINE, 0.1 * HEIGHT + WIDTH_OF_LINE, 0.6 * WIDTH, 0.8 * HEIGHT)
    inner_box = pygame.Rect(x_pos, y_pos, 0.1 * HEIGHT, 0.1 * HEIGHT)
    COLOUR = new_colour(COLOUR)

    WIN.fill(GREY)
    pygame.draw.rect(WIN, SLIDER_COLOR, (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT))

    slider_handle_x = SLIDER_X + int(slider_value * SLIDER_WIDTH)
    slider_handle_x = max(SLIDER_X, min(SLIDER_X + SLIDER_WIDTH, slider_handle_x))
    pygame.draw.circle(WIN, SLIDER_HANDLE_COLOR, (slider_handle_x, SLIDER_Y + SLIDER_HEIGHT // 2), SLIDER_HANDLE_RADIUS)

    pygame.draw.rect(WIN, WHITE, outer_box, width=WIDTH_OF_LINE)
    pygame.draw.rect(WIN, COLOUR, inner_box)
    pygame.draw.rect(WIN, DARKGREY, inner_box, width=WIDTH_OF_LINE // 2)

    if outer_box.colliderect(inner_box):
        if outer_box.top >= inner_box.top:
            inc_or_dec_up_down *= -1

        if outer_box.bottom <= inner_box.bottom:
            inc_or_dec_up_down *= -1

        if outer_box.right <= inner_box.right:
            inc_or_dec_left_right *= -1

        if outer_box.left >= inner_box.left:
            inc_or_dec_left_right *= -1

    x_pos += inc_value * inc_or_dec_left_right
    y_pos += inc_value * inc_or_dec_up_down

    # Draw the trailing boxes with random colors
    for pos, color in box_data:
        pygame.draw.rect(WIN, color, pos)
        pygame.draw.rect(WIN, DARKGREY, pos, width=1)  # Border

    pygame.display.update()
    pygame.time.delay(60)

def main():
    global run, slider_value, slider_dragging, box_data

    WIN.fill(GREY)
    update_volume()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if (
                        SLIDER_X <= mouse_x <= SLIDER_X + SLIDER_WIDTH
                        and SLIDER_Y <= mouse_y <= SLIDER_Y + SLIDER_HEIGHT
                    ):
                        slider_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    slider_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if slider_dragging:
                    mouse_x, _ = event.pos
                    slider_value = max(0, min(1, (mouse_x - SLIDER_X) / SLIDER_WIDTH))
                    update_volume()

        # Store the current slider position as a rectangle with a random color and append it to the list
        box_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        box_data.append((pygame.Rect(x_pos, y_pos, 0.1 * HEIGHT, 0.1 * HEIGHT), box_color))

        draw_window()

if __name__ == "__main__":
    main()

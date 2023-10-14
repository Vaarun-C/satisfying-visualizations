import pygame
import random
from pygame import mixer


# Initialize Pygame
pygame.init()

# Initialize the Pygame mixer
pygame.mixer.init()
pygame.mixer.init()
mixer.music.load("gg.mp3")

volume = 0.5
mixer.music.set_volume(volume)


mixer.music.play(-1)
collision_sound = mixer.Sound("durm.mp3")
collision_sound.set_volume(volume)

WIDTH, HEIGHT = 900, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BoXeS")
clock = pygame.time.Clock()
run = True

FPS = 60
GREY = (128, 128, 128)
DARKGREY = (65, 65, 65)
GRADIENT_START = (30,30,30)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
COLOUR = GRADIENT_START
WIDTH_OF_LINE = 5
inc_or_dec_up_down = -1
inc_or_dec_left_right = 1
x_pos = random.randint(100, 500)
y_pos = random.randint(200, 400)
inc_value = HEIGHT/100
#x_pos = 0.2*WIDTH+2*WIDTH_OF_LINE
#y_pos = 0.8 * HEIGHT
counter = 10

color_inc_or_dec = [1,1,1]

def new_colour(colour):

    global color_inc_or_dec

    colour = list(colour)
    index = random.randint(0, 2)
    if(colour[index] >= 230) or (colour[index] <= 0):
        color_inc_or_dec[index] *= -1
    colour[index] = (colour[index] + counter*color_inc_or_dec[index])
    return tuple(colour)


#function to adjust volume with up and down keys
def adjust_volume(increase):
    global volume
    if increase:
        if volume < 1.0:
            volume += 0.1
    else:
        if volume > 0.0:
            volume -= 0.1
    mixer.music.set_volume(volume)
    collision_sound.set_volume(volume)

def draw_window():

    global x_pos, y_pos, inc_or_dec_left_right, inc_or_dec_up_down, COLOUR

    outer_box = pygame.Rect(0.2*WIDTH+WIDTH_OF_LINE, 0.1*HEIGHT+WIDTH_OF_LINE, 0.6*WIDTH, 0.8*HEIGHT)
    inner_box = pygame.Rect(x_pos, y_pos, 0.1 * HEIGHT, 0.1*HEIGHT)
    COLOUR = new_colour(COLOUR)
    # print(COLOUR)

    pygame.draw.rect(WIN, WHITE, outer_box, width=WIDTH_OF_LINE)
    pygame.draw.rect(WIN, COLOUR, inner_box)
    pygame.draw.rect(WIN, DARKGREY, inner_box, width=WIDTH_OF_LINE//2)

    if outer_box.colliderect(inner_box):
        if outer_box.top >= inner_box.top:
            collision_sound.play()
            # collision_direction: top
            inc_or_dec_up_down *= -1

        if outer_box.bottom <= inner_box.bottom:
            collision_sound.play()
            # collision_direction: bottom
            inc_or_dec_up_down *= -1

        if outer_box.right <= inner_box.right:
            collision_sound.play()
            # collision_direction: left
            inc_or_dec_left_right *= -1

        if outer_box.left >= inner_box.left:
            collision_sound.play()
            # collision_direction: right
            inc_or_dec_left_right *= -1


    x_pos += inc_value*inc_or_dec_left_right
    y_pos += inc_value*inc_or_dec_up_down

    pygame.display.update()
    pygame.time.delay(60)


def main():
    global run
    WIN.fill(GREY)

    # Main game loop    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    adjust_volume(True)  # Increase volume
                elif event.key == pygame.K_DOWN:
                    adjust_volume(False)  # Decrease volume
                    
        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
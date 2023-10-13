import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Initialize the Pygame mixer
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("POLYRYTHMS")
clock = pygame.time.Clock()
run = True

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)

FPS = 60
NUM_ARCS = 15
THICKNESS = 5
TIME = 0
GRADIENT_START = (192, 57, 43)
GRADIENT_END = (142, 68, 173)
FREQ_START = 120
FREQ_END = 330
SAMPLING_RATE = 44100
DURATION = 0.1
COOLDOWN = 0.5
FREQ_COOLDOWN = {}
SYNC_TIME = 300
START_VELOCITY = 50

# Initialize volume (0.0 to 1.0)
volume = 0.5

# Generate a sound with a given frequency and duration
def generate_note(frequency, duration):
    num_samples = int(SAMPLING_RATE * duration)
    sound_data = np.zeros(num_samples, dtype=np.int16)

    for i in range(num_samples):
        t = float(i) / SAMPLING_RATE
        value = int(32767.0 * 0.5 * math.sin(2.0 * math.pi * frequency * t))
        sound_data[i] = value

    sound = pygame.mixer.Sound(buffer=sound_data)
    return sound

def lerp_sound(start_freq, end_freq, t):
    return (start_freq + t * (end_freq - start_freq))

def lerp_color_rgb(color1, color2, t):
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    r = int(r1 + t * (r2 - r1))
    g = int(g1 + t * (g2 - g1))
    b = int(b1 + t * (b2 - b1))

    return r, g, b

# Move the sliders around the arcs
def move_sliders(center, radii, line_y):
    global TIME

    slider_radius = 5

    delta_time = clock.tick(FPS) / 1000.0
    TIME += delta_time

    for i, radius in enumerate(radii):
        velocity = (2 * math.pi * (START_VELOCITY - i)) / SYNC_TIME
        angle = velocity * TIME % (2 * math.pi)
        if (angle > math.pi):
            angle = -angle
        x = center[0] - radius * math.cos(angle)
        y = center[1] - radius * math.sin(angle)
        pygame.draw.circle(WIN, WHITE, (x, y), slider_radius)

        if y >= line_y - slider_radius:
            pygame.draw.line(WIN, GREY, (x - 2 * slider_radius, line_y), (x + 2 * slider_radius, line_y), THICKNESS)
            if TIME > 1:
                freq = lerp_sound(FREQ_START, FREQ_END, i / (len(radii) - 1))

                if freq not in FREQ_COOLDOWN or (TIME - FREQ_COOLDOWN[freq]) >= COOLDOWN:
                    note = generate_note(freq, DURATION)
                    note.set_volume(volume)  # Set volume for the note
                    note.play()
                    FREQ_COOLDOWN[freq] = TIME

# Draw the window
def draw_window():

    start = (0.2 * WIDTH, 0.9 * HEIGHT)
    end = (0.8 * WIDTH, 0.9 * HEIGHT)
    center = (start[0] + (end[0] - start[0]) // 2, start[1] + (end[1] - start[1]) // 2)

    radii = []

    length = end[0] - start[0]
    for i in range(NUM_ARCS):
        radius = (length // (2 * NUM_ARCS)) * (i + 1)
        coords = (center[0] - radius, center[1] - radius, 2 * radius, 2 * radius)
        pygame.draw.arc(WIN, lerp_color_rgb(GRADIENT_START, GRADIENT_END, i / (NUM_ARCS - 1)), coords, 0, math.pi, THICKNESS)
        radii.append(radius)

    pygame.draw.line(WIN, WHITE, start, end, THICKNESS)

    move_sliders(center, radii, end[1])

    # Draw a volume slider
    pygame.draw.rect(WIN, GREY, (20, 20, 20, 250))
    pygame.draw.rect(WIN, WHITE, (20, 20 + 230 * (1 - volume), 20, 20))

    pygame.display.update()

# Main loop
def main():
    global run, volume

    while run:
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 20 <= event.pos[0] <= 40 and 20 <= event.pos[1] <= 270:
                    # Clicked on the volume slider
                    volume = 1 - (event.pos[1] - 20) / 250.0
                    pygame.mixer.music.set_volume(volume)  # Set system audio volume

        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()

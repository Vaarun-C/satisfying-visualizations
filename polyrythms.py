import pygame
import math
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

note_dictionary = {
    98: "A#8",
    97: "A8",
    96: "G#8",
    95: "G8",
    94: "F#8",
    93: "F8",
    92: "E8",
    91: "D#8",
    90: "D8",
    89: "C#8",
    88: "C8",
    87: "B7",
    86: "A#7",
    85: "A7",
    84: "G#7",
    83: "G7",
    82: "F#7",
    81: "F7",
    80: "E7",
    79: "D#7",
    78: "D7",
    77: "C#7",
    76: "C7",
    75: "B6",
    74: "A#6",
    73: "A6",
    72: "G#6",
    71: "G6",
    70: "F#6",
    69: "F6",
    68: "E6",
    67: "D#6",
    66: "D6",
    65: "C#6",
    64: "C6",
    63: "B5",
    62: "A#5",
    61: "A5",
    60: "G#5",
    59: "G5",
    58: "F#5",
    57: "F5",
    56: "E5",
    55: "D#5",
    54: "D5",
    53: "C#5",
    52: "C5",
    51: "B4",
    50: "A#4",
    49: "A4",
    48: "G#4",
    47: "G4",
    46: "F#4",
    45: "F4",
    44: "E4",
    43: "D#4",
    42: "D4",
    41: "C#4",
    40: "C4",
    39: "B3",
    38: "A#3",
    37: "A3",
    36: "G#3",
    35: "G3",
    34: "F#3",
    33: "F3",
    32: "E3",
    31: "D#3",
    30: "D3",
    29: "C#3",
    28: "C3",
    27: "B2",
    26: "A#2",
    25: "A2",
    24: "G#2",
    23: "G2",
    22: "F#2",
    21: "F2",
    20: "E2",
    19: "D#2",
    18: "D2",
    17: "C#2",
    16: "C2",
    15: "B1",
    14: "A#1",
    13: "A1",
    12: "G#1",
    11: "G1",
    10: "F#1",
    9: "F1",
    8: "E1",
    7: "D#1",
    6: "D1",
    5: "C#1",
    4: "C1",
    3: "B0",
    2: "A#0",
    1: "A0",
    0: "G#0",
    -1: "G0",
    -2: "F#0",
    -3: "F0",
    -4: "E0",
    -5: "D#0",
    -6: "D0",
    -7: "C#0",
    -8: "C0 "
}


pygame.init()
pygame.mixer.init()

# Initialize Pygame
pygame.init()

# Initialize the Pygame mixer
pygame.mixer.init()

def note_to_midi(frequency):
    A4_freq = 440.0  # Frequency of A4 (MIDI note 69)
    return int(round(12 * (math.log2(frequency) - math.log2(A4_freq)) + 69))

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("POLYRYTHMS")
clock = pygame.time.Clock()
run = True

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0,0,0)
GREY = (192,192,192)

FPS = 60
NUM_ARCS = 15
THICKNESS = 5
TIME = 0
GRADIENT_START = (192,57,43)
GRADIENT_END = (142,68,173)
FREQ_START = 120
FREQ_END = 330
SAMPLING_RATE = 44100
DURATION = 0.1
COOLDOWN = 0.5
FREQ_COOLDOWN = {}
SYNC_TIME = 300

START_VELOCITY = 50

def generate_note(frequency, duration):
    num_samples = int(SAMPLING_RATE * duration)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    sound_data = (32767.0 * 0.5 * np.sin(2.0 * np.pi * frequency * t)).astype(np.int16)
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

def move_sliders(center, radii, line_y):
    global TIME

    slider_radius = 5

    delta_time = clock.tick(FPS) / 1000.0
    TIME += delta_time

    for i,radius in enumerate(radii):
        velocity = (2*math.pi * (START_VELOCITY-i))/SYNC_TIME
        angle = velocity*TIME % (2*math.pi)
        if(angle>math.pi):
            angle = -angle
        x = center[0]-radius*math.cos(angle)
        y = center[1]-radius*math.sin(angle)
        pygame.draw.circle(WIN, WHITE, (int(x), int(y)), slider_radius)

        if y >= line_y-slider_radius:
            pygame.draw.line(WIN, GREY, (int(x-2*slider_radius),int(line_y)), (int(x+2*slider_radius),int(line_y)), THICKNESS)
            if TIME > 1:
                freq = lerp_sound(FREQ_START, FREQ_END, i / (len(radii) - 1))
                noteNum = note_to_midi(freq)

                if noteNum not in FREQ_COOLDOWN or (TIME - FREQ_COOLDOWN[noteNum]) >= COOLDOWN:
                    note = generate_note(freq, DURATION)
                    note.play()
                    FREQ_COOLDOWN[noteNum] = TIME

def draw_window():
    start = (0.2*WIDTH, 0.9*HEIGHT)
    end = (0.8*WIDTH, 0.9*HEIGHT)
    center = (start[0]+(end[0] - start[0])//2, start[1]+(end[1] - start[1])//2)

    radii = []

    length = end[0] - start[0]
    for i in range(NUM_ARCS):
        radius = (length//(2*NUM_ARCS))*(i+1)
        coords = (int(center[0]-radius), int(center[1]-radius), int(2*radius), int(2*radius))
        pygame.draw.arc(WIN, lerp_color_rgb(GRADIENT_START, GRADIENT_END, i / (NUM_ARCS - 1)), coords, 0, math.pi, THICKNESS)
        radii.append(radius)

    pygame.draw.line(WIN, WHITE, start, end, THICKNESS)

    move_sliders(center, radii, end[1])

    pygame.display.update()

def main():
    global run

    # Main game loop    
    while run:
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()

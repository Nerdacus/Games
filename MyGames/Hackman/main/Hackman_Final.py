import pygame
import sys
import random

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 520
BACKGROUND_COLOR = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PROGRESS_BAR_COLOR = (0, 0, 255)
DOT_RADIUS = 5
TERMINAL_SIZE = 20
PROGRESS_BAR_HEIGHT = 20
HACKMAN_RADIUS = 15
GHOST_SIZE = 20
GHOST_SPEED = 10
GRID_SIZE = 40
MAX_HACKING_TIME = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hack-Man")

clock = pygame.time.Clock()

# Initial position of hackman
hackman_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
hackman_y = ((SCREEN_HEIGHT // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2

font = pygame.font.SysFont(None, 36)

right_frames = []
left_frames = []
up_frames = []
down_frames = []

right_frame_paths = [
    "right-frame-one.png",
    "right-frame-two.png",
    "right-frame-three.png",
    "right-frame-four.png"
]

left_frame_paths = [
    "left-frame-one.png",
    "left-frame-two.png",
    "left-frame-three.png",
    "left-frame-four.png"
]

up_frame_paths = [
    "up-frame-one.png",
    "up-frame-two.png",
    "up-frame-three.png",
    "up-frame-four.png"
]

down_frame_paths = [
    "down-frame-one.png",
    "down-frame-two.png",
    "down-frame-three.png",
    "down-frame-four.png"
]

for path in right_frame_paths:
    image = pygame.image.load(path).convert_alpha()
    right_frames.append(image)

for path in left_frame_paths:
    image = pygame.image.load(path).convert_alpha()
    left_frames.append(image)

for path in up_frame_paths:
    image = pygame.image.load(path).convert_alpha()
    up_frames.append(image)

for path in down_frame_paths:
    image = pygame.image.load(path).convert_alpha()
    down_frames.append(image)

no_movement_image = pygame.image.load('no-movement.png').convert_alpha()
terminal_image = pygame.image.load('terminal.png').convert_alpha()
ghost1_image = pygame.image.load('ghost1.png').convert_alpha()
ghost2_image = pygame.image.load('ghost2.png').convert_alpha()
ghost3_image = pygame.image.load('ghost3.png').convert_alpha()
ghost4_image = pygame.image.load('ghost4.png').convert_alpha()

initial_maze_layout = [
    "####################",
    "#..................#",
    "#.###.#####.#.####..#",
    "#.#...#.....#.#.....#",
    "#.#.#...#.#.#.#.#.#.#",
    "#...#.#.......#.#...#",
    "###.#.##....#.#.#...#",
    "#...#.#.....#.#.#...#",
    "#.###.#.###.#.#.###.#",
    "#.....#...#...#...#.#",
    "#.#####.#.#####.#.###",
    "#.................#",
    "####################"
]

hacked_maze_layout = [
    "####################",
    "#..................#",
    "#.###.#####.#.####..#",
    "#.#...#.....#.#.....#",
    "#.#.#...#.#.#.#.#.#.#",
    "#...#.#.......#.#...#",
    "###.#.##....#.#.#...#",
    "#...#.#.....#.#.#...#",
    "#.###.#.###.#.#.###.#",
    "#.....#...#...#...#.#",
    "#.#####.#.#####.#.###",
    "#.................#",
    "####.###########.###"
]

final_maze_layout = [
    "##########.#########",
    "#.#................#",
    "###................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "####################"
]

final_hacked_layout = [
    "##########.#########",
    "#.#................#",
    "#.#................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "####################"
]

ghost_spawn_x, ghost_spawn_y = 360, 160

ghost_path = [
    (360, 220), (400, 160),
    (440, 100), (480, 160), (520, 220), (480, 280), (440, 340),
    (400, 280), (360, 220), (320, 160), (280, 100), (240, 160),
    (200, 220), (240, 280), (280, 340), (320, 280), (360, 220),
]

ghost_2_path = [
    (620, 460), (660, 460), (700, 460), (700, 420), (700, 380), (660, 380), (620, 380), (620, 340),
    (620, 300), (620, 260), (620, 220), (620, 180), (620, 140), (660, 140), (700, 140), (700, 180),
    (700, 220), (700, 260), (700, 300), (740, 300), (780, 300), (780, 260), (780, 220), (780, 180),
    (780, 140), (740, 140), (700, 140), (660, 140), (620, 140), (620, 180), (620, 220), (620, 260),
    (620, 300), (620, 340), (620, 380), (620, 420), (620, 460)
]

ghost_x, ghost_y = ghost_spawn_x, ghost_spawn_y
path_index = 1
ghost_2_x, ghost_2_y = ghost_2_path[0]
path_index_2 = 1
ghost_3_x = 460
ghost_3_y = 60
ghost_4_x = 380
ghost_4_y = 140
ghost_3_active = False
ghost_4_active = False

current_maze_layout = initial_maze_layout

initial_grid = []
final_grid = []

for row, line in enumerate(initial_maze_layout):
    for col, char in enumerate(line):
        if char == '.':
            initial_grid.append((col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))

for row, line in enumerate(final_maze_layout):
    for col, char in enumerate(line):
        if char == '.':
            final_grid.append((col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))

initial_terminals = [
    (360, 160)
]

final_terminals = [
    (380, 140),
    (620, 420),
    (140, 140)

]

grid = initial_grid
terminals = initial_terminals

for i in range(len(terminals)):
    terminals[i] = ((terminals[i][0] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2,
                    (terminals[i][1] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2)

hacked_terminals = [False] * len(terminals)

running = True
score = 0
frame_count = 0
hacking = False
hacking_time = 0
spacebar_held = False
hackman_old_x = hackman_x
hackman_old_y = hackman_y


def within_boundary(x, y):
    return 60 <= x <= 740 and 60 <= y <= 460


def setup_game_state(map_layout):
    global current_maze_layout, terminals, hacked_terminals, hackman_x, hackman_y, hackman_old_x, hackman_old_y, grid

    current_maze_layout = map_layout

    hackman_old_x = hackman_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
    hackman_old_y = hackman_y = ((SCREEN_HEIGHT // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2

    terminals = [
        (360, 160)
    ]

    for i in range(len(terminals)):
        terminals[i] = ((terminals[i][0] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2,
                        (terminals[i][1] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2)
    hacked_terminals = [False] * len(terminals)

    hackman_x = SCREEN_WIDTH // 2
    hackman_y = SCREEN_HEIGHT // 2

    hackman_x = ((hackman_x // GRID_SIZE) * GRID_SIZE) + GRID_SIZE // 2
    hackman_y = ((hackman_y // GRID_SIZE) * GRID_SIZE) + GRID_SIZE // 2

    if current_maze_layout == hacked_maze_layout:
        hackman_x = 380
        hackman_y = 180

    if map_layout == final_maze_layout:
        hackman_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
        hackman_y = ((SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2

        terminals = []
        for pos in final_terminals:
            terminals.append(
                ((pos[0] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2, (pos[1] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2)
            )

        grid = []
        for [row, line] in enumerate(final_maze_layout):
            for [col, char] in enumerate(line):
                if char == '.':
                    grid.append((col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))

        hacked_terminals = [False] * len(terminals)

    hackman_old_x = hackman_x
    hackman_old_y = hackman_y


mrs_hackman_right_image = pygame.image.load('mrs-hackman-right-one.png').convert_alpha()
mrs_hackman_left_image = pygame.image.load('mrs-hackman-left.png').convert_alpha()
mrs_hackman_down_image = pygame.image.load('mrs-hackman-down.png').convert_alpha()
mrs_hackman_up_image = pygame.image.load('mrs-hackman-up.png').convert_alpha()

mrs_hackman_x = 60
mrs_hackman_y = 60

mrs_hackman_actived = False
mrs_hackman_direction = 'right'


def remove_wall():
    global current_maze_layout

    if current_maze_layout == final_maze_layout and any(hacked_terminals):
        wall_position_to_remove = (1, 2)
        if current_maze_layout[wall_position_to_remove[1]][wall_position_to_remove[0]] == '#':
            current_maze_layout[wall_position_to_remove[1]] = current_maze_layout[wall_position_to_remove[1]][
                                                              :wall_position_to_remove[0]] + '.' + \
                                                              current_maze_layout[wall_position_to_remove[1]][
                                                              wall_position_to_remove[0] + 1:]


def activate_mrs_hackman():
    global mrs_hackman_actived

    if current_maze_layout == final_maze_layout:
        mrs_hackman_actived = True


def move_mrs_hackman():
    global mrs_hackman_x, mrs_hackman_y, mrs_hackman_direction, new_x, new_y, score

    direction = random.randint(0, 100)

    if current_maze_layout == final_hacked_layout and mrs_hackman_actived:
        movement_speed: int = GRID_SIZE
        if direction <= 25:
            mrs_hackman_direction = 'right'
            new_x = mrs_hackman_x + movement_speed
            if within_boundary(new_x, mrs_hackman_y):
                mrs_hackman_x = new_x

        elif 25 < direction <= 50:
            mrs_hackman_direction = 'down'
            new_y = mrs_hackman_y + movement_speed
            if within_boundary(mrs_hackman_x, new_y):
                mrs_hackman_y = new_y

        elif 50 < direction <= 75:
            mrs_hackman_direction = 'left'
            new_x = mrs_hackman_x - movement_speed
            if within_boundary(new_x, mrs_hackman_y):
                mrs_hackman_x = new_x

        elif direction > 75:
            mrs_hackman_direction = 'up'
            new_y = mrs_hackman_y - movement_speed
            if within_boundary(mrs_hackman_x, new_y):
                mrs_hackman_y = new_y

        for dot in grid:
            if pygame.Rect(dot[0] - DOT_RADIUS, dot[1] - DOT_RADIUS, DOT_RADIUS * 2, DOT_RADIUS * 2).colliderect(
                    (mrs_hackman_x - HACKMAN_RADIUS, mrs_hackman_y - HACKMAN_RADIUS, HACKMAN_RADIUS * 2,
                     HACKMAN_RADIUS * 2)):
                grid.remove(dot)
                score += 100


def draw_progress_bar():
    global hacking, hacking_time, MAX_HACKING_TIME

    if hacking:
        #  print(f"Hacking time: {hacking_time}, Max Hacking Time: {MAX_HACKING_TIME}")
        #  print("Hacking")
        progress_bar_width = (hacking_time / MAX_HACKING_TIME) * 100
        pygame.draw.rect(screen, GREEN,
                         (hackman_x - TERMINAL_SIZE // 2, hackman_y - TERMINAL_SIZE // 2 - PROGRESS_BAR_HEIGHT,
                          progress_bar_width, PROGRESS_BAR_HEIGHT))


def move_third_ghost():
    global ghost_3_x, ghost_3_y

    direction = random.randint(0, 100)

    if current_maze_layout == final_hacked_layout and ghost_3_active:
        movement_speed = GRID_SIZE
        if direction <= 25:
            new_x = ghost_3_x + movement_speed
            if within_boundary(new_x, ghost_3_y):
                ghost_3_x = new_x

        elif 25 < direction <= 50:
            new_y = ghost_3_y + movement_speed
            if within_boundary(ghost_3_x, new_y):
                ghost_3_y = new_y

        elif 50 < direction <= 75:
            new_x = ghost_3_x - movement_speed
            if within_boundary(new_x, ghost_3_y):
                ghost_3_x = new_x

        elif direction > 75:
            new_y = ghost_3_y - movement_speed
            if within_boundary(ghost_3_x, new_y):
                ghost_3_y = new_y


def move_fourth_ghost():
    global ghost_4_x, ghost_4_y

    direction = random.randint(0, 100)

    if current_maze_layout == final_hacked_layout and ghost_4_active:
        movement_speed = GRID_SIZE
        if direction <= 25:
            new_x = ghost_4_x + movement_speed * 2
            if within_boundary(new_x, ghost_4_y):
                ghost_4_x = new_x

        elif 25 < direction <= 50:
            new_y = ghost_4_y + movement_speed * 2
            if within_boundary(ghost_4_x, new_y):
                ghost_4_y = new_y

        elif 50 < direction <= 75:
            new_x = ghost_4_x - movement_speed * 2
            if within_boundary(new_x, ghost_4_y):
                ghost_4_x = new_x

        elif 75 < direction <= 99:
            new_y = ghost_4_y - movement_speed * 2
            if within_boundary(ghost_4_x, new_y):
                ghost_4_y = new_y

        elif direction == 100:
            new_y = hackman_y
            new_x = hackman_x
            if within_boundary(new_x, new_y):
                ghost_4_x = new_x
                ghost_4_y = new_y


def draw_game_screen():
    screen.fill(BACKGROUND_COLOR)
    global hacking, hacking_time, MAX_HACKING_TIME

    for row, line in enumerate(current_maze_layout):
        for col, char in enumerate(line):
            if char == '#':
                pygame.draw.rect(screen, (100, 100, 100), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    for dot in grid:
        pygame.draw.circle(screen, WHITE, dot, DOT_RADIUS)

    screen.blit(ghost1_image, (ghost_x - 20, ghost_y - 20))
    screen.blit(ghost2_image, (ghost_2_x - 20, ghost_2_y - 20))

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    keys = pygame.key.get_pressed()

    if hacking:
        hacking_text = font.render("Hacking: ", True, WHITE)
        screen.blit(hacking_text, (560, 10))

        progress_bar_width = (hacking_time / MAX_HACKING_TIME) * 100
        pygame.draw.rect(screen, GREEN,
                         (670, 10, progress_bar_width, PROGRESS_BAR_HEIGHT))

    if current_maze_layout != hacked_maze_layout:
        for i, terminal in enumerate(terminals):
            if i < len(hacked_terminals):
                if not hacked_terminals[i]:
                    screen.blit(terminal_image, (terminal[0] - 20, terminal[1] - 20))

    if mrs_hackman_actived:
        if mrs_hackman_direction == 'right':
            screen.blit(mrs_hackman_right_image, (mrs_hackman_x - 20, mrs_hackman_y - 20))
        if mrs_hackman_direction == 'left':
            screen.blit(mrs_hackman_left_image, (mrs_hackman_x - 20, mrs_hackman_y - 20))
        if mrs_hackman_direction == 'down':
            screen.blit(mrs_hackman_down_image, (mrs_hackman_x - 20, mrs_hackman_y - 20))
        if mrs_hackman_direction == 'up':
            screen.blit(mrs_hackman_up_image, (mrs_hackman_x - 20, mrs_hackman_y - 20))

    if ghost_3_active:
        screen.blit(ghost3_image, (ghost_3_x - 20, ghost_3_y - 20))

    if ghost_4_active:
        screen.blit(ghost4_image, (ghost_4_x - 20, ghost_4_y - 20))

    keys = pygame.key.get_pressed()
    if not any(keys):
        screen.blit(no_movement_image, (hackman_x - 20, hackman_y - 20))
    else:
        if keys[pygame.K_LEFT]:
            frame_count = (pygame.time.get_ticks() // 100) % len(left_frames)
            current_image = left_frames[frame_count]
        elif keys[pygame.K_UP]:
            frame_count = (pygame.time.get_ticks() // 100) % len(up_frames)
            current_image = up_frames[frame_count]
        elif keys[pygame.K_DOWN]:
            frame_count = (pygame.time.get_ticks() // 100) % len(down_frames)
            current_image = down_frames[frame_count]
        else:
            frame_count = (pygame.time.get_ticks() // 100) % len(right_frames)
            current_image = right_frames[frame_count]

        screen.blit(current_image, (hackman_x - 20, hackman_y - 20))

    pygame.display.flip()
    clock.tick(20)


def check_ghost_collision():
    global hackman_x, hackman_y, ghost_x, ghost_y, ghost_2_x, ghost_2_y, \
        ghost_3_x, ghost_3_y, ghost_4_x, ghost_4_y, score

    hackman_rect = pygame.Rect(hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS, HACKMAN_RADIUS * 2,
                               HACKMAN_RADIUS * 2)
    ghost_rect = pygame.Rect(ghost_x, ghost_y, GHOST_SIZE, GHOST_SIZE)
    ghost_2_rect = pygame.Rect(ghost_2_x, ghost_2_y, GHOST_SIZE, GHOST_SIZE)
    ghost_3_rect = pygame.Rect(ghost_3_x, ghost_3_y, GHOST_SIZE, GHOST_SIZE)
    ghost_4_rect = pygame.Rect(ghost_4_x, ghost_4_y, GHOST_SIZE, GHOST_SIZE)

    if (hackman_rect.colliderect(ghost_rect) or hackman_rect.colliderect(ghost_2_rect)
            or hackman_rect.colliderect(ghost_3_rect) or hackman_rect.colliderect(ghost_4_rect)):
        score -= 100
        print("Hit, loss of points")
        hackman_x = hackman_old_x
        hackman_y = hackman_old_y


def check_exit():
    global hackman_x, hackman_y, ghost_x, ghost_y

    if hackman_y > SCREEN_HEIGHT:
        setup_game_state(final_maze_layout)
        hackman_x = (((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2)
        hackman_y = (((SCREEN_HEIGHT // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2)


def main():
    global hackman_x, hackman_y, hackman_old_x, hackman_old_y, terminals, hacked_terminals, \
        current_maze_layout, grid, score, ghost_x, ghost_y, \
        ghost_speed, path_index, ghost_2_x, ghost_2_y, path_index_2, \
        mrs_hackman_x, mrs_hackman_y, hacking, hacking_time, MAX_HACKING_TIME, \
        ghost_3_active, ghost_3_x, ghost_3_y, ghost_4_active, ghost_4_x, ghost_4_y, terminal, movement_speed, i

    last_movement_time = pygame.time.get_ticks()
    running = True
    hacking = False
    hacking_time = 0
    ghost_speed = 40

    setup_game_state(initial_maze_layout)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if hackman_y > SCREEN_HEIGHT:
            setup_game_state(final_maze_layout)
            hackman_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
            hackman_y = 20

        for dot in grid[:]:
            if pygame.Rect(dot[0] - DOT_RADIUS, dot[1] - DOT_RADIUS, DOT_RADIUS * 2, DOT_RADIUS * 2).colliderect(
                    (hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS, HACKMAN_RADIUS * 2, HACKMAN_RADIUS * 2)):
                grid.remove(dot)
                score += 100

        keys = pygame.key.get_pressed()
        activate_mrs_hackman()

        hackman_old_x = hackman_x
        hackman_old_y = hackman_y

        current_time = pygame.time.get_ticks()
        if current_time - last_movement_time >= 10:
            movement_speed = GRID_SIZE
        if current_time - last_movement_time >= 350:
            move_mrs_hackman()
            move_third_ghost()
            move_fourth_ghost()

            if keys[pygame.K_LEFT]:
                hackman_x -= movement_speed
            if keys[pygame.K_RIGHT]:
                hackman_x += movement_speed
            if keys[pygame.K_UP]:
                hackman_y -= movement_speed
            if keys[pygame.K_DOWN]:
                hackman_y += movement_speed

            # if current_time - last_movement_time >= 350:
            # print(f"Hack-Man Coordinates: ({hackman_x}, {hackman_y})")

            last_movement_time = current_time

        if (ghost_x, ghost_y) != ghost_path[path_index]:
            dx = ghost_path[path_index][0] - ghost_x
            dy = ghost_path[path_index][1] - ghost_y

            norm = max(abs(dx), abs(dy))
            move_x = dx / norm
            move_y = dy / norm

            ghost_x += move_x * GHOST_SPEED
            ghost_y += move_y * GHOST_SPEED

        else:
            path_index = (path_index + 1) % len(ghost_path)

        if (ghost_2_x, ghost_2_y) != ghost_2_path[path_index_2]:
            dx = ghost_2_path[path_index_2][0] - ghost_2_x
            dy = ghost_2_path[path_index_2][1] - ghost_2_y
            norm = max(abs(dx), abs(dy))
            move_x = dx / norm
            move_y = dy / norm
            ghost_2_x += move_x * GHOST_SPEED
            ghost_2_y += move_y * GHOST_SPEED
        else:
            path_index_2 = (path_index_2 + 1) % len(ghost_2_path)

        for row, line in enumerate(current_maze_layout):
            for col, char in enumerate(line):
                if char == '#':
                    wall_rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    if wall_rect.colliderect(
                            (hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS, HACKMAN_RADIUS * 2,
                             HACKMAN_RADIUS * 2)):
                        hackman_x = hackman_old_x
                        hackman_y = hackman_old_y

        check_ghost_collision()

        if mrs_hackman_actived and not ghost_3_active and any(hacked_terminals):
            ghost_3_active = True
            ghost_4_active = True

        if all(hacked_terminals):
            for row, line in enumerate(current_maze_layout):
                for col, char in enumerate(line):
                    if char == '.':
                        exit_rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                        if exit_rect.colliderect((
                                hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS, HACKMAN_RADIUS * 2,
                                HACKMAN_RADIUS * 2)):
                            if hacked_terminals[0] and final_terminals[0] not in terminals:
                                current_maze_layout = final_hacked_layout
                            else:
                                current_maze_layout = final_maze_layout

            if all(hacked_terminals) and all(terminal in terminals for terminal in final_terminals):
                if current_maze_layout == final_maze_layout:
                    print("You Win! Game Over")
                    print(f"Final Score: {score}")
                    running = False
                    break
                else:
                    setup_game_state(hacked_maze_layout)
                    pygame.time.delay(500)

            check_exit()
            setup_game_state(hacked_maze_layout)
            pygame.time.delay(500)

        if not hacking:
            for i, terminal in enumerate(terminals):
                terminal_rect = pygame.Rect(terminal[0] - TERMINAL_SIZE // 2, terminal[1] - TERMINAL_SIZE // 2,
                                            TERMINAL_SIZE, TERMINAL_SIZE)
                if terminal_rect.colliderect((
                        hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS, HACKMAN_RADIUS * 2,
                        HACKMAN_RADIUS * 2)):
                    if keys[pygame.K_SPACE]:
                        print("Hack started")
                        hacking = True
                        hacking_time = 0
        else:
            hacking_time += 1
            # print(f"Hacking time: {hacking_time}, Max Hacking Time: {MAX_HACKING_TIME}")
            draw_progress_bar()
            terminal_rect = pygame.Rect(terminals[i][0] - TERMINAL_SIZE // 2, terminals[i][1] - TERMINAL_SIZE // 2,
                                        TERMINAL_SIZE, TERMINAL_SIZE)
            if not terminal_rect.colliderect((hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS,
                                              HACKMAN_RADIUS * 2, HACKMAN_RADIUS * 2)):
                hacking = False
                hacking_time = 0
                print("Player moved - Timer reset")
            if hacking_time >= MAX_HACKING_TIME:
                print("Hack successful, doors opened")
                terminals.remove(terminal)
                hacked_terminals[i] = True
                score += 250
                hacking = False
        if current_maze_layout == final_maze_layout:
            remove_wall()
            if len(terminals) <= 0:
                print("You win")
                running = False

        draw_game_screen()
        clock.tick(60)

    print(f"Game over! Final Score: {score}")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

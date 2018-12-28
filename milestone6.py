import random
import pygame
from pygame.locals import *
from sys import exit

pygame.init()

class Icon:
    def __init__(self, icon_type, direction, x, y, width, height, color, points):
        self.icon_type = icon_type
        self.direction = direction
        self.width = width
        self.height = height
        self.color = color
        self.points = points
        self.pos = [x, y]
        self.change_color = True
        self.frame = 0
        self.current_color = (173, 216, 230)
        self.pressed = False

    def set_icon(self, window):
        if self.icon_type == 'target':
            pygame.draw.rect(window, self.color, (self.pos[0] - 25, self.pos[1] - 25,
                                self.width, self.height), 3)
            pygame.draw.polygon(window, self.color, self.points, 3)
        if self.icon_type == 'arrow':
            pygame.draw.polygon(window, self.color, self.points)

    def move(self, delta_y):
        if self.direction == 'left':
            for point in LEFT_list[0].points:
                point[1] -= delta_y
            LEFT_list[0].y -= delta_y
        elif self.direction == 'back':
            for point in BACK_list[0].points:
                point[1] -= delta_y
            BACK_list[0].y -= delta_y
        elif self.direction == 'front':
            for point in FRONT_list[0].points:
                point[1] -= delta_y
            FRONT_list[0].y -= delta_y
        elif self.direction == 'right':
            for point in RIGHT_list[0].points:
                point[1] -= delta_y
            RIGHT_list[0].y -= delta_y

    def overlap(self, icon_stream):
        self.icon_stream = icon_stream
        # area of target = 2500, height =  85 - icon.pos[1], width = 50
        try:
            overlap_area = 50 * (85 - self.icon_stream.detected_icons[0].pos[1])
            return overlap_area / 2500
        except IndexError:
            return 0

    def target_color(self, window):

        self.pressed = True
        if self.change_color == True and self.overlap(self.icon_stream) < 0.60:
            self.current_color = (240, 128, 128) # RED
            self.change_color = False

        elif self.change_color == True and 0.60 <= self.overlap(self.icon_stream) < 0.90:
            self.current_color = (244, 164, 96) # ORANGE
            self.change_color = False

        elif self.change_color == True and 0.90 <= self.overlap(self.icon_stream):
            self.current_color = (189, 236, 182) # GREEN
            self.change_color = False

    def color_hold(self, window):
        if self.current_color == 'RESET':
            pygame.draw.rect(window, self.color, (self.pos[0] - 25, self.pos[1] - 25,
                                self.width, self.height), 3)
            pygame.draw.polygon(window, self.color, self.points, 3)
            if self.pressed == False:
                self.change_color = True

        elif self.change_color == False:
            if self.frame < 3:
                self.frame += 1
                pygame.draw.rect(window, self.current_color, (self.pos[0] - 22, self.pos[1] - 22, self.width - 6, self.height - 6))
                pygame.draw.polygon(window, (255, 255, 255), self.points)
            if self.frame == 3:
                self.current_color = 'RESET'
                self.frame = 0

class IconStream:
    def __init__(self, icon_list):
        self.icon_list = icon_list
        self.detected_icons = []
    def insert(self, icon):
        self.icon_list.append(icon)
    def move(self, delta_y):
        for point in icon.points:
            point[1] -= delta_y
        icon.pos[1] -= delta_y
    def flush(self, icon):
        if icon.pos[1] < -50:
            self.icon_list.remove(icon)
    def detect(self, icon):
        if icon.pos[1] == 85:
            self.detected_icons.append(icon)
        elif icon.pos[1] == 30:
            self.detected_icons.pop(0)
    def icon_flow(self):
        global icon
        for icon in self.icon_list:
            self.move(5)
            self.detect(icon)
            icon.set_icon(game.window)
        for icon in self.icon_list:
            self.flush(icon)

class Game:
    window = pygame.display.set_mode((250, 300), 0, 32)

    target_left = Icon('target','left', 35, 35, 50, 50, (173, 216, 230),
                ((20, 35), (30, 25), (30, 30), (50, 30),
                (50, 40), (30, 40), (30, 45)))

    target_back = Icon('target','back', 95, 35, 50, 50, (173, 216, 230),
                    ((95, 50), (105, 40), (100, 40),
                    (100, 20), (90, 20), (90, 40), (85, 40)))

    target_front = Icon('target','front', 155, 35, 50, 50, (173, 216, 230),
                    ((155, 20), (165, 30), (160, 30),
                    (160, 50), (150, 50), (150, 30), (145, 30)))

    target_right = Icon('target','right', 215, 35, 50, 50, (173, 216, 230),
                    ((230, 35), (220, 25), (220, 30),
                    (200, 30), (200, 40), (220, 40), (220, 45)))

    def __init__(self):
        pygame.display.set_caption("Machine Problem II")

game = Game()

LEFT_list = []
BACK_list = []
FRONT_list = []
RIGHT_list = []

LEFT_stream = IconStream(LEFT_list)
BACK_stream = IconStream(BACK_list)
FRONT_stream = IconStream(FRONT_list)
RIGHT_stream = IconStream(RIGHT_list)

INSERT_ARROW = pygame.USEREVENT + 1
pygame.time.set_timer(INSERT_ARROW, 1000)

clock = pygame.time.Clock()
'''MAIN LOOP'''
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == INSERT_ARROW:
            # Direction of icons to be inserted:
            # 0: none, 1: left, 2: back, 3: front, 4: right
            icon_directions = [0, 1, 2, 3, 4]
            icon_directions.remove(random.choice(icon_directions))
            icon_directions.remove(random.choice(icon_directions))
            if 1 not in icon_directions:
                LEFT_stream.insert(Icon('arrow','left', 35, 350, 50, 50, (173, 216, 230),
                            [[20, 350], [30, 340], [30, 345], [50, 345],
                            [50, 355], [30, 355], [30, 360]]))
            if 2 not in icon_directions:
                BACK_stream.insert(Icon('arrow','back', 95, 350, 50, 50, (173, 216, 230),
                                [[95, 365], [105, 355], [100, 355],
                                [100, 335], [90, 335], [90, 355], [85, 355]]))
            if 3 not in icon_directions:
                FRONT_stream.insert(Icon('arrow','front', 155, 350, 50, 50, (173, 216, 230),
                                [[155, 335], [165, 345], [160, 345],
                                [160, 365], [150, 365], [150, 345], [145, 345]]))
            if 4 not in icon_directions:
                RIGHT_stream.insert(Icon('arrow','right', 215, 350, 50, 50, (173, 216, 230),
                                [[230, 350], [220, 340], [220, 345],
                                [200, 345], [200, 355], [220, 355], [220, 360]]))
    game.window.fill((255, 255, 255))

    game.target_left.set_icon(game.window)
    game.target_back.set_icon(game.window)
    game.target_front.set_icon(game.window)
    game.target_right.set_icon(game.window)

    keys = pygame.key.get_pressed() #Creates a tuple representing the
                                    # pressed state for every key on the keyboard.

    if keys[pygame.K_LEFT]:
        game.target_left.overlap(LEFT_stream)
        game.target_left.target_color(game.window)
    else:
        game.target_left.pressed = False

    if keys[pygame.K_RIGHT]:
        game.target_right.overlap(RIGHT_stream)
        game.target_right.target_color(game.window)
    else:
        game.target_right.pressed = False

    if keys[pygame.K_DOWN]:
        game.target_back.overlap(BACK_stream)
        game.target_back.target_color(game.window)
    else:
        game.target_back.pressed = False

    if keys[pygame.K_UP]:
        game.target_front.overlap(FRONT_stream)
        game.target_front.target_color(game.window)
    else:
        game.target_front.pressed = False


    game.target_left.color_hold(game.window)
    game.target_right.color_hold(game.window)
    game.target_back.color_hold(game.window)
    game.target_front.color_hold(game.window)

    LEFT_stream.icon_flow()
    BACK_stream.icon_flow()
    FRONT_stream.icon_flow()
    RIGHT_stream.icon_flow()

    clock.tick(30)
    pygame.display.update()


pygame.quit()

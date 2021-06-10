from textbox import TextBox

import pygame
import pickle
import random
import time

BLACK = 0, 0, 0
GREEN = 0, 255, 0

BLOCK_SIZE = 15
DELAY = 0
WIDTH = 45
HEIGHT = 45


class App:
    def __init__(self):
        pygame.display.set_caption('Conway\'s Game of Life')
        self.screen = pygame.display.set_mode([WIDTH * BLOCK_SIZE,
                                               HEIGHT * BLOCK_SIZE])
        self.quit = False

        self.grid = generate_grid(WIDTH, HEIGHT)
        self.playing = True

        self.reset_grid = self.grid
        self.textbox = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.grid = self.reset_grid

                if event.key == pygame.K_c and not self.playing:
                    self.grid = generate_empty_grid(WIDTH, HEIGHT)

                if event.key == pygame.K_s:
                    self.textbox = TextBox([10, 10, 100, 20])

                if event.key == pygame.K_SPACE:
                    if not self.playing:
                        self.reset_grid = self.grid
                    self.playing = not self.playing

    def render_grid(self):
        y = 0
        for i in range(HEIGHT):
            x = 0
            for j in range(WIDTH):
                if self.grid[i][j] == 1:
                    rect = [x, y, BLOCK_SIZE, BLOCK_SIZE]
                    pygame.draw.rect(self.screen, GREEN, rect)
                x += BLOCK_SIZE
            y += BLOCK_SIZE

    def update(self):
        self.render_grid()

        if self.textbox:
            self.textbox.update()
            self.textbox.draw(self.screen)
        elif self.playing:
            self.grid = update(self.grid)
        else:
            j, i = snap_to_grid(pygame.mouse.get_pos())
            if pygame.mouse.get_pressed()[0] == 1:
                self.grid[i][j] = 1
            elif pygame.mouse.get_pressed()[2] == 1:
                self.grid[i][j] = 0

    def main_loop(self):
        while True:
            self.handle_events()
            
            self.screen.fill(BLACK)
            self.update()
            pygame.display.update()

            time.sleep(DELAY)
            
            if self.quit:
                break


def generate_grid(width, height):
    grid = []
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(random.choice([0, 1]))
        grid.append(row)
    return grid


def generate_empty_grid(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]


def count_neighbors(grid, x, y):
    result = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                result += get(grid, x + i, y + j)

    return result


def update(grid):
    new_grid = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            neighbors = count_neighbors(grid, x, y)
            if get(grid, x, y) == 1 and (neighbors < 2 or neighbors > 3):
                row.append(0)
            elif get(grid, x, y) == 0 and neighbors == 3:
                row.append(1)
            else:
                row.append(get(grid, x, y))
        new_grid.append(row)
    return new_grid


def snap_to_grid(mouse_pos):
    mouseX, mouseY = mouse_pos
    x = (mouseX - (mouseX % BLOCK_SIZE)) // BLOCK_SIZE
    y = (mouseY - (mouseY % BLOCK_SIZE)) // BLOCK_SIZE
    return x, y


def index(foo, bar):
    return foo[bar % len(foo)]


def get(grid, x, y):
    return index(index(grid, y), x)


if __name__ == '__main__':
    pygame.init()

    app = App()
    app.main_loop()

    pygame.quit()

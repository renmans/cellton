import random
import pygame
from pygame.locals import QUIT, Rect
import yaml
import launcher


class GameOfLife:
    def __init__(self, width=500, height=500, cell_size=10, speed=10,
                 cell_color='black'):
        self.width = width
        self.height = height
        self.field = width // cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_size = cell_size
        self.cell_color = cell_color
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed
        self.randomize = True
        self.figure = []
        self.cells = self.cell_list()

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def cell_list(self, randomize=False):
        if randomize:
            for i in range(self.height // self.cell_size):
                for j in range(self.width // self.cell_size):
                    self.cells[i][j] = random.randint(0, 1)
            return self.cells
        else:
            return [[0 for x in range(self.width // self.cell_size)]
                    for y in range(self.height // self.cell_size)]

    def draw_cell_list(self, list):
        column, row = 0, 0
        for cell in list:
            column = 0
            for cell_state in cell:
                if cell_state:
                    pygame.draw.rect(self.screen,
                                     pygame.Color(self.cell_color),
                                     Rect(column, row, self.cell_size,
                                          self.cell_size))
                else:
                    pygame.draw.rect(self.screen,
                                     pygame.Color('white'),
                                     Rect(column, row, self.cell_size,
                                          self.cell_size))
                column += self.cell_size
            row += self.cell_size

    def get_neighbours(self, i, j):
        alive = 0
        for y in [i-1, i, i+1]:
            for x in [j-1, j, j+1]:
                if (y == i and x == j):
                    continue
                if (x < self.field-1 and y < self.field-1):
                    alive += self.cells[y][x]
                elif (y == self.field-1 and x < self.field-1):
                    alive += self.cells[0][x]
                elif (y < self.field-1 and x == self.field-1):
                    alive += self.cells[y][0]
                else:
                    alive += self.cells[0][0]
        return alive

    def get_next_generation(self):
        nextgen = self.cell_list()
        for y in range(self.field):
            for x in range(self.field):
                alive = self.get_neighbours(y, x)
                if (self.cells[y][x] == 1 and alive < 2):
                    nextgen[y][x] = 0
                elif (self.cells[y][x] == 1 and (alive == 2 or alive == 3)):
                    nextgen[y][x] = 1
                elif (self.cells[y][x] == 1 and alive > 3):
                    nextgen[y][x] = 0
                elif (self.cells[y][x] == 0 and alive == 3):
                    nextgen[y][x] = 1
        return nextgen

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Cellton')
        self.screen.fill(pygame.Color('white'))
        running = True
        self.cells = self.cell_list(self.randomize)
        for cell in self.figure:
            self.cells[cell[0]][cell[1]] = 1
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_cell_list(self.cells)
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
            self.cells = self.get_next_generation()
        pygame.quit()


if __name__ == '__main__':
    if launcher.main():
        game = GameOfLife()
        try:
            with open('settings.yml', 'r') as f:
                params = yaml.safe_load(f)
                game = GameOfLife(params['width'], params['height'],
                                  params['cell_size'], params['speed'],
                                  params['cell_color'])
                if params['figure']:
                    game.randomize = False
                    game.figure = params['figure']

        except FileNotFoundError:
            game = GameOfLife()
        game.run()

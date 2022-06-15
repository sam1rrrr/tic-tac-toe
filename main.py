# импорты
import pygame
import time

pygame.init()

BACKGROUND_COLOR = (91, 125, 171) # цвет фона
RESOLUTION = (900, 900) # размер окна
NAME = 'Крестики нолики' # название программы

screen = pygame.display.set_mode(RESOLUTION)
screen.fill(BACKGROUND_COLOR)
pygame.display.set_caption(NAME)

X_IMG = pygame.image.load('assets/x.png') # X
O_IMG = pygame.image.load('assets/o.png') # O
BOARD_IMG = pygame.image.load('assets/board.png') # доска

screen.blit(BOARD_IMG, (64, 64))
pygame.display.update()

class Game:
    # инициализация
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[''] * width for _ in range(height)]
        
        self.move = 'X' # игрок, который ходит
    

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
    

    # рендер доски
    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x] # ячейка
                size = (x * self.cell_size - self.left, y * self.cell_size + self.top, self.cell_size,
                        self.cell_size)

                # отрисовываем X или O
                if cell == 'X':
                    screen.blit(X_IMG, size)
                elif cell == 'O':
                    screen.blit(O_IMG, size)

                screen.blit(BOARD_IMG, (64, 64)) # отрисовываем поле

    # обновляем пустую ячейку и изменяем игрока, который ходит
    def update_cell(self, x, y, value):
        if self.board[x][y] not in ['X', 'O']:
            self.board[x][y] = value
            if value == 'X':
                self.move = 'O'
            else:
                self.move = 'X'


    # возвращает координаты ячейки по координатам мыши
    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[1] < self.left + self.height * self.cell_size and self.top <= mouse_pos[
            0] < self.top + self.width * self.cell_size:
            return (int((mouse_pos[1] - self.left) / self.cell_size), int((mouse_pos[0] - self.top) / self.cell_size))
        else:
            return None

    # получение клика мыши и изменение ячейки
    def get_input(self, mouse_pos):
        data = self.get_cell(mouse_pos)
        self.update_cell(*data, self.move)

    # проверка победы
    def check_win(self):
        win_coord = [((0, 0), (0, 1), (0, 2)),
            ((1, 0), (1, 1), (1, 2)),
            ((2, 0), (2, 1), (2, 2)),
            ((0, 0), (1, 0), (2, 0)),
            ((0, 1), (1, 1), (2, 1)),
            ((0, 2), (1, 2), (2, 2)),
            ((0, 0), (1, 1), (2, 2)),
            ((2, 2), (1, 1), (0, 0)),
            ((0, 2), (1, 1), (2, 0)),
            ((0, 0), (1, 1), (2, 2)),]

        for i in win_coord:
            results = [self.board[j[0]][j[1]] for j in i]
            if len(set(results)) == 1 and results[0] != '':
                return True, results[0] # возвращает true и победителя

        return False

    # проверка ничьи
    def check_draw(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                if cell not in ['X', 'O']:
                    return False

        if not self.check_win():
            return True


def main():
    screen.fill(BACKGROUND_COLOR)

    board = Game(3, 3)
    board.set_view(0, 0, 300)
    board.render(screen)

    running = True
    while running:
        for event in pygame.event.get():
            # выход из игры
            if event.type == pygame.QUIT:
                pygame.quit()

            # клик мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_input(event.pos) # получение клика
                board.render(screen)
                win = board.check_win()
                draw = board.check_draw()

                if win:
                    pygame.display.set_caption(f'Победитель: {win[1]}')
                    pygame.display.flip()
                    time.sleep(2)
                    return 'GG'

                if draw:
                    pygame.display.set_caption('Ничья!')
                    pygame.display.flip()
                    time.sleep(2)
                    return 'GG'

        pygame.display.flip()


while True:
    main()

from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс для игровых объектов.

    Атрибуты:
        position (tuple): Позиция объекта на игровом поле (x, y).
        body_color (tuple): Цвет объекта в формате RGB.

    """

    def __init__(self):
        """Инициализирует позицию объекта по центру экрана."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовывает объект на экране.

        Этот метод должен быть переопределен в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Класс, представляющий яблоко в игре.

    Атрибуты:
        body_color (tuple): Цвет яблока в формате RGB (по умолчанию красный).
        position (tuple): Позиция яблока на игровом поле.

    """

    def __init__(self):
        """Инициализирует яблоко, задает цвет и случайную позицию."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс, представляющий змейку в игре.

    Атрибуты:
        length (int): Длина змейки (количество сегментов).
        positions (list): Список позиций каждого сегмента змейки.
        direction (tuple): Текущее направление движения змейки.
        next_direction (tuple): Направление, в котором будет двигаться змейка
                                после обработки нажатия клавиши.
        body_color (tuple): Цвет змейки в формате RGB (по умолчанию зеленый).
        last (tuple): Координаты последнего сегмента змейки.

    """

    def __init__(self):
        """
        Инициализирует змейку, задает цвет,
        начальную позицию и направление.
        """
        super().__init__()
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Перемещает змейку на одну клетку в текущем направлении.

        Обновляет список позиций сегментов змейки, добавляя новую
        позицию головы и удаляя последний сегмент (хвост),
        если длина змейки не увеличивается.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_x = (head_x + (dx * GRID_SIZE)) % SCREEN_WIDTH
        new_head_y = (head_y + (dy * GRID_SIZE)) % SCREEN_HEIGHT
        new_head_position = (new_head_x, new_head_y)

        if new_head_position in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None

    def draw(self):
        """Отрисовывает змейку на экране, затирая последний сегмент."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        # Обработка событий
        handle_keys(snake)

        # Обновление состояния игры
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()

        # Контроль скорости игры
        clock.tick(SPEED)


if __name__ == '__main__':
    main()

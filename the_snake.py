"""
Игра "Змейка" (Изгиб Питона)
Реализация с использованием PyGame и ООП.
"""

import pygame
import random

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
BOARD_BACKGROUND_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """
        Инициализация игрового объекта.

        Args:
            position (tuple): Начальная позиция объекта.
            body_color (tuple): Цвет объекта в формате RGB.
        """
        self.position = (
            position if position
            else (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока."""
        x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """
        Отрисовывает яблоко на поверхности.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку."""
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % SCREEN_WIDTH
        new_y = (head[1] + y) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Проверка на столкновение с собой
        if new_head in self.positions[1:]:
            self.reset()
            return

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def draw(self, surface):
        """
        Отрисовывает змейку и затирает её след.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)
        # Затирание последнего сегмента
        if self.last:
            rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш.

    Args:
        snake (Snake): Объект змейки для управления.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Яблоко не должно появляться на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(10)  # Скорость игры


if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()

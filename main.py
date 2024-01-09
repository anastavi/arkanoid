import pygame
import sys
import math

from facade import GameFacade
from model import Ball, Paddle
from view import View


def main():
    # Создание экземпляров классов
    game_facade = GameFacade()
    ball = Ball(200, 300, 10, 3.5)
    paddle = Paddle(200, 450, 80, 10)

    # Загрузка уровней и рекордов
    game_facade.load_levels('levels')
    game_facade.load_high_scores('high_scores.txt')

    # Инициализация отображения
    view = View(600, 500)

    # Получение имени игрока
    player_name = view.get_player_name()

    # Выбор уровня
    selected_level = view.level_selection_window(game_facade)
    game_facade.load_level(selected_level)

    # Основной игровой цикл
    while True:
        # Обработка событий
        view.handle_events(paddle)

        # Обновление состояния игры
        ball.move()
        paddle.move()

        # Ограничение движения мяча и платформы в пределах экрана
        if ball.x < 0 or ball.x > view.width:
            ball.reverse_x_direction()
        if ball.y < 0:
            ball.reverse_y_direction()
        if ball.y > view.height:
            view.game_over()
            game_facade.save_high_score(player_name, view.score)
            view.draw_high_scores(game_facade.get_high_scores())
            break

        if len(game_facade.level.bricks) == 0:
            view.game_won()
            game_facade.save_high_score(player_name, view.score)
            view.draw_high_scores(game_facade.get_high_scores())
            break

        if paddle.x < 0:
            paddle.x = 0
        if paddle.x + paddle.width > view.width:
            paddle.x = view.width - paddle.width

        # Проверка столкновения мяча с платформой
        if ball.collides_with(paddle):
            ball.reverse_y_direction()


        # Проверка столкновения мяча с блоками
        for brick in game_facade.level.bricks:
            if ball.collides_with(brick):
                brick.hit()
                if brick.is_destroyed():
                    game_facade.level.bricks.remove(brick)
                    view.score += 10
                ball.reverse_y_direction()

        # Отрисовка игровых объектов
        view.screen.fill((0, 0, 0))
        view.draw_ball(ball)
        view.draw_paddle(paddle)
        view.draw_bricks(game_facade.level.bricks)
        view.update_screen()

if __name__ == "__main__":
    main()
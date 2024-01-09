import unittest
from model import Ball

class TestBallMovement(unittest.TestCase):
    def test_ball_moves(self):
        ball = Ball(x=5, y=5, radius=1, speed=3.5)
        old_x, old_y = ball.x, ball.y

        ball.move()

        # Проверяем, что координаты мяча изменились после движения
        self.assertNotEqual(old_x, ball.x)
        self.assertNotEqual(old_y, ball.y)

    def test_ball_changes_x_direction(self):
        ball = Ball(x=5, y=5, radius=1, speed=3.5)
        old_direction_x = ball.direction_x

        ball.reverse_x_direction()

        # Проверяем, что направление движения по X изменилось
        self.assertNotEqual(old_direction_x, ball.direction_x)

    def test_ball_changes_y_direction(self):
        ball = Ball(x=5, y=5, radius=1, speed=3.5)
        old_direction_y = ball.direction_y

        ball.reverse_y_direction()

        # Проверяем, что направление движения по Y изменилось
        self.assertNotEqual(old_direction_y, ball.direction_y)

if __name__ == "__main__":
    unittest.main()
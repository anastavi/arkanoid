import unittest
from model import Ball, Paddle, Brick

class TestCollisions(unittest.TestCase):
    def test_ball_collides_with_paddle(self):
        ball = Ball(x=5, y=5, radius=1, speed=3.5)
        paddle = Paddle(x=4, y=4, width=2, height=2)

        # Мяч и платформа пересекаются, поэтому столкновение должно произойти
        self.assertTrue(ball.collides_with(paddle))

        # Переместим платформу за пределы мяча, столкновения не должно быть
        paddle.x = 10
        paddle.y = 10
        self.assertFalse(ball.collides_with(paddle))

    def test_ball_collides_with_brick(self):
        ball = Ball(x=5, y=5, radius=1, speed=3.5)
        brick = Brick(x=4, y=4, width=2, height=2, hp = 1)

        # Мяч и блок пересекаются, поэтому столкновение должно произойти
        self.assertTrue(ball.collides_with(brick))

        # Переместим блок за пределы мяча, столкновения не должно быть
        brick.x = 10
        brick.y = 10
        self.assertFalse(ball.collides_with(brick))

if __name__ == "__main__":
    unittest.main()
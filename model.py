import math
import random

class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction_x = 1
        self.direction_y = -1
        angle = math.radians(random.uniform(45, 135))
        self.direction_x = math.cos(angle)
        self.direction_y = -math.sin(angle)

    def move(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

    def reverse_x_direction(self):
        self.direction_x *= -1

    def reverse_y_direction(self):
        self.direction_y *= -1

    def collides_with(self, object):
        ball_left = self.x - self.radius
        ball_right = self.x + self.radius
        ball_top = self.y - self.radius
        ball_bottom = self.y + self.radius

        object_left = object.x
        object_right = object.x + object.width
        object_top = object.y
        object_bottom = object.y + object.height

        if (
            ball_right >= object_left
            and ball_left <= object_right
            and ball_bottom >= object_top
            and ball_top <= object_bottom
        ):
            return True
        else:
            return False

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dx = 0

    def move(self):
        self.x += self.dx

class Brick:
    def __init__(self, x, y, width, height, hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp

    def hit(self):
        self.hp -= 1

    def is_destroyed(self):
        if self.hp <= 0:
            return 1

        return 0
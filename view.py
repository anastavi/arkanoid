import pygame
import random
pygame.init()

class View:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.input_box = InputBox(100, 100, 140, 32)

    def get_player_name(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.draw_input_box()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.input_box.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return self.input_box.text

    def level_selection_window(self, game_facade):
        buttons = [LevelButton(50, 50 + i * 60, 150, 50, f"Level {i + 1}", level)
                   for i, level in enumerate(game_facade.levels)]
        while True:
            self.screen.fill((0, 0, 0))
            for button in buttons:
                button.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                for button in buttons:
                    level = button.handle_event(event)
                    if level is not None:
                        return level

    def draw_high_scores(self, high_scores):
        self.screen.fill((0, 0, 0))

        for i, (name, score, level) in enumerate(high_scores):
            score_text = self.font.render("{}: {} - {} ({})".format(i + 1, name, score, level), True, (255, 255, 255))
            self.screen.blit(score_text, (20, 20 + i * 20))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    return

            pygame.display.flip()

    def draw_ball(self, ball):
        pygame.draw.circle(self.screen, (255, 255, 255), (ball.x, ball.y), ball.radius)

    def draw_paddle(self, paddle):
        pygame.draw.rect(self.screen, (255, 255, 255), (paddle.x, paddle.y, paddle.width, paddle.height))

    def draw_bricks(self, bricks):
        for brick in bricks:
            if brick.is_destroyed:
                color = random.choice(['red', 'blue', 'green', 'yellow'])
                pygame.draw.rect(self.screen, pygame.Color(color), (brick.x, brick.y, brick.width, brick.height))

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (0, 0))

    def draw_input_box(self):
        self.input_box.draw(self.screen)

    def update_screen(self):
        self.draw_score()
        pygame.display.flip()
        self.clock.tick(60)

    def handle_events(self, paddle):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle.dx = -5
                elif event.key == pygame.K_RIGHT:
                    paddle.dx = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    paddle.dx = 0

            self.input_box.handle_event(event)

    def game_over(self):
        game_over_text = self.font.render("Game Over", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    return

            self.screen.fill((0, 0, 0))
            self.screen.blit(game_over_text, text_rect)
            pygame.display.flip()

    def game_won(self):
        game_over_text = self.font.render("Game Won", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    return

            self.screen.fill((0, 0, 0))
            self.screen.blit(game_over_text, text_rect)
            pygame.display.flip()


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    #self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class LevelButton:
    def __init__(self, x, y, w, h, text, level):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.level = level

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.level
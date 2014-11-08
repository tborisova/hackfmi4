from pygame.locals import *
import pygame
import math
import json

from settings import *


class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y, image_name='ball.png'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(IMAGES_PATH + image_name)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = GRAVITY
        self.cap = CAP
        self.bounce = BOUNCE
        self.friction = FRICTION
        self.kick = KICK
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.on_ground = False
        self.spin = 0
        self.angle = 0
        self.center()

    def center(self):
        self.rect.centerx, self.rect.centery = CENTER
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        self.x += self.dx / 2
        self.y += self.dy / 2
        self.angle += self.spin
        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle -= 360
        if not self.on_ground:
            self.dy += self.gravity
        if self.dy > self.cap:
            self.dy = self.cap
        if self.on_ground:
            self.dx *= self.friction
            self.spin = -self.dx
        if self.on_ground and abs(self.dx) - 0.5 < 0:
            self.dx = 0
            self.spin = -self.dx
        self.rect.x = self.x
        self.rect.y = self.y

    def get_json(self):
        return json.dumps({str(id(self)): {'image': 'ball', 'x': self.x, 'y': self.y}})


class Pointer(pygame.sprite.Sprite):

    def __init__(self):
        self.rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        self.mask = pygame.Mask((1, 1))
        self.mask.set_at((0, 0), 1)


class Game:

    def __init__(self, difficulty):
        self.ball = Ball(*CENTER)
        self.pointer = Pointer()
        self.score = 0
        self.difficulty = difficulty
        self.highscore = 0
        self.paused = False
        self.subrect = self.ball.image.get_rect()
        self.subrect.width = 84
        self.subrect.height = 83
        self.newimg = self.ball.image
        self.tries = TRIES
        self.game_over = False

    def check_for_collision(self):
        if pygame.sprite.collide_mask(self.pointer, self.ball) and not self.paused:
            if self.ball.mask.get_at((int(self.pointer.rect.x - self.ball.x), int(self.pointer.rect.y - self.ball.y))):
                hit = self.ball.mask.overlap(
                    self.pointer.mask, (int(self.pointer.rect.x - self.ball.x), int(self.pointer.rect.y - self.ball.y)))
                hit = (
                    hit[0] - self.ball.rect.width / 2, hit[1] - self.ball.rect.height / 2)
                angle = math.degrees(math.atan2(hit[0], hit[1]))
                dx = 30 * math.cos(math.radians(angle + 90))
                dy = 30 * math.sin(math.radians(angle - 90))
                self.ball.dx = dx
                self.ball.dy = dy
                self.ball.on_ground = False
                self.ball.spin = -dx / 5
                self.score += 1

    def update(self):
        self.check_for_collision()
        if self.ball.x > WINDOWWIDTH - self.ball.rect.width:
            self.ball.x = WINDOWWIDTH - self.ball.rect.width
            self.ball.dx = -self.ball.dx * self.ball.friction
            self.ball.spin = self.ball.dy
        if self.ball.y > WINDOWHEIGHT - self.ball.rect.height:
            if not self.paused and self.score > 0:
                self.tries -= 1
                self.score = 0
            self.ball.y = WINDOWHEIGHT - self.ball.rect.height
            if not self.ball.on_ground:
                self.ball.dx *= self.ball.friction
            self.ball.spin = -self.ball.dx
            if (self.ball.dy * self.ball.bounce) - 5 > 0:
                self.ball.dy = -self.ball.dy * self.ball.bounce
            else:
                self.ball.dy = 0
                self.ball.on_ground = True
        if self.ball.x < 0:
            self.ball.x = 0
            self.ball.dx = -self.ball.dx * self.ball.bounce
            self.ball.spin = -self.ball.dy

        if self.score > self.highscore:
            self.highscore = self.score

        self.ball.update()
        rotated = pygame.transform.rotate(self.ball.image, self.ball.angle)
        size = rotated.get_size()
        self.subrect.centerx = size[0] / 2
        self.subrect.centery = size[1] / 2
        self.newimg = rotated.subsurface(self.subrect)

        if self.tries == 0:
            self.game_over = True

    def get_json(self):
        json = json



class Gui:

    def __init__(self, difficulty):
        pygame.init()
        pygame.display.set_caption('Kick Ball')
        pygame.display.set_icon(pygame.image.load('./data/icon.png'))
        self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.game = Game(difficulty)
        self.screen.fill((0, 0, 0))
        self.screen.set_colorkey((0, 0, 0))
        self.screen_center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.Font('./data/font.ttf', 40)
        self.font2 = pygame.font.Font('./data/font.ttf', 22)
        self.font3 = pygame.font.Font('./data/font.ttf', 52)
        self.font4 = pygame.font.Font('./data/font.ttf', 16)
        self.draw_info()
        self.game.ball.update()
        self.screen.blit(self.game.newimg, self.game.ball.rect)
        pygame.display.flip()

    def start_game(self):
        while True:
            self.clock.tick(60)
            self.handle_game_event()
            self.game.update()
            self.screen.fill((0, 0, 0))
            # self.draw_message(str(self.game.score), 22)
            # self.draw_message(str(self.game.highscore), 22)
            self.screen.blit(self.game.newimg, self.game.ball.rect)
            self.draw_info()
            pygame.display.flip()
            if self.game.game_over:
                return self.game.highscore

    def handle_game_event(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    if event.key == K_p:
                        self.game.paused = not self.game.paused
        self.game.pointer.rect.x, self.game.pointer.rect.y = pygame.mouse.get_pos()

    def draw_message(self, message):
        font = pygame.font.Font('./data/font.ttf', 52)
        label = font.render(message, 1, WHITE)
        rect = label.get_rect()
        rect.center = CENTER
        self.screen.blit(label, rect)

    def draw_info(self):
        score_text = self.font1.render(str(self.game.score), 1, (255, 155, 155))
        score_rect = score_text.get_rect()
        score_rect.x = 20
        highscore_text = self.font2.render(str(self.game.highscore), 1, (255, 255, 255))
        highscore_rect = highscore_text.get_rect()
        highscore_rect.y = score_rect.bottom + 5
        highscore_rect.x = 5
        info2 = self.font4.render('P - Pause', 1, (255, 255, 255))
        if self.game.paused:
            self.draw_message('Paused')
        if self.game.game_over:
            self.draw_message('Game over :(')
        info1 = self.font4.render('Esc - Quit', 1, (255, 255, 255))
        info1_rect = info1.get_rect()
        info1_rect.right = WINDOWWIDTH - 5
        info1_rect.y = 5
        info2_rect = info2.get_rect()
        info2_rect.x = info1_rect.x
        info2_rect.y = info1_rect.bottom + 5
        title = self.font3.render('Keep the ball in the air!', 1, (255, 255, 255))
        title_rect = title.get_rect()
        title_rect.centerx = (
        WINDOWWIDTH - score_rect.width - info1_rect.width) / 2
        title_rect.y = score_rect.centery
        title_rect = title.get_rect()
        title_rect.y = score_rect.centery
        title_rect.centerx = (
        WINDOWWIDTH - score_rect.width - info1_rect.width) / 2
        self.screen.blit(score_text, score_rect)
        self.screen.blit(highscore_text, highscore_rect)
        self.screen.blit(title, title_rect)
        self.screen.blit(info1, info1_rect)
        self.screen.blit(info2, info2_rect)

if __name__ == "__main__":
    gui = Gui(10)
    gui.start_game()
    pygame.quit()



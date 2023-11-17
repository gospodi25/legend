import math
import random
import pygame


delay = 1000
FPS = 30
g = 3
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
points = 0

WIDTH = 800
HEIGHT = 600



class Ball:
    def __init__(self, screen: pygame.Surface, y = 550):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x_0
        self.y = y
        self.r = 10
        self.r1 = 5
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.vy = self.vy - g
        if self.x + 10 >= 800:
            self.vx = -self.vx
        if self.y -self.r >= 550:
            if -5 < self.vy < 5:
                self.vy = 0
                self.y = self.r + 551
            else:
                self.vy = -self.vy / 1.5
            self.vx = self.vx / 1.2
        self.x += self.vx
        self.y -= self.vy

    def draw_1(self):
        pygame.draw.polygon(
            self.screen,
            self.color,
            [[self.x - 10, self.y + 10], [self.x + 10, self.y + 10],
             [self.x + 10, self.y - 10], [self.x - 10, self.y - 10]]
        )
    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False

class Circle:
    def __init__(self, screen: pygame.Surface, x=30, y=550):
        self.screen = screen
        self.x = x_0
        self.y = y
        self.r = 10
        self.r1 = 5
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = 30


    def move(self):
        self.vy = self.vy - g
        if self.x + 10 >= 800:
            self.vx = -self.vx
        if self.y - self.r >= 550:
            if -4 < self.vy < 4:
                self.vy = 0
                self.y = self.r + 551
            else:
                self.vy = -self.vy / 1.5
            self.vx = self.vx / 1.2
        self.x += self.vx
        self.y -= self.vy

    def draw_2(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r,
            self.r1,
        )

    def hittest(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.x = 30
        self.y = 550
        self.color = GREY
        self.r = 20
    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        global balls, bullet
        bullet += 1
        i = random.randint(1,2)
        if i == 1:
            new_ball = Ball(self.screen)
        else:
            new_ball = Circle(self.screen)
        new_ball.r += 5
        if not abs(event.pos[0] - new_ball.x) < 2:
            self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)

        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        if event:
            if not abs(event.pos[0] - x_0) < 2:
                 self.an = math.atan((event.pos[1]-550) / (event.pos[0]-x_0))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        global x_0
        length = self.f2_power

        if self.an < 0:
            x = self.x + math.sin(self.an) + length * math.cos(self.an)
            y = self.y - math.cos(self.an) + length * math.sin(self.an)
        else:
            x = self.x - math.sin(self.an) - length * math.cos(self.an)
            y = self.y + math.cos(self.an) - length * math.sin(self.an)

        pygame.draw.line(surface = self.screen, color = self.color, start_pos = [self.x, self.y],
                         end_pos = [x, y], width = 10)
        pygame.draw.polygon(self.screen, self.color,
                            [[self.x + 15, self.y], [self.x + 15, self.y + 12],
                            [self.x - 15, self.y + 12], [self.x - 15, self.y]])
        pygame.draw.circle(self.screen, BLACK, [self.x + 11, self.y + 17], 5)
        pygame.draw.circle(self.screen, BLACK, [self.x - 11, self.y + 17], 5)
        pygame.draw.polygon(self.screen, BLACK, [[self.x + 11, self.y + 22], [self.x - 11, self.y + 22],
                                                 [self.x + 11, self.y + 12], [self.x - 11, self.y + 12]])
        x_0 = self.x

    def move(self):
        keys = pygame.key.get_pressed()
        if self.x <= 780:
            if keys[pygame.K_RIGHT]:
                self.x += 5
        if self.x >= 20:
            if keys[pygame.K_LEFT]:
                self.x -= 5

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

class Target:
    def __init__(self, c):
        self.x = random.randint(400, 700)
        self.y = random.randint(300, 500)
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.color = c
        self.r = random.randint(20, 50)
        self.live = 1
        self.points = 1
        self.new_target()
        self.a = 2
        mx, my = pygame.mouse.get_pos()
        self.an = math.atan2((my - self.y), (mx - self.x))
        self.ay = self.a * math.cos(self.an)
        self.ax = self.a * math.sin(self.an)
        self.vr = 1.5

    def new_target(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(300, 400)
        self.r = random.randint(20, 50)
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.live = 1


    def hit(self, points = 1):
        self.points += points

    def draw(self):
        pygame.draw.circle(screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        self.r += self.vr
        if 5 >= self.r or self.r >= 100:
            self.vr = -1 * self.vr

    def draw_2(self):
        pygame.draw.circle(screen,
           self.color,
           (self.x, self.y),
           self.r
           )

    def move(self):
        self.x
        self.y

    def move_2(self):
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= 750 or self.x <= 0:
            self.x = self.x
            self.vx = -self.vx
        if self.y + self.r >= 550 or self.y <= 40:
            self.y = self.y
            self.vy = -self.vy

class Platform:
    def __init__(self, screen):
        self.screen = screen
        self.x = 400
        self.y = 40
        self.color = BLACK
        self.vx = 5
        self.vy = 0
        self.r = 30

    def draw(self):
        global x_3
        pygame.draw.polygon(self.screen, self.color,
            [[self.x + 20, self.y], [self.x + 20, self.y + 12],
            [self.x - 20, self.y + 12], [self.x - 20, self.y]])
        x_3 = self.x
        pygame.draw.ellipse(self.screen, BLACK, [self.x - 40, self.y - 5, 80, 20], 40)
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), 15)

    def move(self):
        keys = pygame.key.get_pressed()
        if self.x <= 780:
            if keys[pygame.K_d]:
                self.x += 8
        if self.x >= 20:
            if keys[pygame.K_a]:
                self.x -= 8

    def fire_platform(self):
        global bombs
        if event:
            new_bomb = Bombs(self.screen)
            new_bomb.x = self.x
            bombs.append(new_bomb)



class Bombs:
    def __init__(self, screen):
        self.screen = screen
        self.y = 40
        self.x = 400
        self.color = BLACK
        self.vy = 0
        self.vx = 0
        self.r = 7

    def bomb(self):
        self.vy += 0.5
        self.y += self.vy
        if self.y > 550:
            self.y = 565
            self.vy = 0

    def move_3(self):
        self.vy += 0.5
        self.y += self.vy
        if self.y > 560:
            self.y = 570
            self.vy = 0
        if b.y >= 565:
            bombs.remove(b)

    def draw_3(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r,
        )
        pygame.draw.polygon(self.screen, YELLOW, [[self.x + 2, self.y - 12], [self.x - 2, self.y - 12],
                            [self.x + 2, self.y - 5],[self.x + 2, self.y - 5]])
        pygame.draw.polygon(self.screen, RED, [[self.x + 2, self.y - 12], [self.x - 2, self.y - 12],
                                                  [self.x + 2, self.y - 15], [self.x + 2, self.y - 15]])

    def hittest(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False

background_image = pygame.image.load('background.jpg')
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
count_1 = 0
count_2 = 0
balls = []
bombs = []

clock = pygame.time.Clock()
gun = Gun(screen)
target_first = Target(CYAN)
target_second = Target(MAGENTA)
target = Target(BLACK)
platform = Platform(screen)
bomb = Bombs(screen)
finished = False
game_over_1 = False
game_over_2 = False

while not finished:
    if not game_over_1 and not game_over_2:
        screen.blit(background_image, (0, 0))
        gun.draw()
        gun.move()
        platform.draw()
        platform.move()
        target_first.draw()
        target_second.draw_2()
        target_first.move()
        target_second.move_2()


        for b in balls:
            if isinstance(b, Ball):
                b.draw_1()
            else:
                b.draw_2()

        for b in bombs:
            b.draw_3()

        font = pygame.font.Font(None, 36)
        text = font.render("Очков: " + str(points), True, (0, 0, 0))
        screen.blit(text, (10, 10))

        pygame.display.flip()

        pygame.display.update()

        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gun.fire2_start(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    platform.fire_platform()

        for b in bombs:
            b.move_3()
            if b.hittest(target_first) and target_first.live:
                bombs.remove(b)
            if b.hittest(target_second) and target_second.live:
                bombs.remove(b)
            if b.hittest(gun):
                count_1 += 1
                bombs.remove(b)

        if count_1 >= 5:
            game_over_1 = True
        elif count_2 >= 5:
            game_over_2 = True

        for b in balls:
            b.move()
            if b.hittest(target_first) and target_first.live:
                target_first.live = 0
                target_first.hit()
                target_first.new_target()
                points += 1
            if b.hittest(target_second) and target_second.live:
                target_second.live = 0
                target_second.hit()
                target_second.new_target()
                points += 1
            if b.hittest(platform):
                count_2 += 1
                balls.remove(b)

        pygame.display.update()

        pygame.display.flip()

        gun.power_up()

    elif game_over_1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        screen.fill(WHITE)
        f2 = pygame.font.SysFont('serif', 60)
        text2 = f2.render("UFO win", False,
                          (0, 180, 130))

        screen.blit(text2, (280, 230))
        pygame.display.update()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            screen.fill(WHITE)
        f2 = pygame.font.SysFont('serif', 60)
        text2 = f2.render("Tank win", False,
                          (0, 180, 130))

        screen.blit(text2, (280, 230))
        pygame.display.update()

pygame.quit()

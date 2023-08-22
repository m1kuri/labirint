from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
    def shoot(self):
        bullet = Bullet('bullet.png', 5, 5, self.rect.right, self.rect.centery, 15)

class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= 615:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 710:
            self.kill()

window = display.set_mode((700, 500))
display.set_caption('Моя первая игра')
background = transform.scale(image.load('fon.jpg'), (700, 500))
wall_1 = GameSprite('wall.jpg', 80, 250, 200, 250)
wall_2 = GameSprite('wall2.jpg', 140, 45, 280, 250)
wall_3 = GameSprite('wall.jpg', 140, 45, 600, 355)
goal = GameSprite('goal.png', 80, 80, 615, 400)
player = Player('hero.jpg', 50, 50, 0, 0, 0, 0)
enemy1 = Enemy('enemy.png', 80, 80, 620, 80, 5)
enemy2 = Enemy('enemy.png', 80, 80, 680, 180, 5)
walls = sprite.Group()
walls.add(wall_1)
walls.add(wall_2)
walls.add(wall_3)
enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)
bullets = sprite.Group()
run = True
while run:
    time.delay(50)
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.x_speed -= 5
            elif e.key == K_RIGHT:
                player.x_speed += 5
            elif e.key == K_UP:
                player.y_speed -= 5
            elif e.key == K_DOWN:
                player.y_speed += 5
            elif e.key == K_SPACE:
                player.shoot()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                player.x_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0
            elif e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0
    if sprite.spritecollide(player, enemies, False):
        player.rect.x = 0
        player.rect.y = 0
    if sprite.spritecollide(player, walls, False):
        player.x_speed *= -1
        player.y_speed *= -1
    if sprite.collide_rect(player, goal):
        goal.rect.x = randint(100, 600)
        goal.rect.y = randint(100, 400)
    if sprite.groupcollide(bullets, enemies, True, True):
        pass
    player.update()
    player.reset()
    goal.reset()
    walls.update()
    enemies.update()
    bullets.update()
    walls.draw(window)
    enemies.draw(window)
    bullets.draw(window)
    display.update()
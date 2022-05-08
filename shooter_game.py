from pygame import *
from tk import *
from random import randint
# import time


class GameSprite(sprite.Sprite):
    # Конструктор
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        wd.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet(bullet1, self.rect.centerx - 10, self.rect.top, 20, 35, 10)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > width:
            self.rect.x = randint(80, height-80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -=self.speed
        if self.rect.y < 0:
            self.kill()


class Asteroid(GameSprite):
    def update(self):
        self.rect.y +=self.speed*5
        self.rect.x -=self.speed
        # self.rect.x -=self.speed
        if self.rect.y > 500:
            self.kill()
            aster = Asteroid(asteroid, randint(200, 700), -100, 70, 70,randint(2, 3))
            asteroids.add(aster)

# фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_s = mixer.Sound('fire.ogg')

# картинки
back = 'galaxy.jpg'
hero = 'rocket.png'
enemy = 'ufo.png'
bullet1 = 'bullet.png'
asteroid = 'asteroid.png'
# надписи
font.init()
font2 = font.Font(None, 30)
font1 = font.Font(None, 100)
lost = 0 # Переменная для счета пропусков
score = 0 # Переменная для счета попаданий
max_s = 10 # Максимальное кол-во попаданий
max_lost = 40# максимальное кол-во промахов
life = '❤ ' # Картинка жизни
factor = 3 # Начальное кол-во жизней
wait = 200

height = 700 #длина
width = 500 # ширина
wd = display.set_mode((height, width)) # создание экрана
display.set_caption('Межгалактическая битва миров') # название экрана
background = transform.scale(image.load(back), (height, width)) # фон

ship = Player(hero, 5, width-100, 60, 80, 10) # игрок
monsters = sprite.Group() # группа для врагов
for i in range(1, 6):
    monster = Enemy(enemy, randint(80, 600), 0, 50, 40, randint(2, 5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1, 3):
        aster = Asteroid(asteroid, randint(200, 700), -100, 70, 70,randint(2, 3))
        asteroids.add(aster)
bullets = sprite.Group()
finish = False
run = True


while run:
    for i in event.get():
        # Проверка: нажата ли кнопка завершения
        if i.type == QUIT:
            run = False
        elif i.type == KEYDOWN:
            # проверка нажатия пробела
            if i.key == K_SPACE:
                fire_s.play()
                ship.fire()
            elif i.key == K_q:
                # обновление игры при нажатии на "Q" и сборс по умолчанию
                finish = False
                lost = 0
                score = 0
                

    if not finish:
        wd.blit(background, (0, 0)) # Создание окна
        # Счетчик количества попаданий
        text = font2.render('Счет: '+ str(score), 1, (255, 255, 255))
        wd.blit(text, (10, 20))
        #  Пропущено врагов
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        wd.blit(text_lose, (10, 50))
        # Кол-во жизней
        text_life = font2.render('Жизни: ' + life*factor, 1, (255, 255, 255))
        wd.blit(text_life, (10, 80))

        # Изменение координат спрайтов
        monsters.update()
        ship.update()
        bullets.update()
        asteroids.update()

        # new_func(collide, monsters, bullets) # проверка касания и прочее
        for bullet in bullets:
            bullet.reset()
        for ast in asteroids:
            ast.reset()
            wait = 200
            while wait > 0:
                wait -= 1

        # sprite.groupcollide(bullets, monsters, True, True)
        collides = sprite.groupcollide(bullets, monsters, True, True)
        # collides1 = sprite.spritecollide(asteroids, ship, True, True)
        for i in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 600), 0, 50, 40, randint(2, 5))
            # score = score + 1
            monsters.add(monster)

        if (sprite.spritecollide(ship, monsters, False)) or (lost >= max_lost):
            over = font1.render('GAME OVER', 1, (255,255,255))
            wd.blit(over, (100, 200))
            # global finish
            finish = True

        if score>=max_s:
            win = font1.render('YOU WIN', 1, (255, 255, 255))
            wd.blit(win, (200, 250))
            finish = True
        # Визуальное обновление 
        ship.reset()
        monsters.draw(wd)
        display.update() # штука непонятная, но нужная
        time.delay(50) # то же самоедо жл 

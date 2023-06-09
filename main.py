from pygame import *
from random import randint
from time import time as timer

init()



window = display.set_mode((700, 700)) #Створюємо вікно
display.set_caption("Real Minecraft not fake 100%") #Також називаэмо його
display.set_icon(image.load('grass.png'))# Встановлюємо іконку програми
background = transform.scale(image.load("phon.png"), (700, 700))

clock = time.Clock()
font.init() 

font1 = font.SysFont('Arial', 20)
font2 = font.SysFont('Arial', 50)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite): # Клас игрока и его параметры и что он умеет
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self): #наша ракета будет растреливать криперов :) 
        bullet = Bullet('Chrest.png', self.rect.centerx, self.rect.top, 15, 5, 9)
        bullets.add(bullet)

lost = 0 # зміна яка збережує пропусків
class Enemy(GameSprite): #создаёт клас врагов
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x = randint(50, 600)
            lost += 1

class Asteroids(GameSprite): #создаёт клас астероидов 

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x = randint(50, 600)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player('ra.png', 310, 600, 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('creeper.png', randint(50, 600), -50, 80, 50, randint(1, 2))
    monsters.add(enemy)
bedrocks = sprite.Group()
for i in range(3):
    bedrock = Asteroids("bedrock.png", randint(50, 600), -50, 80, 50, randint(1, 3))
    bedrocks.add(bedrock)
bullets = sprite.Group() 

#mixer.init()
#mixer.music.load('space.ogg')  
#mixer.music.play()

fps = 60 
game = True
finish = False
rel_time = False


mixer.init()
fire_snd = mixer.Sound('fire.ogg')
 
killed = 0
life = 5
num_fire = 0

while game: # игровой цикл 

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and rel_time == False:
                    num_fire += 1
                    player.fire()
                    fire_snd.play()
                if num_fire > 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()

    if not finish:

        

        window.blit(background, (0, 0))

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        bedrocks.draw(window)
        bedrocks.update()

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('Поливаем себя святой водой...', 1, (255, 0, 0))
                window.blit(reload, (250, 500))
            else:
                rel_time = False 
                num_fire = 0
        
        collides = sprite.groupcollide(bullets, monsters, True, True)
        for col in collides:
            enemy = Enemy('sPIDOR.png', randint(50, 600), -50, 80, 50, randint(1, 3))
            monsters.add(enemy)
            killed += 1
        
        if sprite.spritecollide(player, monsters, True):
            life -= 1 #
        if sprite.spritecollide(player, bedrocks, True):
            life -= 1
            bedrock = Asteroids("bedrock.png", randint(50, 600), -50, 80, 50, randint(1, 3))
            bedrocks.add(bedrock)
        

        score = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(score, (10, 20))
        life1 = font1.render(str(life), 1, (255, 255, 255))
        score = font1.render('Пропущено: ' + str(lost) ,1, (0, 0, 0))
        window.blit(score, (10, 20))
        killed_txt = font1.render('Збито: ' + str(killed), 1, (255, 255, 255))
        window.blit(killed_txt, (10, 45))

        if killed >= 20:
            finish = True
            win1 = font2.render("Ты збив " + str(killed) + ' мобов', 1, (0,255,0))
            win2 = font2.render("Ти спас майнкрафт! пупсик :)))", 1, (0, 255, 0))
            window.blit(win1, (125, 350))
            window.blit(win2, (125, 400))


        if lost >= 20 or life == 0:
            finish = True
            lose = font2.render('Неееттт майнкрафт упал!! Ти збил ' + str(killed) + "НЛО", 1, (0, 255, 0))
            window.blit(lose, (125,350))
        display.update()
    else:
        keys = key.get_pressed()
        if keys[K_r]:
            finish = False
            lost = 0
            killed = 0
            life = 5
            for b in bullets:
                b.kill()
            for m in monsters:
                m.kill()
            for i in range(5):
                enemy = Enemy('creeper.png', randint(50, 600), -50, 80, 50, randint(1, 2))
                monsters.add(enemy)



        display.update()

    display.update()
    clock.tick(fps)
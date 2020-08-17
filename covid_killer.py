#Shmup Game (shootem' up)
import pygame
import random
from os import path
from pygame import mixer

img_dir = path.join(path.dirname(__file__), 'img_dir')
player_explosion_dir = path.join(path.dirname(__file__), 'img_dir/player_explosion_blue_ring')
snd_dir = path.join(path.dirname(__file__), 'sounds')

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREENSCREEN = (15, 255, 39)

# initialize pygame and create screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("COViD 19 KiLLER")
clock = pygame.time.Clock()

# load background music
pygame.mixer.music.load(path.join(snd_dir, 'friend_gameloop.mp3'))
pygame.mixer.music.set_volume(1)
mixer.music.play(loops=-1)

font_name = pygame.font.match_font('ariel')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_WIDTH = 10
    BAR_HEIGHT = 100
    fill = (pct / 100 * BAR_HEIGHT)
    outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y + 100, BAR_WIDTH, -fill)
    pygame.draw.rect(surf, GREEN, fill_rect)
    # pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x - 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 150
        self.speedx, self.speedy = 0, 0
        self.shield = 100

        # rapid fire
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()

        # lives
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()


    def update(self):
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 150

        # resets speed to 0 when key is not pressed
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -7
        if keystate[pygame.K_RIGHT]:
            self.speedx = 7
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < WIDTH - WIDTH:
            self.rect.left = WIDTH - WIDTH

        if keystate[pygame.K_UP]:
            self.speedy = -7
        if keystate[pygame.K_DOWN]:
            self.speedy = 7
        self.rect.y += self.speedy
        if self.rect.top < HEIGHT - HEIGHT:
            self.rect.top = HEIGHT - HEIGHT
        if not self.hidden:
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT


    def shoot(self):
        if not player.hidden:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bulletL = Bullet(self.rect.left + 5, self.rect.bottom - 5)
                bulletR = Bullet(self.rect.right - 5, self.rect.bottom - 5)
                all_sprites.add(bulletL)
                all_sprites.add(bulletR)
                bullets.add(bulletL)
                bullets.add(bulletR)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 1000)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(mob_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(5, 12)
        self.speedx = random.randrange(-4, 4)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot += self.rot_speed % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.right < (WIDTH - WIDTH - 10) or self.rect.left > (WIDTH + 10):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-4, 4)
            self.speedy = random.randrange(1, 10)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 74))
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y - 20
        self.rect.centerx = x
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'shield', 'shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, radius, size, frame_rate):
        pygame.sprite.Sprite.__init__(self)
        self.frame_rate = frame_rate
        self.size = size
        self.radius = int(radius**1.6)

        if size == 'exp':
            self.image = pygame.transform.scale(explosion_anim[self.size][0], (self.radius, self.radius))
        elif size == 'sm':
            self.image = explosion_anim[self.size][0]
        elif size == 'player_ex':
            self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                if self.size == 'exp':
                    self.image = pygame.transform.scale(explosion_anim[self.size][self.frame], (self.radius, self.radius))
                elif self.size == 'sm':
                    self.image = pygame.transform.scale(explosion_anim[self.size][self.frame],(32, 32))
                elif self.size == 'player_ex':
                    self.image = pygame.transform.scale(explosion_anim[self.size][self.frame],(250, 250))
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "C     O     V     i     D", 25, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "K          i          L          L         E          R", 35, WIDTH / 2, HEIGHT / 4 + 30)
    # draw_text(screen, "ARROW KEYS TO MOVE, SPACE TO FIRE", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "PRESS A KEY", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Load all GAME GRAPHICS:
background = pygame.image.load(path.join(img_dir, "background.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "ship1-1copy.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 20))
player_mini_img.set_colorkey(BLACK)
laser_img = pygame.image.load(path.join(img_dir, "lasers2.png")).convert()

mob_images = []
mob_list = ["corona copy.png", "corona copy_big.png", "corona copy_small.png"]
for img in mob_list:
    mob_images.append(pygame.image.load(path.join(img_dir, img)).convert())

# explosions
explosion_anim = {}
explosion_anim['exp'] = []
explosion_anim['sm'] = []
explosion_anim['player_ex'] = []
for i in range(13):
    filename = 'explosion{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['exp'].append(img)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

for j in range(1, 17):
    filename = 'player_explosion_blue_ring{}.png'.format(j)
    img1 = pygame.image.load(path.join(player_explosion_dir, filename)).convert()
    img1.set_colorkey(BLACK)
    img1 = pygame.transform.scale(img1, (250, 250))
    explosion_anim['player_ex'].append(img1)

# powerups
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'powerupGreen_shield.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'powerupRed_bolt.png')).convert()

# load all game sounds:
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Bottle Rocket.wav'))
corona_explosion_sound = pygame.mixer.Sound(path.join(snd_dir, 'corona_Explosion1.wav'))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'player_explosion.wav'))
shields_sound = pygame.mixer.Sound(path.join(snd_dir, 'power_up2.wav'))
weapons_sound = pygame.mixer.Sound(path.join(snd_dir, 'power_up1.wav'))

# main game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        # GROUPS
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        powerups = pygame.sprite.Group()
        all_sprites.add(player)
        for i in range(10):
            newmob()
        score = 0

    # keep loop running at the correct speed
    clock.tick(FPS)

    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            # running = False
            quit()

    # update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        corona_explosion_sound.play()
        expl = Explosion(hit.rect.center, hit.radius, 'exp', 25)
        all_sprites.add(expl)
        #powerup lotto
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 1.90
        expl = Explosion(hit.rect.center, hit.radius, 'sm', 25)
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, hit.radius, 'player_ex', 50)
            all_sprites.add(death_explosion)
            player_die_sound.play()
            player.hide()
            player.lives -= 1
            player.shield = 100
            if not death_explosion.alive():
                death_explosion.kill()

    # check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            shields_sound.play()
            player.shield += 20
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            weapons_sound.play()
            player.shoot_delay -= 50
            if player.shoot_delay <= 100:
                player.shoot_delay = 50

    # if the player died and the explosion has finished
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(f'score: {score}'), 20, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 495, player.shield)
    draw_lives(screen, WIDTH - 30, HEIGHT - 20, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
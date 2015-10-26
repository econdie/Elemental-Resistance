# Elemental Resistance
import pygame
import random

WIDTH = 1280
HEIGHT = 720
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elemental Resistance")
clock = pygame.time.Clock()

#define classes
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((40, 40))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.speedy = 0
		self.status = 'gather'


	def update(self):
		self.speedx = 0
		self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -20
		if keystate[pygame.K_RIGHT]:
			self.speedx = 20
		self.rect.x += self.speedx

		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

		if keystate[pygame.K_UP]:
			self.speedy = -15
		if keystate[pygame.K_DOWN]:
			self.speedy = 15
		self.rect.y += self.speedy

		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > 600:
			self.rect.bottom = 600

class ElementMob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class FireMob(ElementMob):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((30, 30))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.top = 0
		self.speedx = 0

	def update(self):
		pass

class PlayerResources(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class WaterResource(PlayerResources):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.water = 0
		font = pygame.font.Font(None, 24)
		font_color = (200,200,200)
		font_background = (0, 0, 0)
		self.image = font.render(str(self.water), True, font_color, font_background)
		self.rect = self.image.get_rect()
		self.rect.centerx = 100
		self.rect.centery = 100
		

	def update(self):
		font = pygame.font.Font(None, 24)
		font_color = (200,200,200)
		font_background = (0, 0, 0)
		self.image = font.render(str(self.water), True, font_color, font_background)

class Raindrop(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((15, 15))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(0, WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 8)

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(0, WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)

all_sprites = pygame.sprite.Group()
all_resources = pygame.sprite.Group()
all_fireMobs = pygame.sprite.Group()
all_raindrops = pygame.sprite.Group()

# Initiate game
player = Player()
all_sprites.add(player)

fireMob = FireMob()
all_fireMobs.add(fireMob)
all_sprites.add(fireMob)

waterResource = WaterResource()
all_sprites.add(waterResource)
all_resources.add(waterResource)

for i in range(8):
	raindrop = Raindrop()
	all_sprites.add(raindrop)
	all_raindrops.add(raindrop)

# Game loop
running = True
while running:
	# keep loop running at the right speed
	clock.tick(FPS)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False
	# Update
	all_sprites.update()

	waterGather = pygame.sprite.spritecollide(player, all_raindrops, True)
	for hits in waterGather:
		raindrop = Raindrop()
		all_sprites.add(raindrop)
		all_raindrops.add(raindrop)
		waterResource.water += 1
		
	# Draw / render
	screen.fill(BLACK)
	all_sprites.draw(screen)
	# after drawing everything, flip the display
	pygame.display.flip()

pygame.quit()

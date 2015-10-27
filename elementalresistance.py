# Elemental Resistance
import pygame
import random
import time

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

	def initiateWater(self):
		self.status = 'water'
		self.image.fill(BLUE)
		
	def initiateGather(self):
		self.status = 'gather'
		self.image.fill(GREEN)
		for i in range(8):
			raindrop = Raindrop()
			all_sprites.add(raindrop)
			all_raindrops.add(raindrop)

	def initiateSupernova(self):
		supernova = SupernovaMob()
		all_sprites.add(supernova)
		all_supernovas.add(supernova)

	def initiateLight(self):
		self.status = 'light'
		self.image.fill(WHITE)



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

class SupernovaMob(ElementMob):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.explosionTimer = time.clock()
		self.image = pygame.Surface((30, 30))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(0, WIDTH - self.rect.width)
		self.rect.top = random.randrange(0, HEIGHT - 100)
		

	def update(self):
	 	if time.clock() - self.explosionTimer > 5:
	 		explosion = pygame.sprite.spritecollide(player, all_supernovas, False)
	 		if explosion:
	 			lightResource.light += 1000
	 			self.kill()
	 		else:
	 			pygame.quit()
	 		
	 	


class PlayerResources(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class WaterResource(PlayerResources):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.water = 0
		self.font = pygame.font.Font(None, 24)
		self.font_color = (200,200,200)
		self.font_background = (0, 0, 0)
		self.image = self.font.render(str(self.water), True, self.font_color, self.font_background)
		self.rect = self.image.get_rect()
		self.rect.centerx = 100
		self.rect.centery = 100
		

	def update(self):
		self.image = self.font.render(str(self.water), True, self.font_color, self.font_background)

class LightResource(PlayerResources):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.light = 0
		self.font = pygame.font.Font(None, 24)
		self.font_color = (200,200,200)
		self.font_background = (0, 0, 0)
		self.image = self.font.render(str(self.light), True, self.font_color, self.font_background)
		self.rect = self.image.get_rect()
		self.rect.centerx = 100
		self.rect.centery = 200

	def update(self):
		self.image = self.font.render(str(self.light), True, self.font_color, self.font_background)


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

		if player.status != 'gather':
			for raindrops in all_raindrops:
				if raindrops.rect.y > HEIGHT:
					raindrops.kill()


all_sprites = pygame.sprite.Group()
all_resources = pygame.sprite.Group()
all_fireMobs = pygame.sprite.Group()
all_raindrops = pygame.sprite.Group()
all_supernovas = pygame.sprite.Group()

# Initiate game
player = Player()
all_sprites.add(player)

fireMob = FireMob()
all_fireMobs.add(fireMob)
all_sprites.add(fireMob)

waterResource = WaterResource()
all_sprites.add(waterResource)
all_resources.add(waterResource)
lightResource = LightResource()
all_sprites.add(lightResource)
all_resources.add(lightResource)

player.initiateGather()
counter = 0

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
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				player.initiateWater()
				player.initiateSupernova()
			elif event.key == pygame.K_e:
				player.initiateGather()
			elif event.key == pygame.K_r:
				player.initiateLight()
				# initiate black bullets that come horizontally
				
				
				
	# Update
	all_sprites.update()
	counter += 0.3
	if player.status == 'light':
		if lightResource.light > 0:
			counter -= 0.6
			lightResource.light -= 1

	if player.status == 'gather':
		waterGather = pygame.sprite.spritecollide(player, all_raindrops, True)
		for hits in waterGather:
			raindrop = Raindrop()
			all_sprites.add(raindrop)
			all_raindrops.add(raindrop)
			waterResource.water += 1
	
	elif player.status == 'water':
		waterUsage = pygame.sprite.spritecollide(player, all_fireMobs, True)
		for hits in waterUsage:
			if waterResource.water >= 10:
				waterResource.water -= 10
			else:
				running = False
		pass
	# Draw / render
	if counter <= 255 and counter >= 0:
		screen.fill((255 - counter, 255 - counter, 255 - counter))
	elif counter <= 255: 
		screen.fill((255, 255, 255))
	else:
		running = False
	all_sprites.draw(screen)
	# after drawing everything, flip the display
	pygame.display.flip()

pygame.quit()

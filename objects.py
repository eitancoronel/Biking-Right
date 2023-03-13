import math
import pygame
import random

SCREEN = WIDTH, HEIGHT = 432, 768

BLUE = (53, 81, 92)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

lane_pos = [75, 142, 220, 300]

class Road():
	def __init__(self):
		self.image = pygame.image.load('Assets/road.png')
		self.image = pygame.transform.scale(self.image, (WIDTH-60, HEIGHT))

		self.reset()
		self.move = True

	def update(self, speed):
		if self.move:
			self.y1 += speed
			self.y2 += speed

			if self.y1 >= HEIGHT:
				self.y1 = -HEIGHT
			if self.y2 >= HEIGHT:
				self.y2 = -HEIGHT

	def draw(self, win):
		win.blit(self.image, (self.x, self.y1))
		win.blit(self.image, (self.x, self.y2))

	def reset(self):
		self.x = 30
		self.y1 = 0
		self.y2 = -HEIGHT

RESIZE_FACTOR = 1.2
class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, type):
		super(Player, self).__init__()
		if type<8:
			self.image = pygame.image.load(f'Assets/cars/{type+1}.png')
		else:
			self.image = pygame.image.load(f'Assets/cars/Picture_bike.png')
		self.image = pygame.transform.scale(self.image, (int(48*RESIZE_FACTOR), int(82*RESIZE_FACTOR)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, left, right,left_foot,right_foot):
		if left:
			self.rect.x -= 5*(left_foot/50)
			if self.rect.x <= 40:
				self.rect.x = 40
		if right:
			self.rect.x += 5*(right_foot/50)
			if self.rect.right >= WIDTH-38:
				self.rect.right = WIDTH-38

		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)

class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type):
		super(Obstacle, self).__init__()
		dx = 0
		self.type = type

		if type == 1:
			ctype = random.randint(1, 8)
			self.image = pygame.image.load(f'Assets/cars/{ctype}.png')
			self.image = pygame.transform.flip(self.image, False, True)
			self.image = pygame.transform.scale(self.image, (int(48*RESIZE_FACTOR), int(82*RESIZE_FACTOR)))
		if type == 2:
			self.image = pygame.image.load('Assets/barrel.png')
			self.image = pygame.transform.scale(self.image, (int(24*RESIZE_FACTOR), int(36*RESIZE_FACTOR)))
			dx = 10
		elif type == 3:
			self.image = pygame.image.load('Assets/roadblock.png')
			self.image = pygame.transform.scale(self.image, (int(50*RESIZE_FACTOR), int(25*RESIZE_FACTOR)))

		self.rect = self.image.get_rect()
		self.rect.x = random.choice(lane_pos) + dx
		self.rect.y = -100

	def update(self, speed):
		self.rect.y += speed

		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)


class Tree(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Tree, self).__init__()

		type = random.randint(1, 4)
		self.image = pygame.image.load(f'Assets/trees/{type}.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed):
		self.rect.y += speed
		if self.rect.top >= HEIGHT:
			self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)

val = 0
class Fuel(pygame.sprite.Sprite):

	def __init__(self, x, y):
		super(Fuel, self).__init__()
		self.image = pygame.image.load('Assets/arrows/Picture1.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


	def update(self, speed,color_average):
		global val
		pic_1 = "Assets/arrows/Picture1.png"
		pic_2 = "Assets/arrows/Picture2.png"
		pic_3 = "Assets/arrows/Picture3.png"
		pic_4 = "Assets/arrows/Picture4.png"
		pic_5 = "Assets/arrows/Picture5.png"
		pic_6 = "Assets/arrows/Picture6.png"
		pic_7 = "Assets/arrows/Picture7.png"
		pic_8 = "Assets/arrows/Picture8.png"
		pic_9 = "Assets/arrows/Picture9.png"
		pic_10 = "Assets/arrows/Picture9.png"
		base_value = 0
		if 0 <= color_average < base_value:
			self.image = pygame.image.load(pic_1)
			val=5
		elif base_value <= color_average < base_value + 20:
			self.image = pygame.image.load(pic_2)
			val=6
		elif base_value + 20 <= color_average < base_value + 40:
			self.image = pygame.image.load(pic_3)
			val = 7
		elif base_value + 40 <= color_average < base_value + 60:
			self.image = pygame.image.load(pic_4)
			val = 8
		elif base_value + 60 <= color_average < base_value + 70:
			self.image = pygame.image.load(pic_5)
			val = 10
		elif base_value + 70 <= color_average < base_value + 80:
			self.image = pygame.image.load(pic_6)
			val = 15
		elif base_value + 80 <= color_average < base_value + 90:
			self.image = pygame.image.load(pic_7)
			val = 20
		elif base_value + 90 <= color_average < base_value + 100:
			self.image = pygame.image.load(pic_8)
			val = 25
		elif base_value + 100 <= color_average < base_value + 110:
			self.image = pygame.image.load(pic_9)
			val = 30
		else:
			self.image = pygame.image.load(pic_10)
			val = 40

		self.rect.y += speed

		if self.rect.top >= HEIGHT:
			self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)

	def getVal(self):
		return val

class Coins(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Coins, self).__init__()

		self.images = []
		for i in range(1, 7):
			img = pygame.image.load(f'Assets/Coins/{i}.png')
			self.images.append(img)

		self.counter = 0
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed):
		self.counter += 1
		if self.counter % 5 == 0:
			self.index = (self.index + 1) % len(self.images)

		self.rect.y += speed
		if self.rect.top >= HEIGHT:
			self.kill()

		self.image = self.images[self.index]

	def draw(self, win):
		win.blit(self.image, self.rect)

class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()
		
		self.scale = scale
		self.image = pygame.transform.scale(img, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action
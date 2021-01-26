import pygame
from pygame.locals import * 
import time


clock = pygame.time.Clock()  # getting computer performance
fps = 60   # setting fps to 60

screenWidth = 600  # setting screen height
screenHeight = 800  # settign screen width

# defining colors for the health bar
yellow = (255,214,98)
blue = (0,83,156) 
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)


screen = pygame.display.set_mode((screenWidth, screenHeight))  #set screen width and height
pygame.display.set_caption('Space Invaders')  # set window caption


# class to create spaceship
class Spaceship(pygame.sprite.Sprite):  # using pygame sprite class
  def __init__(self, x, y, health):  # define attributes of Spaceship class
    pygame.sprite.Sprite.__init__(self)  #  inheriting sprite attribues
    self.image = pygame.image.load("img/spaceship.png")  # define sprite image property
    self.rect = self.image.get_rect() # define sprite rectangle property
    self.rect.center = [x, y]  # define center of rectangle
    self.initialHealth = health
    self.currentHealth = health

  # overwriting default update function
  def update(self):
    speed = 5  # speed of spaceship
    key = pygame.key.get_pressed()  # key listener
    if key[pygame.K_LEFT] and self.rect.left >= 0:  # if the left key was pressed
      self.rect.x -= speed  # move to the left
    if key[pygame.K_RIGHT] and self.rect.right <= screenWidth:  # if the right key was pressed
      self.rect.x += speed  # move to the right
    if key[pygame.K_SPACE] and self.rect.right <= screenWidth:  # if the space key was pressed
      print(self.rect.center, self.rect.centerx)
      bullet = Bullets(self.rect.centerx, self.rect.top)  # create a bullet right above the spaceship
      bullet_group.add(bullet)  # add bullet to the sprite group

    # draw health bar 
    pygame.draw.rect(screen, red, (500, 25, self.rect.width, 15))  # draw the red rectangle (representing damage taken)
    if self.currentHealth > 0:  # if player still alive
      pygame.draw.rect(screen, green, (500, 25, self.rect.width * (self.currentHealth // self.initialHealth), 15))  # draw the health which user has


# class to create bullets
class Bullets(pygame.sprite.Sprite):  # using pygame sprite class
  def __init__(self, x, y):  # define attributes of Bullet class
    pygame.sprite.Sprite.__init__(self)  #  inheriting sprite attribues
    self.image = pygame.image.load("img/bullet.png")  # define sprite image property
    self.rect = self.image.get_rect() # define sprite rectangle property
    self.rect.center = [x, y]  # define center of rectangle

  # overwriting default update function
  def update(self):
    print('updating bullet... ')
    print(self.rect.x, self.rect.y)
    self.rect.y -= 5  # each time called (in while loop), mode down 5

    
# create sprite groups 
'''sprite groups are container class to contain a group of classes (kind of like a list for class obejcts) -> allows you to perform group updates '''
spaceship_group = pygame.sprite.Group()  # spaceship sprite group
bullet_group = pygame.sprite.Group()  # bullet sprite group

# instantiate the spaceship (user)
spaceship = Spaceship(screenWidth // 2, screenHeight - 75, 3)
spaceship_group.add(spaceship)  # adding spaceship obejct to sprite group



run = True


while run: 

  #load image
  bg = pygame.image.load("img/bg.png")
  screen.blit(bg, (0, 0))

  # limit fps to predefined variable
  clock.tick(fps)

  # event handler
  for event in pygame.event.get():  # look through pygame events
    if event.type == pygame.QUIT:  # if the quit event is called
      run = False  # leave while loop

  spaceship.update()  # updating spaceship
  bullet_group.update()  # updating all bullets in sprite group
  
  # draw spaceship on screen (using sprite's draw method)
  spaceship_group.draw(screen)
  bullet_group.draw(screen)

  
  # display 
  pygame.display.update()

pygame.quit()
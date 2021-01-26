import pygame
from pygame.locals import * 
import time
import random

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
    self.initialHealth = health  # health we started with
    self.currentHealth = health  # current health of spaceship
    self.gunShot = time.time()  # time of last gunshot

  # overwriting default update function
  def update(self):
    speed = 5  # speed of spaceship
    currentTime = time.time()  # getting current time

    key = pygame.key.get_pressed()  # key listener
    if key[pygame.K_LEFT] and self.rect.left >= 0:  # if the left key was pressed
      self.rect.x -= speed  # move to the left
    if key[pygame.K_RIGHT] and self.rect.right <= screenWidth:  # if the right key was pressed
      self.rect.x += speed  # move to the right
    if key[pygame.K_SPACE] and currentTime - self.gunShot >= 0.5:  # if the space key was pressed
      bullet = Bullets(self.rect.centerx, self.rect.top)  # create a bullet right above the spaceship
      bullet_group.add(bullet)  # add bullet to the sprite group
      self.gunShot = currentTime  # update the last shot time

    # draw health bar 
    pygame.draw.rect(screen, red, (500, 25, self.rect.width, 15))  # draw the red rectangle (representing damage taken)
    if self.currentHealth > 0:  # if player still alive
      pygame.draw.rect(screen, green, (500, 25, self.rect.width * (self.currentHealth / self.initialHealth), 15))  # draw the health which user has


# class to create bullets
class Bullets(pygame.sprite.Sprite):  # using pygame sprite class
  def __init__(self, x, y):  # define attributes of Bullet class
    pygame.sprite.Sprite.__init__(self)  #  inheriting sprite attribues
    self.image = pygame.image.load("img/bullet.png")  # define sprite image property
    self.rect = self.image.get_rect() # define sprite rectangle property
    self.rect.center = [x, y]  # define center of rectangle

  # overwriting default update function
  def update(self):
    self.rect.y -= 10  # each time called (in while loop), mode down 5
    if self.rect.bottom < 0:  # if the bullet has left the screen
      self.kill()  # delete it from the pygame sprite class
    if pygame.sprite.spritecollide(self, alien_group, True): # cheking if a bullet has come into contact with any instance in our alien sprite group
      self.kill()


# class to create aliens
class Aliens(pygame.sprite.Sprite):  # using pygame sprite class
  def __init__(self, x, y, numAlien):  # define attributes of Alien class
    pygame.sprite.Sprite.__init__(self)  #  inheriting sprite attribues
    self.image = pygame.image.load("img/alien" + str(numAlien) + ".png")  # define sprite image property
    self.rect = self.image.get_rect() # define sprite rectangle property
    self.rect.center = [x, y]  # define center of rectangle
    self.direction = 1  # initialize the direction of the aliens
    self.counter = 1  # initialize the alien movement counter

  # overwriting default update function
  def update(self):
    self.rect.x += self.direction  # move aliens either left or right (depending on direction)
    self.counter += self.direction  # track how far the aliens have shifted left/right
    if abs(self.counter) > 75:  # if the aliens have moved more than 75 points left/right
      self.direction *= -1  # change the direction
      self.rect.y += 3  # shift each alien down 3
      self.counter *= self.direction  # reverse the counter


# class to create AlienBullets
class AlienBullets(pygame.sprite.Sprite):  # using pygame sprite class
  def __init__(self, x, y):  # define attributes of AlienBullets class
    pygame.sprite.Sprite.__init__(self)  #  inheriting sprite attribues
    self.image = pygame.image.load("img/alien_bullet.png")  # define sprite image property
    self.rect = self.image.get_rect() # define sprite rectangle property
    self.rect.center = [x, y]  # define center of rectangle

  # overwriting default update function
  def update(self):
    self.rect.y += 7  # each time called (in while loop), mode up 5
    if self.rect.top < 0:  # if the bullet has left the screen
      self.kill()  # delete it from the pygame sprite class
    if pygame.sprite.spritecollide(self, spaceship_group, False): # cheking if a bullet has come into contact with the spaceship
      spaceship.currentHealth -= 1  # reduce the health of the spaceship
      self.kill()


# create sprite groups 
'''sprite groups are container class to contain a group of classes (kind of like a list for class obejcts) -> allows you to perform group updates  '''
spaceship_group = pygame.sprite.Group()  # spaceship sprite group
bullet_group = pygame.sprite.Group()  # bullet sprite group
alien_group = pygame.sprite.Group()  # alien sprite group
alien_bullet_group = pygame.sprite.Group()  # alien sprite group

# instantiate the spaceship (user)
spaceship = Spaceship(screenWidth // 2, screenHeight - 75, 3)
spaceship_group.add(spaceship)  # adding spaceship obejct to sprite group


# function to create aliens
def createAliens(rows, cols):
  for row in range(rows):  #  loop through rows
    for col in range(cols):  # loop through columns
      alien = Aliens(100+ col*100, 100 + row * 75, row+1)  # initialize aliens
      alien_group.add(alien)  # add alien to sprite group


createAliens(5, 5)  # create 5 rows & 5 cols of aliens

gamePlaying = True  # variable to track whether user is still playing
lastShot = time.time()  # time game starts
while gamePlaying: 

  # limit fps to predefined variable
  clock.tick(fps)

  #load image
  bg = pygame.image.load("img/bg.png")
  screen.blit(bg, (0, 0))

  # create alien bullets
  timeNow = time.time()  # current time
  if timeNow - lastShot > 1 and len(alien_group) > 0:
    alien = random.choice(alien_group.sprites())
    alienBullet = AlienBullets(alien.rect.centerx, alien.rect.bottom)
    alien_bullet_group.add(alienBullet)
    lastShot = timeNow  # updating the last shot


  
  # event handler
  for event in pygame.event.get():  # look through pygame events
    if event.type == pygame.QUIT or len(alien_group) == 0 or spaceship.currentHealth == 0:  # if the quit event is called
      gamePlaying = False  # leave while loop


  spaceship.update()  # updating spaceship
  bullet_group.update()  # updating all bullets in sprite group
  alien_group.update()  # updating all aliens in sprite group
  alien_bullet_group.update()  # updating all alien bullets in sprite group
  
  spaceship_group.draw(screen)  # draw spaceship on screen
  bullet_group.draw(screen)  # drawing bullets on screen
  alien_group.draw(screen)  # drawing aliens on screen
  alien_bullet_group.draw(screen)  # drawing alien bullets on screen

  
  # display updated classes to screen
  pygame.display.update()

pygame.quit()  # quit pygame
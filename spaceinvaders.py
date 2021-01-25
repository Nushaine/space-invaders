import pygame
from pygame.locals import * 


clock = pygame.time.Clock()  # getting computer performance
fps = 60   # setting fps to 60

screenWidth = 600  # setting screen height
screenHeight = 800  # settign screen width

screen = pygame.display.set_mode((screenWidth, screenHeight))  #set screen width and height
pygame.display.set_caption('Space Invaders')  # set window caption


# class to create spaceship
class Spaceship(pygame.sprite.Sprite):  # using pygame sprite class
  def __init__(self, x, y):  # define attributes of Spaceship class
    pygame.sprite.Sprite.__init__(self)  #  inheriting sprite attribues
    self.ship = pygame.image.load("img/spaceship.png")  # define image of spaceship
    self.rectangle = self.ship.get_rect() # get rectangle from ship iamge
    self.rectangle.center = [x, y]  # define center of rectangle

# create sprite groups -> container class to 
spceship_group = pygame.sprite.Group()





run = True


while run: 

  # limit fps to predefined variable
  clock.tick(fps)

  # event handler
  for event in pygame.event.get():  # look through pygame events
    if event.type == pygame.QUIT:  # if the quit event is called
      run = False  # leave while loop
  
  # display 
  pygame.display.update()

pygame.quit()
import pygame
import sys
import random
import math
import os
#importování potřebných knihoven


class Snowfall: #třída Snowfall

    def __init__(self, **kwargs):   #inicializační metoda třídy Snowfall.
        pygame.init()

        self.__info = pygame.display.Info()
        self.__width = kwargs['width'] if 'width' in kwargs else self.__info.current_w
        self.__height = kwargs['height'] if 'height' in kwargs else self.__info.current_h
        self.__snowflakes_amount = kwargs['snowflakes_amount'] if 'snowflakes_amount' in kwargs else 250
        self.__bg_image = kwargs['bg_image'] if 'bg_image' in kwargs else ("baldyu.webp", "judgement.jpg", "yagami.webp")
        self.__white = kwargs['white'] if 'white' in kwargs else ((250, 25, 250, 10), (240, 240, 20, 10), (23, 230, 230, 10))
        self.__caption = kwargs['caption'] if 'caption' in kwargs else "Snowfall Screensaver"
        self.__speed = kwargs['speed'] if 'speed' in kwargs else 30
        self.__snowflakes = []

        pygame.mixer.init()
        pygame.mixer.music.load("original_screensaver_soundtrack.mp3") #načtení hudby
        pygame.mixer.music.play(-1)  # -1 opakovat do nekonečna

        self.__surface = pygame.display.set_mode((self.__width, self.__height), pygame.SRCALPHA, pygame.RESIZABLE)
        pygame.display.set_caption(self.__caption)
        self.__bg = pygame.image.load(f"{os.path.dirname(os.path.realpath(__file__))}\\img\\{self.__bg_image[random.randint(0, len(self.__bg_image) - 1)]}")
        self.__bg = pygame.transform.scale(self.__bg, (self.__width, self.__height))
        pygame.mouse.set_visible(0)
        pygame.display.flip()
        
    def clearSnowflakes(self):   #metoda co maže vločky
        self.__snowflakes = []

    def generateSnowflakes(self): #metoda generující vločky
        for _ in range(self.__snowflakes_amount):
            self.__snowflakes.append(Snowflake(random.randint(0, self.__width), random.randint(0, self.__height), self.__width, self.__height))        
    
    def go(self): #metoda pro spouštění sněžení
        
        self.generateSnowflakes()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONUP:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.__width == self.__info.current_w:
                        self.__width = self.__info.current_w // 2
                        self.__height = self.__info.current_h // 2
                        self.__snowflakes_amount //= 4
                        self.clearSnowflakes()
                        self.generateSnowflakes()
                        self.__surface = pygame.display.set_mode((self.__width, self.__height), pygame.SRCALPHA, pygame.RESIZABLE)
                        self.__surface.blit(self.__surface, (self.__width - self.__surface.get_width() // 2, self.__height - self.__surface.get_height() // 2))
                        self.__bg = pygame.transform.scale(self.__bg, (self.__width, self.__height))
                        pygame.display.flip()

            self.__surface.blit(self.__bg, (0, 0))  

            for snowflake in self.__snowflakes:
                snowflake.fall(self.__width, self.__height)
                snowflake.draw(self.__surface, self.__white)

            pygame.display.flip()
            pygame.time.Clock().tick(self.__speed)

class Snowflake: #třída Vločka
    def __init__(self, x, y, width, height):
        self.__x = x
        self.__y = y
        self.__size = random.randint(15, 25)
        self.__wind = random.randint(-1, 1)
        self.__color = random.randint(0, 2)

    def fall(self, width, height): #metoda pro padání vločky
        self.__y += self.__size

        if self.__wind == -1:
            self.__x += math.sin(self.__y / 90)
        elif self.__wind == 1:
            self.__x += math.cos(self.__y / 90)           

        if self.__y > height:
            self.__y = 0
            self.__x = random.randint(0, width)
            self.__size = random.randint(15, 25)
            self.__wind = random.randint(-1, 1)
            self.__color = random.randint(0, 2)

    def draw(self, surface, white):
        pygame.draw.circle(surface, white[self.__color], (self.__x, self.__y), self.__size)

snow = Snowfall(\
    width=1920,\
    height=1080,\
    speed=40,\
    snowflakes_amount=250,\
    bg_image=("baldyu.webp", "judgement.jpg", "yagami.webp"))
snow.go()
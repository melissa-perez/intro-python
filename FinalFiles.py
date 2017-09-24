#Student: Melissa Perez

#Programming Project  Final



#IMPORTS PYGAME 
import pygame, random, sys
from pygame.locals import *

#MAIN FUNCTION, MAKES THE GAME OBJECT
def main():
   a = Game()

#GAME CLASS
class Game():

    #THESE ARE CONSTANTS USED BY ALL CLASSES FOR FUNCTION USE
    
    WINDOWWIDTH = 1000
    WINDOWHEIGHT = 600
    TEXTCOLOR = (255, 255, 255)
    BACKGROUNDCOLOR = (0, 0, 0)
    FPS = 40

    #GAME CLASS CONSTRUCTOR
    def __init__(self):
        #===========================================================
        
        self._topScore = 0 #INITIALIZES SCORE AND TOPSCORE, 
        self._score = 0

        
        pygame.init()
        self._mainClock = pygame.time.Clock()

        pygame.display.set_caption('Final')

        self._background = pygame.image.load("background.png")
        self._backgroundRect = self._background.get_rect()
        self._size = (self.WINDOWWIDTH, self.WINDOWHEIGHT) = self._background.get_size()
        self._windowSurface = pygame.display.set_mode(self._size)
        self._gameOverSound = pygame.mixer.Sound('gameover.wav')
        pygame.mixer.music.load('Ridley.mid')


        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))

        self._font = pygame.font.SysFont(None, 48)

        #============================================================

        #CALLS ON PAUSED MENU
        self.startScreen()
        
        #RETURNS FROM PLAYER KEY INPUT
        while self.waitForPlayerToPressKey() is True:
            # BEGINS ACTUAL GAME
            self.gameLoop()

    #SETS HOW DRAWTEXT IS USED
            #@PARAM: TEXT, STRING TO BE USED, FONT: SYSTEM WIDE DEFAULT, X AND Y ARE THE POSITIONS
    def drawText(self, text, font, surface, x, y):
        textobj = font.render(text, 1, self.TEXTCOLOR)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    #CREATES TERMINATION PROCESS FOR PYGAME
    def terminate(self):
        pygame.quit()
        sys.exit()

    #START SCREEN DISPLAYS THE BEGINNING TEXT
    def startScreen(self):
        self.drawText('Final', self._font, self._windowSurface, (self.WINDOWWIDTH -600), (self.WINDOWHEIGHT / 3))
        self.drawText('Press any button to start! ESC : Exits the game.', self._font, self._windowSurface, (120 ) , (self.WINDOWHEIGHT / 3) + 60 )
        pygame.display.update()

    #RUNS LOOP UNTIL ACTION IS PLACED, CUTS PROGRAM IF ESC OR QUIT
        #RETURNS TRUE IF ANY OTHER KEY IS PRESSED

    def waitForPlayerToPressKey(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: # pressing escape quits
                        self.terminate()
                    return True

    #CHECKS TO SEE IF TWO OBJECTS COLLIDE WITH PYGAME FUNCTION
                #@ PARAM: PLAYERRECT IS PLAYER ICON AND BADDIES IS THE DICTIONARY HOLDING RECT STATS
                #RETURNS TRUE OR FALSE
    def playerHasHitBaddie(self, playerRect, baddies):
        for b in baddies:
            if playerRect.colliderect(b['rect']):
                return True
        return False

    #CHECKS TO SEE IF MOUSE CURSOR AND ENEMIES MATCH UP
    #IF THEY DO THEY ARE REMOVED
    #@PARAM: MOUSE POSITION TUPLE AND ENEMY DICTIONARY
    #RETURNS 
    

    def checkCrash(self, mouse,baddies):
        
        for b in baddies:
           if b['rect'].collidepoint(mouse):
               baddies.remove(b)
               return

    #THIS IS THE MAIN GAME LOOP

    def gameLoop(self):

        #VARIABLES FOR GAME
        baddieAddCounter = 0
        pygame.mixer.music.play(-1, 0.0)
        baddies = [] # holds the enemies
        moveLeft = moveRight = moveUp = moveDown = False

        self._score = 0
        Player.playerRect.topleft = (Game.WINDOWWIDTH / 2, Game.WINDOWHEIGHT - 50)

        while True: 
            self._score += 1 # INCREASES SCORE UNTIL PLAYER IS HIT

            #CHECKS TO SEE IF THE PROGRAM IS TERMINATED

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
            # THESE ARE ALL THE BUTTONS USED TO MOVE THE MAGE AS WELL AS MOUSE CURSOR 

                if event.type == KEYDOWN:               
                    if event.key == K_LEFT or event.key == ord('a'):
                        moveRight = False
                        moveLeft = True
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moveLeft = False
                        moveRight = True
                    if event.key == K_UP or event.key == ord('w'):
                        moveDown = False
                        moveUp = True
                    if event.key == K_DOWN or event.key == ord('s'):
                        moveUp = False
                        moveDown = True

                if event.type == MOUSEBUTTONUP:
                    self.checkCrash(pygame.mouse.get_pos(),baddies)

                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                            self.terminate()

                    if event.key == K_LEFT or event.key == ord('a'):
                        moveLeft = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moveRight = False
                    if event.key == K_UP or event.key == ord('w'):
                        moveUp = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        moveDown = False


            #ADDS COUNTER UNTIL NEXT ENEMY IS RELEASED
            baddieAddCounter += 1

            # IF THE COUNTER IS EQUAL TO THE MAX THEN CREATE NEW ENEMIES

            if baddieAddCounter == Enemy.ADDNEWBADDIERATE:
                baddieAddCounter = 0
                #RESET TO BEGIN AGAIN
                #DICTIONARY HOLDS THE ELEMENTS OF THE ENEMY
                baddieSize = random.randint(Enemy.BADDIEMINSIZE, Enemy.BADDIEMAXSIZE)
                newBaddie = {'rect': pygame.Rect(self.WINDOWWIDTH, random.randint(0, self.WINDOWHEIGHT - baddieSize), baddieSize, baddieSize),
                        'speed': random.randint(Enemy.BADDIEMINSPEED, Enemy.BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(Enemy.baddieImage, (baddieSize, baddieSize)),
                        }
            
                #APPEND TO THE LIST OF ENEMIES
                baddies.append(newBaddie)

            #RELEASES THE BIG ENEMY, SAME IDEA

            if self._score % 1000 == 0:
                baddieSize =  Enemy.BIGBADDIEMAXSIZE
                newBaddie = {'rect': pygame.Rect(self.WINDOWWIDTH, random.randint(0, self.WINDOWHEIGHT - baddieSize), baddieSize, baddieSize),
                        'speed': random.randint(Enemy.BADDIEMINSPEED, Enemy.BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(Enemy.bigbaddieImage, (baddieSize, baddieSize)),
                        }
                baddies.append(newBaddie)

            #SETS THE MOVEMENT RATE FOR THE WIZARD

            if moveLeft and Player.playerRect.left > 0:
                Player.playerImage = pygame.image.load('wizard1.png')

                Player.playerRect.move_ip(-1 * Player.PLAYERMOVERATE, 0)
            if moveRight and Player.playerRect.right < self.WINDOWWIDTH:
                Player.playerImage = pygame.image.load('wizard2.png')
                Player.playerRect.move_ip(Player.PLAYERMOVERATE, 0)
                
            if moveUp and Player.playerRect.top > 0:
                Player.playerRect.move_ip(0, -1 * Player.PLAYERMOVERATE)
            if moveDown and Player.playerRect.bottom < self.WINDOWHEIGHT:
                Player.playerRect.move_ip(0, Player.PLAYERMOVERATE)


            #ENEMIES MOVE TO THE LEFT
            for b in baddies:
                b['rect'].move_ip(-5, 0)
            #REMOVES THE ENEMIES OFF THE SCREEN

            for b in baddies[:]:
                if b['rect'].top > self.WINDOWHEIGHT:
                    baddies.remove(b)

            # DRAWS THE BACKGROUND WORLD
            self._windowSurface.blit(self._background,self._backgroundRect)

            # DRAWS THE SCORE ON THE SCREEN
            self.drawText('Score: %s' % (self._score), self._font, self._windowSurface, 10, 0)
            self.drawText('Top Score: %s' % (self._topScore), self._font, self._windowSurface, 10, 40)

            # DRAWS THE PLAYER TO THE SCREEN
            self._windowSurface.blit(Player.playerImage, Player.playerRect)

            # DRAWS THE MONSTER TO THE SCREEN 
            for b in baddies:
                self._windowSurface.blit(b['surface'], b['rect'])

            pygame.display.update()

            # Check if any of the baddies have hit the player.
            if self.playerHasHitBaddie(Player.playerRect, baddies):
                if self._score > self._topScore:
                    self._topScore = self._score # set new top score
                    
                break

            #SETS THE GAME SPEED

            self._mainClock.tick(Game.FPS)

        pygame.mixer.music.stop()
        self._gameOverSound.play()

        #DISPLAYS THE GAME OVER TEXT AND UPDATES THE SCREEN

        self.drawText('GAME OVER', self._font, self._windowSurface, (self.WINDOWWIDTH / 3), (self.WINDOWHEIGHT / 3))
        self.drawText('Press a key to play again.', self._font, self._windowSurface, (self.WINDOWWIDTH / 3) - 80, (self.WINDOWHEIGHT / 3) + 50)
        pygame.display.update()

                

class Player:

    #PLAYER CLASS CONSTANTS
    
    PLAYERMOVERATE = 5
    playerImage = pygame.image.load('wizard.png')
    playerRect = playerImage.get_rect()
    playerRect.topleft = (Game.WINDOWWIDTH / 2, Game.WINDOWHEIGHT - 50)
    def __init__(self):
        pass



class Enemy:
    # ENEMY CLASS CONSTANTS

        BADDIEMINSIZE = 30
        BADDIEMAXSIZE = 40
        BADDIEMINSPEED = 1
        BADDIEMAXSPEED = 8
        BIGBADDIEMAXSIZE = 292
        ADDNEWBADDIERATE = 6
        baddieImage = pygame.image.load('ball.png')
        bigbaddieImage =pygame.image.load('legion.png')


        def __init__(self):
            pass
      

        

#START OF THE MAIN FUNCTION

main()
        

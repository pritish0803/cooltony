import pygame,random,sys
from pygame.locals import *
pygame.init()

window_height=600
window_width=1200

blue=(0,0,255)
black=(0,0,0)
white=(255,255,255)

fps=40
level=0
addnewflamerate=20

class attacker:
	global firerect,imagerect,Canvas
	right=False
	left=True
	velocity=15
	def __init__(self):
		self.image=load_image("dragon.png")
		self.imagerect=self.image.get_rect()
		self.imagerect.right=window_width/2
		self.imagerect.top=20
	def update(self):
		if (self.imagerect.right > cactusrect.left):
			self.right=False
			self.left=True
		if (self.imagerect.left < firerect.right):
			self.right=True
			self.left=False
		if (self.left):
			self.imagerect.left -=self.velocity
		if (self.right):
			self.imagerect.right +=self.velocity
		Canvas.blit(self.image,self.imagerect)
	def return_height(self):

        	h = self.imagerect.left
        	return h
class flames:
    flamespeed = 30

    def __init__(self):
        self.image = load_image('fireball.png')
        self.imagerect = self.image.get_rect()
        self.height = Dragon.return_height() + 20
        self.surface = pygame.transform.scale(self.image, (20,20))
        self.imagerect = pygame.Rect(self.height, 30, 0, 0)

    def update(self):
            self.imagerect.bottom += self.flamespeed
	    
    def collision(self):
        if self.imagerect.bottom == window_height:
            return True
        else:
            return False
class defender:
    global moveleft, moveright, gravity, cactusrect, firerect
    speed = 20
    downspeed = 20

    def __init__(self):
        self.image = load_image('maryo.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.bottomleft = (window_width/2,window_height)
        self.score = 0

    def update(self):
        
        if (moveright and (self.imagerect.right < cactusrect.left)):
            self.imagerect.right += self.speed
            self.score += 1
            
        if (moveleft and (self.imagerect.left > firerect.right)):
            self.imagerect.left -= self.downspeed
            self.score += 1
            
        
def terminate():        #to end the program
    pygame.quit()
    sys.exit()

def waitforkey():
    while True :                                        #to wait for user to start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:     #to terminate if the user presses the escape key
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return
def flamehitsdefender(playerrect,flames):
	for f in flame_list:
		if playerrect.colliderect(f.imagerect):
			return True
		return False
def drawtext(text,font,surface,x,y):
	textobj=font.render(text,1,white)
	textrect=textobj.get_rect()
	textrect.center=(x,y)
	surface.blit(textobj,textrect)
def check_level(score):
    global window_width, level, cactusrect, firerect
    if score in range(0,250):
        firerect.right = 50
        cactusrect.left =window_width - 50
        level = 1
    elif score in range(250, 500):
        firerect.right = 100
        cactusrect.left = window_width-100
        level = 2
    elif score in range(500,750):
        level = 3
        firerect.right = 150
        cactusrect.left = window_width-150
    elif score in range(750,1000):
        level = 4
        firerect.right = 200
        cactusrect.left = window_width-200           
			
def load_image(imagename):
    return pygame.image.load(imagename)
mainClock = pygame.time.Clock()
Canvas = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('plane game')

#setting up font and sounds and images

font = pygame.font.SysFont(None, 48)
scorefont = pygame.font.SysFont(None, 30)

fireimage = load_image('fire_bricks1.png')
firerect = fireimage.get_rect()

cactusimage = load_image('cactus_bricks1.png')
cactusrect = cactusimage.get_rect()

startimage = load_image('gamestart.png')
startimagerect = startimage.get_rect()
startimagerect.centerx = window_width/2
startimagerect.centery = window_height/2

endimage = load_image('gameover.jpg')
endimagerect = startimage.get_rect()
endimagerect.centerx = window_width/2
endimagerect.centery = window_height/2

pygame.mixer.music.load('mario_theme.wav')
gameover = pygame.mixer.Sound('mario_dies.wav')

#getting to the start screen

drawtext('plane game', font, Canvas,(window_width/2), (window_height/2))
Canvas.blit(startimage, startimagerect)

pygame.display.update()
waitforkey()

topscore = 0
Dragon = attacker()

while True:

    flame_list = []
    player = defender()
    moveleft = moveright = gravity = False
    flameaddcounter = 0

    gameover.stop()
    pygame.mixer.music.play(-1,0.0)

    

    while True:     #the main game loop
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                
                if event.key == K_RIGHT:
                    moveleft = False
                    moveright = True
                    gravity = False

                if event.key == K_LEFT:
                    moveleft = True
                    moveright = False
                    gravity = False

            if event.type == KEYUP:

                if event.key == K_LEFT:
                    moveleft = False
                    
                if event.key == K_RIGHT:
                    moveright = False
                   
                    
                if event.key == K_ESCAPE:
                    terminate()
	flameaddcounter += 1
        check_level(player.score)
        
        if flameaddcounter == addnewflamerate:

            flameaddcounter = 0
            newflame = flames()
            flame_list.append(newflame)

        
        
        for f in flame_list:
            flames.update(f)

        for f in flame_list:
            if f.imagerect.bottom >= window_height:
                flame_list.remove(f)

        player.update()
        Dragon.update()
        

        Canvas.fill(black)
        Canvas.blit(fireimage, firerect)
        Canvas.blit(cactusimage, cactusrect)
        Canvas.blit(player.image, player.imagerect)
        Canvas.blit(Dragon.image, Dragon.imagerect)
        

        drawtext('Score : %s | Top score : %s | Level : %s' %(player.score, topscore, level), scorefont, Canvas, 400, 350)
        
        for f in flame_list:
            Canvas.blit(f.surface, f.imagerect)

               

        if flamehitsdefender(player.imagerect, flame_list):
            if player.score > topscore:
                topscore = player.score
            break
        
        if ((player.imagerect.right >= cactusrect.left) or (player.imagerect.left <= firerect.right)):
            if player.score > topscore:
                topscore = player.score
            break

        pygame.display.update()

        mainClock.tick(fps)
    
    pygame.mixer.music.stop()
    gameover.play()
    Canvas.blit(endimage, endimagerect)
    pygame.display.update()
    waitforkey()
        
    

		

import pygame
import sys
import random

GameCaption = "Doodle Jump"
ScreenSize = (1300, 700)
GridSize = (14, 14)
WordSize = (25, 25)
ColorFloral = (255,250,240) # for screen
ColorKhaki = (240,230,140) # for grid
ColorGreen = (0,255,0) # for grid
ColorBlack = (0, 0, 0) # for score
MaxVel = 20
class DoodleJump:
    def __init__(self):
        ### control the game
        self.platforms = [] # positions of platforms
        self.springs = [] # positions of springs
        self.score = 0
        self.player_x = 400 # player x: direction
        self.direction = 0
        self.movement = 0 # screen x: loop

        self.player_y = 400 # player y: doodle jump!
        self.velocity = 0
        self.gravity = -0.8
        self.screen_y = 0 # screen y: roll

        ### draw the screen
        self.screen = None
        self.clock = None
        self.font = None
        self.img_platform = [None, None, None, None]
        self.img_spring = [None, None]
        self.img_player = [None, None, None, None]
        self.size_platform = None
        self.size_spring = None
        self.size_player = None
    
    def init_highest(self):
        self.highestscore = 0
        self.startmenu()

    def updatePlayer(self):
        ### player x: direction # 0 for right, 1 for left
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.player_x+=20
            self.direction=0
        elif key[pygame.K_LEFT]:
            self.player_x-=20
            self.direction=1
        else:
            pass
            """
            TASK 4.1
            """
        ### screen x: loop
        if self.player_x<=0-(self.size_player[0]): self.player_x=ScreenSize[0]
        elif self.player_x>=ScreenSize[0]: self.player_x=0-(self.size_player[0])
        ### player y: doodle jump!
        self.velocity+=self.gravity
        self.player_y-=self.velocity
        if self.movement>0: self.movement-=1
        ### screen y: roll
        if self.player_y-self.screen_y<100:
            self.screen_y=(self.player_y-100)
        ### draw the player
        if self.movement: a=2
        else :a=0
        self.screen.blit(self.img_player[self.direction+a],(self.player_x,self.player_y-self.screen_y))

    def updatePlatforms(self):
        for p in self.platforms:
            ### collide with the platform
            rect_platform = pygame.Rect(p[0], p[1], self.size_platform[0], self.size_platform[1])
            rect_player = pygame.Rect(self.player_x, self.player_y, self.size_player[0], self.size_player[1])
            if rect_platform.colliderect(rect_player)  and self.velocity<0 and (self.player_y + self.size_player[1] - 15) <= (p[1] - self.screen_y) and (self.player_y+self.size_player[1])<=(p[1]+self.size_platform[1]):
                #TASK 3.1  if red: break, else: doodle jump!
                if p[2]==2:
                    self.movement=3
                    self.velocity=MaxVel
                    p[2]=3
                elif p[2]==3:
                    pass
                else:
                    self.movement=3
                    self.velocity=MaxVel
            ### if blue: move
            if p[2]==1:
                if p[0]<=1 and p[3]<0: p[3]=2
                elif p[0]>=ScreenSize[0]-self.size_platform[0] and p[3]>0: p[3]=-2
                elif p[3]==0 : p[3]=2
                p[0]+=p[3]
    def drawPlatforms(self):
        ### draw platforms
        for p in self.platforms:
            next_y = self.platforms[1][1] - self.screen_y
            if next_y > ScreenSize[1]:
                ### add a new platform
                x = random.randint(0,ScreenSize[0]-self.size_platform[0])
                platform_type = 0
                a=random.randint(0,100)
                if a<80:platform_type=0
                elif a<90:platform_type=1
                else: platform_type=2
                self.platforms.append([x,self.screen_y-50, platform_type, 0])
                ### add a spring
                if platform_type==0:
                    r=random.randint(0,10)
                    if r<2:
                        self.springs.append([x,self.screen_y-50-self.size_spring[1],0])
                self.platforms.pop(0) # delete the old platform
                self.score += 80 # renew the score
            ### draw the platform
            self.screen.blit(self.img_platform[p[2]],(p[0],p[1]-self.screen_y))
        rect_player = pygame.Rect(self.player_x, self.player_y, self.size_player[0], self.size_player[1])
        for s in self.springs:
            ### collide with the spring
            rect_spring = pygame.Rect(s[0], s[1], self.size_spring[0], self.size_spring[1])
            if rect_spring.colliderect(rect_player) and self.velocity < 0 and (self.player_y + self.size_player[1] - 15) <= (s[1] - self.screen_y) and (self.player_y+self.size_player[1])<=(s[1]+self.size_spring[1]): 
                self.velocity=MaxVel*1.5
                s[2]=1
                self.movement=3
            ### draw the spring
            if s[1]-self.screen_y>ScreenSize[1]: self.springs.pop(0)
            self.screen.blit(self.img_spring[s[2]],(s[0],s[1]-self.screen_y))
                

    def drawBackground(self):
        ### fill color
        self.screen.fill(ColorFloral)
        ### draw grids
        for i in range(ScreenSize[0]//14+1): pygame.draw.line(self.screen,ColorKhaki,(i*14,0),(i*14,ScreenSize[1]),1)
        for i in range(ScreenSize[1]//14+1): pygame.draw.line(self.screen,ColorKhaki,(0,i*14),(ScreenSize[0],i*14),1)

    def generatePlatforms(self):
        y = ScreenSize[1]
        while y >= -50:
            if y == 500: # the first platform on which the player stands
                x = 400
                platform_type = 0
            else: # generate random x and type
                x = random.randint(0,ScreenSize[0]-self.size_platform[0])
                platform_type = 0
                a=random.randint(0,100)
                if a<80:platform_type=0
                elif a<90:platform_type=1
                else: platform_type=2
            self.platforms.append([x, y, platform_type, 0])
            y -= 50

    def initialize(self):
        pygame.init()
        pygame.display.set_caption(GameCaption)
        self.screen = pygame.display.set_mode(ScreenSize)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Comic Sans MS", 25)  
        self.font1 = pygame.font.SysFont("Comic Sans MS", 35)
        ### load all images
        self.img_platform[0] = pygame.image.load("assets/platform_green.png").convert_alpha()
        self.img_platform[1] = pygame.image.load("assets/platform_blue.png").convert_alpha()
        self.img_platform[2] = pygame.image.load("assets/platform_red.png").convert_alpha()
        self.img_platform[3] = pygame.image.load("assets/platform_red_break.png").convert_alpha()
        self.img_spring[0] = pygame.image.load("assets/spring.png").convert_alpha()
        self.img_spring[1] = pygame.image.load("assets/spring_bounce.png").convert_alpha()
        self.img_player[0] = pygame.image.load("assets/player_right.png").convert_alpha()
        self.img_player[1] = pygame.image.load("assets/player_left.png").convert_alpha()
        self.img_player[2] = pygame.image.load("assets/player_right_jump.png").convert_alpha()
        self.img_player[3] = pygame.image.load("assets/player_left_jump.png").convert_alpha()
        ### for convenience
        self.size_platform = self.img_platform[0].get_size()
        self.size_spring = self.img_spring[0].get_size()
        self.size_player = self.img_player[0].get_size()
    
    def startmenu(self): 
        self.initialize()
        #self.screen.fill(ColorFloral)
        #self.generatePlatforms()
        #words = self.font.render('You are in the Menu.\n Space to play. \n Esc exits.'
        #'\n Press h to see highest score.',True, ColorBlack)
        while True:
            self.screen.fill(ColorFloral)
            #self.generatePlatforms()
            words = self.font.render('You are in the Menu.\n Space to play. \n Esc exits.'
            '\n Press h to see highest score.',True, ColorBlack)
            self.drawBackground()
            #self.generatePlatforms()
            words = self.font1.render('JUMP! You are in the Menu.',True, ColorBlack)
            self.screen.blit(words,(150,100))
            words1 = self.font.render('Press Anykey to play.',True,ColorBlack)
            self.screen.blit(words1,(150,170))
            words2 = self.font.render('Press ESC to leave.',True, ColorBlack)
            self.screen.blit(words2,(150,230))
            sss = 'Highest score: ' + str(self.highestscore)
            words4 = self.font.render(sss,True, ColorGreen)
            self.screen.blit(words4,(150,350))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            sys.exit()
                        else:
                            self.run()
    def run(self):
        ### init the game
        self.__init__()
        self.score=0
        self.initialize()
        self.generatePlatforms()
        while True:
            ### close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            ### restart the game
            if self.player_y-self.screen_y>ScreenSize[1]:
                #import ipdb; ipdb.set_trace()
                if self.score > self.highestscore:
                    self.highestscore = self.score
                break
                '''
                self.score=0
                self.__init__()
                self.initialize()
                self.generatePlatforms()
                '''
            ### update the game
            self.drawBackground()
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            self.screen.blit(self.font.render(str(self.score), -1, ColorBlack), WordSize)
            pygame.display.flip()
            self.clock.tick(60)
        self.startmenu()

DoodleJump().init_highest()

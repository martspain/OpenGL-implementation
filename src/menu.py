import pygame

class Menu(object):
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.width/2, self.game.height/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.offset = -100
    
    def drawCursor(self):
        cursorImg = pygame.image.load('res/textures/deagle.png')
        cursorImg = pygame.transform.scale(cursorImg, (50, 30))
        self.game.display.blit(cursorImg, (self.cursor_rect.x, self.cursor_rect.y - 10))
        #self.game.drawText('>', 15, self.cursor_rect.x, self.cursor_rect.y)
    
    def blitScreen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.resetKeys()
    
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 60
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 90

        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def displayMenu(self):
        self.run_display = True
        while self.run_display:
            self.game.checkEvents()

            self.checkInput()

            bgImg = pygame.image.load('res/backgrounds/mainMenu.jpg')
            bgX = 0
            bgY = 0

            bgImg = pygame.transform.scale(bgImg, (self.game.width, self.game.height))
            self.game.display.blit(bgImg, (bgX, bgY))

            #self.game.display.fill(self.game.BLACK)
            self.game.drawText('OpenGL Implementation', 40, self.mid_w, self.mid_h - 20)
            self.game.drawText('Start', 25, self.startx, self.starty)
            self.game.drawText('Instrucions', 25, self.optionsx, self.optionsy)
            self.game.drawText('Exit Game', 25, self.creditsx, self.creditsy)
            self.drawCursor()

            self.blitScreen()
    
    def moveCursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Exit'
            elif self.state == 'Instructions':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Start'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Instructions'
    
    def checkInput(self):
        self.moveCursor()

        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                pygame.quit()
            elif self.state == 'Instructions':
                self.game.curr_menu = self.game.instructions
            elif self.state == 'Exit':
                self.game.running = False
                self.game.playing = False
            
            self.run_display = False

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    
    def displayMenu(self):
        self.run_display = True
        while self.run_display:
            self.game.checkEvents()
            if self.game.START_KEY or self.game.BACK_KEY:
                if self.game.isPaused:
                    self.game.curr_menu = self.game.pause
                else:
                    self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.drawText('Credits', 30, self.mid_w, self.mid_h - 20)
            self.game.drawText('Made by Martspain', 25, self.mid_w, self.mid_h + 10)
            self.blitScreen()

class InstructionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    
    def displayMenu(self):
        self.run_display = True
        while self.run_display:
            self.game.checkEvents()
            if self.game.START_KEY or self.game.BACK_KEY:
                if self.game.isPaused:
                    self.game.curr_menu = self.game.pause
                else:
                    self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.drawText('Instructions', 30, self.mid_w, self.mid_h - 20)
            self.game.drawText('Made by Martspain', 25, self.mid_w, self.mid_h + 10)
            self.blitScreen()

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    
    def displayMenu(self):
        self.run_display = True
        while self.run_display:
            self.game.checkEvents()
            if self.game.START_KEY or self.game.BACK_KEY:
                if self.game.isPaused:
                    self.game.curr_menu = self.game.pause
                else:
                    self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.drawText('Options', 30, self.mid_w, self.mid_h - 20)
            self.game.drawText('Under construction...', 25, self.mid_w, self.mid_h + 10)
            self.blitScreen()

class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Resume"
        self.resumex, self.resumey = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 60
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.offset = -150

        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)

    def displayMenu(self):
        self.run_display = True
        while self.run_display:
            self.game.checkEvents()

            self.checkInput()

            bgImg = pygame.image.load('res/backgrounds/pauseMenu.jpg')
            bgX = 0
            bgY = 0

            bgImg = pygame.transform.scale(bgImg, (self.game.width, self.game.height))
            self.game.display.blit(bgImg, (bgX, bgY))

            #self.game.display.fill(self.game.BLACK)
            self.game.drawText('Pause Menu', 40, self.mid_w, self.mid_h - 20)
            self.game.drawText('Resume', 25, self.resumex, self.resumey)
            self.game.drawText('Instructions', 25, self.optionsx, self.optionsy)
            self.game.drawText('Exit to Main Menu', 25, self.exitx, self.exity)
            self.drawCursor()

            self.blitScreen()
    
    def moveCursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Resume':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Instructions'
            elif self.state == 'Instructions':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
                self.state = 'Resume'

        elif self.game.UP_KEY:
            if self.state == 'Resume':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Instructions':
                self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
                self.state = 'Resume'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Instructions'
    
    def checkInput(self):
        self.moveCursor()

        if self.game.START_KEY:
            if self.state == 'Resume':
                self.run_display = False
                self.game.playing = True
                self.game.isPaused = False
            elif self.state == 'Instructions':
                self.game.curr_menu = self.game.instructions
            elif self.state == 'Exit':
                self.game.playing = False
                self.game.isPaused = False
                self.game.curr_menu = self.game.main_menu
            
            self.run_display = False
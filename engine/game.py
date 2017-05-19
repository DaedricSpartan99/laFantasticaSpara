from pygame.locals import *
from exceptions import *

# USAGE
#
# def gameloop(delta_time):
#     .... define your own tick action
#
# def onQuit(cause):
#     .... define your own quit game handler
#
# mygame = Game(gameloop, onQuit)
# mygame.start()
#

fullResolution = (0, 0) # Pygame default value for fullscreen resolution

class Screen:
    def __init__(self, resolution = (1024, 768), fullscreen = False):
        pygame.display.init()
        self.resolution = resolution
        self.fullscreen = fullscreen
        self.loaded = False
        
    def load(self):
        
        flags = DOUBLEBUF
        
        if (self.fullscreen):
            flags |= FULLSCREEN
            self.resolution = fullResolution
            
        self.pygame_screen = pygame.display.set_mode(self.resolution, flags)
        self.loaded = True

    def quit(self):
        self.pygame.quit()
        self.loaded = False

    def resize(self, resolution):
        self.resolution = resolution
        self.updateMode()
            
    def setFullscreen(self, value):
        self.fullscreen = value
        self.updateMode()

    def updateMode(self):
        if (self.loaded):
            self.load()     # RECALL
            self.update()

    def update(self):
        pygame.display.flip()

class Game:
    def __init__(self, execfunc, quithandler = None, screen = Screen(), fps = 30):
        self.screen = screen    # screen object
        self.execfunc = execfunc    # pointer to executable function
        self.quithandler = quithandler    # handler of the quit action
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = False

    def start(self):

        # Screen setup
        
        self.screen.load()
        
        # Starting game
        
        self.running = True
        
        while(self.running):
            
            dt = self.clock.tick(self.fps)   # wait
            quitcause = None
            
            try:
                self.execfunc(dt)     # execute
            except IntCall:
                self.running = False
                break
            except Exception as error:
                print "An error occured"
                self.running = False
                quitcause = GameError(error)
                break
            
            self.screen.update()       # flip screen

        if (self.quithandler is not None):
            self.quithandler(quitcause)

        self.screen.quit()    # close window
        pygame.quit()   # close game execution

    def stop(self):
        raise IntCall

    def setQuitHandler(self, quithandler):
        self.quithandler = quithandler

def interrupt():    #statically interrupts the game
    raise IntCall

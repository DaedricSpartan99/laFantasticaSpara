from pygame.locals import *
from gamemath import *
from exceptions import *

gm_display = pygame.display

# USAGE
#
# def gameloop(delta_time):
#     .... define your own tick action
#
# def onQuit(cause):
#     .... define your own quit game handler
#
# myscreen = Screen(gameloop, onQuit)
# myscreen.start()
#

class Screen:
    def __init__(self, execfunc, quithandler = None, res = (1024, 768), fps = 30):
        self.res = Vector(res)
        self.execfunc = execfunc    # pointer to executable function
        self.quithandler = quithandler    # handler of the quit action
        self.fullscrn = False
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = False

    def start():

        # Window setup
        
        if (self.fullscrn):
            self.screen = gm_display.set_mode(self.res.tuple(), FULLSCREEN | DOUBLEBUF)
        else:
            self.screen = gm_display.set_mode(self.res.tuple(), DOUBLEBUF)

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
            
            self.update()       # update screen

        if (not (self.quithandler is None)):
            self.quithandler(quitcause)

        pygame.display.quit()    # close window
        pygame.quit()   # close game execution

    def stop():
        raise IntCall

    def setFullscreen(self, fullsrcn):

        if (self.running):
            if (fullsrcn):
                self.screen = gm_display.set_mode(self.res.tuple(), FULLSCREEN | DOUBLEBUF)
            else
                self.screen = gm_display.set_mode(self.res.tuple(), DOUBLEBUF)
                
            self.update()
            
        self.fullscrn = fullscrn

    def setResolution(self, res):

        if (self.running):
            if (self.fullscrn):
                self.screen = gm_display.set_mode(res, FULLSCREEN | DOUBLEBUF)
            else:
                self.screen = gm_display.set_mode(res, DOUBLEBUF)

            self.update()
            
        self.res = Vector(res)

    def update(self):
        gm_display.flip()

    def setQuitHandler(self, quithandler):
        self.quithandler = quithandler

def interrupt():    #statically interrupts the game
    raise IntCall

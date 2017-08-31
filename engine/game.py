import calls
import vector
import pygame
import events

"""
USAGE

def gameloop(delta_time):
   .... define your own tick action

def onQuit(cause):
    .... define your own quit game handler

screen = Screen("LaFantasticaSpara")

mygame = Game(gameloop, screen, onQuit)
mygame.start()

"""

fullResolution = (0, 0) # Pygame default value for fullscreen resolution, const

screen_res = (1024, 768)    # Accessible game.screen_res
# ratio
render_ratio = (50.0, 50.0)
screen_coords = vector.Coords((512, 384), render_ratio)

class Screen:
    def __init__(self, caption = "MyGame", resolution = screen_res, fullscreen = False):
        pygame.display.init()
        self.resolution = resolution
        self.fullscreen = fullscreen
        self.caption = caption
        self.loaded = False
	self.pygame_screen = None
        
    def load(self):

        global screen_res
        
        flags = pygame.DOUBLEBUF
        
        if (self.fullscreen):
            flags |= pygame.FULLSCREEN
            self.resolution = fullResolution
            
        self.pygame_screen = pygame.display.set_mode(self.resolution, flags)
        
        if (self.fullscreen):
            info = pygame.display.Info()
            screen_res = (info.current_w, info.current_h)
        else:
            screen_res = self.resolution
            
        pygame.display.set_caption(self.caption)
        self.loaded = True

    def getPygameScreen(self):
        return self.pygame_screen

    def quit(self):
        pygame.quit()
        self.loaded = False

    def setCaption(self, caption):
        self.caption = caption
        self.pygame_screen.set_caption(self.caption)

    def resize(self, resolution):
        self.resolution = resolution
        self.updateMode()
            
    def setFullscreen(self, value):
        self.fullscreen = value
        self.updateMode()

    def getSize(self):
        return self.pygame_screen.get_size()

    def updateMode(self):
        if (self.loaded):
            self.load()     # RECALL
            self.update()

    def update(self):
        pygame.display.flip()

delta_time = 0.0    # accessible game.delta_time

default_bg = pygame.Surface(screen_res)
default_bg.fill((0, 0, 0))

class World:
    def __init__(self, screen, group = pygame.sprite.Group(), background = default_bg):
        self.group = group
        self.screen = screen.getPygameScreen()
        self.background = background
        self.events_enabled = True
        self.comp_mouse_clicks = []
        self.comp_mouse_overs = []

    def setScreen(self, screen):
        self.screen = screen.getPygameScreen()

    # callback function foo(Component, Actor, Buttons)
    def addClickCallback(self, func):
        self.comp_mouse_clicks.append(func)

    # callback function foo(Component, Actor)
    def addOverCallback(self, func):
        self.comp_mouse_overs.append(func)

    def _mouse_buttons(self):

        bs = pygame.mouse.get_pressed()

        if (bs[0] or bs[1] or bs[2]):
            return bs
        else:
            return None

    def _click_inside_comp(self, comp, pos, actor, buttons, cb_func):
        if comp.isInside(pos):
            cb_func(comp, actor, buttons)
            for child in comp.getChildren():
                _click_inside_comp(child, pos, actor, buttons, cb_func)

    def _inside_comp(self, comp, pos, actor, cb_func):
        if comp.isInside(pos):
            cb_func(comp, actor)
            for child in comp.getChildren():
                _inside_comp(child, pos, actor, cb_func)

    def _process_events(self):

        # manage mouse over
        pos = pygame.mouse.get_pos()

        for over_cb in self.comp_mouse_overs:
            for actor in self.group:
                comp = actor.getComponent()
                self._inside_comp(comp, pos, actor, click_cb)

        # manage mouse clicks
        buttons = self._mouse_buttons()

        if buttons is not None:
            for click_cb in self.comp_mouse_clicks:
                for actor in self.group:
                    comp = actor.getComponent()
                    self._click_inside_comp(comp, pos, actor, buttons, click_cb)
        
    def update(self):

        if self.events_enabled:
            self._process_events()
                
        self.group.clear(self.screen, self.background)
        self.group.update()
        self.group.draw(self.screen)

class Game:
    def __init__(self, execfunc, initfunc = None, screen = Screen(), quithandler = None, fps = 30):
        self.screen = screen    # screen object
        self.execfunc = execfunc    # pointer to the gameloop function
        self.initfunc = initfunc    # pointer to the init function before the gameloop
        self.quithandler = quithandler    # handler of the quit action
        self.fps = fps
        self.world = World(self.screen)
        self.clock = pygame.time.Clock()
        self.running = False

    def start(self):

        # Screen setup
        
        self.screen.load()

        # Call init function

        if self.initfunc is not None:
            self.initfunc()
        
        # Starting game
        
        self.running = True
        global delta_time
        
        while(self.running):
            
            delta_time = self.clock.tick(self.fps) / 1000.0  # wait
            quitcause = None
            
            try:
		events.get()	# process events
                self.execfunc(delta_time)     # execute
                self.world.update()
            except calls.IntCall:
                self.running = False
                break
            except Exception as error:
                print "An error occured"
                self.running = False
                quitcause = calls.GameError(error)
                break
            
            self.screen.update()       # flip screen

        if (self.quithandler is not None):
            self.quithandler(quitcause)

        self.screen.quit()    # close window
        pygame.quit()   # close game execution

    def stop(self):
        raise calls.IntCall

    def setQuitHandler(self, quithandler):
        self.quithandler = quithandler

    def getWorld(self):
        return self.world

def interrupt():    #statically interrupts the game
    raise calls.IntCall

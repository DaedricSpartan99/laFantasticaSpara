import vector
import game
import pygame

class Component:
    def __init__(self, surface, location = vector.Vector((0, 0)), angle = 0.0, parent = None):
        # parent object
        self.parent = parent
        # relative render state
        self.location = location
        self.angle = angle
        self.moved = False
        self.rotated = False
        # surface objet
        self.original_surface = surface
        self.reset()
        # internal coordinates
        self.coords = vector.Coords((surface.get_width() // 2, surface.get_height() // 2), game.render_ratio)
        # nested components
        self.attached = []
        self.flushed = False

    def setSurface(self, surface):
        self.original_surface = surface
        self.reset()

    def move(self, dx):
        self.location += dx
        self.flush_moved = True

    def rotate(self, angle):
        self.angle += angle
        self.flush_rotated = True

    def flush_moved(self):
        self.moved = True

    def flush_rotated(self):
        self.rotated = True

    def flush(self):
        self.flushed = True

    def getChildren(self):
        return self.attached

    def isOverlapping(self, component):
        return self.rect.colliderect(component.rect)

    def isInside(self, point):
        return self.rect.collidepoint(point)

    def reset(self):
        self.surface = self.original_surface.copy()
	coords = None
	if self.parent is None:
	    coords = game.screen_coords
	else:
	    coords = self.parent.coords
        self.rect = self.surface.get_rect(center = vector.get_px(self.location, coords))
        
    def attach(self, component):
        self.attached.append(component)
        self.surface.blit(component.surface, vector.get_px(component.location, self.coords))
        component.parent = self

    def re_blit(self, dest):
        self.surface.blit(dest, vector.get_px(dest.location, self.coords))

    def _flush(self):
        # reinitialize the surface
        self.reset()
        # update all attached components
        for component in self.attached:
            component.update(delta_time, self.coords, True)

    def _rotate(self):
        self.surface = pygame.transform.rotate(self.original_surface, vector.degrees(self.angle))
        self.rect = self.surface.get_rect()

    def _move(self, coords):
        r = vector.get_px(self.location, coords)
        self.rect.move(r[0], r[1])

    def update(self, delta_time, coords, reblit = False):

        # update internal surfaces

        #if self.flushed or self.rotated:
        self._flush()
        reblit = True
        self.flushed = False

        # update rotation

        if self.rotated:
            self._rotate()
            self.rotated = False

        # update location
            
        if self.moved:
            self._move(coords)
            self.moved = False

        # re-blit if necessary,
        # this method has a different callback
        # depending on the parent type

        if reblit:
            self.parent.re_blit(self.surface)

class PhysComponent(Component):
    def __init__(self, surface, location = vector.Vector((0, 0)), angle = 0.0, mass = 1.0, inertia = 1.0, parent = None):
        Component.__init__(self, surface, location, angle, parent)
        # physical state
        self.mass = mass
        self.inertia = inertia
        # first derivate
        self.speed = vector.Vector()
        self.ang_speed = 0.0
        # second derivate
        self.force = vector.Vector()
        self.momentum = 0.0

    def addForce(self, force):
        self.force += force

    def addMomentum(self, force, point):
        self.momentum += force ^ (point - self.location)

    def update(self, delta_time, coords, reblit = False):

        if (self.force != vector.null):
            self.speed += self.force * (delta_time / self.mass)
            self.force.null()   #reset
        if (self.momentum != 0.0):
            self.ang_speed += self.momentum * (delta_time / self.inertia)
            self.momentum.null()    #reset

        if (self.speed != vector.null):
            self.location += self.speed * delta_time
            self.flush_moved()  # update location
        if (self.ang_speed != 0.0):
            self.angle += self.rotation * delta_time
            self.flush_rotated() # update rotation

        Component.update(self, delta_time, coords, reblit)  # super update all
        

class Actor(pygame.sprite.Sprite):
    def __init__(self, component):
        pygame.sprite.Sprite.__init__(self)
        # main component
        self.component = component
        self.component.parent = self
        self.image = self.component.surface
	self.rect = self.component.rect
	self.coords = game.screen_coords

    def move(self, dx):
        self.component.move(dx)

    def rotate(self, angle):
        self.component.rotate(angle)

    def getComponent(self):
        return self.component

    def getLocation(self):
        return self.component.location

    def getAngle(self):
        return self.component.angle

    def flush(self):
        self.component.flush()

    def re_blit(self, dest):
        self.image = dest
	self.rect = self.component.rect

    def update(self):
        self.component.update(game.delta_time, game.screen_coords)

class PhysActor(Actor):
    def __init__(self, component):
        Actor.__init__(self, component)

    def addForce(self, force):
        self.component.addForce(force)

    def addMomentum(self, force, point):
        self.component.addMomentum(force, point)

    def getMass(self):
        return self.component.mass

    def getInertia(self):
        return self.component.inertia

    def getSpeed(self):
        return self.component.speed

    def getAngularSpeed(self):
        return self.component.ang_speed

def load(filename, location, alpha = False):

    if (alpha):
        img = pygame.image.load(filename).convert_alpha()
    else:
        img = pygame.image.load(filename).convert()
        
    comp = Component(img, location)
    return Actor(comp)

def loadPhys(filename, location, mass = 1.0, alpha = False):
    
    if (alpha):
        img = pygame.image.load(filename).convert_alpha()
    else:
        img = pygame.image.load(filename).convert()
        
    comp = PhysComponent(img, location, 0.0, mass)
    return PhysActor(comp)
    

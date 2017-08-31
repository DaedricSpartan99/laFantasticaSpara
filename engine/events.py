import pygame

LEFT_CLICK = 1
RIGHT_CLICK = 3

quit_handler = None
keydown_handler = None
mouseclick_handler = None
mousemotion_handler = None

def setQuitHandler(handler):
    global quit_handler
    quit_handler = handler

def setKeyDownHandler(handler):
    global keydown_handler
    keydown_handler = handler

def setMouseClickHandler(handler):
    global mouseclick_handler
    mouseclick_handler = handler

def setMouseMotionHandler(handler):
    global mousemotion_handler
    mousemotion_handler = handler

def get():
    
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (keydown_handler is not None):
                keydown_handler(event.key)
        elif (event.type == pygame.QUIT):
            if (quit_handler is not None):
                quit_handler()
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            if (mouseclick_handler is not None):
                mouseclick_handler(event.button, event.pos)
        elif (event.type == pygame.MOUSEMOTION):
            if (mousemotion_handler is not None):
                mousemotion_handler(event.pos)
            

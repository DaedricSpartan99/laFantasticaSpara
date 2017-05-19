from gamemath import *

def acceleration(speed, accel, deltatime):   # returns the new speed in m/s
    speed.x += accel.x * deltatime
    speed.y += accel.y * deltatime
    return speed

g = Vector(0, -9.81)

def gravity(speed, deltatime):
    return acceleration(speed, g, deltatime)

def force(speed, force, mass, deltatime):    # returns the new speed in m/s
    accel = Vector(force.x / mass, force.y / mass)
    return acceleration(speed, accel, deltatime)

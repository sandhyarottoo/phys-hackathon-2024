
import numpy as np
import pygame

def CoulombForce(r,A = 2):
    #r**3 instead of r**2 because we have another r for the direction when we call this
    return A/r**3

def StrongForce(r,k = 1):
    return -k*np.exp(-k*r)/r**2 -np.exp(-k*r)/r**3

'''
Demonstrates how to calculate positions on a 3d-vector

This functionality is used to place and orient labels on atoms in the povray.pdb module
'''

__author__ = "Marcel Kempenaar"
__version__ = "2016.1"

import math
import copy
import numpy as np
from povray import povray
from vapory import Scene, Sphere, LightSource, Texture, Pigment, Cylinder, Finish

def scene(step):
    ''' Returns the scene at step number (1 step per frame) '''
    A = np.array([-10, 8, 0])
    B = np.array([5, 2, -20])
    
    # Find a point with distance 3 from A
    BA = B-A # Vector B->A
    d = math.sqrt(sum(np.power(BA, 2))) # distance
    BA = BA / d # Normalize by its length; BA / ||BA||
    scale = 4
    N = A + scale * BA # Scale and add to A
    l = Cylinder(A, B, 0.05, Pigment('color', [0, 1, 0]))
    s1 = Sphere(N, 0.5, Texture(Pigment('color', [0.9, 0.05, 0.05])))
    
    scale = 15
    N = A + scale * BA # Scale and add to A
    s2 = Sphere(N, 0.5, Texture(Pigment('color', [0.9, 0.05, 0.05])))
    
    scale = 24
    N = A + scale * BA # Scale and add to A
    s3 = Sphere(N, 0.5, Texture(Pigment('color', [0.9, 0.05, 0.05])))
    
    return Scene(povray.floor_camera,
                 objects=[povray.default_light, povray.checkered_ground, 
                 l, s1, s2, s3],
                 included=['colors.inc'])

if __name__ == '__main__':
    # Create a frame
    povray.make_frame(0, scene, time=True)

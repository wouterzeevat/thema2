'''
Shows how to get text on a sphere by curving the text
'''

__author__ = "Marcel Kempenaar"
__version__ = "2016.1"

import math
import copy
import numpy as np
from povray import povray, pdb, load_config
from vapory import *

def scene(step):
    camera = Camera('location', [-2, -2, -25], 'look_at', [0, 0, -15])
    # Add a light to the front
    light = LightSource([0, 5, -29], 'color', [1, 1, 1],
                              'fade_distance', 15, 'fade_power', 2,
                              'area_light', 3, 3, 12, 12,
                              'circular orient adaptive', 0)

    # Spheres
    s1 = Sphere([0, 2, -18], 1.5, Texture(Pigment('color', 'Gold')))
    s2 = Sphere([0, 2, -17.9], 1.5, 
                Texture(Pigment('color', 'Red'), 
                        Finish('phong', 0.6, 'reflection', 0.8)))
    
    # Intersecting text
    t = Text('ttf', '"timrom.ttf"', '"Atom!"', 1, 0,
             Texture(Pigment('color', 'Gold'), Finish('phong', 0.6, 'reflection', 0.6)),
             'translate', [-1, 2, -19.5])

    return Scene(camera,
                 objects=[light, Union(Intersection(s1, t), s2, 
                 'translate', [-1, 1.5, 0], 'rotate', [-14, -3, 0])],
                 included=['colors.inc'])

if __name__ == 'vapory':
    # Create a frame
    povray.make_frame(0, scene, time=True)

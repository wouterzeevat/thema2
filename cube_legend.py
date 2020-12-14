#!/usr/bin/env python3

"""
Module that creates a cube with a legend. 
Needs legend.py to work.
Assignment for week 2
"""

__author__ = "Keimpe, Wouter"

from pypovray import pypovray, models
from vapory import Sphere, Scene, Box, LightSource, Texture, Finish, Pigment, Cone, Camera
from legend import legend


def frame(step):
    """ Creates a frame of 4 cones, 4 boxes, 1 sphere and a legend """

    # Define textures for different models
    sphere_model = Texture(Pigment('color', [1, 0, 1], ), Finish('reflection', 0.5))
    box_model = Texture(Pigment('color', [0, 1, 1], ), Finish('reflection', 0))
    cone_model = Texture(Pigment('color', [1, 0, 1], ), Finish('reflection', 0))

    # Create objects
    sphere = Sphere([0, 0, 0], 3, sphere_model)

    box_1 = Box([-5, -5, -4], [-3, 5, 4], box_model)
    box_2 = Box([3, -5, -4], [5, 5, 4], box_model)
    box_3 = Box([-5, 4, -4], [5, 6, 4], box_model)
    box_4 = Box([-5, -5, -4], [5, -3, 4], box_model)

    cone_1 = Cone([0, 6, 0], 3, [0, 10, 0], 0, cone_model)
    cone_2 = Cone([0, -6, 0], 3, [0, -10, 0], 0, cone_model)
    cone_3 = Cone([-5, 0, 0], 3, [-9, 0, 0], 0, cone_model)
    cone_4 = Cone([5, 0, 0], 3, [9, 0, 0], 0, cone_model)

    light_1 = LightSource([0, 10, -25], 'color', [1, 1, 1])
    light_2 = LightSource([0, 8, -7], 'color', [1, 1, 1])

    xyz_legend = legend([-15, 0, 0], 5)

    camera = Camera('location', [0, 7, -30], 'look_at', [0, 2, 1])

    # Return the Scene object for rendering
    return Scene(camera,
                 objects=[sphere, box_1, box_2, box_3, box_4,
                          cone_1, cone_2, cone_3, cone_4, light_1, light_2] + xyz_legend)


if __name__ == '__main__':  # If module not imported
    pypovray.render_scene_to_png(frame)  # Render as an image

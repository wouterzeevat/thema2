#!usr/bin/env python3

"""
Module that creates a legend.
Needs to be imported by assignment2b.py
Assignment for week 2
"""

__author__ = "Keimpe, Wouter"

from pypovray import pypovray, models
from vapory import Scene, Cylinder, Cone, Pigment, Texture, Finish, LightSource, Camera

def legend(loc, length):
    """
    Creates a legend in a given location.
        Usage: legend([x, y, z], length)
    """

    # Defining textures for each axis
    x_model = Texture(Pigment('color', [1, 0, 0], ), Finish('reflection', 0))
    z_model = Texture(Pigment('color', [0, 0, 1], ), Finish('reflection', 0))
    y_model = Texture(Pigment('color', [0, 1, 0], ), Finish('reflection', 0))

    # Create objects
    x_cyl = Cylinder(loc, [loc[0] + length, loc[1], loc[2]], 0.1, x_model)
    x_cone = Cone([loc[0] + length, loc[1], loc[2]], 0.3, [loc[0] + length + 1, loc[1], loc[2]], 0, x_model)

    z_cyl = Cylinder(loc, [loc[0], loc[1], loc[2] + length], 0.1, y_model)
    z_cone = Cone([loc[0], loc[1], loc[2] + length], 0.3, [loc[0], loc[1], loc[2] + length + 1], 0, y_model)

    y_cyl = Cylinder(loc, [loc[0], loc[1] + length, loc[2]], 0.1, z_model)
    y_cone = Cone([loc[0], loc[1] + length, loc[2]], 0.3, [loc[0], loc[1] + length + 1, loc[2]], 0, z_model)

    return [x_cyl, x_cone, y_cyl, y_cone, z_cyl, z_cone]

def frame(step):

    camera = Camera('location', [0, 7, -30], 'look_at', [0, 2, 1])
    xyz_legend = legend([-15, 0, 0], 5)
    light = LightSource([0, 10, -25], 'color', [1, 1, 1])

    return Scene(camera,
                 objects=[light] + xyz_legend)

if __name__ == '__main__':  # If module not imported
    pypovray.render_scene_to_png(frame)  # Render as an image
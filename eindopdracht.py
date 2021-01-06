#!/usr/bin/env python3

"""
Final assignment of theme 2
Animation visualising the process of insulin binding on it's receptor
    usage: python3 eindopdracht.py - <-- runs all frames
    usage: python3 eindopdracht.py <frame> <-- runs curtain frame
    usage: python3 eindopdracht.py <start_frame> <end_frame> <-- runs curtain part
"""

__author__ = "Keimpe Dijkstra, Wouter Zeevat"
__version__ = "2020.1"

import sys
import pydoc
from pypovray import pypovray, SETTINGS, models, pdb, logger
from vapory import Scene, Camera, LightSource, Finish, Pigment, Texture, Sphere, Cylinder, Text, LightSource
from read_pdb import get_ins

#global variables
PATH_PDB = "/homes/kdijkstra/thema2/pdb/6ce7.pdb"


def make_receptor(loc, size=5):
    """
    Creates the receptor and returns the object
    """
    rec_model = Texture(Pigment('color', [0, 1, 1], ), Finish('reflection', 0))

    x = loc[0]
    y = loc[1]
    z = loc[2]

    rec = list()
    rec.append(Cylinder([x - size * 1.2, y - size * 15, z], [x - size * 1.2, y + size*2, z], size, rec_model))
    rec.append(Cylinder([x + size * 1.2, y - size * 15, z], [x + size * 1.2, y + size*2, z], size, rec_model))
    rec.append(Cylinder([x - size * 1.2, y + size * 1.2, z], [x - size * 5, y + size * 4, z], size, rec_model))
    rec.append(Cylinder([x - size * 7.2, y + size * 4, z - size/2],
                        [x - size * 3.2, y + size * 4, z - size/2],
                        size / 1.321, rec_model))

    rec.append(Cylinder([x + size * 1.2, y + size * 1.2, z], [x + size * 5, y + size * 4, z], size, rec_model))
    rec.append(Cylinder([x + size * 7.2, y + size * 4, z - size/2],
                        [x + size * 3.2, y + size * 4, z - size/2],
                        size / 1.321, rec_model))

    rec.append(Sphere([x, y - size * 6, z], size * 3, rec_model))

    return rec


def make_membrane(loc, amount, size=5):
    """
    Create the membrane and returns the object
    """

    sphere_model = Texture(Pigment('color', [1, 0, 0], ), Finish('reflection', 0))
    cyl_model = Texture(Pigment('color', [0.7, 0.3, 0], ), Finish('reflection', 0))

    x_position = loc[0]
    y_position = loc[0] - size * 6
    objects = []
    for index in range(1, amount + 1):

        # Create top spheres
        objects.append(Sphere([x_position, loc[1], loc[2]], size, sphere_model))
        objects.append(Sphere([0 - x_position, loc[1], loc[2]], size, sphere_model))

        # Create top cylinders
        location = [x_position - size/3, loc[1], loc[2]], [x_position - size/3, loc[1] - size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [x_position + size/3, loc[1], loc[2]], [x_position + size/3, loc[1] - size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [0-x_position - size/3, loc[1], loc[2]], [0-x_position - size/3, loc[1] - size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [0-x_position + size/3, loc[1], loc[2]], [0-x_position + size/3, loc[1] - size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        # Create bottom spheres
        objects.append(Sphere([x_position, y_position, loc[2]], size, sphere_model))
        objects.append(Sphere([0 - x_position, y_position, loc[2]], size, sphere_model))

        # Create bottom cylinders
        location = [x_position - size/3, y_position, loc[2]], [x_position - size/3, y_position + size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [x_position + size/3, y_position, loc[2]], [x_position + size/3, y_position + size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [0-x_position - size/3, y_position, loc[2]], [0-x_position - size/3, y_position + size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [0-x_position + size/3, y_position, loc[2]], [0-x_position + size/3, y_position + size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        x_position += size * 2

    return objects


def make_tyrine(loc, size):
    """
    Creates the tyrine molecules
    """
    text_model = Texture(Pigment('color', [1, 1, 0], ), Finish('reflection', 0))
    cyl_model = Texture(Pigment('color', [0, 1, 0.5], ), Finish('reflection', 0))

    tyr = []
    y_always = [13, 13, 10, 10]
    x_text = [-3, 5, -3, 5]
    x_end = [-5, 5, -5, 5]
    x = loc[0]
    y = loc[1]
    z = loc[2] + 7
    for _ in range(4):
        tyr.append(Cylinder([x, y-size * y_always[_], z], [x-size*x_end[_], y-size*y_always[_], z], size, cyl_model))
        text = Text('ttf', '"timrom.ttf"', '"{}"'.format(str('Tyr')), 2, [0, 0, 0], text_model, 'scale', 5, 'translate', [x-size*x_text[_], y-size*y_always[_], z - 7])
        tyr.append(text)
    return tyr


def zoom_in(frame):
    """
    Animating the zooming in part
    """
    return


def bind_insuline(frame):
    """
    Animating the insuline binding
    """
    return


def zoom_out(frame):
    """
    Animating the zooming out part
    """
    return


def bind_phosphorus(frame):
    """
    Animating the process of phosfor binding to the Tyr
    """
    return


def bind_IRS(frame):
    """
    Animating the process of IRS binding to the phosfor
    """
    return


def activation(frame):
    """
    Visualizing the cell activation
    """
    return


def frame(step):
    """ Returns the scene at step number (1 step per frame) """

    camera = Camera('location', [0, 7, -200], 'look_at', [0, 0, 0])
    lights = [LightSource([0, -10, -60], 0.5),
              LightSource([0, -50, -60], 0.5),
              ]

    receptor = make_receptor([0, 0, -2], 5)
    membrane = make_membrane([0, 0, 0], 10, 5)
    tyrine = make_tyrine([0, 0, -2], 5)

    # Return the Scene object containing all objects for rendering
    return Scene(camera,
                 objects=[models.default_light] + tyrine + membrane + receptor + tyrine + lights)


def main(args):
    """ Main function performing the rendering """

    # Checks how to run animation depending on given arguments
    if len(args) < 2:
        pydoc.help(__name__)
    elif len(args) < 3:
        if args[1] == "-":
            pypovray.render_scene_to_mp4(frame)
        else:
            pypovray.render_scene_to_png(frame, int(args[1]))
    elif len(args) < 4:
        pypovray.render_scene_to_mp4(frame, range(int(args[1]), int(args[2]) + 1))
    else:
        pydoc.help(__name__)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

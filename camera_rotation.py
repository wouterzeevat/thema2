#!/usr/bin/env python3
"""
Uses cos and sin to create a camera rotating around objects.
    Usage: python3 camera_rotation.py
"""

__author__ = "Keimpe Dijkstra, Wouter Zeevat"
__version__ = " 2020.1"

import sys
from pypovray import pypovray, SETTINGS, models, logger
from vapory import Sphere, Scene, Texture, Pigment, Finish, Cylinder, Camera
import math
from legend import legend


def frame(step):
    """ Creates a frame of a given frame (step) number. """

    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)

    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)

    # Calculates rotation positions
    angle_per_frame = math.pi * 2 / nframes  # Calculates how much the angle needs to move per frame
    angle = angle_per_frame * step # Calculates the angle of the frame

    # Gets locations
    x = math.cos(angle) * 20
    z = math.sin(angle) * 20

    # Create objects
    sphere = Sphere([6, 2, -2], 3, models.default_sphere_model)
    cylinder = Cylinder([-6, -1, 4], [-6, 7, 4], 3, models.default_sphere_model)
    legend_1 = legend([-15, 0, 0], 5)
    camera = Camera('location', [x, 8, z], 'look_at', [0, 0, 0])

    # Return the Scene object containing all objects for rendering
    return Scene(camera,
                 objects=[sphere, models.default_light, models.checkered_ground, cylinder] + legend_1)


def main(args):
    """ Main function that will run other functions """
    logger.info(" Total time: %d (frames: %d)", SETTINGS.Duration, eval(SETTINGS.NumberFrames))
    pypovray.render_scene_to_gif(frame)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

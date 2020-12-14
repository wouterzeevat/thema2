#!/usr/bin/env python3
"""
Simple template moving a sphere from left to right using Povray

Uses a number of pre-defined Povray objects to simplify scene building

    usage:
        python3 template.py
"""

__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2017.3"

import sys
from pypovray import pypovray, SETTINGS, models, logger
from vapory import Sphere, Scene, Cylinder, Texture, Pigment, Finish, Camera
from assignment2b import legend
import math


def frame(step):
    """ Returns the scene at step number (1 step per frame) """

    cylinder = Cylinder([-6, -1, 4], [-6, 8, 4], 4, models.default_sphere_model)
    sphere = Sphere([6, 2, -2], 3, models.default_sphere_model)
    xyz_legend = legend([-15, 0, 0], 5)

    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)

    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)

    distance_per_frame = 50 / nframes
    z_start = -25
    z_end = 25

    if step < (nframes / 2):

        z = z_start + step * distance_per_frame
        x = math.sqrt(25 ** 2 - z ** 2)
    else:

        z = z_end - step * distance_per_frame
        x = -1 * math.sqrt(25 ** 2 - z ** 2)


    camera = Camera('location', [x, 8, z], 'look_at', [0, 0, 0])

    # Return the Scene object containing all objects for rendering
    return Scene(camera,
                 objects=[sphere, cylinder, models.checkered_ground, models.default_light])


def main(args):
    """ Main function performing the rendering """
    logger.info(" Total time: %d (frames: %d)", SETTINGS.Duration, eval(SETTINGS.NumberFrames))
    pypovray.render_scene_to_mp4(frame)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

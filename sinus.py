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
from vapory import Sphere, Scene, Texture, Pigment, Finish
import math


def frame(step):
    """ Returns the scene at step number (1 step per frame) """
    sphere_model = Texture(Pigment('color', [250, 0, 0], ), Finish('reflection', 0.5))

    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)

    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)

    # Start- and end-points
    x_start = -5
    x_end = 5
    distance = x_end - x_start

    # Calculate distance to move at each step
    distance_per_frame = (distance / nframes) * 2

    # Calculate new x-coordinate
    if step < (nframes / 2):
        # Move from left to right (starting at x = -10)
        x_coord = x_start + step * distance_per_frame
    else:
        # Move from right to left (starting at x = 10)
        x_coord = x_end - (step - (nframes / 2)) * distance_per_frame

    y_coord = 2 * math.sin((2*math.pi/2)*(x_coord-1))+0.5
    # Create sphere at calculated x-coordinate using default model
    sphere = Sphere([x_coord, y_coord, 0], 1, sphere_model)

    # Return the Scene object containing all objects for rendering
    return Scene(models.default_camera,
                 objects=[sphere, models.default_light])


def main(args):
    """ Main function performing the rendering """
    logger.info(" Total time: %d (frames: %d)", SETTINGS.Duration, eval(SETTINGS.NumberFrames))
    pypovray.render_scene_to_gif(frame)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

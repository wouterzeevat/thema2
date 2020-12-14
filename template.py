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
from vapory import Sphere, Scene


def frame(step):
    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)

    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)

    # Start- and end-points
    x_start = -10
    x_end = 10
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

    # Create sphere at calculated x-coordinate using default model
    sphere = Sphere([x_coord, 0, 0], 2, models.default_sphere_model)

    # Return the Scene object containing all objects for rendering
    return Scene(models.default_camera,
                 objects=[sphere, models.default_ground, models.default_light])


def main(args):
    """ Main function performing the rendering """
    logger.info(" Total time: %d (frames: %d)", SETTINGS.Duration, eval(SETTINGS.NumberFrames))
    pypovray.render_scene_to_mp4(frame)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

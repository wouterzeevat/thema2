#!/usr/bin/env python3

"""
Module that will visualize the progress of ATP becoming ADP.
"""

__author__ = "Keimpe Dijkstra, Wouter Zeevat"

import sys
from pypovray import pypovray, SETTINGS, models, pdb, logger
from vapory import Scene, Camera, LightSource
import numpy as np


def frame(step):
    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)

    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)

    # Create molecule
    atp = pdb.PDBMolecule('{}/pdb/ATP_ideal.pdb'.format(SETTINGS.AppLocation), center=True)
    atp.move_to([0, 5, 0])

    # Creates phospate sliced molecule
    phosphate = atp.divide([0, 1, 2, 3, 7, 31, 32], 'phosphate')

    # Creates other objects
    camera = Camera('location', [25, 5, 10], 'look_at', [0, 5, 0])
    light = LightSource([25, 5, 10], 'color', [1, 1, 1])

    # Splicing the molecules animation
    if step <= 20 and step > 5:
        y = (0 - 4 / 15) * (step - 5)  # Moves for 15 frames, -4x in total
        phosphate.move_offset([0, y, 0])

    # Keeping the phospate in it's position after it moved
    elif step > 5:
        y = (0 - 4 / 15) * (20 - 5)  # Moves it like the 20th frame to keep it's position
        phosphate.move_offset([0, y, 0])

        # Rotating the molecules
        if step >= 30 and step < 70:
            phosphate.rotate([1, 0, 0], np.pi * 2 / 40 * (step - 30))  # Rotates it for 40 frames, 1 - 2pi
            atp.rotate([0, 1, 0], np.pi * 2 / 40 * (step - 30))

    # Return the Scene object containing all objects for rendering
    return Scene(camera,
                 objects=[models.checkered_ground,
                          models.default_light, light] + atp.povray_molecule + phosphate.povray_molecule)


def main(args):
    """ Main function performing the rendering """
    logger.info(" Total time: %d (frames: %d)", SETTINGS.Duration, eval(SETTINGS.NumberFrames))
    pypovray.render_scene_to_mp4(frame)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

'''
Simple template rendering a molecule originating from a PDB file.

The animation demonstrates the molecule both rotating and traversing on a
trajectory using the move_to and rotate methods.

NOTE: also shows how to do prototyping using multithreading; see the
prototype.ini configuration file.

Uses a number of pre-defined Povray objects to simplify scene building
'''

__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2017.3"

import math
import copy
from pypovray import pypovray, pdb, load_config, models, logger
from vapory.vapory import Scene, LightSource, Sphere

ETHANOL = RAD_PER_SCENE = FRONT_LIGHT = TRACER = None


def scene_objects():
    """ Creates molecule objects and any other pre-calculated data """
    global ETHANOL, RAD_PER_SCENE, FRONT_LIGHT, TRACER

    FRONT_LIGHT = LightSource([0, 14, -28], 'color', [1, 0.8, 0.4],
                              'fade_distance', 6, 'fade_power', 2,
                              'area_light', 3, 3, 12, 12,
                              'circular orient adaptive', 0)

    # Calculate the radians per scene (one full rotation)
    RAD_PER_SCENE = (math.pi / eval(pypovray.SETTINGS.NumberFrames)) * 2
    # Create a list holding the 'tracing' spheres that are drawn as the molecule moves
    TRACER = []
    # Read in a PDB file and construct a molecule
    ETHANOL = pdb.PDBMolecule('pdb/ethanol.pdb', center=False, offset=[-10, 8, -5])


def frame(step):
    """ Returns the scene at step number (1 step per frame) """
    logger.info("@ Step %d", step)

    # The Ethanol molecule is moved on a trajectory representing a 'figure 8' or the infinity
    # symbol by calculating the x- and y-coordinates using the lemniscate of Bernoulli.
    alpha = 9
    scale = alpha * math.sqrt(2)
    radians = step*RAD_PER_SCENE

    x = scale * math.cos(radians) / \
        (math.sin(radians) ** 2 + 1)

    y = scale * math.cos(radians) * \
        math.sin(radians) / \
        (math.sin(radians)**2 + 1)

    # Draws spheres on each of the calculated x,y coordinates
    TRACER.append(Sphere([x, y, -4], 0.2, models.default_sphere_model))

    # Copying the full molecule - only needed for multithreading
    # This is required for multithreading
    ethanol = copy.deepcopy(ETHANOL)

    # Move the molecule to the calculated coordinates
    ethanol.move_to([x, y, -5])

    # Rotate the molecule on x- and y-axes
    # NOTE: default rotate does NOT work when using a thread-pool,
    # use the molecule.rotate_by_step method instead
    ethanol.rotate_by_step([1, 0, 0], RAD_PER_SCENE, step)

    # Return a 'Scene' object containing -all- objects to render, i.e. the camera,
    # lights and in this case, a molecule and a list of spheres (TRACER).
    return Scene(models.default_camera,
                 objects=[models.default_light, FRONT_LIGHT] + ethanol.povray_molecule + TRACER,
                 included=['colors.inc'])


if __name__ == '__main__':
    # Load the prototyping settings instead of the default
    pypovray.SETTINGS = load_config('prototype.ini')

    # Create static objects
    scene_objects()

    # Render as an MP4 movie
    pypovray.render_scene_to_mp4(frame, range(20, 40))

    # Timing for running the current simulation including creating the movie:
    #  |  Single-thread (s)  |  Multi-threaded (s) |
    #  |---------------------|---------------------|
    #  |       101.561       |       16.341        |
    #  |---------------------|---------------------|

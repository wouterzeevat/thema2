#!/usr/bin/env python3
"""
Simple template rendering a number of molecules originating from PDB files.

It also demonstrates the usage of different configuration files to influence
the rendering (use -h to see how).

Uses a number of pre-defined Povray objects to simplify scene building
"""

__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2017.3"

import sys
import math
import argparse
from pypovray import pypovray, pdb, load_config, models, logger
from vapory import Scene, LightSource

# This program uses globals as the `scene` function requires them at each step
ETHANOL = VIAGRA = BENZENE = RAD_PER_SCENE = FRONT_LIGHT = None


def scene_objects():
    """ Creates molecule objects and any other pre-calculated data """
    global ETHANOL, VIAGRA, BENZENE, RAD_PER_SCENE, FRONT_LIGHT

    FRONT_LIGHT = LightSource([0, 14, -28], 'color', [1, 0.8, 0.4],
                              'fade_distance', 6, 'fade_power', 2,
                              'area_light', 3, 3, 12, 12,
                              'circular orient adaptive', 0)

    # Calculate the radians per scene
    RAD_PER_SCENE = (math.pi / 180) * 3

    # Read in a PDB file and construct a molecule
    ETHANOL = pdb.PDBMolecule('pdb/ethanol.pdb', center=False, offset=[-10, 8, -5])
    VIAGRA = pdb.PDBMolecule('pdb/viagra.pdb', center=False, offset=[3, -3, -7])
    BENZENE = pdb.PDBMolecule('pdb/benzene.pdb', center=False, offset=[0, 8, -5])


def frame(step):
    """ Returns the scene at step number (1 step per frame) """

    # Rotate the molecules updating its orientation (a persistent modification)
    ETHANOL.rotate([1, 1, 0], RAD_PER_SCENE)
    VIAGRA.rotate([1, 0, 1], RAD_PER_SCENE)
    BENZENE.rotate([0, 1, 1], RAD_PER_SCENE)

    # Combine molecule objects (an object.povray_molecule is a list of atoms, they need
    # to be concatenated to be added to the scene)
    molecules = ETHANOL.povray_molecule + VIAGRA.povray_molecule + BENZENE.povray_molecule

    logger.info(' @Step: %s', step)
    # Return a 'Scene' object containing -all- objects to render, i.e. the camera,
    # light(s) and in this case, molecules too.
    return Scene(models.default_camera,
                 objects=[models.default_light, FRONT_LIGHT] + molecules,
                 included=['colors.inc'])


def main(args):
    """ Runs the simulation """

    # Load a user defined configuration file
    if args.config:
        pypovray.SETTINGS = load_config(args.config)
    if args.frame:
        # Create objects for the scene (i.e. parse PDB files)
        scene_objects()
        # User entered the specific frame to render
        pypovray.render_scene_to_png(frame, args.frame)
    else:
        # No output file type and no specific frame, exit
        if not args.gif and not args.mp4:
            parser.print_help()
            sys.exit('\nPlease specify either a specific frame number or ' +
                     'output format for a movie file')
        else:
            # Create objects for the scene (i.e. parse PDB files)
            scene_objects()
        # Render a movie, depending on output type selected (both files is possible)
        if args.gif:
            pypovray.render_scene_to_gif(frame)
        if args.mp4:
            pypovray.render_scene_to_mp4(frame)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Render PDB files using Python and Povray')
    parser.add_argument('--config', help='Load a configuration file containing pypovray settings')
    parser.add_argument('--frame', type=int,
                        help='A specific frame (number) to render ' +
                        '(single image output file)')
    parser.add_argument('--gif', action="store_true", default=False,
                        help='Create a GIF movie file using moviepy. ' +
                        'Note; this reduces the output quality')
    parser.add_argument('--mp4', action="store_true", default=False,
                        help='Create a high-quality MP4 output file using ffmpeg')

    pargs = parser.parse_args()

    sys.exit(main(pargs))

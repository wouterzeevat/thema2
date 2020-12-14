#!/usr/bin/env python3

""" Example of the ball-and-stick model for rendering a molecule from a PDB file. """

from pypovray import pypovray, SETTINGS, pdb, models
from vapory.vapory import Scene
from math import pi

__author__ = 'Niels van der Vegt'

VIAGRA = None


def molecule():
    """ Creates a molecule for rendering """
    global VIAGRA
    VIAGRA = pdb.PDBMolecule('{}/pdb/viagra.pdb'.format(SETTINGS.AppLocation), center=True)
    VIAGRA.move_offset([0, 1, 0])
    VIAGRA.scale_atom_distance(1.75)


def scene(step):
    rotate_coo = pi * 2 / 180
    VIAGRA.rotate([0, 1, 0], rotate_coo)
    # Change model to ball-and-stick
    VIAGRA.show_stick_model()
    return Scene(models.default_camera,
                 objects=[models.default_light] + VIAGRA.povray_molecule)


def main():
    molecule()
    pypovray.render_scene_to_mp4(scene)


main()


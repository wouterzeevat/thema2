'''
Simple template rendering an ATP molecule originating from PDB files.
'''

__author__ = "Marcel Kempenaar"
__version__ = "2016.1"

import math
from povray import povray, pdb
from vapory import Scene, LightSource


def scene_objects():
    ''' Creates molecule objects and any other pre-calculated data '''
    # Store in the global namespace so the scene() method has access
    global ATP, RAD_PER_SCENE, FRONT_LIGHT

    FRONT_LIGHT = LightSource([0, 5, -29], 'color', [1, 1, 1],
                              'fade_distance', 15, 'fade_power', 2,
                              'area_light', 3, 3, 12, 12,
                              'circular orient adaptive', 0)

    # Calculate the radians per scene
    RAD_PER_SCENE = (math.pi / 180) * 3

    # Read in a PDB file and construct a molecule
    ATP = pdb.PDBMolecule('pdb/ATP_ideal.pdb', center=False)
    # Move to the center, and raise a little
    ATP.move_to([0, 6, 0])
    # Rotate so that the N-tail points downwards a bit
    ATP.rotate([0, 1, 1], [0, 1, -1.5])

def scene(step):
    ''' Returns the scene at step number (1 step per frame) '''
    ATP.rotate([0, 1, 0], [0, RAD_PER_SCENE, 0])
    ATP.show_label(camera=povray.floor_camera, name=True)

    # Return a 'Scene' object containing -all- objects to render, i.e. the camera,
    # lights and in this case, a molecule with its labels.
    return Scene(povray.floor_camera,
                 objects=[povray.default_light,
                          FRONT_LIGHT,
                          povray.checkered_ground] + ATP.povray_molecule,
                 included=['colors.inc'])

if __name__ == '__main__':
    # Create static objects
    scene_objects()

    # Render a movie with the rotating molecule
    povray.render_scene_to_mp4(scene, time=True)

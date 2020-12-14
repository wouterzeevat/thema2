#!/usr/bin/env python3

from povray import povray, SETTINGS, load_config
from vapory import Sphere, Scene, Pigment, POVRayElement, Cylinder, Camera, Texture, Finish
from assignment2 import legend

def scene(step):
    # Storing the cylinders
    cylinders = []
    n = 7
    for i in range(n):
        cylinders.append(Cylinder([0, 0, 0], [1.2, 0, 0], 1.0, 1.0,
                         'scale', [1, 0.25, 1],
                         'rotate', [-30, 0, 0],
                         'translate', [1.25, 0, 0],
                         'rotate', [0, i * 360/n, 0],
                         Texture('Chrome_Texture'), 
                                 Pigment('color', [0.1, 0.1, 0.1]), 
                                 Finish('phong', 1, 'reflection', 1)))

    # Reset color for the center sphere
    degrees = (360/(SETTINGS.Duration*SETTINGS.RenderFPS))*step
    
    prop = Blob('threshold', 0.65,
                # Add a Sphere with radius and strength = 1
                Sphere([0, 0, 0], 1.00, 1.00,
                # Double the heigth of the Sphere
                'scale', [1, 2, 1],
                # Make it shine
                Texture('Chrome_Texture', 
                        Pigment('color', [0.1, 0.1, 0.1]), 
                        Finish('phong', 0.5, 'reflection', 0.5))),
                # unpack cylinders
                *cylinders,
                # Scale the whole objects (enlarge)
                'scale', 1.8,
                # rotate counter-clockwise
                'rotate', [90, 0, degrees],
                # re-center
                'translate', [0, 0.5, 0])

    camera = Camera('location', [5, 10, -8], 'look_at', [0, 0, 0])
    xyz_legend = legend([-10, 0, 0], 3)
    return Scene(camera, objects=[prop] + xyz_legend + povray.default_spots, 
                 # The 'Chrome_Texture comes from the 'textures.inc' file
                 included=['textures.inc'])

class Blob(POVRayElement):
    """ Blob(blob_item1, blob_item2, ...) """

if __name__ == '__main__':
    # Render as an image
    povray.make_frame(0, scene, time=True)
    
    # Uncomment to create rotation animation
    #SETTINGS = povray.SETTINGS = load_config('prototype.ini')
    #povray.render_scene_to_gif(scene, time=False)


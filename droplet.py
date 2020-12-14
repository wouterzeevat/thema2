#!/usr/bin/env python3

"""
Demonstrates how extracellular elements can enter a membrane through pinocytosis

Uses a mathematical model devised by Dr. T. Wassenaar
    see povray/drop.py
"""

from pypovray import pypovray, drop, load_config, SETTINGS, models
from vapory.vapory import Camera, Scene, Sphere, Cylinder, Pigment, Merge


def scene(step):
    """ Gets the coordinates of a (variable) number of points on the membrane
    Arguments given to the membrane function are:
        step: the current step (frame number)
        10  : the radius of the circle falling through the membrane
        10  : 'gamma'; the angle of the pinch
        10  : the start (y-value) of the circle 'falling through the membrane'
        -35 : the stop (y-value)
        nframes : number of frames for the simulation
        [0, 2, 0] : the offset to move the membrane around the scene
        80  : the total length (povray 'units') of the membrane
        2.0 : the 'apl' defines the space between the coordinates (with size = 80 and apl = 2.0 you get
              40 coordinates (80/2) for a straight membrane)

    When increasing the 'size' and 'apl' parameters remember to also increase the 'radius', 'gamma'
    and 'start/stop' values accordingly.
    """
    nframes = SETTINGS.Duration * SETTINGS.RenderFPS
    coordinates = drop.membrane(step, 10, 5, 11, -40, nframes, offset=[0, 15, 0], size=80, apl=2.0)

    ''' The 'coordinates' is a list containing three-element lists with x- y- and z-coordinates
    that we can use to draw Spheres (this example) or for positioning lipoproteins etc. '''
    spheres = []
    lipos = []
    lipo_length = 2

    for coord in coordinates:
        # Use the coordinates to place a sphere with radius 1
        spheres.append(Sphere([coord[0], coord[1], coord[2]], 1,
                       Pigment('color', [1, 1, 1])))

        if coord[3] != 0:
            '''
            These 'lipos' are placeholders for either atomic models of lipoproteins or can be altered
            to show a simplified membrane structure.

            The Cylinder is first placed at [0, 0, 0] and extended on the y-axis (from -lipo_length to
            +lipo_length), then it is rotated using the 'angle' stored in coord[3] and finally positioned
            at the location of the added Sphere using the 'translate' function:
            'translate': http://www.f-lohmueller.de/pov_tut/trans/trans_100e.htm
            'rotate': http://www.f-lohmueller.de/pov_tut/trans/trans_200e.htm

            An alternative method would be to use the angle and the Sphere coordinate to calculate
            the Cylinder start- and end-point.
            '''
            cyl = Cylinder([0, -lipo_length, 0],
                           [0, lipo_length, 0], 0.5,
                           Pigment('color', [1, 0, 0]))
            bottom_sphere = Sphere([0, -lipo_length, 0], 1,
                                   Pigment('color', [1, 0, 0]))
            top_sphere = Sphere([0, lipo_length, 0], 1,
                                Pigment('color', [1, 0, 0]))
            lipos.append(Merge(cyl, top_sphere, bottom_sphere, 'rotate', [0, 0, coord[3]],
                               'translate', [coord[0], coord[1], coord[2]]))
    # The camera looks straight at the membrane otherwise the vesicle looks like an ellipse
    camera = Camera('location', [0, 0, -60], 'look_at', [0, 0, 0])
    return Scene(camera, objects=[models.default_light] + spheres + lipos)


if __name__ == '__main__':
    # Uncomment to use prototype settings
    #SETTINGS = povray.SETTINGS = load_config('prototype.ini')
    #pypovray.render_scene_to_gif(scene)
    pypovray.render_scene_to_png(scene, 5)

#!/usr/bin/env python3
"""
Renders a movie using Povray

Usage:
    - To get the help for this program, use:
        simulation.py -h
    - To render a single frame (frame number 10):
        simulation.py --time 10
    - To render a series of frames into an MP4 movie:
        simulation.py --mp4 --range [0, 10]
    - To use a different configuration file:
        simulation.py --config prototype.ini
    - To render an MP4 movie using default settings:
        simulation.py --mp4
"""

import argparse
import sys
import ast
from pypovray import pypovray, SETTINGS, load_config, logger
from vapory import Scene, LightSource, Camera, Sphere, Cylinder, Plane, Texture, Pigment, Finish, Interior, Difference

# Scene Global Settings
RADIUS = 10  # scene circle radius

# Scene Settings and Static Objects
MAIN_LIGHT = LightSource([2, 4, -3], 3, 'fade_distance', 5,
                         'fade_power', 2, 'area_light', 3, 3, 12, 12,
                         'circular orient adaptive', 0)
BACK_LIGHT = LightSource([-8, 3, -1], 'color', [1, 0.8, 0, 4],
                         'fade_distance', 6, 'fade_power', 2,
                         'area_light', 3, 3, 12, 12,
                         'circular orient adaptive', 0)
CAMERA = Camera('location', [0, 10, -20], 'look_at', [0, 0, -3])
GROUND = Plane([0, 1, 0], -4, Texture(Pigment('color', [1.5, 1, 1])))

def sphere_circle():
    """ Creates a circle made up of 20 small spheres.
        A list of Sphere objects is returnded ready for rendering. """
    spheres = 20  # number of spheres to create
    ring = []
    ring_node_size = 0.6
    smodel = Texture(Pigment('color', [1, 0, 0], 'filter', 0.5),
                     Finish('phong', 0.8, 'reflection', 0.5))
    for i in range(spheres):
        ring.append(Sphere([0, 0, 0], ring_node_size, smodel,
                           'translate', [RADIUS, 0, 0],
                           'rotate', [0, 360/spheres * i, 0]))
    return ring


# Create a list of sphere objects forming the circle (only build once)
RING = sphere_circle()


def frame(step):
    """ Returns the scene at the given step  """
    # Show some information about how far we are with rendering
    curr_time = step * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)

    ## Rotating sphere, placed in the center
    sphere_rad = 1.8
    sphere = Sphere([0, 0, 0], sphere_rad,
                    Pigment('color', [0.9, 0.05, 0.05], 'filter', 0.7),
                    Interior('ior', 1), Finish('phong', 0.6, 'reflection', 0.4))

    # Intersecting cylinder object
    rod = Cylinder([0, 0, 3], [0, 0, -3],
                   1.0, 'open', Pigment('color', [1, 0, 0], 'filter', 0.8),
                   Interior('ior', 1), Finish('phong', 0, 'reflection', 0))

    # 'Hollow out' the rotating sphere with the intersecting cylinder using the Difference,
    # move to a spot on the circle (top) and rotate on the x-axis
    traveller = Difference(sphere, rod, 'translate', [RADIUS, 0, 0],
                           'rotate', [0, 360/eval(SETTINGS.NumberFrames)*step*2, 0])

    return Scene(CAMERA, objects=[GROUND, MAIN_LIGHT, BACK_LIGHT, traveller] + RING)


# Argument parsing and main function below

def main(args):
    """ Runs the simulation """
    if args.config:
        pypovray.SETTINGS = load_config(args.config)
    if args.range:
        # User entered a range of frames to render
        start, stop = ast.literal_eval(args.range)
        frame_range = range(start, stop)
    else:
        # No range entered, use default 0, n_frames
        print(pypovray.SETTINGS.NumberFrames)
        frame_range = range(0, eval(pypovray.SETTINGS.NumberFrames))
    if args.time:
        # User entered the specific timepoint to render (in seconds)
        pypovray.render_scene_to_png(frame, args.time)
    else:
        # No output file type and no specific time, exit
        if not args.gif and not args.mp4 and not args.range:
            parser.print_help()
            sys.exit("\nPlease specify either a specific time point, range of frames" \
                     " or output format for a movie file")
        # Render a movie, depending on output type selected (both files is possible)
        if args.gif:
            pypovray.render_scene_to_gif(frame, frame_range)
        if args.mp4:
            pypovray.render_scene_to_mp4(frame, frame_range)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a rendered movie using Povray')
    parser.add_argument('--config', help='Load a configuration file containing pypovray settings')
    parser.add_argument('--time', type=int,
                        help='A specific time (T) in seconds to render (single image output file)')
    parser.add_argument('--range', help="A range of frame numbers given as a Python List syntax " \
                        "containing start and stop frame numbers: [0, 10] or '0, 10'")
    parser.add_argument('--gif', action="store_true", default=False,
                        help='Create a GIF movie file using moviepy. Note; this reduces the output quality')
    parser.add_argument('--mp4', action="store_true", default=False,
                        help='Create a high-quality MP4 output file using ffmpeg')

    args = parser.parse_args()
    sys.exit(main(args))

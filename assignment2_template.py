#!/usr/bin/env python

"""
Assignment 2 Template script
----------------------------

This template contains a single function ('legend') that needs to be completed
to make an importable legend for use in other programs.

* Write the function docstring explaining what it does and its arguments
* Fill in the two dictionaries ('cylinders' and 'cones')

This function stores all objects to render in dictionaries, try to understand
the code in this template:
    * open an Idle or interactive Python session
    * create a 'start_position' list with values [0, 10, 20]
    * copy/ paste code from the template into IDle to see its effects
    * print/ inspect contents of the 'cylinder_coords' and 'cones_coords_*' dictionaries
    * experiment with any other unclear statements

"""

from vapory import Cylinder, Cone, Pigment, Texture, Finish


def legend(start_position, axis_length):
    """ Function docstring ... """

    # Reduce the AXIS_LENGTH by the length of the Cone (1) so that
    # the total length is exactly the AXIS_LENGTH
    axis_length -= 1

    # Initialize the Cylinder END-position to a COPY of the start position
    cylinder_coords_end = {
        'x': list(start_position),
        'y': list(start_position),
        'z': list(start_position)
    }

    # Add the AXIS_LENGTHs to the corresponding coordinate
    cylinder_coords_end['x'][0] += axis_length
    cylinder_coords_end['y'][1] += axis_length
    cylinder_coords_end['z'][2] += axis_length

    ''' CREATE THE CYLINDERS'''
    cylinders = {
        'x': None,
        'y': None,
        'z': None
    }

    # Cone START is the same as the Cylinder END, so we COPY these lists
    cones_coords_start = {
        'x': list(cylinder_coords_end['x']),
        'y': list(cylinder_coords_end['y']),
        'z': list(cylinder_coords_end['z'])
    }

    # Copy the START as END coordinate
    cones_coords_end = {
        'x': list(cones_coords_start['x']),
        'y': list(cones_coords_start['y']),
        'z': list(cones_coords_start['z'])
    }

    # Extend the tip of the cones with length 1
    cones_coords_end['x'][0] += 1
    cones_coords_end['y'][1] += 1
    cones_coords_end['z'][2] += 1

    ''' CREATE THE CONES '''
    cones = {
        'x': None,
        'y': None,
        'z': None
    }

    # Add ALL objects to a LIST and return
    legend_objects = list(cylinders.values()) + list(cones.values())

    return legend_objects

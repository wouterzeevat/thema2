#!/usr/bin/env python3
"""
Simple template moving a sphere from left to right using Povray

Uses a number of pre-defined Povray objects to simplify scene building

    usage:
        python3 template.py
"""

__author__ = "Keimpe Dijkstra"
__status__ = "Test"
__version__ = "2020.0"

import sys
from pypovray import pypovray, SETTINGS, models, logger, pdb
from vapory import Sphere, Scene, LightSource, Camera
import math
import argparse
from read_pdb import get_ins

PATH = "..\\thema2\\pdb\\6sof.pdb"
PATH_LINUX = "/homes/kdijkstra/thema2/pdb/6sof.pdb"



    

def frame(step):
    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    #curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    #logger.info(" @Time: %.3fs, Step: %d", curr_time, step)

    # Getting the total number of frames, see the configuration file
    #nframes = eval(SETTINGS.NumberFrames)

    ins_id, atom_pos = get_ins(PATH_LINUX)
    

    camera = Camera('location', [0, 0, -100], 'look_at', [0, 0, 0])
    light = LightSource([0, 0, -100], 'color', [1, 1, 1])
    

    insulin_pos = atom_pos["N"] + atom_pos["O"] 
    INSULIN_RECEPTOR = pdb.PDBMolecule(PATH_LINUX, center=False, offset=[-10, 8, -5])
    insulin = INSULIN_RECEPTOR.divide(insulin_pos, 'insulin')
    insulin.move_to([0,0,0])
    
    
    return Scene(camera,
                 objects=[light] + insulin.povray_molecule)

    
def main(args):
    """ Main function performing the rendering """
    
    
    #logger.info(" Total time: %d (frames: %d)", SETTINGS.Duration, eval(SETTINGS.NumberFrames))
    
    
    

    return 0


if __name__ == '__main__':
    #sys.exit(main(sys.argv))
    pypovray.render_scene_to_png(frame)
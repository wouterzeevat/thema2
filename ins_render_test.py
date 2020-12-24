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

PATH = "..\\thema2\\pdb\\6ce7.pdb"
PATH_LINUX = "/homes/kdijkstra/thema2/pdb/6ce7.pdb"



    

def frame(step):
    """ Returns the scene at step number (1 step per frame) """
    # Show some information about how far we are with rendering
    curr_time = step / eval(SETTINGS.NumberFrames) * eval(SETTINGS.FrameTime)
    logger.info(" @Time: %.3fs, Step: %d", curr_time, step)

    # Getting the total number of frames, see the configuration file
    nframes = eval(SETTINGS.NumberFrames)

    if step < 31:
        ins_id, atom_pos = get_ins(PATH_LINUX)
    
        camera = Camera('location', [0, 0, -300], 'look_at', [0, 0, 0])
        light = LightSource([0, 0, -100], 'color', [1, 1, 1])
    
        insulin_pos = atom_pos["N"] + atom_pos["O"] 
        #these need to be removed because the used insulin (b chain) is from a sheep, for humans the last aa must be removed
        insulin_pos.remove(9997)
        insulin_pos.remove(9998)
        insulin_pos.remove(9999)
        insulin_pos.remove(10000)
        insulin_pos.remove(10001)
        insulin_pos.remove(10002)
    

        INSULIN_RECEPTOR = pdb.PDBMolecule(PATH_LINUX, center=False, offset=[-10, 8, -5])
        INSULIN_RECEPTOR.move_to([0,0,0])
        insulin = INSULIN_RECEPTOR.divide(insulin_pos, 'insulin')
        #insulin.move_to([-100,0,0])
        x = (30 * 0.1) - (0.1 * step)
        y = (30*2) - (2*step)
        insulin.move_offset([x, y, 0])
    

    if step > 30:
        camera = Camera('location', [0, 0, -200], 'look_at', [0, 0, 0])
        light = LightSource([0, 0, -100], 'color', [1, 1, 1])

        ins_id, atom_pos = get_ins(PATH_LINUX)
        alphact_stage_one = atom_pos["P"]
        alphact_stage_one_sliced = []
        INSULIN_RECEPTOR_noshow = pdb.PDBMolecule(PATH_LINUX, center=False, offset=[-10, 8, -5])
        for pos in alphact_stage_one:
            if pos in range(10014, 10211):
                alphact_stage_one_sliced.append(pos)
        alphact_stage_one_sliced_mol = INSULIN_RECEPTOR_noshow.divide(alphact_stage_one, 'alphact_one')
        alphact_stage_one_sliced_mol.move_to([-50,0,0])
        
        ins_id, atom_pos = get_ins("/homes/kdijkstra/thema2/pdb/4oga.pdb")
        alphact_stage_two = atom_pos["F"]
        site_one_complex = pdb.PDBMolecule("/homes/kdijkstra/thema2/pdb/4oga.pdb", center=False, offset=[-10, 8, -5])
        alphact_stage_two_mol = site_one_complex.divide(alphact_stage_two, "alphact_two")
        alphact_stage_two_mol.move_to([50,0,0])

        


    
    return Scene(camera,
                 objects=[light] + insulin.povray_molecule + INSULIN_RECEPTOR.povray_molecule  + alphact_stage_two_mol.povray_molecule)

    
def main(args):
    """ Main function performing the rendering """
    
    
    logger.info(" Total time: %d (frames: %d)", SETTINGS.Duration, eval(SETTINGS.NumberFrames))
    
    
    

    return 0


if __name__ == '__main__':
    #sys.exit(main(sys.argv))
    #pypovray.render_scene_to_png(frame)
    pypovray.render_scene_to_png(frame, 31)
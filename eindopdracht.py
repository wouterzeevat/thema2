#!/usr/bin/env python3

"""
Final assignment of theme 2
Animation visualising the process of insulin binding on it's receptor
    usage: python3 eindopdracht.py - <-- runs all frames
    usage: python3 eindopdracht.py <frame> <-- runs curtain frame
    usage: python3 eindopdracht.py <start_frame> <end_frame> <-- runs curtain part
"""

__author__ = "Keimpe Dijkstra, Wouter Zeevat"
__version__ = "2020.1"

import sys
import pydoc
from pypovray import pypovray, SETTINGS, models, pdb, logger
from vapory import Scene, Camera, LightSource, Finish, Pigment, Texture, Sphere, Cylinder, Text, LightSource
from read_pdb import get_ins


#global variables
PATH_PDB = "/homes/kdijkstra/thema2/pdb/6ce7.pdb" #change this to the path on your pc

INS_ID, ATOM_POS = get_ins(PATH_PDB)

INSULIN_ATOM = ATOM_POS["N"] + ATOM_POS["O"] 
INSULIN_ATOM = [pos for pos in INSULIN_ATOM if pos not in range(9997, 10003)] #remove because in difference between sheep and human insulin



def make_receptor(loc, size=5):
    """
    Creates the receptor and returns the object
    """
    rec_model = Texture(Pigment('color', [0, 1, 1], ), Finish('reflection', 0))

    x = loc[0]
    y = loc[1]
    z = loc[2]

    rec = list()
    rec.append(Cylinder([x - size * 1.2, y - size * 15, z], [x - size * 1.2, y + size*2, z], size, rec_model))
    rec.append(Cylinder([x + size * 1.2, y - size * 15, z], [x + size * 1.2, y + size*2, z], size, rec_model))
    rec.append(Cylinder([x - size * 1.2, y + size * 1.2, z], [x - size * 5, y + size * 4, z], size, rec_model))
    rec.append(Cylinder([x - size * 7.2, y + size * 4, z - size/2],
                        [x - size * 3.2, y + size * 4, z - size/2],
                        size / 1.321, rec_model))

    rec.append(Cylinder([x + size * 1.2, y + size * 1.2, z], [x + size * 5, y + size * 4, z], size, rec_model))
    rec.append(Cylinder([x + size * 7.2, y + size * 4, z - size/2],
                        [x + size * 3.2, y + size * 4, z - size/2],
                        size / 1.321, rec_model))

    rec.append(Sphere([x, y - size * 6, z], size * 3, rec_model))

    return rec


def make_membrane(loc, amount, size=5):
    """
    Create the membrane and returns the object
    """

    sphere_model = Texture(Pigment('color', [1, 0, 0], ), Finish('reflection', 0))
    cyl_model = Texture(Pigment('color', [0.7, 0.3, 0], ), Finish('reflection', 0))

    x_position = loc[0]
    y_position = loc[0] - size * 6
    objects = []
    for index in range(1, amount + 1):

        # Create top spheres
        objects.append(Sphere([x_position, loc[1], loc[2]], size, sphere_model))
        objects.append(Sphere([0 - x_position, loc[1], loc[2]], size, sphere_model))

        # Create top cylinders
        location = [x_position - size/3, loc[1], loc[2]], [x_position - size/3, loc[1] - size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [x_position + size/3, loc[1], loc[2]], [x_position + size/3, loc[1] - size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [0-x_position - size/3, loc[1], loc[2]], [0-x_position - size/3, loc[1] - size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [0-x_position + size/3, loc[1], loc[2]], [0-x_position + size/3, loc[1] - size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        # Create bottom spheres
        objects.append(Sphere([x_position, y_position, loc[2]], size, sphere_model))
        objects.append(Sphere([0 - x_position, y_position, loc[2]], size, sphere_model))

        # Create bottom cylinders
        location = [x_position - size/3, y_position, loc[2]], [x_position - size/3, y_position + size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [x_position + size/3, y_position, loc[2]], [x_position + size/3, y_position + size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [0-x_position - size/3, y_position, loc[2]], [0-x_position - size/3, y_position + size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        location = [0-x_position + size/3, y_position, loc[2]], [0-x_position + size/3, y_position + size*2.5, loc[2]]
        objects.append(Cylinder(location[0], location[1], size/6, cyl_model))

        x_position += size * 2

    return objects


def make_tyrine(loc, size):
    """
    Creates the tyrine molecules
    """
    text_model = Texture(Pigment('color', [1, 1, 0], ), Finish('reflection', 0))
    cyl_model = Texture(Pigment('color', [0, 1, 0.5], ), Finish('reflection', 0))

    tyr = []
    y_always = [13, 13, 10, 10]
    x_text = [-3, 5, -3, 5]
    x_end = [-5, 5, -5, 5]
    x = loc[0]
    y = loc[1]
    z = loc[2] + 7
    for _ in range(4):
        tyr.append(Cylinder([x, y-size * y_always[_], z], [x-size*x_end[_], y-size*y_always[_], z], size, cyl_model))
        text = Text('ttf', '"timrom.ttf"', '"{}"'.format(str('Tyr')), 2, [0, 0, 0], text_model, 'scale', 5, 'translate', [x-size*x_text[_], y-size*y_always[_], z - 7])
        tyr.append(text)
    return tyr


def bind_schematic(frame, size):

    """
    Animating the binding part schematicly
    """

    insuline_model = Texture(Pigment('color', [0, 1, 0.5], ), Finish('reflection', 0))
    text_model = Texture(Pigment('color', [1, 1, 0], ), Finish('reflection', 0))

    insuline = []
    s = size

    # frame 30 -> 120
    if frame < 120:
        x = (frame - 30) * (24.5*s / 90) - 30*s
        y = (frame - 30) * (-15*s / 90) + 20*s 
    else:
        x = -5*s
        y = 5*s

    insuline.append(Sphere([x, y, 0], s * 1.5, insuline_model))
    insuline.append(Text('ttf', '"timrom.ttf"', '"{}"'.format(str('Insulin')), 0.5, [0, 0, 0], text_model, 'scale', 5, 'translate', [x - s, y-0.5*s, -2*s]))

    insuline.append(Sphere([0-x, y, 0], s * 1.5, insuline_model))
    insuline.append(Text('ttf', '"timrom.ttf"', '"{}"'.format(str('Insulin')), 0.5, [0, 0, 0], text_model, 'scale', 5, 'translate', [0-x -1.4*s, y-0.5*s, -2*s]))

    return insuline


def move_camera(frame, frames, start, end, start_frame):
    """
    Animating the zooming into the binding process part
    """ 

    # Frame 120 -> 180
    x = (frame - start_frame) * ((end[0] - start[0]) / frames) + start[0]
    y = (frame - start_frame) * ((end[1] - start[1]) / frames) + start[1]
    z = (frame - start_frame) * ((end[2] - start[2]) / frames) + start[2]

    camera = Camera('location', [x, y, z], 'look_at', [x, y, z + 1])

    return camera


def bind_insuline_complete_ectodomain(frame):
    """
    Animating the insuline binding to the insulin receptor ectodomain part
    """

    light = LightSource([0, 0, -100], 'color', [1, 1, 1])
    INSULIN_RECEPTOR = pdb.PDBMolecule(PATH_PDB, center=False)
    INSULIN_RECEPTOR.move_to([0,0,0])
   
    insulin = INSULIN_RECEPTOR.divide(INSULIN_ATOM, 'insulin')
    y = 120 - ( 2 * (frame - 180) )
    insulin.move_offset([0, y, 0])
    
    return INSULIN_RECEPTOR, insulin, light
    

def insulin_bonded_to_ectodomain(frame):
    """
    Showing the complete ectodomain of the insulin receptor in complex with one insulin molecule
    """
    
    light = LightSource([0, 0, -100], 'color', [1, 1, 1])
    INSULIN_RECEPTOR = pdb.PDBMolecule(PATH_PDB, center=False)
    INSULIN_RECEPTOR.move_to([0,0,0])
    
    return INSULIN_RECEPTOR, light


def slice_alphact():
    alphact = ATOM_POS["P"]
    alphact_stage_one_sliced = []
    alphact_stage_two_sliced = []
    
    #deze moeten nog naar list comprhensions geschreven worden 
    for pos in alphact:
            if pos in range(10014, 10171):
                alphact_stage_one_sliced.append(pos)
            if pos in range(10115, 10211):
                alphact_stage_two_sliced.append(pos)
    
    return alphact_stage_one_sliced, alphact_stage_two_sliced


def alphact_conformational_change(frame, alphact_stage_one_sliced, alphact_stage_two_sliced):
    INSULIN_RECEPTOR = pdb.PDBMolecule(PATH_PDB, center=False)
    INSULIN_RECEPTOR.move_to([0,0,0])
    frame_start = 300
    
    #FIX
    for num in range(10014, 10115):
        if num < (frame - frame_start) * round(101/90) + 10014:
            if num not in alphact_stage_two_sliced:
                alphact_stage_one_sliced.remove(num)
    for num in range(10171, 10211):
        if num < (frame - frame_start) * round(40/90) + 10171:
            alphact_stage_one_sliced.append(num)

    alphact_stage_one_sliced_mol = INSULIN_RECEPTOR.divide(alphact_stage_one_sliced, 'alphact_one')
    rotation = (frame - frame_start - 90) * -0.01
    alphact_stage_one_sliced_mol.rotate([0,0,1], rotation)
                
    insulin_alpha = INSULIN_RECEPTOR.divide(ATOM_POS["N"], "alphact_two")
    insulin_alpha.move_offset([0,30,0])
                
    return alphact_stage_one_sliced_mol, insulin_alpha
        

def alphains_binding_alphact(frame, alphact_stage_two_sliced): #FIX
    INSULIN_RECEPTOR = pdb.PDBMolecule(PATH_PDB, center=False)
    INSULIN_RECEPTOR.move_to([0,0,0])
    alphact_stage_two_sliced_mol = INSULIN_RECEPTOR.divide(alphact_stage_two_sliced, 'alphact_two')
    insulin_alpha = INSULIN_RECEPTOR.divide(ATOM_POS["N"], "insulin_alpha")
    frame_start = 330

    insulin_offset = (60 - frame - frame_start + 1) / 2
    insulin_alpha.move_offset([0,insulin_offset,0])

    return alphact_stage_two_sliced_mol, insulin_alpha


def alphains_bonded_to_alphact(frame, alphact_stage_two_sliced):
    INSULIN_RECEPTOR = pdb.PDBMolecule(PATH_PDB, center=False)
    INSULIN_RECEPTOR.move_to([0,0,0])
    alphact_complex_insulinalpha_pos = alphact_stage_two_sliced + ATOM_POS["N"]
    alphact_complex_insulinalpha_mol = INSULIN_RECEPTOR.divide(alphact_complex_insulinalpha_pos, 'alphact_complex_insulinalpha')

    return alphact_complex_insulinalpha_mol


def bind_phosphorus(frame, size):
    """
    Animating the process of phosfor binding to the Tyr
    """

    phosphorus_model = Texture(Pigment('color', [1, 0, 1], ), Finish('reflection', 0))
    text_model = Texture(Pigment('color', [1, 1, 0], ), Finish('reflection', 0))

    phosphorus = []
    s = size

    # frame 390 -> 480
    x_locs = [[-20, -5], [20, 5], [-20, -5], [20, 5]]
    y_locs = [13, 13, 10, 10]

    for _ in range(4):
        if frame < 480:
            x = (frame - 390) * ((x_locs[_][1]*s - x_locs[_][0]*s) / 90) + x_locs[_][0]*s
            y = 0 - y_locs[_] * s
        else:
            x = x_locs[_][1]*s
            y = y_locs[_]*s
        phosphorus.append(Sphere([x, y, 2], s * 1.2, phosphorus_model))
        phosphorus.append(Text('ttf', '"timrom.ttf"', '"{}"'.format(str('P')), 0.5, [0, 0, 0], text_model, 'scale', 7, 'translate', [x - 0.2*s, y-0.5*s, -1.5*s]))
    
    return phosphorus


def bind_IRS(frame):
    """
    Animating the process of IRS binding to the phosfor
    """
    return


def activation(frame):
    """
    Visualizing the cell activation
    """
    return


def frame(step):
    """ Returns the scene at step number (1 step per frame) """

    camera = Camera('location', [0, 7, -200], 'look_at', [0, 0, 0])
    lights = [LightSource([0, -10, -60], 0.5),
              LightSource([0, -50, -60], 0.5),
              ]

    receptor = make_receptor([0, 0, -2], 5)
    membrane = make_membrane([0, 0, 0], 10, 5)
    tyrine = make_tyrine([0, 0, -2], 5)
    alphact_stage_one_sliced, alphact_stage_two_sliced = slice_alphact()

    seconds = step / 30
    if seconds < 1:  # Frame 0 -> 30
        return Scene(camera,
                objects=[models.default_light] + tyrine + membrane + receptor + tyrine + lights)

    elif seconds < 4:  # Frame 30 -> 120
        insuline_schematic = bind_schematic(step, 5)
        return Scene(camera,
                 objects=[models.default_light] + tyrine + membrane + receptor + tyrine + lights + insuline_schematic)

    elif seconds < 6:  # Frame 120 -> 180
        insuline_schematic = bind_schematic(step, 5)
        camera = move_camera(step, 60, [0, 7, -200], [-20, 20, 3], 120)
        return Scene(camera,
                 objects=[models.default_light] + tyrine + membrane + receptor + tyrine + lights + insuline_schematic)

    elif seconds < 8:  # Frame 180 -> 240
        camera = Camera('location', [0, 0, -300], 'look_at', [0, 0, 0])
        INSULIN_RECEPTOR, insulin, light = bind_insuline_complete_ectodomain(step)
        return Scene(camera,
                 objects=[light] + INSULIN_RECEPTOR.povray_molecule + insulin.povray_molecule)

    elif seconds < 10: # Frame 240 -> 300
        camera = Camera('location', [0, 0, -300], 'look_at', [0, 0, 0])
        INSULIN_RECEPTOR, light = insulin_bonded_to_ectodomain(step)
        return Scene(camera,
                 objects=[light] + INSULIN_RECEPTOR.povray_molecule)
    
    elif seconds < 11: 
        camera = Camera('location', [0, 0, -300], 'look_at', [0, 0, 0])
        light = LightSource([0, 0, -100], 'color', [1, 1, 1])
        alphact_stage_one_sliced_mol, insulin_alpha = alphact_conformational_change(step, alphact_stage_one_sliced, alphact_stage_two_sliced)
        return Scene(camera,
                 objects=[light] + alphact_stage_one_sliced_mol.povray_molecule + insulin_alpha.povray_molecule )

    elif seconds < 13:
        camera = Camera('location', [0, 0, -300], 'look_at', [0, 0, 0])
        light = LightSource([0, 0, -100], 'color', [1, 1, 1])
        alphact_stage_two_sliced_mol, insulin_alpha = alphains_binding_alphact(step, alphact_stage_two_sliced)
        return Scene(camera,
                 objects=[light] + alphact_stage_two_sliced_mol.povray_molecule + insulin_alpha.povray_molecule )
  
    elif seconds < 14:
        camera = Camera('location', [0, 0, -300], 'look_at', [0, 0, 0])
        light = LightSource([0, 0, -100], 'color', [1, 1, 1])
        alphact_complex_insulinalpha_mol = alphains_bonded_to_alphact(step, alphact_stage_two_sliced)
        return Scene(camera,
                 objects=[light] + alphact_complex_insulinalpha_mol.povray_molecule )

'''
    elif seconds < 13:  # Frame 330 -> 390
        if seconds < 11.7:  # Frame 330 -> 351
            camera = move_camera(step, 21, [0, 0, -300], [0, 0, 3], 330)
            INSULIN_RECEPTOR, light = insulin_bonded_to_ectodomain(step)
            return Scene(camera,
                 objects=[light] + INSULIN_RECEPTOR.povray_molecule)

        else:  # Frame 351 -> 390
            camera = move_camera(step, 39, [0, 0, 3], [0, 7, -200], 351)
            insuline_schematic = bind_schematic(step, 5)
            return Scene(camera,
                 objects=[models.default_light] + tyrine + membrane + receptor + tyrine + lights + insuline_schematic)
    
    elif seconds < 16:  # Frame 390 -> 480
            insuline_schematic = bind_schematic(step, 5)
            phosphorus = bind_phosphorus(step, 5)
            return Scene(camera,
                 objects=[models.default_light] + tyrine + membrane + receptor + tyrine + lights + insuline_schematic + phosphorus)

    return Scene(camera,
        objects=[models.default_light] + tyrine + membrane + receptor + tyrine + lights)
'''

def main(args):
    """ Main function performing the rendering """

    # Checks how to run animation depending on given arguments
    if len(args) < 2:
        pydoc.help(__name__)
    elif len(args) < 3:
        if args[1] == "-":
            pypovray.render_scene_to_mp4(frame)
        else:
            pypovray.render_scene_to_png(frame, int(args[1]))
    elif len(args) < 4:
        pypovray.render_scene_to_mp4(frame, range(int(args[1]), int(args[2]) + 1))
    else:
        pydoc.help(__name__)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

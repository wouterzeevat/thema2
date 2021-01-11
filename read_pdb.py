#!/usr/bin/env python3

"""
Extracts the various atom positions of the molecules in a pdb-file
"""


__author__ = "keimpe dijkstra"


import sys


PATH = "..\\thema2\\pdb\\6ce7.pdb"


def get_ins(PATH):
    """
    Loops through a given pdb-file and extracts atom positions per molecule
    """
    ins_id = [] #will contain the letters corresponding to the molecule 
    atom_pos = {} #will contain the molecules with their atom positions
    file_name = open(PATH) #open the pdb-file 
    for line in file_name:
        if line.startswith("DBREF"):
            if line[12:15].strip() not in ins_id:
                #check for molecules, if there is a new one add them to ins_id
                ins_id += line[12:15].strip()
        elif line.startswith("ATOM") and line[21:23].strip() in ins_id:
            if line[21:23].strip() in atom_pos:
                #add a atom position to a existing molecule
                atom_pos[line[21:23].strip()].append(int(line[6:12].strip()))
            else:
                #make a new molecule and store the atom position in it
                atom_pos[line[21:23].strip()] = [int(line[6:12].strip())]
    file_name.close()
    return ins_id, atom_pos

        
def main(args):
    ins_id, atom_pos = get_ins(PATH)
    return 0

if __name__ == "__main__":
    exitcode = main(sys.argv)
    sys.exit(exitcode)



#!/usr/bin/env python3


"""
Extracts the various atom positions of the molecules in the 6ce7.pd file 
"""


__author__ = "keimpe dijkstra"


import sys

PATH = "..\\thema2\\pdb\\6ce7.pdb"


def get_ins(PATH):
    ins_id = []
    atom_pos = {}
    file_name = open(PATH)
    for line in file_name:
        if line.startswith("DBREF"):
            if line[12:15].strip() not in ins_id:
                ins_id += line[12:15].strip()
        elif line.startswith("ATOM") and line[21:23].strip() in ins_id:
            if line[21:23].strip() in atom_pos:
                atom_pos[line[21:23].strip()].append(int(line[6:12].strip()))
            else:
                atom_pos[line[21:23].strip()] = [int(line[6:12].strip())]
    file_name.close()
    return ins_id, atom_pos

        
def main(args):
    ins_id, atom_pos = get_ins(PATH)
    print(ins_id)
    INSULIN_ATOM = atom_pos["N"] + atom_pos["O"] 
    INSULIN_ATOM = [pos for pos in INSULIN_ATOM if pos not in range(9997, 10003)]
    print(INSULIN_ATOM)
    return 0


if __name__ == "__main__":
    exitcode = main(sys.argv)
    sys.exit(exitcode)



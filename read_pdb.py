#!/usr/bin/env python3


"""
description of the program
"""


__author__ = "my name"


import sys

def get_ins(file_name):
    ins_id = []
    atom_pos = {}
    for line in file_name:
        if line.startswith("DBREF") and line[42:53].strip() == "INS_HUMAN":
            if line[12:15].strip() not in ins_id:
                ins_id += line[12:15].strip()
        elif line.startswith("ATOM") and line[21:23].strip() in ins_id:
            if line[21:23].strip() in atom_pos:
                atom_pos[line[21:23].strip()].append(line[6:12].strip())
            else:
                atom_pos[line[21:23].strip()] = [line[6:12].strip()]
    return ins_id, atom_pos

        
def main(args):
    path = "..\\thema2\\pdb\\6sof.pdb"
    file_name = open(path)
    ins_id, atom_pos = get_ins(file_name)
    return 0


if __name__ == "__main__":
    exitcode = main(sys.argv)
    sys.exit(exitcode)



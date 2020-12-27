def create_ethanol():
    from pypovray import pypovray, SETTINGS, models, logger, pdb
    from vapory import Sphere, Scene, LightSource, Camera
    path = "/homes/kdijkstra/thema2/pdb/ethanol.pdb"
    ethanol = pdb.PDBMolecule(path, center=False, offset=[-10, 8, -5])
    return ethanol
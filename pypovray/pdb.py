"""
Module for creating and managing Povray molecules originating from
a PDB file.
"""

import math
import numpy as np
from vapory.vapory import Sphere, Cylinder, Text, Pigment, Texture, Finish, Intersection
from pypovray import SETTINGS, logger
from pypovray.models import atom_colors, atom_sizes, text_model
from scipy.linalg import expm, norm


class PDBMolecule(object):
    """ Models a molecule for rendering using Povray given a PDB file """

    def __init__(self, pdb_file, center=True, offset=[0, 0, 0], atoms=False, model=None):
        """ Parses and renders the molecule given a PDB file """

        # If a list of atoms is provided, use these instead of a PDB file
        # This allows dividing the molecule in segments, see divide()
        if atoms:
            self.atoms = atoms
        else:
            self._parse_pdb(pdb_file)
            self.povray_molecule = []

        # Molecule name
        self.molecule = pdb_file
        self.warnings = set()
        # If an offset is provided, apply this
        self.offset = np.array(offset)
        if np.count_nonzero(self.offset) > 0:
            self._recenter_molecule()
        self.center = self._center_of_mass()

        # Center the molecule based on the 'pseudo' center of mass
        if center:
            self.center_molecule()
            self.center = self._center_of_mass()
        logger.info("Created a molecule from '%s' placed at [%s] (centered is %d)",
                    pdb_file, ', '.join([str(coord) for coord in np.around(self.center, 2)]), center)

        # Required for the labels
        self.show_name = False
        self.show_index = False
        self.camera = None

        self.model = model
        self.render_molecule(offset)

    def _parse_pdb(self, fname):
        """ Read in a PDB file and create an atom object for each ATOM definition """
        self.atoms = []
        with open(fname) as pdbfile:
            for line in pdbfile:
                if line.startswith('ATOM') | line.startswith('HETATM'):
                    self.atoms.append(PDBAtom(line))
                elif line.startswith('CONECT'):
                    # Splicing the CONNECTS like this keeps the code compact but
                    # it limits the amount of atoms to be in the thousands.
                    atom_serial = int(line[7:11].strip()) - 1
                    atom_bonds = [int(bond)-1 for bond in line[12:].split()]
                    self.atoms[atom_serial].bonds = atom_bonds

    def _recenter_molecule(self):
        """ Moves the molecule by a given offset when instantiating the object """
        for atom in self.atoms:
            atom.x += self.offset[0]
            atom.y += self.offset[1]
            atom.z += self.offset[2]

    def _get_atom(self, element, offset):
        """ Creates a Povray Sphere object representing an atom """
        if element.element not in atom_colors:
            self.warnings.add(element.element)

        if self.model:
            atom_model = self.model
        else:
            atom_model = Texture(Pigment('color', atom_colors.get(element.element, [0, 1, 1])),
                                 Finish('phong', 0.9, 'reflection', 0.1))
        return Sphere([element.x + offset[0], element.y + offset[1], element.z + offset[2]],
                      atom_sizes.get(element.element, 0.5), atom_model)

    def render_molecule(self, offset=[0, 0, 0]):
        """ Renders a molecule given a list with atoms """
        if self.show_name:
            self.show_label(camera=self.camera, name=True)
        if self.show_index:
            self.show_label(camera=self.camera, name=False)
        self.povray_molecule = [self._get_atom(a, offset) for a in self.atoms]

        # Warn if unknown atoms are found
        if len(self.warnings) > 0:
            if any(element == '' for element in self.warnings):
                logger.warning("The PDB file is missing atom names!")
            else:
                logger.warning("The following atoms are not defined in the 'models' module: %s",
                               ", ".join(self.warnings))

            self.warnings = set()

    def _update_render(self, offset=[0, 0, 0]):
        """ Updates the render without re-applying the labels """
        self.povray_molecule = [self._get_atom(a, offset) for a in self.atoms]

    def _center_of_mass(self):
        """ Calculates the 'center of mass' for the molecule
        Note: assumes equal weights, not the true center of mass """
        x, y, z = 0, 0, 0
        for atom in self.atoms:
            x += atom.x
            y += atom.y
            z += atom.z
        return np.array([x/len(self.atoms), y/len(self.atoms), z/len(self.atoms)])

    def center_molecule(self):
        """ Centers the molecule by subtracting the calculated COM value """
        curr_center = self._center_of_mass()
        for atom in self.atoms:
            atom.x -= curr_center[0]
            atom.y -= curr_center[1]
            atom.z -= curr_center[2]

    def set_model(self, model):
        """ Set render specific options for the atoms (i.e. reflection) """
        self.model = model

    def move_offset(self, v):
        """ Move the molecule - and thus each individual atom - on the given axes by vector v """
        for atom in self.atoms:
            atom.x += v[0]
            atom.y += v[1]
            atom.z += v[2]

        # Calculate the new center of mass
        self.center = self._center_of_mass()

        # Regenerate the molecule
        self.render_molecule()

    def move_to(self, pos):
        """ Move the center of the molecule to the position pos """
        offset = np.array(pos) - self.center

        # Move each atom
        for atom in self.atoms:
            atom.x += offset[0]
            atom.y += offset[1]
            atom.z += offset[2]

        # Calculate the new center of mass
        self.center += offset

        # Regenerate the molecule
        self.render_molecule()

    def rotate(self, axis, theta):
        """ Rotates the molecule around a given axis with angle theta (radians) """
        for atom in self.atoms:
            # subtract center
            coords = np.array([atom.x, atom.y, atom.z]) - self.center
            rcoords = np.array(self._calc_rotate(axis, theta, coords))
            # update coordinates
            atom.x, atom.y, atom.z = rcoords + self.center
        # Regenerate the molecule
        self.render_molecule()

    def rotate_by_step(self, axis, theta, step, time=False):
        """ Rotates the molecule around a given axis with angle theta (radians)
            but always resets the molecule to its original rotation first which
            makes it usable in a multi-threaded environment. """

        # If step is in seconds, divide by the FrameTime to get the integer (actual) step
        if time:
            step = int(step/eval(SETTINGS.FrameTime))

        for atom in self.atoms:
            # subtract center
            coords = np.array([atom.x, atom.y, atom.z]) - self.center

            # Reset the coordinates 
            reset = np.array(self._calc_rotate(axis, -(theta*(step)), coords))
            atom.x, atom.y, atom.z = reset

            # Calculate rotation coordinates
            rcoords = np.array(self._calc_rotate(axis, theta*(step+1), coords))

            # update coordinates
            atom.x, atom.y, atom.z = rcoords + self.center

        # Regenerate the molecule
        self.render_molecule()

    def scale_atom_distance(self, scale):
        """ Scales all atom distances using the given scale parameter """
        for atom in self.atoms:
            coordinates = np.array([atom.x, atom.y, atom.z])
            coordinates *= scale
            
            # Set the atom's new coordinates
            atom.x = coordinates[0]
            atom.y = coordinates[1]
            atom.z = coordinates[2]

        # Update the rendering
        self._update_render()

    def show_label(self, camera, name=False):
        """ Shows a label of each atom in the list of atoms by printing either
            its index or atom name on the 'front' of the atom. The position
            of the label depends on the camera position; it always faces the
            camera so that it's readable. """
        # Storing all label Povray objects
        labels = []
        # Get the coordinates of the camera
        # TODO: does not work for all camera's!
        camera_coords = np.array(camera.args[1])

        for i, atom in enumerate(self.atoms):
            # Default atom size (for undefined atoms) is 0.5
            atom_radius = atom_sizes.get(atom.element, 0.5)
            if name:
                label = atom.element
                letter_offset = np.array([0.15 * len(label), 0.13 * len(label), 0.0])
                self.show_name = True
            else:
                label = i
                ndigits = len(str(abs(label)))
                letter_offset = np.array([0.15 * ndigits, 0.13 * ndigits, 0.0])
                self.show_index = True
            self.camera = camera

            # Defining the two vectors; Atom center (A) and camera viewpoint (B)
            A = np.array([atom.x, atom.y, atom.z])
            B = np.array(camera_coords)
            BA = B - A  # Vector B->A
            d = math.sqrt(sum(np.power(BA, 2)))  # Euclidean distance between the vectors
            BA = BA / d  # Normalize by its length; BA / ||BA||
            # Here we find a point on the vector B->A with a distance of 'scale' from the
            # atom center towards the camera (outside of the atom).
            scale = atom_radius * 1.2
            N = A + scale * BA # Scale and add to A

            # Now that we have the distance, we calculate the angles facing the camera
            x1, y1, z1 = A
            x2, y2, z2 = B
            y_angle = math.degrees(math.atan2(x1 - x2, z1 - z2))
            x_angle = math.degrees(math.atan2(y1 - y2, z1 - z2))

            # Correct for the letter size since text is never centered and place
            # the text in front of the atom to make it visible (emboss)
            N -= letter_offset
            emboss = -0.15

            # 'rotate' rotates the text to the camera and 'translate' positions the text
            # on the vector originating from the camera viewpoint to the atom center.
            # The scaling parameter scales (reduces) the text size
            text = Text('ttf', '"timrom.ttf"', '"{}"'.format(str(label)), 1, 0,
                        'scale', [0.35, 0.35, 0.35], text_model,
                        'rotate', [-x_angle, y_angle, 0], 'translate', N)

            # Create a sphere with the same position and dimensions as the atom
            sphere = Sphere(A, atom_radius, text_model)
            # Add the intersection of this sphere and the text to the labels
            labels.append(Intersection(sphere, text, 'translate', [0, 0, emboss]))

        # Update the rendering
        self._update_render()
        # Add the labels to atoms
        self.povray_molecule += labels

    def show_stick_model(self, scale=1):
        """Turns the space filling model into a stick and ball model.
           The scaling function is used to create distance between atoms
           which creates the opportunity to place cylinders between atoms.
           TODO's: see issue reported at:
           https://bitbucket.org/mkempenaar/pypovray/issues/9/pdb-rendering-ball-and-stick-model-todos
           """
        # Declaring storage for all cylinders
        sticks = []
        # Scale the atom distance using the default (or given) scaling number
        self.scale_atom_distance(scale)

        for serial, atom in enumerate(self.atoms):
            # Declare a model that follows the atom's styling guidelines
            stick_model_a = Texture(Pigment('color', atom_colors.get(atom.element, [0, 1, 1])),
                                    Finish('phong', 0.3, 'reflection', 0.1))
            # Iterate through all the atom's bonds
            for bond in atom.bonds:
                # In PDB files bonds are displayed twice. Once so A connects to B
                # and once so B connects to A. Since we only need one cylinder
                # this simple if-statement prevents overlapping cylinders.
                if bond > serial:
                    bond_atom = self.atoms[bond]
                    # Declare a model that follows the bonded atom's styling guidelines
                    stick_model_b = Texture(Pigment('color', atom_colors.get(bond_atom.element, [0, 1, 1])),
                                    Finish('phong', 0.3, 'reflection', 0.1))

                    # Declare a vector to place the cylinder on
                    A = np.array([atom.x, atom.y, atom.z])
                    B = np.array([bond_atom.x, bond_atom.y, bond_atom.z])
                    # Declare the midwaypoint so we can use bi-colored cylinders*
                    midpoint = (A + B) / 2

                    stick_a = Cylinder(A, midpoint, scale / 3, stick_model_a)
                    stick_b = Cylinder(midpoint, B, scale / 3, stick_model_b)
                    sticks.extend((stick_a, stick_b))

        # Update the rendering
        self._update_render()
        # Add sticks to the atoms
        self.povray_molecule += sticks

    def divide(self, atoms, name, offset=[0, 0, 0]):
        """ Given a list of atom indices, split the current molecule into two molecules
            where the original one is reduced and a new one is built with the defined
            atoms """
        molecule = [self.atoms[i] for i in atoms]

        # Remove atoms from self
        for index in sorted(atoms, reverse=True):
            del self.atoms[index]

        # Regenerate the reduced molecule
        self.render_molecule()

        # Return a new PDBMolecule
        return PDBMolecule(name, center=False, offset=offset, atoms=molecule)

    def _calc_rotate(self, axis, theta, v):
        """ Calculates the new coordinates for a rotation
            axis:  vector, axis to rotate around
            theta: rotation in radians
            v:     vector, original object coordinates
        """
        # Compute the matrix exponential using Taylor series
        M0 = expm(np.cross(np.eye(3), axis/norm(axis)*theta))
        # Multiply the rotation matrix with the vector v
        return np.dot(M0, v)

    def __repr__(self):
        pass

    def __str__(self):
        """ Provides an overview of the molecule
            For each atom the index in the self.atoms list, its name and
            current coordinates are shown. """
        curr_center = np.around(self._center_of_mass(), 2)
        header = ('\nOverview for the molecule read from {}\n'.format(self.molecule) +
                  '=' * 54 + '\nIdx\t\tAtom\t\tx\ty\tz\n')
        footer = ('=' * 54 +
                  '\nMolecule is currently centered at {}'.format(curr_center))

        structure = []
        for idx, atm in enumerate(self.atoms):
            structure.append('{}:\t\t{}\t\t{}\t{}\t{}\t'.format(idx, atm.name,
                                                                format(atm.x, '.2f'),
                                                                format(atm.y, '.2f'),
                                                                format(atm.z, '.2f')))
        return '{}{}\n{}\n'.format(header, '\n'.join(structure), footer)


class PDBAtom(object):
    ''' Simple class to parse a single ATOM to retrieve x, y and z coordinates'''
    def __init__(self, string):
        #this is what we need to parse
        #ATOM      1  CA  ORN     1       4.935   1.171   7.983  1.00  0.00      sega
        #XPLOR pdb files do not fully agree with the PDB conventions 
        self.name = string[12:17].strip()
        #self.name = ''.join(re.findall('[0-9]*([A-Za-z]+)[0-9]*', name))
        self.x = float(string[30:38].strip())
        self.y = float(string[38:46].strip())
        self.z = float(string[46:54].strip())
        self.warnings = []
        if len(string) < 78:
            self.element = string[12:16].strip()
            self.warnings.append('Chemical element name guessed ' +\
                                 'to be "%s" from atom name "%s"' % (self.element, self.name))
        else:
            self.element = string[76:78].strip()
        # List of bonded atoms
        self.bonds = []

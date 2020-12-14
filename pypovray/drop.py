import math
import numpy as np

class Droplet:
    def __init__(self, radius, height, gamma, size=10):

        # __________     _w__________ 0
        #           \   /
        #            | |  B
        #           /   p
        #          |  A  |            h
        #           \___/
        #

        self.radius = float(radius)
        self.height = float(height)
        self.gamma = float(gamma)
        self.size = float(size)

        # Normalize values to match droplet sphere of radius 1
        r = self.gamma/self.radius
        h = self.height/self.radius

        # Find the point on the droplet sphere where the
        # bending sphere touches
        # The z-coordinate is the sine
        z = (h-r)/(1+r)
        # ... the x-coordinate the cosine,
        # and x**2 + z**2 equals 1 (unit sphere)
        x = np.sqrt(1 - z**2)
        self.p = np.array((x, z))
        # The center of the other circle lies in the
        # same direction, but separated by both radii
        # (the circles touch, right)
        self.B = self.p*(self.radius + self.gamma)
        self.p[1] -= height
        self.B[1] -= height

        # Angle of the half circle that is not drawn
        self.alpha = np.arctan2(x, z)
        if np.isnan(self.alpha):
            self.alpha = 0
        # Angle of the circle that is drawn
        # (needed for drawing the circle)
        self.beta = np.pi - self.alpha

        # x coordinate of point from which line runs straight
        self.w = self.B[0] if (-1 <= z <= 1) else 0

        # Lengths of line parts
        if z < -1:
            # The circle is above the line
            self.arclen1 = self.arclen2 = 0
            self.linelen = self.size
        elif z > 1:
            # The circle is fully immersed,
            # detached from the surface
            # (a circle with radius gamma fits between them)
            self.arclen1 = np.pi*radius
            self.arclen2 = 0
            self.linelen = size
        else:
            # The circle is protruding the surface,
            # and is connected.
            self.arclen1 = (np.pi - self.alpha)*self.radius
            self.arclen2 = (np.pi - self.alpha)*self.gamma
            if z > 0 and self.B[0] < gamma:
                self.arclen2 -= 2*np.arccos(self.B[0]/self.gamma)*self.gamma
            self.linelen = self.size - self.w

        return

def droplet(radius, height, gamma, size=10, shift=0, offset=[0, 0, 0], apl=0.5, tag=""):
    """Draw a line of a droplet on/in a membrane"""

    drop = Droplet(radius, height+shift, gamma, size)

    alpha = drop.alpha
    (x, z) = drop.p
    c = drop.B
    a = drop.p

    w = size - drop.linelen

    lipids = []
    total = drop.linelen + drop.arclen1 + drop.arclen2
    dots = int(total / apl)
    apl = total / dots

    linedots = int(drop.linelen / apl)
    line  = w+(np.arange(linedots) + 0.5)*apl
    lipids += [u for i in line for u in [i, 0, shift, math.degrees(np.pi),
                                         -i, 0, shift, -(math.degrees(-np.pi))]]

    # Circle B (sides)
    if drop.arclen2:
        arc2dots = int(drop.beta * drop.gamma / apl + 0.5)
        if arc2dots:
            angle2 = drop.beta / arc2dots
            arc2 = 0.5*np.pi+(np.arange(arc2dots)+0.5)*angle2
            arc2x = np.cos(arc2)*drop.gamma + c[0]
            arc2z = np.sin(arc2)*drop.gamma + c[1] + shift
            mask = arc2x >= 0
            l = [u for i, j in zip(arc2x[mask,], arc2z[mask,])
                 for u in [i, 0, j, math.degrees(math.atan2(c[1]-j, c[0]-i)) + 90,
                           -i, 0, j, -(math.degrees(math.atan2(c[1]-j, c[0]-i)) + 90)]]
            lipids += l

    # Main circle ('drop')
    if drop.arclen1:
        arc1dots = int(drop.arclen1 / apl + 0.5)
        if arc1dots:
            angle1 = drop.beta / arc1dots
            arc1 = -0.5*np.pi+(np.arange(arc1dots)+0.5)*angle1
            arc1x = np.cos(arc1) * drop.radius
            arc1z = np.sin(arc1) * drop.radius - height
            l = [u for i, j in zip(arc1x,arc1z)
                 for u in [i, 0, j, math.degrees(math.atan2(a[1]-j, -i)) + 90,
                           -i, 0, j, -(math.degrees(math.atan2(a[1]-j, -i)) + 90)]]
            lipids += l

    ''' Circles (B and p) center points
    lipids += [c[0], 0, c[1] + shift, 0]
    lipids += [-c[0], 0, c[1] + shift, 0]
    lipids += [a[0], 0, a[1] + shift, 0]
    '''

    # Return the coordinates for all points in the line
    coordinates = []
    for l in chunks(lipids, 4):
        # Coordinates
        coordinates.append([l[0] + offset[0], l[2] + offset[1], l[1] + offset[2], l[3]])
    return coordinates

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def membrane(step, radius, gamma, start, stop, nframes, offset, size, apl):
    """ Creates a list of coordinates for a membrane involved in pinocytosis """
    start = float(start)
    stop = float(stop)
    delta = stop - start
    stepsize = abs(delta / float(nframes))
    nsteps = abs(int(delta/stepsize))
    s = delta / nsteps
    x = -start-step*s
    coordinates = droplet(radius, x, gamma, offset=offset, size=size, apl=apl)
    return coordinates

// ===================================================================
// "String" of torus segments ~~~~~~
// Copyright 2000 by Tor Olav Kristensen.
// ===================================================================

#version 3.1;
#include "colors.inc"

// ===================================================================

#declare Origo = <0, 0, 0>;
#declare Nullv = <0, 0, 0>;
#declare Unitv = <1, 1, 1>;

// ===================================================================
// Just some of my macros

#macro vCos(UU, VV)
// Returns cosinus of the angle between two vectors

  (vdot(UU, VV)/(vlength(UU)*vlength(VV)))

#end // macro vCos


#macro vangle(UU, VV)
// Returns the angle in radians between two vectors
// 0 <= angle < pi/2

  acos(vCos(UU, VV))

#end // macro vangle


#macro VectorAngles(Vector)
// Returnes two angles.
// The first is the angle between Vector and the Y-axis
// The second is the angle between the projection
// of Vector to the XZ-plane and the X-axis

  #local VAngles = Nullv;
  #if (vlength(Vector) > 0)
    #local VAngles = y*vangle(Vector, y);
    #if (VAngles.y > 0)
      #local tmp = vangle(<Vector.x, 0, Vector.z>, x);
      #if (Vector.z < 0)
        #local tmp = -tmp;
      #end
      #local VAngles = VAngles + tmp*x;
    #end
  #end // if

  VAngles

#end // macro VectorAngles


#macro vtilt(Thing, TiltVector)
// Returns the object Thing "tilted" in the direction of
// TiltVector

  #local RotateAngles = VectorAngles(TiltVector);

  object {
    Thing
    rotate  degrees(RotateAngles.x)*y
    rotate -degrees(RotateAngles.y)*z
    rotate -degrees(RotateAngles.x)*y
  }

#end // macro vtilt


#macro TorusSegment(Centerpoint, Point1, Point2, SmallRadius)
// A segment of a torus that has Centerpoint as its
// center is returned.
// The torus is cut off by two planes:
// Both these planes are perpendicular to the plane
// that Centerpoint, Point1 and Point2 are in.
// The plane that Centerpoint, Point1 and Point2 lies
// in has the normal vector: VectorUp

// Point1 and the following two direction vectors
// describes the  first plane: VectorUp and Vector1

// Point2 and the following two direction vectors
// describes the second plane: VectorUp and Vector2

  #local Vector1 = Point1-Centerpoint;
  #local Vector2 = Centerpoint-Point2;
  #local VectorUp = vcross(Vector2, Vector1);
  #local BigRadius = vlength(Vector1); // or Vector2

  intersection {
    vtilt(torus { BigRadius, SmallRadius }, VectorUp)
    plane { vcross(Vector1, VectorUp), 0 }
    plane { vcross(Vector2, VectorUp), 0 }
    translate Centerpoint
  }

#end // macro TorusSegment

// ===================================================================
// Here the fun starts

#declare V1 = <2, 3, -1>;
#declare V2 = vlength(V1)*vnormalize(<4, 7, 9>);

#declare CPt1 = Origo-4*V2+2*V1; // Center of 1. torus segment
#declare Pt11 = CPt1 + V1*2;     // Start of 1. torus segment
#declare Pt12 = CPt1 + V2*2;     // End of 1. torus segment

#declare Pt21 = Pt12;            // Start of 2. torus segment
#declare CPt2 = Pt21+V2/3;       // Center of 2. torus segment
#declare Pt22 = CPt2-V1/3;       // End of 2. torus segment

#declare Pt31 = Pt22;            // Start of 3. torus segment
#declare CPt3 = Pt31-V1/3*2;       // Center of 3. torus segment
#declare Pt32 = CPt3+V2/3*2;       // End of 3. torus segment

#declare Pt41 = Pt32;            // Start of 4. torus segment
#declare CPt4 = Pt41+V2;         // Center of 4. torus segment
#declare Pt42 = CPt4-V1;         // End of 4. torus segment

/*
#declare V3 = vcross(V1, V2);
#declare V4 = vcross(V2, V3);
#declare V5 = V3-V2/2;
#declare V6 = V4-4*V3;

#declare R = 2;
#declare Pt51 = Pt32;                  // Start of 5. torus segment
#declare CPt5 = Pt51+R*vnormalize(V5); // Center of 5. torus segment
#declare Pt52 = CPt5-R*vnormalize(V6); // End of 5. torus segment
*/

// ===================================================================
// And then we visualize it all

#declare sr = 0.5; // sphere radius
#declare cr = 0.2; // cylinder radius
#declare tr = 0.4; // torus radius

union {
  sphere { Pt11, sr }
  sphere { Pt12, sr }
  sphere { Pt21, sr }
  sphere { Pt22, sr }
  sphere { Pt31, sr }
  sphere { Pt32, sr }
  sphere { Pt41, sr }
  sphere { Pt42, sr }
//  sphere { Pt51, sr }
//  sphere { Pt52, sr }
  pigment { color Yellow }
}

union {
  sphere { CPt1, sr }
  sphere { CPt2, sr }
  sphere { CPt3, sr }
  sphere { CPt4, sr }
//  sphere { CPt5, sr }
  pigment { color Cyan }
}

union {
  cylinder { CPt1, Pt11, cr }
  cylinder { CPt1, Pt12, cr }
  cylinder { CPt2, Pt21, cr }
  cylinder { CPt2, Pt22, cr }
  cylinder { CPt3, Pt31, cr }
  cylinder { CPt3, Pt32, cr }
  cylinder { CPt4, Pt41, cr }
  cylinder { CPt4, Pt42, cr }
//  cylinder { CPt5, Pt51, cr }
//  cylinder { CPt5, Pt52, cr }
  pigment { color Green }
}

union {
  TorusSegment(CPt1, Pt11, Pt12, tr)
  TorusSegment(CPt2, Pt21, Pt22, tr)
  TorusSegment(CPt3, Pt31, Pt32, tr)
  TorusSegment(CPt4, Pt41, Pt42, tr)
//  TorusSegment(CPt5, Pt51, Pt52, tr)
  pigment { color Red }
}


// ===================================================================

light_source {  100*<1,-1,  0>, White }
light_source {  100*Unitv,  White }


camera {
  location <10, -2, 2>
  look_at (Pt31+Pt32)/2
}

background { color White }

// ===================================================================
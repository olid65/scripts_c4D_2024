from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

NB_ETAGES = 6
NB_SEPARATIONS = 6

def main() -> None:

    # Get the active object
    op = doc.GetActiveObject()
    if op is None:
        #Message
        c4d.gui.MessageDialog('Please select an object.')
        return
    # Get the active object's polygon selection
    polySel = op.GetPolygonS()
    if polySel is None:
        #Message
        c4d.gui.MessageDialog('Please select an object with a polygon selection.')
        return
    poly = None
    for i in range(op.GetPolygonCount()):
        if polySel.IsSelected(i):
            poly = op.GetPolygon(i)
            break
    if poly is None:
        #Message
        c4d.gui.MessageDialog('Please select a polygon.')
        return

    # Get the points of the polygon
    mg = op.GetMg()
    points = [op.GetPoint(i) for i in [poly.a,poly.b,poly.c,poly.d]]

    #center of the polygon
    center = c4d.Vector(0,0,0)
    for p in points:
        center += p
    center /= 4

    #change the order of the points
    #first point is the one with the lowest x value and y value
    #second point is the one with the lowest x value and highest y value
    #third point is the one with the highest x value and highest y value
    #fourth point is the one with the highest x value and lowest y value
    points.sort(key=lambda p: (p.x, p.y))
    p1,p2,p3,p4 = points

    #calculate the normal of the polygon
    normal = (p2-p1).Cross(p3-p1)
    normal.Normalize()
    #create a matrix with the normal as the z axis
    mg_normal = c4d.Matrix()
    mg_normal.v3 = normal
    mg_normal.off = center*mg
    mg_normal.v2 = (p1-p2).GetNormalized()
    mg_normal.v1 = mg_normal.v3.Cross(mg_normal.v2)

    #calculate the points in the new coordinate system
    points = [p*mg_normal for p in points]
    p1,p2,p3,p4 = points
    print(points)

    # Create a cloner object
    cloner = c4d.BaseObject(c4d.Omgcloner)
    mg_cloner = c4d.Matrix(op.GetMg())
    mg_cloner.off = c4d.Vector(center*mg)
    cloner.SetMg(mg_normal)

    # calculate height and width of the facade
    height = abs(points[1].y - points[0].y)
    width = abs(points[2].x - points[1].x)

    height_plane = height/NB_ETAGES
    width_plane = width/NB_SEPARATIONS
    print(height_plane)
    print(width_plane)

    cloner[c4d.MG_GRID_SIZE] = c4d.Vector(width-width_plane,height-height_plane,0)
    cloner[c4d.MG_GRID_RESOLUTION] = c4d.Vector(NB_SEPARATIONS,NB_ETAGES,0)

    plane = c4d.BaseObject(c4d.Oplane)
    plane[c4d.PRIM_AXIS] = c4d.PRIM_AXIS_ZP
    plane[c4d.PRIM_PLANE_SUBW] = 1
    plane[c4d.PRIM_PLANE_SUBH] = 1
    plane[c4d.PRIM_PLANE_WIDTH] = width_plane
    plane[c4d.PRIM_PLANE_HEIGHT] = height_plane
    plane.InsertUnder(cloner)


    doc.InsertObject(cloner)
    c4d.EventAdd()










"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
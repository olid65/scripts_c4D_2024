from typing import Optional
import c4d
import sys

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

ALT_BASE = 450

def add_point_at_base(pts, alt_base = ALT_BASE):
    # insert point at the beginning and the end of the list with y = alt_base
    pt = c4d.Vector(pts[0])
    pt.y = alt_base
    pts.insert(0, pt)
    pt = c4d.Vector(pts[-1])
    pt.y = alt_base
    pts.append(pt)
    return pts

def create_spline(pts, name = None):
    spline = c4d.SplineObject(len(pts), c4d.SPLINETYPE_LINEAR)
    spline.SetAllPoints(pts)
    spline[c4d.SPLINEOBJECT_CLOSED] = True
    spline.Message(c4d.MSG_UPDATE)
    if name :
        spline.SetName(name)
    return spline

def create_loft_object(spline):
    loft = c4d.BaseObject(c4d.Oloft)
    loft[c4d.CAPSANDBEVELS_CAP_TYPE] = c4d.CAPSANDBEVELS_CAP_TYPE_DELAUNAY
    spline.InsertUnder(loft)
    return loft


def main() -> None:

    if not op or not op.IsInstanceOf(c4d.Opolygon):
        #message dialog
        c4d.gui.MessageDialog("Please select a polygonal object")
        return
    alt_base = ALT_BASE
    #objet connector
    connector = c4d.BaseObject(c4d.Oconnector)
    connector[c4d.CONNECTOBJECT_PHONG_MODE] = c4d.CONNECTOBJECT_PHONG_MODE_MANUAL
    connector.SetMg(c4d.Matrix(op.GetMg()))

    # bounding box of the object
    #parse all points of the object
    #get the min and max of each axis
    max_x = max_z = -sys.maxsize
    min_x = min_z = sys.maxsize
    for p in op.GetAllPoints():
        #print(p)
        if p.x > max_x:
            max_x = p.x
        if p.x < min_x:
            min_x = p.x
        if p.z > max_z:
            max_z = p.z
        if p.z < min_z:
            min_z = p.z
    #print(max_x, min_x, max_z, min_z)

    #spline with all points min_x
    pts_max_x = [pt for pt in op.GetAllPoints() if pt.x == max_x]
    pts_min_x = [pt for pt in op.GetAllPoints() if pt.x == min_x]
    pts_max_z = [pt for pt in op.GetAllPoints() if pt.z == max_z]
    pts_min_z = [pt for pt in op.GetAllPoints() if pt.z == min_z]

    #on inverse les points max pour que le spline soit dans le bon sens
    pts_max_x.reverse()
    pts_max_z.reverse()

    lst_pts = [pts_max_x, pts_min_x, pts_max_z, pts_min_z]
    names = ["max_x", "min_x", "max_z", "min_z"]

    for pts,name in zip(lst_pts,names):
        pts = add_point_at_base(pts,alt_base)
        sp = create_spline(pts,name)
        loft = create_loft_object(sp)
        loft.InsertUnder(connector)

    #Polygone pour la base
    pts_base = [c4d.Vector(min_x, alt_base, min_z), c4d.Vector(min_x, alt_base, max_z), c4d.Vector(max_x, alt_base, max_z), c4d.Vector(max_x, alt_base, min_z)]
    poly = c4d.PolygonObject(4, 1)
    poly.SetAllPoints(pts_base)
    poly.SetPolygon(0, c4d.CPolygon(3,2,1,0))
    poly.Message(c4d.MSG_UPDATE)
    poly.InsertUnder(connector)

    doc.StartUndo()

    doc.InsertObject(connector)
    doc.AddUndo(c4d.UNDOTYPE_NEW, connector)

    doc.EndUndo()

    c4d.EventAdd
    return


"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
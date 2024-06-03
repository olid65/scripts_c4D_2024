from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def point_inside_polygon(point, polygon):
    x, y = point.x,point.z
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_intersection = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= x_intersection:
                            inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def pt2tuple2D(p):
    return p.x,p.z

def main() -> None:
    
    pts2D = list(map(lambda p:(p.x,p.z), op.GetAllPoints()))
    print(pts2D)
    
    return

    sculpt_obj = c4d.modules.sculpting.GetSelectedSculptObject(doc)

    if not sculpt_obj:
        print('pas sculptobject')

    lyr = sculpt_obj.GetCurrentLayer()
    lyr.ClearMask()
    for i in range(lyr.GetPointCount()):
        print(lyr.GetOffset(i))
        break
    c4d.EventAdd()

    return
    if not op:
        print('sélectionez une spline')
        return
    sp = op.GetRealSpline()
    if not sp:
        print('pas une spline')
    mg = op.GetMg()
    pts2D = [pt2tuple2D(p*mg) for p in sp.GetAllPoints()]

    p = c4d.Vector(0)
    print(point_inside_polygon(p,pts2D))

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
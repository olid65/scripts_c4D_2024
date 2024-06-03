from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def main() -> None:
    sel_pts = op.GetPointS()
    sel_poly = op.GetPolygonS()
    
    sel_poly.DeselectAll()
    
    for i in range(op.GetPolygonCount()):
        poly2lst = lambda p : [p.a,p.b,p.c,p.d]
        for id_pt in poly2lst(op.GetPolygon(i)):
            if sel_pts.IsSelected(id_pt):
                sel_poly.Select(i)
                break
    
    c4d.EventAdd()

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
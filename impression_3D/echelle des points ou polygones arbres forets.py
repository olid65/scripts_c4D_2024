from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

"""Sélectionner les objets polygonaux des points d'arbres
   ou des polygones des forets"""

ID_BUILDING_SCALE = 1059451

SCALE_MNT = 2.5

def main() -> None:
    for op in doc.GetActiveObjects(0):
        mg = op.GetMg()
        alt_obj = mg.off.y
        alt_obj_scale = alt_obj*SCALE_MNT
        f = lambda v : c4d.Vector(v.x,(v.y+alt_obj)*SCALE_MNT-alt_obj,v.z)
        pts = [f(p) for p in op.GetAllPoints()]
        op.SetAllPoints(pts)
        op.Message(c4d.MSG_UPDATE)

    c4d.EventAdd()


"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
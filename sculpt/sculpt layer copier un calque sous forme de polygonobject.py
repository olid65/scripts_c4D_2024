import c4d
from random import random


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

# Main function
def main():

    sculpt_op = c4d.modules.sculpting.GetSelectedSculptObject(doc)
    if not sculpt_op:
        return
    lyr = sculpt_op.GetCurrentLayer()
    
    nb_pts = lyr.GetPointCount()
    res = c4d.PolygonObject(nb_pts,0)
    res .SetName(lyr.GetName())
    
    pts = [lyr.GetOffset(i) for i in range(nb_pts)]
    res.SetAllPoints(pts)
    res.Message(c4d.MSG_UPDATE)
    
    doc.InsertObject(res)
    c4d.EventAdd()
    return


# Execute main()
if __name__=='__main__':
    main()
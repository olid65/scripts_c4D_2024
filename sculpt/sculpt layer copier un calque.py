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
    sculpt_op.StartUndo()
    lyr_srce = sculpt_op.GetCurrentLayer()
    
    lyr_dst = sculpt_op.AddLayer()
    lyr_dst.SetName(lyr_srce.GetName()+'_copy')

    for i in range(lyr_srce.GetPointCount()):
        
        offset = lyr_srce.GetOffset(i)
        lyr_dst.SetOffset(i,c4d.Vector(offset))

    sculpt_op.Update()
    sculpt_op.EndUndo()

    c4d.EventAdd()
    return

    sculpt_op = c4d.modules.sculpting.GetSelectedSculptObject(doc)
    if not sculpt_op:
        if not op :
            raise Warning('No selected object')
        if not op.CheckType(c4d.Opolygon):
            raise  Warning('The object is not a polygon object')
        sculpt_op = c4d.modules.sculpting.MakeSculptObject(op, doc)
        if not sculpt_op : return

    #sculpt_op.Subdivide()
    lyr = sculpt_op.AddLayer()
    lyr.SetName('prout')

    for i in range(sculpt_op.GetPolygonCount()):
        norm = sculpt_op.GetFaceNormal(i)
        rdm = random()*10
        offset = norm*rdm
        lyr.SetOffset(i, offset)

    sculpt_op.Update()

    c4d.EventAdd()


# Execute main()
if __name__=='__main__':
    main()
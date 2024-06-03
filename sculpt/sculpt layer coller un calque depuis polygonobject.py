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
    obj = sculpt_op.GetOriginalObject()
    for o in obj.GetChildren():
        lyr_dst = sculpt_op.AddLayer()
        lyr_dst.SetName(o.GetName())
        for i,p in enumerate(o.GetAllPoints()):
            lyr_dst.SetOffset(i,p)

    sculpt_op.Update()
    sculpt_op.EndUndo()
    c4d.EventAdd()
    return

# Execute main()
if __name__=='__main__':
    main()
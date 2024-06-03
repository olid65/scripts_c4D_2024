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
    lyr = sculpt_op.GetCurrentLayer()

    for i in range(lyr.GetPointCount()):
        offset = lyr.GetOffset(i)
        if offset.y < 0:
            lyr.TouchPointForUndo(i)
            offset.y = 0
            lyr.SetOffset(i,offset)
    sculpt_op.Update()
    sculpt_op.EndUndo()

    c4d.EventAdd()
    return


# Execute main()
if __name__=='__main__':
    main()
import c4d
from c4d import gui
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

# Main function
def main():
    res = c4d.BaseObject(c4d.Onull)
    res.SetName("Mosplines_animation_complete")
    for sp in op.GetChildren():
        mospline = c4d.BaseObject(440000054) #Mospline
        mospline[c4d.MGMOSPLINEOBJECT_MODE] = c4d.MGMOSPLINEOBJECT_MODE_SPLINE
        mospline[c4d.MGMOSPLINEOBJECT_SOURCE_SPLINE] = sp
        mospline.SetName(sp.GetName())

        mospline.InsertUnderLast(res)
    doc.InsertObject(res)
    c4d.EventAdd()


# Execute main()
if __name__=='__main__':
    main()
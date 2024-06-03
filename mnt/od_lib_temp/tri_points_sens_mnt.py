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
    mg = op.GetMg()
    #on inverse le z pour que ce soit dans le sens mnt !
    vec2tuple = lambda v : (-v.z,v.x,v.y)
    pts_temp = [vec2tuple(p*mg) for p in op.GetAllPoints()]
    pts_temp.sort()
    
    tuple2vec = lambda z,x,y : c4d.Vector(x,y,-z)
    pts = [tuple2vec(z,x,y) for z,x,y in pts_temp]
    poly = c4d.PolygonObject(len(pts),0)
    poly.SetAllPoints(pts)
    poly.Message(c4d.MSG_UPDATE)
    doc.InsertObject(poly)
    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()
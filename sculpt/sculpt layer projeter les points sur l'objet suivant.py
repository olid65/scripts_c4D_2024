import c4d
from c4d import gui
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

DELTA_ALT = 100

def getMinMaxY(obj):
    """renvoie le minY et le maxY en valeur du monde d'un objet"""
    mg = obj.GetMg()
    alt = [(pt * mg).y for pt in obj.GetAllPoints()]
    return min(alt) - DELTA_ALT, max(alt) + DELTA_ALT

def pointsOnSurface(op,mnt,lyr, mask_lst = None):
    grc = c4d.utils.GeRayCollider()
    grc.Init(mnt)

    mg_op = op.GetMg()
    mg_mnt = mnt.GetMg()
    invmg_mnt = ~mg_mnt
    invmg_op = ~op.GetMg()

    minY,maxY = getMinMaxY(mnt)

    ray_dir = ((c4d.Vector(0,0,0)*invmg_mnt) - (c4d.Vector(0,1,0)*invmg_mnt)).GetNormalized()
    length = maxY-minY

    mask = 1.

    for i,p in enumerate(op.GetAllPoints()):
        if mask_lst:
            mask = mask_lst[i]

        #si le point est masqué on continue
        if not mask : continue
        p = p*mg_op
        dprt = c4d.Vector(p.x,maxY,p.z)*invmg_mnt
        intersect = grc.Intersect(dprt,ray_dir,length)
        if intersect :
            pos = grc.GetNearestIntersection()['hitpos']*mg_mnt*invmg_op
            offset = (p.y-pos.y)*mask
            lyr.TouchPointForUndo(i)
            lyr.SetOffset(i,c4d.Vector(0,-offset,0))
            #op.SetPoint(i,pos*mg_mnt*invmg_op)

    #op.Message(c4d.MSG_UPDATE)

# Main function
def main():

    sculpt_op = c4d.modules.sculpting.GetSelectedSculptObject(doc)
    if not sculpt_op:
        return

    obj_cible = sculpt_op.GetOriginalObject().GetNext()
    if not obj_cible:
        return

    if not obj_cible.CheckType(c4d.Opolygon):
        obj_cible = obj_cible.GetCache()

        if not obj_cible or not obj_cible.CheckType(c4d.Opolygon):
            return


    polyo = sculpt_op.GetDisplayPolygonObject()

    #pour le masque quand c'est masqué la valeur est de 0
    #j'inverse pour la multiplivcation après
    mask = [1-sculpt_op.GetMaskCachePoint(i) for i in range(sculpt_op.GetPointCount())]

    sculpt_op.StartUndo()
    lyr = sculpt_op.GetCurrentLayer()

    pointsOnSurface(polyo,obj_cible,lyr, mask_lst = mask)

    sculpt_op.Update()
    sculpt_op.EndUndo()

    #doc.InsertObject(polyo.GetClone())

    c4d.EventAdd()
    return


    return
    sculpt_op.StartUndo()
    lyr = sculpt_op.GetCurrentLayer()

    for i in range(lyr.GetPointCount()):

        offset = lyr.GetOffset(i)
        if offset.x or offset.z:
            lyr.TouchPointForUndo(i)
            offset.x = 0
            offset.z = 0
            lyr.SetOffset(i,offset)
    sculpt_op.Update()
    sculpt_op.EndUndo()

    c4d.EventAdd()
    return

# Execute main()
if __name__=='__main__':
    main()
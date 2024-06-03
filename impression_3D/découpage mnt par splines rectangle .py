from typing import Optional
import c4d
import time

"""sélectionner le mnt
   les splines rectangles doivent être en enfant de l'objet suivant
   si on prend des splines à 4 points mettre l'axe au centre ?
   ATTENTION (pour l'instant) l'axe de l'objet parent doit être à zéro (y compris rotation !)
   et l'axe du MNT aussi
   le script crée une copie de l'objet avec les polygones à l'intérieur de la spline rectangle
   pour chaque tuile avec nom_mnt +nom_tuile"""

#pour un mnt de 8Mio de points et 30 tuiles ça a mis 300 secondes -> 5min.

#BUFFER = 2*37 #si on a un terrain la largeur de la maille ne suffit pas -> 2x

def cut_mnt_by_rectangle(mnt,sp,delta = 200) -> None:
    #altitudes min et max
    alts = [p.y for p in mnt.GetAllPoints()]
    ymin,ymax = min(alts),max(alts)

    #cube from rectangle
    if sp.CheckType(c4d.Osplinerectangle):
        width = sp[c4d.PRIM_RECTANGLE_WIDTH]
        height = sp[c4d.PRIM_RECTANGLE_HEIGHT]
    else:
        xs = [p.x for p in sp.GetAllPoints()]
        zs = [p.z for p in sp.GetAllPoints()]
        width = max(xs)-min(xs)
        height = max(zs)-min(zs)
    cube = c4d.BaseObject(c4d.Ocube)
    cube[c4d.PRIM_CUBE_LEN,c4d.VECTOR_X] = width
    cube[c4d.PRIM_CUBE_LEN,c4d.VECTOR_Z] = height
    cube[c4d.PRIM_CUBE_LEN,c4d.VECTOR_Y] = ymax-ymin + delta

    mg = c4d.Matrix(sp.GetMg())
    pos = mg.off
    pos.y = (ymin+ymax)/2
    mg.off = pos
    cube.SetMg(mg)

    #intersection boolean
    boolobj = c4d.BaseObject(c4d.Oboole)
    boolobj[c4d.BOOLEOBJECT_HIGHQUALITY] = False
    boolobj[c4d.BOOLEOBJECT_TYPE] = c4d.BOOLEOBJECT_TYPE_INTERSECT
    cube.InsertUnder(boolobj)
    mnt_clone = mnt.GetClone()
    mnt_clone.InsertUnder(boolobj)
    mnt_clone.SetMg(c4d.Matrix(mnt.GetMg()))
    doc.InsertObject(boolobj)

    #
    res = c4d.utils.SendModelingCommand(command=c4d.MCOMMAND_MAKEEDITABLE,
                                    list=[boolobj],
                                    mode=c4d.MODELINGCOMMANDMODE_ALL,
                                    bc=c4d.BaseContainer(),
                                    doc=doc)

    if res:
        #print(res)
        resobj = res[0]
        if resobj:
            resobj.SetName(mnt.GetName())
        doc.InsertObject(resobj)

        mnt_cut = resobj.GetDown()
        if mnt_cut:
            mnt_cut.InsertBefore(resobj)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,mnt_cut)
            resobj.Remove()


def main() -> None:
    doc.StartUndo()
    tps1 = time.time()
    # Called when the plugin is selected by the user. Similar to CommandData.Execute.
    parent_spline = op.GetNext()
    pointobj = op

    #calcul de la taille d'une maille, d'après le premier polygone
    poly = pointobj.GetPolygon(0)
    pts = [pointobj.GetPoint(i) for i in [poly.a,poly.b,poly.c,poly.d]]
    x = [p.x for p in pts]
    z = [p.z for p in pts]
    larg_maille = max(x)-min(x)
    haut_maille = max(z)-min(z)

    for sp in parent_spline.GetChildren():
        #on vérifie que c'est bien une splinerectangle
        #TODO si c'est une spline à 4 points vérifier que c'est un rectangle '
        #print(sp.GetPointCount() != 4)
        if not sp.CheckType(c4d.Osplinerectangle) and sp.GetPointCount() != 4:
            print(f"{sp.GetName()} n'est pas une spline rectangle !")
            continue

        #sélection des points à l'intérieur de la spline rectangle'
        ml = sp.GetMl()
        rad = sp.GetRad()
        #je prends 2x la largeur de la maille de chaque côté par sécuritéé !
        xmin = -rad.x-larg_maille*2
        xmax =+rad.x +haut_maille*2
        zmin = -rad.z -larg_maille*2
        zmax = rad.z +haut_maille*2

        bs = pointobj.GetPointS()
        bs.DeselectAll()

        for i,p in enumerate(pointobj.GetAllPoints()):
            pt = p*pointobj.GetMg()*~ml
            if pt.x>xmin and pt.x<xmax and pt.z>zmin and pt.z<zmax:
                bs.Select(i)

        #conversion de la sélection en polygone
        settings = c4d.BaseContainer()  # Settings

        settings[c4d.MDATA_CONVERTSELECTION_LEFT] = 0
        settings[c4d.MDATA_CONVERTSELECTION_RIGHT] = 2
        settings[c4d.MDATA_CONVERTSELECTION_TOLERANT] = False

        res = c4d.utils.SendModelingCommand(command=c4d.MCOMMAND_CONVERTSELECTION,
                                        list=[pointobj],
                                        bc=settings,
                                        doc=doc)


        #SPLIT

        res = c4d.utils.SendModelingCommand(command=c4d.MCOMMAND_SPLIT,
                                        list=[pointobj],
                                        mode = c4d.MODELINGCOMMANDMODE_POLYGONSELECTION  ,
                                        doc=doc)
        if res:
            obj = res[0]
            obj.SetName(f'{pointobj.GetName()}_{sp.GetName()}')
            doc.InsertObject(obj)

            cut_mnt_by_rectangle(obj,sp,delta = 200)
            obj.Remove()

        #doc.SetActiveObject(pointobj)
    tps2 = time.time()
    print(tps2 - tps1)
    doc.SetActiveObject(pointobj)
    doc.EndUndo()
    c4d.EventAdd()

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
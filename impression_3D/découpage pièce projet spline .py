from typing import Optional
import c4d
import time

"""sélectionner la spline pour la découpe de la pièce projet
   METTRE L'ALTITUDE DE LA BASE DE LA SPLINE A L?ALTITUDE DE LA BASE DE LA PIECE
   """


MODE = c4d.BOOLEOBJECT_TYPE_INTERSECT
MODE = c4d.BOOLEOBJECT_TYPE_SUBTRACT

#pour un mnt de 8Mio de points et 30 tuiles ça a mis 300 secondes -> 5min.

#BUFFER = 2*37 #si on a un terrain la largeur de la maille ne suffit pas -> 2x




def extrusion_from_spline(sp, hauteur =200):
    clone = sp.GetClone()

    extr = c4d.BaseObject(c4d.Oextrude)
    extr.SetName(f'{sp.GetName()}_extrusion')
    extr[c4d.EXTRUDEOBJECT_DIRECTION] = c4d.EXTRUDEOBJECT_DIRECTION_Y
    extr[c4d.EXTRUDEOBJECT_EXTRUSIONOFFSET] = hauteur
    clone.InsertUnder(extr)
    extr.SetMg(c4d.Matrix(sp.GetMg()))
    clone.SetMl(c4d.Matrix())
    return extr

def cut_obj_by_spline(obj,sp) -> None:
    #objet extrusion depuis la spline
    extr = extrusion_from_spline(sp, hauteur =200)

    #intersection boolean
    boolobj = c4d.BaseObject(c4d.Oboole)
    boolobj[c4d.BOOLEOBJECT_HIGHQUALITY] = True
    boolobj[c4d.BOOLEOBJECT_TYPE] = MODE
    boolobj[c4d.BOOLEOBJECT_SINGLE_OBJECT] = True

    extr.InsertUnder(boolobj)
    obj_clone = obj.GetClone()
    obj_clone.InsertUnder(boolobj)
    obj_clone.SetMg(c4d.Matrix(obj.GetMg()))
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
            resobj.SetName(f'{obj.GetName()}_{sp.GetName()}')
        doc.InsertObject(resobj)

        mnt_cut = resobj.GetDown()
        if mnt_cut:
            mnt_cut.InsertBefore(resobj)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,mnt_cut)
            resobj.Remove()


def main() -> None:

    spline = op
    extr = extrusion_from_spline(spline)

    if not spline or not spline.CheckType(c4d.Ospline):
        c4d.gui.MessageDialog("Il n'y a pas de spline sélectionnée")
        return

    objs_poly = [o for o in op.GetNext().GetChildren() if o.CheckType(c4d.Opolygon)]

    if not objs_poly:
        c4d.gui.MessageDialog("L'objet suivant doit contenir des objets polygonaux en enfant")
        return

    #if not bats.GetMg() == c4d.Matrix() or not op.GetNext().GetMg() == c4d.Matrix():
        #c4d.gui.MessageDialog("Mettez d'abord les axes à zéro !")
        #return

    doc.StartUndo()
    for obj in objs_poly:
        cut_obj_by_spline(obj,spline)

    doc.EndUndo()
    c4d.EventAdd()
    return


"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
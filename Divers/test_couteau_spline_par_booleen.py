import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

DELTA = 100

"""Sélectionner la spline de découpe puis le mnt
   ATTENTION la spline doit avoir les points à la même hauteur que l'axe"""

def convert_edges_sel_to_tag(op):
    bs = op.GetEdgeS()
    tag = c4d.BaseTag(c4d.Tedgeselection)
    op.InsertTag(tag)
    bs_tag = tag.GetBaseSelect()
    bs.CopyTo(bs_tag)


def main() -> None:
    
    """Called by Cinema 4D when the script is being executed.
    """
    objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

    if len(objs) !=2:
        c4d.gui.MessageDialog('Il faut sélectionner deux objets')
        return

    sp, mnt = objs

    if sp.GetType() != c4d.Ospline:
        c4d.gui.MessageDialog('Le premier objet doit être une spline')
        return

    rad = mnt.GetRad()
    
    rad = mnt.GetRad()
    mp = mnt.GetMp()*mnt.GetMg()
    alt_base = mp.y-rad.y - DELTA
    alt_haut = mp.y+rad.y + DELTA
    haut_extr = alt_haut-alt_base


    boole = c4d.BaseObject(c4d.Oboole)
    boole[c4d.BOOLEOBJECT_SEL_CUT_EDGES] = True
    extr = c4d.BaseObject(c4d.Oextrude)
    extr.InsertUnder(boole)
    extr[c4d.EXTRUDEOBJECT_DIRECTION] = c4d.EXTRUDEOBJECT_DIRECTION_Y
    extr[c4d.EXTRUDEOBJECT_EXTRUSIONOFFSET] = haut_extr
    
    #on place la spline à la base du mnt
    #TODO faire un clone de la spline plutôt    
    sp.InsertUnder(extr)
    mg = sp.GetMg()
    off = mg.off
    off.y = alt_base
    mg.off = off
    sp.SetMg(mg)
    mnt.InsertUnder(boole)
    doc.InsertObject(boole)
    
    #TODO Current State to object
    doc.SetActiveObject(boole,c4d.SELECTION_NEW)
    c4d.CallCommand(12233) # Current State to Object
    nullo =  boole.GetNext()
    mnt_new = nullo.GetDown()
    convert_edges_sel_to_tag(mnt_new)
    
    boole[c4d.ID_BASEOBJECT_GENERATOR_FLAG] =False
    boole[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = c4d.OBJECT_OFF
    boole[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = c4d.OBJECT_OFF
    
    mnt_new.InsertAfter(boole)
    doc.SetActiveObject(mnt_new,c4d.SELECTION_NEW)
    nullo.Remove()
    
    

    c4d.EventAdd()




if __name__ == '__main__':
    main()
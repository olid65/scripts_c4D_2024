import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""ATTENTION ne fonctionne que pour un calque subdivision level 0"""

"""Pas encore très au points car il faut être en mode points activer le soft selection
   Mais il faut bien avoir un layer de sculpt sélectionné
   Pour voir le résultat il faut repasser en mode objet et activer l'outil masque du sculpt"""

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    if not op :
        c4d.gui.MessageDialog("""Vous devez sélectionner un seul objet polygonal ou une spline""")
        return
    tag = op.GetTag(c4d.Tsoftselection)
    if not tag :
        c4d.gui.MessageDialog("""Il n'y a pas de soft selection""")
        return

    sculpt_op = c4d.modules.sculpting.GetSelectedSculptObject(doc)
    if not sculpt_op:
        print('no sculpt')
        return

    polyo = sculpt_op.GetDisplayPolygonObject()

    #On vérifie qu'on a bien le même nombre de points dans ée layer
    if not sculpt_op.GetPointCount() == polyo.GetPointCount():
        print("ne fonctionne que pour une subdivision équivalente")
        return

    #pour le masque quand c'est masqué la valeur est de 0
    #j'inverse pour la multiplivcation après
    #mask = [1-sculpt_op.GetMaskCachePoint(i) for i in range(sculpt_op.GetPointCount())]


    lyr = sculpt_op.GetCurrentLayer()
    sculpt_op.StartUndo()

    for i,(p,ts) in enumerate(zip(op.GetAllPoints(), tag.GetAllHighlevelData())):
        lyr.TouchMaskForUndo(i)
        lyr.SetMask(i,ts)


    sculpt_op.Update()
    sculpt_op.EndUndo()

    #doc.InsertObject(polyo.GetClone())

    c4d.EventAdd()
    return


if __name__ == '__main__':
    main()
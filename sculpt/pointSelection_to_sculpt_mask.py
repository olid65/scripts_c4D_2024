import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""ATTENTION ne fonctionne que pour un calque subdivision level 0"""
def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    sculpt_op = c4d.modules.sculpting.GetSelectedSculptObject(doc)
    if not sculpt_op:
        print('no sculpt')
        return

    polyo = sculpt_op.GetDisplayPolygonObject()

    #pour le masque quand c'est masqué la valeur est de 0
    #j'inverse pour la multiplivcation après
    mask = [1-sculpt_op.GetMaskCachePoint(i) for i in range(sculpt_op.GetPointCount())]


    lyr = sculpt_op.GetCurrentLayer()



    bs = polyo.GetPointS()
    #print(bs)
    #On vérifie qu'on a bien le même nombre de points dans ée layer
    if not sculpt_op.GetPointCount() == polyo.GetPointCount():
        print("ne fonctionne que pour une subdivision équivalente")
        return
    if not bs.GetCount():
        print("Il n'y a pas de points séletionnés")
        return
    sculpt_op.StartUndo()
    #lyr.TouchMaskForUndo()

    for i in range(polyo.GetPointCount()):
        lyr.TouchMaskForUndo(i)
        if bs.IsSelected(i):
            lyr.SetMask(i, 1.0)
        else:
            lyr.SetMask(i, 0.0)

    #on active l'outil mask -> si on veut un blur on appuie ensuite sur le bouton
    #c4d.CallCommand(1024506) # Mask

    sculpt_op.Update()
    sculpt_op.EndUndo()

    #doc.InsertObject(polyo.GetClone())

    c4d.EventAdd()
    return


if __name__ == '__main__':
    main()
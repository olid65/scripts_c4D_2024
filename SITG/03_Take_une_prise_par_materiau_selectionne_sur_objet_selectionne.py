import c4d
"""Sélectionner les matériaux et l'objet
   L'objet doit avoir au moins un tag texture
   Le matériau du dernier tag sera modifié pour chaque take"""
   
doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    if not op :
        c4d.gui.MessageDialog("Il faut sélectionner un objet")
        return

    tex_tags =[t for t in op.GetTags() if t.CheckType(c4d.Ttexture)]
    if not tex_tags :
        c4d.gui.MessageDialog("Il n'y a pas de Texture tag sur l'objet sélectionné")
        return
    tex_tag = tex_tags[-1]
    mat_dprt = tex_tag[c4d.TEXTURETAG_MATERIAL]
    # Gets the TakeData from the active document (holds all information about Takes)
    takeData = doc.GetTakeData()
    if takeData is None:
        raise RuntimeError("Failed to retrieve the take data.")

    if not takeData.GetTakeMode() == c4d.TAKE_MODE_AUTO:
        c4d.gui.MessageDialog("Vous devez activer l'Auto Take (bouton A de la palette take)")
        return
    doc.StartUndo()
    for mat in doc.GetActiveMaterials():
        tex_tag_clone = tex_tag.GetClone(c4d.COPYFLAGS_NONE)
        newTake = takeData.AddTake(mat.GetName(), None, None)
        newTake.SetChecked(True)
        if newTake is None:
            raise RuntimeError("Failed to add a new take.")
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,newTake)
        # Defines the created Take as the active one
        #takeData.SetCurrentTake(newTake)


        # Checks if there is some TakeData and the current mode is set to auto Take
        if takeData and takeData.GetTakeMode() == c4d.TAKE_MODE_AUTO:
            tex_tag[c4d.TEXTURETAG_MATERIAL] = mat
            newTake.AutoTake(takeData, tex_tag, tex_tag_clone)
    tex_tag[c4d.TEXTURETAG_MATERIAL] = mat_dprt
    doc.EndUndo()
    c4d.EventAdd()


if __name__ == '__main__':
    main()
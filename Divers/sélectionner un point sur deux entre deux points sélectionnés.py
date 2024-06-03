import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    bs = op.GetPointS()
    
    if not bs.GetCount()==2:
        c4d.gui.MessageDialog(f'Il y a {bs.GetCount()} points sélectionnés, il en faut 2 !')
        return
    
    id_p1,id_p2 = [i for i in range(op.GetPointCount()) if bs.IsSelected(i)]
    
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SELECTION,op)
    
    bs.DeselectAll()
    i = id_p1 +1
    while i<id_p2:
        bs.Select(i)
        i+=2
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
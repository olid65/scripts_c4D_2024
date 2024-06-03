import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    obj = op
    lst_poly = [o for o in op.GetChildren() if o.CheckType(c4d.Opolygon)]
    res = c4d.BaseObject(c4d.Onull)
    doc.InsertObject(res)
    for o in lst_poly:
        mg = o.GetMg()
        inst = c4d.BaseObject(c4d.Oinstance)
        inst.SetName(o.GetName())
        inst[c4d.INSTANCEOBJECT_LINK] = o
        inst.InsertAfter(o)
        inst.SetMg(c4d.Matrix(o.GetMg()))
        o.InsertUnderLast(res)
        o.SetMg(mg)
    c4d.EventAdd()



if __name__ == '__main__':
    main()
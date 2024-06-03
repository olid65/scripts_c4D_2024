import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    name = "piece"
    dic = {}
    for o in doc.GetActiveObjects(0):
        dic.setdefault(o.GetName()[-8:],[]).append(o)

    for k,lst in sorted(dic.items()):
        no = c4d.BaseObject(c4d.Onull)
        no.SetName(k)
        
        doc.InsertObject(no)
        for o in lst:
            o.InsertUnderLast(no)
    c4d.EventAdd()

if __name__ == '__main__':
    main()
import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

DENOM = 5


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    cnt = op.GetPointCount()

    pts = [p for i,p in enumerate(op.GetAllPoints()) if not i % DENOM ]
    nb_pts = len(pts)
    print(nb_pts)
    res = c4d.PolygonObject(nb_pts,0)
    res.SetAllPoints(pts)
    res.SetMg(c4d.Matrix(op.GetMg()))
    res.SetName(f"{op.GetName()}_1pt/{DENOM}")
    res.Message(c4d.MSG_UPDATE)
    doc.InsertObject(res)
    c4d.EventAdd()


if __name__ == '__main__':
    main()
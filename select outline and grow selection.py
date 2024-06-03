import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

#Nombre d'itérations pour étendre la sélection
#après la sélection du contour'
NB_GROW = 1

def selectContourEdge():

    nb = c4d.utils.Neighbor()
    nb.Init(op)
    bs = op.GetSelectedEdges(nb,c4d.EDGESELECTIONTYPE_SELECTION)
    bs.DeselectAll()
    for i,poly in enumerate(op.GetAllPolygons()):
        inf = nb.GetPolyInfo(i)
        if nb.GetNeighbor(poly.a, poly.b, i)==-1:
            bs.Select(inf['edge'][0])

        if nb.GetNeighbor(poly.b, poly.c, i)==-1:
            bs.Select(inf['edge'][1])


        #si pas triangle
        if not poly.c == poly.d :
            if nb.GetNeighbor(poly.c, poly.d, i)==-1:
                bs.Select(inf['edge'][2])

        if nb.GetNeighbor(poly.d, poly.a, i)==-1:
            bs.Select(inf['edge'][3])

    op.SetSelectedEdges(nb,bs,c4d.EDGESELECTIONTYPE_SELECTION)



def selectContourPoints(op):
    nb = c4d.utils.Neighbor()
    nb.Init(op)
    bs = op.GetPointS()
    bs.DeselectAll()
    pts_sel = []
    for i,poly in enumerate(op.GetAllPolygons()):
        inf = nb.GetPolyInfo(i)
        if nb.GetNeighbor(poly.a, poly.b, i)==-1:
            pts_sel.append(poly.a)
            pts_sel.append(poly.b)

        if nb.GetNeighbor(poly.b, poly.c, i)==-1:
            pts_sel.append(poly.b)
            pts_sel.append(poly.c)


        #si pas triangle
        if not poly.c == poly.d :
            if nb.GetNeighbor(poly.c, poly.d, i)==-1:
                pts_sel.append(poly.c)
                pts_sel.append(poly.d)

        if nb.GetNeighbor(poly.d, poly.a, i)==-1:
            pts_sel.append(poly.d)
            pts_sel.append(poly.a)
    for i in set(pts_sel): bs.Select(i)

def growPointS(op):
    bs = op.GetPointS()
    ptsS = [i for i in range(op.GetPointCount()) if bs.IsSelected(i)]
    nb = c4d.utils.Neighbor()
    nb.Init(op)
    polys = []
    for i in ptsS:
        polys+= nb.GetPointPolys(i)

    new_sel = []
    for id_poly in set(polys):
        poly = op.GetPolygon(id_poly)
        new_sel += [poly.a,poly.b,poly.c,poly.d]
    for i in set(new_sel):
        bs.Select(i)


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """

    #selectContourEdge()
    selectContourPoints(op)
    for i in range(NB_GROW):
        growPointS(op)
    c4d.EventAdd()


if __name__ == '__main__':
    main()
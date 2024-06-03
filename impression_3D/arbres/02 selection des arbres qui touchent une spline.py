import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


"""Sélectionner la spline
   le null contenant les arbres doit être placé juste après
   (ou objets circulaire en 2D -> centre +rayon)"""


def circle_touch_segments(circle,segments):
    pos,rayon = circle
    for segmentPoint1,segmentPoint2 in segments:
        dist,intesect_point,offset = c4d.utils.PointLineSegmentDistance(segmentPoint1, segmentPoint2, pos)
        #dist = c4d.utils.PointLineDistance(p0, v, p).GetLength()
        if dist <=rayon : return True
    return False

def main() -> None:

    """Called by Cinema 4D when the script is being executed.
    """
    sp_rect = op
    null_arbres = op.GetNext()
    mg = sp_rect.GetMg()
    pts = [p*mg for p in sp_rect.GetAllPoints()]
    pts.append(pts[0])

    #on stacke les lignes sous forme pdprt, line vector (p2-p1)
    segments = []
    for p1,p2 in zip(pts,pts[1:]):
        p1 = c4d.Vector(p1.x,0,p1.z)
        p2 = c4d.Vector(p2.x,0,p2.z)
        segments.append((p1,p2))

    #parcours de tous les cercles
    for arbre in null_arbres.GetChildren():
        pos = c4d.Vector(arbre.GetMg().off) #* inv_mg_rect
        pos.y = 0
        rayon = max((arbre.GetRad().x,arbre.GetRad().z)) *arbre.GetAbsScale().x
        cercle = (pos,rayon)
        if circle_touch_segments(cercle, segments):
            if doc.GetActiveObject()==op:
                doc.SetActiveObject(arbre,mode=c4d.SELECTION_NEW)
            else:
                doc.SetActiveObject(arbre,mode=c4d.SELECTION_ADD)
    c4d.EventAdd()
    return




    return
    inv_mg_rect = ~sp_rect.GetMg()


    #le rectangle est défini par les coordonnées de ses coins supérieur gauche (rx1, ry1) et inférieur droit (rx2, ry2) :
    pts = [p*mg for p in sp_rect.GetAllPoints()]
    xmin = min([p.x for p in pts])
    xmax = max([p.x for p in pts])
    zmin = min([p.z for p in pts])
    zmax = max([p.z for p in pts])

    rect = (xmin,zmin,xmax,zmax)


    for o in null_arbres.GetChildren():
        pos = o.GetMg().off #* inv_mg_rect
        rayon = max(o.GetRad().x,o.GetRad().x)
        cercle = (pos.x,pos.z,rayon)
        if cercle_touche_rectangle(cercle, rect):
            if doc.GetActiveObject()==op:
                doc.SetActiveObject(o,mode=c4d.SELECTION_NEW)
            else:
                doc.SetActiveObject(o,mode=c4d.SELECTION_ADD)
    c4d.EventAdd()
    return


if __name__ == '__main__':
    main()
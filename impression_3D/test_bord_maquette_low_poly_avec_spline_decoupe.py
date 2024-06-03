from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected



"""Sélectionner toutes les tuiles de terrain (sans socle)
   les splines "base" doivent être juste après et avoir 4 points ->rectangle
   ATTENTION de régler ALT_BASE"""

ALT_BASE = 700


def is_clockwise(pts):
    somme_produits = 0
    n = len(pts)

    for i in range(n):
        current = pts[i]
        next = pts[(i + 1) % n]  # Gestion du dernier élément

        somme_produits += (next.x - current.x) * (next.z + current.z)

    return somme_produits >= 0

def selectContour(op):

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

def edge2spline(op):

    res = c4d.utils.SendModelingCommand(command = c4d.MCOMMAND_EDGE_TO_SPLINE,
                                    list = [op],
                                    mode = c4d.MODELINGCOMMANDMODE_EDGESELECTION,
                                    doc = doc)
    return op.GetDown()


def main() -> None:

    objects = doc.GetActiveObjects(0)
    splines = [o.GetNext() for o in objects if o.GetNext().CheckType(c4d.Ospline) ]

    if not len(objects)==len(splines):
        c4d.gui.MessageDialog("Problème il doit manquer des splines après les tuiles")
        return

    for idx,(op,spline_decoupe_mnt) in enumerate(zip(objects,splines)):
        print(op)
        # on vérifie qu'il y a bien un objet sélectionné
        if not op:
            c4d.gui.MessageDialog("il faut sélectionner un objet")
            return

        #on vérifie que l'objet sélectionné est un objet polygonal
        if not op.CheckType(c4d.Opolygon):
            c4d.gui.MessageDialog("il faut sélectionner un objet polygonal")
            return

        #spline_decoupe_mnt = op.GetNext()
        #on vérifie qu'il y a bien un objet suivant
        #if not spline_decoupe_mnt:
            #c4d.gui.MessageDialog("L'objet suivant doit être une spline à 4 points")
            #return

        #on vérifie que l'objet suivant est une spline et a 4 points

        if not spline_decoupe_mnt.CheckType(c4d.Ospline):
            c4d.gui.MessageDialog("L'objet suivant doit être une spline à 4 points")
            return

        if spline_decoupe_mnt.GetPointCount()!=4:
            c4d.gui.MessageDialog("L'objet suivant doit être une spline à 4 points")
            return

        selectContour(op)
        spline_contour_mnt = edge2spline(op)

        if not spline_contour_mnt:
            c4d.gui.MessageDialog("la spline contour n'a pas pu être générée")
            return

        #on vérifie que la spline contour n'a qu'un segment
        if not spline_contour_mnt.GetSegmentCount()==1:
            c4d.gui.MessageDialog("la spline contour a plusieurs segments")
            return


        #trouver les angles selon les points de spline_decoupe_mnt
        mg_contour = spline_contour_mnt.GetMg()
        pts_contour = [p*mg_contour for p in  spline_contour_mnt.GetAllPoints()]

        #on s'assure que les points sont dans le sens horaire inverse
        if is_clockwise(pts_contour):
            pts_contour.reverse()

        pts_contour_2D = [c4d.Vector(p.x,0,p.z) for p in pts_contour]

        mg_base = spline_decoupe_mnt.GetMg()
        pts_base = [p*mg_base for p in  spline_decoupe_mnt.GetAllPoints()]
        #on s'assure que les points sont dans le sens horaire inverse
        if is_clockwise(pts_base):
            pts_base.reverse()

        pts_base_2D = [c4d.Vector(p.x,0,p.z) for p in pts_base]

        p0,p1,p2,p3 = pts_base_2D
        d0 = d1 = d2 = d3 = float('inf')
        i0 =i1 =i2 = i3 = -1

        #on cherche les points les plus proches
        #il y a certainement plus élégant !
        for i,p in enumerate(pts_contour_2D):
            d = (p-p0).GetSquaredLength()
            if d < d0:
                d0 = d
                i0 = i
            d = (p-p1).GetSquaredLength()
            if d < d1:
                d1 = d
                i1 = i
            d = (p-p2).GetSquaredLength()
            if d < d2:
                d2 = d
                i2 = i
            d = (p-p3).GetSquaredLength()
            if d < d3:
                d3 = d
                i3 = i

        #on redéfinit la liste des points de la spline de découpe pour qu'elle commence à i0
        pts_contour = pts_contour[i0:] + pts_contour[:i0]

        #on recalcule les identifiants i0,i2,i3,i4 après le décalage
        i1 = (i1-i0)%len(pts_contour)
        i2 = (i2-i0)%len(pts_contour)
        i3 = (i3-i0)%len(pts_contour)
        i0 = 0

        #on met l'altitude ALT_BASE aux points de la base
        pts_base = [c4d.Vector(p.x,ALT_BASE,p.z) for p in pts_base]
        p0,p1,p2,p3 = pts_base

        #on extrait différentes parties de la liste des points de la spline de découpe
        pts_contour_1 = pts_contour[i0:i1+1]
        pts_contour_2 = pts_contour[i1:i2+1]
        pts_contour_3 = pts_contour[i2:i3+1]
        pts_contour_4 = pts_contour[i3:] + pts_contour[:i0+1]

        #on insère les points de la base au début et à la fin de la liste des points de la spline de découpe
        pts_contour_1.insert(0,p0)
        pts_contour_1.append(p1)
        pts_contour_2.insert(0,p1)
        pts_contour_2.append(p2)
        pts_contour_3.insert(0,p2)
        pts_contour_3.append(p3)
        pts_contour_4.insert(0,p3)
        pts_contour_4.append(p0)

        #on crée les splines fermées
        spline_contour_1 = c4d.SplineObject(len(pts_contour_1), c4d.SPLINETYPE_LINEAR)
        spline_contour_2 = c4d.SplineObject(len(pts_contour_2), c4d.SPLINETYPE_LINEAR)
        spline_contour_3 = c4d.SplineObject(len(pts_contour_3), c4d.SPLINETYPE_LINEAR)
        spline_contour_4 = c4d.SplineObject(len(pts_contour_4), c4d.SPLINETYPE_LINEAR)

        #on définit les points des splines
        spline_contour_1.SetAllPoints(pts_contour_1)
        spline_contour_2.SetAllPoints(pts_contour_2)
        spline_contour_3.SetAllPoints(pts_contour_3)
        spline_contour_4.SetAllPoints(pts_contour_4)

        #on crée les splines fermées
        spline_contour_1[c4d.SPLINEOBJECT_CLOSED] = True
        spline_contour_2[c4d.SPLINEOBJECT_CLOSED] = True
        spline_contour_3[c4d.SPLINEOBJECT_CLOSED] = True
        spline_contour_4[c4d.SPLINEOBJECT_CLOSED] = True

        #on nomme les splines
        spline_contour_1.SetName("contour_1")
        spline_contour_2.SetName("contour_2")
        spline_contour_3.SetName("contour_3")
        spline_contour_4.SetName("contour_4")

        #mise à jour des splines
        spline_contour_1.Message(c4d.MSG_UPDATE)
        spline_contour_2.Message(c4d.MSG_UPDATE)
        spline_contour_3.Message(c4d.MSG_UPDATE)
        spline_contour_4.Message(c4d.MSG_UPDATE)

        #liste des splines
        splines = [spline_contour_1,spline_contour_2,spline_contour_3,spline_contour_4]

        #on crée un objet connector
        connector = c4d.BaseObject(c4d.Oconnector)
        connector.SetName(op.GetName()+'_socle')
        connector[c4d.CONNECTOBJECT_PHONG_MODE] = c4d.CONNECTOBJECT_PHONG_MODE_MANUAL
        connector.SetMg(c4d.Matrix(op.GetMg()))


        for sp in splines:
            #on crée un loft nurbs
            loft = c4d.BaseObject(c4d.Oloft)
            loft[c4d.CAPSANDBEVELS_CAP_TYPE] = c4d.CAPSANDBEVELS_CAP_TYPE_DELAUNAY
            sp.InsertUnder(loft)
            loft.InsertUnderLast(connector)

        #on crée un objet polygon object pour la base
        poly = c4d.PolygonObject(len(pts_base), 1)
        poly.SetAllPoints(pts_base)
        poly.SetPolygon(0, c4d.CPolygon(0,1,2,3))
        poly.Message(c4d.MSG_UPDATE)
        poly.InsertUnder(connector)



        doc.InsertObject(connector)
        doc.AddUndo(c4d.UNDOTYPE_NEW, connector)

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, op)
        op.InsertUnder(connector)

        if idx == 0:
            doc.SetActiveObject(connector, mode=c4d.SELECTION_NEW)

        else:
            doc.SetActiveObject(connector, mode=c4d.SELECTION_ADD)

    doc.EndUndo()
    c4d.EventAdd()


"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
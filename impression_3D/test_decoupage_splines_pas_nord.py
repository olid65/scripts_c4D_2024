from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def point_dans_polygone(point, polygone):
    """point = c4d.Vector, polygone = list of tuple x,z"""
    # Récupérer les coordonnées du point
    x, y = point.x,point.z

    # Compter le nombre de côtés du polygone
    nb_sommets = len(polygone)
    est_a_l_interieur = False

    j = nb_sommets - 1
    for i in range(nb_sommets):
        xi, yi = polygone[i]
        xj, yj = polygone[j]

        # Vérifier si le point est entre les bornes en Y du segment
        condition_1 = (yi < y and yj >= y) or (yj < y and yi >= y)

        # Vérifier si le point est à gauche du segment
        condition_2 = xi + (y - yi) / (yj - yi) * (xj - xi) < x

        # Inverser l'état de est_a_l_interieur si les conditions sont remplies
        if condition_1 and condition_2:
            est_a_l_interieur = not est_a_l_interieur

        j = i

    return est_a_l_interieur

def sel_points_from_spline(point_obj,spline) -> None:
    
    #récupérer la liste de points de la spline
    #et les mettre en relatif de l'objet
    p2v = lambda p: (p.x,p.z)
    poly = [p2v(p *spline.GetMg() *~point_obj.GetMl()) for p in spline.GetAllPoints()]

    sel = point_obj.GetPointS()
    sel.DeselectAll()
    for i,p in enumerate(point_obj.GetAllPoints()):
        if point_dans_polygone(p, poly):
            sel.Select(i)
    
    c4d.EventAdd()
    
def sel_points2sel_polys_large(op) -> None:
    sel_pts = op.GetPointS()
    sel_poly = op.GetPolygonS()
    
    sel_poly.DeselectAll()
    
    for i in range(op.GetPolygonCount()):
        poly2lst = lambda p : [p.a,p.b,p.c,p.d]
        for id_pt in poly2lst(op.GetPolygon(i)):
            if sel_pts.IsSelected(id_pt):
                sel_poly.Select(i)
                break


def main() -> None:
    mnt = op.GetNext()
    for sp in op.GetChildren():
        sel_points_from_spline(mnt,sp)
        sel_points2sel_polys_large(mnt)
        # Define the settings container for the tool.
        settings: c4d.BaseContainer = c4d.BaseContainer()
        #settings.SetFloat(c4d.MDATA_SPLINE_OUTLINE, 25.0)
    
        # Run the command and print the result.
        res: bool = utils.SendModelingCommand(
            command=c4d.MCOMMAND_SPLIT,
            list=[mnt],
            mode=c4d.MODELINGCOMMANDMODE_POLYGONSELECTION,
            bc=settings,
            doc=doc)
        mnt.GetNext()

        break
    
    c4d.EventAdd()

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
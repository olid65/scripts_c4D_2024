import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""Sélectionner l'objet contenant les arbres
   Les splines rectangles doivent ^être en enfant de l'objet suivant
   et avoir l'axe tourné dans le sens du rectangle
   Pour l'instant colore chaque arbre en fonction
   du rectangle dans lequel il tombre"""

def bbox(obj):
    xmin = min([p.x for p in obj.GetAllPoints()])
    xmax = max([p.x for p in obj.GetAllPoints()])
    zmin = min([p.z for p in obj.GetAllPoints()])
    zmax = max([p.z for p in obj.GetAllPoints()])
    return xmin,zmin,xmax,zmax

def is_inside(pos,bbox):
    x, y = pos.x,pos.z
    xmin, ymin, xmax, ymax = bbox

    if xmin <= x <= xmax and ymin <= y <= ymax:
        return True
    else:
        return False

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """

    trees = op.GetChildren()
    splines_rect = op.GetNext().GetChildren()

    nb_sp = len(splines_rect)

    for i,sp in enumerate(splines_rect):
        inv_ml = ~sp.GetMl()
        bbox_sp = bbox(sp)

        color = c4d.utils.HSVToRGB(c4d.Vector(i*1.0/nb_sp,1,1))
        print(i*1.0/nb_sp)

        for tree in trees:
            #position relative à la spline
            pos = tree.GetMg().off * inv_ml
            if is_inside(pos,bbox_sp):
                #Faire quelque chose avec les arbres qui tombent à l'intérieur
                #pour l'instant je change la couleur ...
                tree[c4d.ID_BASEOBJECT_USECOLOR] = c4d.ID_BASEOBJECT_USECOLOR_ALWAYS
                tree[c4d.ID_BASEOBJECT_COLOR] = color
    c4d.EventAdd()


if __name__ == '__main__':
    main()
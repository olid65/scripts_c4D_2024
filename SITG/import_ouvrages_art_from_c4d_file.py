import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""sélectionner un objet pour l'emprise
   le fichier doit être géoréférencé"""

CONTAINER_ORIGIN = 1026473

FN_OA = '/Volumes/My Passport Pro/SITG/Ouvrage_art_2023/C4D/ouvrages_art_2023.c4d'

def empriseObject(obj, origine):
    geom = obj
    if not geom.CheckType(c4d.Opoint):
        geom = geom.GetCache()
        if not geom.CheckType(c4d.Opoint) : return None
    mg = obj.GetMg()
    pts = [p*mg+origine for p in geom.GetAllPoints()]
    lst_x = [p.x for p in pts]
    lst_y = [p.y for p in pts]
    lst_z = [p.z for p in pts]

    xmin = min(lst_x)
    xmax = max(lst_x)
    ymin = min(lst_y)
    ymax = max(lst_y)
    zmin = min(lst_z)
    zmax = max(lst_z)

    mini = c4d.Vector(xmin,ymin,zmin)
    maxi = c4d.Vector(xmax,ymax,zmax)

    return xmin,zmin,xmax,zmax


def get_spline_from_bbox(xmin,zmin,xmax,zmax,origine):
    sp = c4d.SplineObject(4,c4d.SPLINETYPE_LINEAR)
    sp.SetName(op.GetName()+'_bbox')
    sp.SetAllPoints([   c4d.Vector(xmin,0,zmin)-origine,
                        c4d.Vector(xmin,0,zmax)-origine,
                        c4d.Vector(xmax,0,zmax)-origine,
                        c4d.Vector(xmax,0,zmin)-origine,])
    sp[c4d.SPLINEOBJECT_CLOSED] = True
    return sp

def check_collision(box1, box2):
    # box1 et box2 sont des tuples contenant les coordonnées des coins opposés de la bounding box
    # box1 : (x1, y1, x2, y2)
    # box2 : (x1, y1, x2, y2)

    # Vérification de la collision sur l'axe horizontal
    if box1[0] <= box2[2] and box1[2] >= box2[0]:
        # Vérification de la collision sur l'axe vertical
        if box1[1] <= box2[3] and box1[3] >= box2[1]:
            return True  # Les bounding boxes se touchent ou se chevauchent
    return False  # Les bounding boxes ne se touchent pas

def get_bbox_from_spline(sp,origine):
    mg = sp.GetMg()
    pts = [p*mg+origine for p in sp.GetAllPoints()]
    xmin = min([p.x for p in pts])
    xmax = max([p.x for p in pts])
    zmin = min([p.z for p in pts])
    zmax = max([p.z for p in pts])
    return [xmin,zmin,xmax,zmax]

def get_ouvrages_arts(bbox,doc_oa):
    lst = []
    oas = doc_oa.GetFirstObject()
    bboxes = oas.GetNext()
    origine = doc_oa[CONTAINER_ORIGIN]
    #TODO vérification que c'est bien les bons objets et qu'il n'a pas eu de modif du doc'
    for oa,sp_bbox in zip(oas.GetChildren(),bboxes.GetChildren()):
        bbox_sp = get_bbox_from_spline(sp_bbox,origine)
        if check_collision(bbox, bbox_sp):
            doc_oa.SetActiveObject( oa, mode=c4d.SELECTION_ADD)
            lst.append(oa)
    return lst

def get_unused_tag_mat(obj,stop = None, lst = []):
    while obj :
        
        lst+= [t for t in obj.GetTags() if t.CheckType(c4d.Ttexture) and not t[c4d.TEXTURETAG_MATERIAL]]
        get_unused_tag_mat(obj.GetDown(),lst)
        if stop == obj :
            return lst
        obj = obj.GetNext()
    return lst


def main() -> None:
    doc_oa = c4d.documents.LoadDocument(FN_OA, loadflags = c4d.SCENEFILTER_OBJECTS)
    origine = doc[CONTAINER_ORIGIN]
    #xmin,zmin,xmax,zmax = 2498066.6458930504, 1114365.6145997695, 2499866.6458930504, 1117565.6145997695
    xmin,zmin,xmax,zmax = empriseObject(op, origine)
    bbox = [xmin,zmin,xmax,zmax]
    lst_oa = get_ouvrages_arts(bbox,doc_oa)
    res = c4d.BaseObject(c4d.Onull)
    res.SetName("Ouvrages d'art")

    for oa in lst_oa:
        clone = oa.GetClone(flags=c4d.COPYFLAGS_NONE, trn=None)
        clone.InsertUnderLast(res)
    doc.InsertObject(res)
    
    lst_tag_to_delete = get_unused_tag_mat(res, stop = res)
    for tag in lst_tag_to_delete:
        tag.Remove()
        
    c4d.EventAdd()
    
if __name__ == '__main__':
    main()
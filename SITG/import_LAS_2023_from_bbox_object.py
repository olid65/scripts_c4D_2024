from typing import Optional
import c4d
import sys

try : import laspy
except :
    sys.path.append('/Users/olivierdonze/.local/lib/python3.11/site-packages')
    import laspy


CONTAINER_ORIGIN = 1026473

classif ={
            1 :("Non classifié","None", c4d.Vector4d(1, 0, 0, 1)),
            2 :("Sol","sol", c4d.Vector4d(0.44, 0.375, 0.141, 1)),
            3 :("Basse végétation (<50cm)","veget_bas", c4d.Vector4d(0.55, 0.73, 0.453, 1)),
            5 :("Haute végétation (>50cm)","veget_haut", c4d.Vector4d(0.213, 0.35, 0.179, 1)),
            6 :("Bâtiments","bati", c4d.Vector4d(0.56, 0.56, 0.56, 1)),
            7 :("Points bas ou isolés","pts_bas", c4d.Vector4d(1, 0.55, 1, 1)),
            9 :("Eau","eau", c4d.Vector4d(0.41, 0.862, 1, 1)),
            13 :("Ponts, passerelles","ponts", c4d.Vector4d(0.23, 0.23, 0.23, 1)),
            15 :("Sol (points complémentaires)","sol", c4d.Vector4d(0.497, 0.5, 0.325, 1)),
            16 :("Bruit","bruit", c4d.Vector4d(1, 0, 0.917, 1)),
            19 :("Points mesurés hors périmètre de l'acquisition","hors_perim", c4d.Vector4d(1, 0.983, 0, 1)),
          }

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

    return mini, maxi

def extract_points_within_bounding_box(las_file_path,  xmin, xmax, ymin, ymax, origine,veget_only = True):
    pts_res = []
    clas = []
    with laspy.open(las_file_path) as file:

        for points in file.chunk_iterator(1024):
            #print(f"{count / file.header.point_count * 100}%")

            # For performance we need to use copy
            # so that the underlying arrays are contiguous
            x, y = points.x.copy(), points.y.copy()
            classif = points.classification.copy()
            #r,v,b = points.r.copy(), points.v.copy(), points.b.copy()
            mask = (x >= xmin) & (x <= xmax) & (y >= ymin) & (y <= ymax)

            ##################################################################
            #MASK MASK MASK CLASSIFICATION
            ##################################################################
            if veget_only:
                inside = points[mask & ((classif == 5) | (classif == 4) | (classif == 3))]
            else:
                inside = points[mask]
            if  inside:
                pts_res.extend([c4d.Vector(x,y,z)-origine for x,y,z in zip(inside.x,inside.z,inside.y)])
                clas.extend([c for c in inside.classification])
    return pts_res, clas

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def extractLAS(list_fn, bbox,doc, veget_only = True):
    origine = doc[CONTAINER_ORIGIN]
    xmin,ymin,xmax,ymax = bbox
    for fn in list_fn:
        if not fn.exists():
            print(f"Le fichier {fn} n'existe pas")
            continue
        pts, lst_classif = extract_points_within_bounding_box(fn, xmin, xmax, ymin, ymax,origine,veget_only=veget_only)

        if pts:
            nb_pts = len(pts)
            res = c4d.PolygonObject(nb_pts,0)
            res.SetAllPoints(pts)
            res.Message(c4d.MSG_UPDATE)
            doc.InsertObject(res)
            #vertexcolor tag
            tag = c4d.VertexColorTag(len(pts))
            res.InsertTag(tag)
            tag[c4d.ID_VERTEXCOLOR_DRAWPOINTS] = True
            data = tag.GetDataAddressW()
            white = c4d.Vector4d(1.0, 1.0, 1.0, 1.0)
            pointCount = res.GetPointCount()
            for idx in range(pointCount):
                class_color = classif.get(lst_classif[idx],None)
                if class_color:
                    color = class_color[2]
                else:
                    color = c4d.Vector4d(0, 0, 0, 1)
    c4d.EventAdd()

def main() -> None:
    fn = '/Users/olivierdonze/Downloads/2501750_1126250.las'
    list_fn = ['/Volumes/My Passport Pro/TEMP/LIDAR_SITG_download/2498250_1117000.las']
    if not op:
        print("pas d'objet sélectionné")
        return
    origine = doc[CONTAINER_ORIGIN]
    mini,maxi = empriseObject(op, origine)
    bbox = mini.x,mini.z,maxi.x,maxi.z
    extractLAS(list_fn, bbox,doc)
    return



"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
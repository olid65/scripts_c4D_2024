import c4d
import os.path


# localimport-v1.7.3-blob-mcw79
import base64 as b, types as t, zlib as z; m=t.ModuleType('localimport');
m.__file__ = __file__; blob=b'\
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\
XVw='
exec(z.decompress(b.b64decode(blob)), vars(m)); _localimport=m;localimport=getattr(m,"localimport")
del blob, b, t, z, m;

CONTAINER_ORIGIN = 1026473



# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

def lst2vec(lst):
    """transformation tuple ou liste coord x,y(z) en vecteur Cinema4D"""
    if len(lst) ==2:
        x,z = lst
        return c4d.Vector(x,0,z)
    elif len(lst) ==3:
        x,z,y = lst
        return c4d.Vector(x,y,z)

def get_centre(pts):
    lst_x = [v.x for v in pts]
    lst_y = [v.y for v in pts]
    lst_z = [v.z for v in pts]
    return c4d.Vector((min(lst_x)+max(lst_x))/2, (min(lst_y)+max(lst_y))/2,(min(lst_z)+max(lst_z))/2)

def point(coord):
    pass

def multipoint(coord):
    pass

def polygon(coord):
    pts = []
    seg = []
    for lst in coord:
        #on supprime le dernier point car c'est le même que le premier
        pts_temp = [lst2vec(l) for l in lst][:-1]
        #stockage du nombre de points par segment
        seg.append(len(pts_temp))
        pts+=pts_temp

    #on calcule le centre des points
    # et on translate tous les points
    centre = get_centre(pts)
    pts = list(map(lambda v: v-centre, pts))
    pcnt = len(pts)
    scnt = len(seg)
    res = c4d.SplineObject(pcnt,c4d.SPLINETYPE_LINEAR)
    res[c4d.SPLINEOBJECT_CLOSED] = True
    res.SetAllPoints(pts)
    res.SetAbsPos(centre)
    if scnt > 1:
        res.ResizeObject( pcnt, scnt=scnt)
        for i,cnt in enumerate(seg):
            res.SetSegment(i, cnt, closed=True)
    res.Message(c4d.MSG_UPDATE)

    return res

def multipolygon(coord):
    pts = []
    seg = []
    for poly in coord:
        for lst in poly:
            #on supprime le dernier point car c'est le même que le premier
            pts_temp = [lst2vec(l) for l in lst][:-1]
            #stockage du nombre de points par segment
            seg.append(len(pts_temp))
            pts+=pts_temp

    #on calcule le centre des points
    # et on translate tous les points
    centre = get_centre(pts)
    pts = list(map(lambda v: v-centre, pts))
    pcnt = len(pts)
    scnt = len(seg)
    res = c4d.SplineObject(pcnt,c4d.SPLINETYPE_LINEAR)
    res[c4d.SPLINEOBJECT_CLOSED] = True
    res.SetAllPoints(pts)
    res.SetAbsPos(centre)
    if scnt > 1:
        res.ResizeObject( pcnt, scnt=scnt)
        for i,cnt in enumerate(seg):
            res.SetSegment(i, cnt, closed=True)
    res.Message(c4d.MSG_UPDATE)

    return res

def linestring(coord):
    pts = [lst2vec(p) for p in coord]


    #on calcule le centre des points
    # et on translate tous les points
    centre = get_centre(pts)
    pts = list(map(lambda v: v-centre, pts))
    pcnt = len(pts)
    #scnt = len(seg)
    res = c4d.SplineObject(pcnt,c4d.SPLINETYPE_LINEAR)
    res[c4d.SPLINEOBJECT_CLOSED] = False
    res.SetAllPoints(pts)
    res.SetAbsPos(centre)
    res.Message(c4d.MSG_UPDATE)

    return res

def multilinestring(coord):
    pass

dico_func = {
                'Point': point,
                'MultiPoint': multipoint,
                'Polygon': polygon,
                'MultiPolygon': multipolygon,
                'LineString': linestring,
                'MultiLineString':multilinestring,
}

# Main function
def main(fn,doc):
    #from geojson import Point, MultiPoint, Polygon, MultiPolygon, LineString, MultiLineString, Feature, FeatureCollection, load
    with localimport(os.path.dirname(__file__)) as importer:
                importer.disable(['geojson'])
                from geojson import Point, MultiPoint, Polygon, MultiPolygon, LineString, MultiLineString, Feature, FeatureCollection, load

                res = c4d.BaseObject(c4d.Onull)
                res.SetName(os.path.basename(fn))
                origine = doc[CONTAINER_ORIGIN]

                with open(fn) as f:
                    data = load(f)

                    features = data.get('features',None)
                    if not features:
                        c4d.gui.MessageDialog(f"Pas de features dans le fichier {os.path.basename(fn)}")
                        return

                    for feature in features:
                        geom = feature.get('geometry',None)

                        #appelle de la fonction selon le type
                        obj = dico_func[geom.get('type',None)](geom['coordinates'])
                        pos = obj.GetAbsPos()
                        if not origine:
                            doc[CONTAINER_ORIGIN] = c4d.Vector(pos)
                            origine = doc[CONTAINER_ORIGIN]
                        pos-= origine


                        #attributs
                        attr = feature['properties']
                        if attr.get('name',None):
                            obj.SetName(attr['name'])

                        if attr.get('ELEV_MAX',None):
                            obj.SetName(attr['ELEV_MAX'])


                        obj.SetAbsPos(pos)
                        obj.InsertUnderLast(res)

                doc.InsertObject(res)
                c4d.EventAdd()


# Execute main()
if __name__=='__main__':
    main()
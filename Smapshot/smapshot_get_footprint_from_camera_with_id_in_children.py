import c4d
from pyproj import Transformer
from urllib import request
import json


doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

CONTAINER_ORIGIN = 1026473

#Sélectionner le neutre contenant les caméras dont le nom est un id smapshot

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    origin = doc[CONTAINER_ORIGIN]
    lst_ids = [int(o.GetName()) for o in op.GetChildren() if o.CheckType(c4d.Ocamera) and o.GetName().isnumeric()]
    
    res = c4d.BaseObject(c4d.Onull)
    res.SetName('footprints')
    # Définir le transformateur entre EPSG:4326 et EPSG:2042
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2056")
    for i in lst_ids:
        url = f'https://smapshot.heig-vd.ch/api/v1/images/{i}/footprint'
        response = request.urlopen(url)
        data = json.loads(response.read())
        footprint = data.get('footprint')
        id_pt = 0
        nb_segments = 0
        for poly in footprint.get('coordinates'):
            pts_wgs84 = []
            segments = []
            for segment in poly:
                for coord in segment:
                    lon, lat = coord
                    pts_wgs84.append((lon, lat))
                    id_pt += 1
                nb_segments += 1
                segments.append(id_pt)
                id_pt = 0
        pts = [transformer.transform(lat, lon) for lon, lat in pts_wgs84]
        pts = [c4d.Vector(x,0,z)-origin for x,z in pts]

        sp = c4d.SplineObject(len(pts),c4d.SPLINETYPE_LINEAR)
        sp[c4d.SPLINEOBJECT_CLOSED] = True
        sp.SetAllPoints(pts)
        if nb_segments>1:
            print(i,nb_segments)
            sp.ResizeObject(len(pts), scnt=nb_segments)
            for id_seg,seg in enumerate(segments):
                sp.SetSegment(id_seg, seg, closed=True)


        sp.Message(c4d.MSG_UPDATE)
        sp.SetName(f'{i}_footprint')
        sp.InsertUnderLast(res)
    doc.InsertObject(res)
    c4d.EventAdd()



if __name__ == '__main__':
    main()
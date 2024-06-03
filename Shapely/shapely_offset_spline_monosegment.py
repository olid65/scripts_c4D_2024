import c4d
#import shapely
from shapely import LineString
doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

DISTANCE = -50

def c4dLineObject_to_Linestring(line_obj):
    return LineString([(p.x,p.z) for p in line_obj.GetAllPoints()])

def lineString_to_Spline(line_str, mg = None):
    pts = [c4d.Vector(x,0,z) for x,z in line_str.coords]
    if not pts : return None
    sp = c4d.SplineObject(len(pts), c4d.SPLINETYPE_LINEAR)
    sp.SetAllPoints(pts)
    sp[c4d.SPLINEOBJECT_INTERPOLATION] = c4d.SPLINEOBJECT_INTERPOLATION_NONE
    if mg:
        sp.SetMg(mg)
    sp.Message(c4d.MSG_UPDATE)
    return sp

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    sph = c4d.utils.SplineHelp()
    #ATTENTION passer dans le flag  c4d.SPLINEHELPFLAGS_RETAINLINEOBJECT
    #si on vet la lineobject
    sph.InitSplineWith(op,flags=c4d.SPLINEHELPFLAGS_GLOBALSPACE | c4d.SPLINEHELPFLAGS_CONTINUECURVE | c4d.SPLINEHELPFLAGS_RETAINLINEOBJECT)

    line_obj = sph.GetLineObject()
    if not line_obj:
        print('pas de LineObject')
        return
    
    #SHAPELY
    line_str = c4dLineObject_to_Linestring(line_obj)
    line_offset = line_str.offset_curve(DISTANCE, quad_segs=16, join_style=1, mitre_limit=5.0)
    sp_offset = lineString_to_Spline(line_offset, mg = c4d.Matrix(op.GetMg()))
    sp_offset.SetName(f'{op.GetName()}_offset_{DISTANCE}')
    doc.InsertObject(sp_offset)
    doc.SetActiveObject(sp_offset)
    c4d.EventAdd()

if __name__ == '__main__':
    main()
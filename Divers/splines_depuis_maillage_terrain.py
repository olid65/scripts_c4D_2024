import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    
    mg = op.GetMg()
    pts_mnt = [p*mg for p in op.GetAllPoints()]
    
    res_x = c4d.BaseObject(c4d.Onull)
    res_x.SetName('spline_vert')
    
    #splines verticales (x identique)
    dic_x = {}
    for p in pts_mnt:
        dic_x.setdefault(p.x,[]).append((p.y,p.z))
    
    for x in sorted(dic_x.keys()):
        pts = []
        for y,z in dic_x[x]:
            pts.append(c4d.Vector(x,y,z))
        sp = c4d.SplineObject(len(pts), c4d.SPLINETYPE_LINEAR)
        sp.SetName(str(round(x)))
        sp.SetAllPoints(pts)
        sp.Message(c4d.MSG_UPDATE)
        sp.InsertUnderLast(res_x)
    doc.InsertObject(res_x) 
    
    #splines horizontales (z identique)
    res_z = c4d.BaseObject(c4d.Onull)
    res_z.SetName('spline_horizontales')
    dic_z = {}
    for p in pts_mnt:
        dic_z.setdefault(p.z,[]).append((p.x,p.y))
    
    for z in sorted(dic_z.keys()):
        pts = []
        for x,y in sorted(dic_z[z]):
            pts.append(c4d.Vector(x,y,z))
        sp = c4d.SplineObject(len(pts), c4d.SPLINETYPE_LINEAR)
        sp.SetName(str(round(z)))
        sp.SetAllPoints(pts)
        sp.Message(c4d.MSG_UPDATE)
        sp.InsertUnderLast(res_z)
    doc.InsertObject(res_z) 
    
    
    
    
    
    
    
    c4d.EventAdd()   
    
            
            


if __name__ == '__main__':
    main()
import c4d
from c4d import gui
#Welcome to the world of Python

DIST = 0.2
def main():
    
    splines = [sp for sp in doc.GetActiveObjects(0) if sp.CheckType(c4d.Ospline)]
    
    for sp in splines:
        pts = sp.GetAllPoints()
        closed = sp[c4d.SPLINEOBJECT_CLOSED]
        if closed :
            pts.append(pts[0])
        new_pts = []
    
        for p1,p2 in zip(pts,pts[1:]):
            dist = (p2-p1).GetLength()
            direction = (p2-p1).GetNormalized()
            nb_sub = int(round(dist/DIST))-1
            new_pts.append(p1)
            if nb_sub>0:
                try : lg = dist/(nb_sub+1)
                except:
                    print(dist, nb_sub)
                    return
                ajout = lg*direction
                pos = p1+ajout
                for i in range(nb_sub):
                    new_pts.append(pos)
                    pos += ajout
        if not closed:
            new_pts.append(p2)
        sp_res = c4d.SplineObject(len(new_pts),c4d.SPLINETYPE_LINEAR)
        sp_res.SetName(f'{sp.GetName()}_subd{DIST*100}cm')
        sp_res.SetMg(sp.GetMg())
        sp_res[c4d.SPLINEOBJECT_CLOSED] = closed
        sp_res.SetAllPoints(new_pts)
        sp_res.Message(c4d.MSG_UPDATE)
        doc.InsertObject(sp_res)
    c4d.EventAdd()




if __name__=='__main__':
    main()
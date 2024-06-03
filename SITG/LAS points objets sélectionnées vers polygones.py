import c4d, random, math

TAILLE = 0.4

def points_2_polygones(op,pts, taille = TAILLE,nom = 'LAS_polygones',rotation = True):
    """transforme une liste de point
       en un objet polygonal avec un polygone carré
       à l'emplacement de chaque point qui tourne de manière aléatoire"""
       
    nbpoly = len(pts)
    nbpts = nbpoly*4

    invmg = ~op.GetMg()
    
    res = c4d.PolygonObject(nbpts,nbpoly)
    res.SetMg(op.GetMg())
    n = 0
    for i in range(nbpoly):
        res.SetPolygon(i,c4d.CPolygon(n,n+1,n+2,n+3))
        n+=4
        
    pts_new = []
    for i,pt in enumerate(pts):
        if rotation :
            hpb = c4d.Vector(random.random()*2*math.pi,random.random()*2*math.pi,random.random()*2*math.pi)
            mr = c4d.utils.HPBToMatrix(hpb)
            
        else : 
            mr = c4d.Matrix()

        mr.off = pt    

        p1 = c4d.Vector(-taille,0,-taille*0.6) * mr #*invmg
        p2 = c4d.Vector(-taille,0,taille) * mr #*invmg
        p3 = c4d.Vector(taille,0,taille) * mr #*invmg
        p4 = c4d.Vector(taille,0,-taille*0.6) * mr #*invmg
        

        pts_new.extend([p1,p2,p3,p4])

    res.SetAllPoints(pts_new)
    res.SetName(nom)
    res.Message(c4d.MSG_UPDATE)
    return res

def main():
    res = c4d.BaseObject(c4d.Onull)
    
    for o in doc.GetActiveObjects(0):
        pts = o.GetAllPoints()
        poly = points_2_polygones(o,pts, taille = TAILLE)
        poly.InsertUnderLast(res)
    doc.StartUndo()
    
    #res.SetMg(op.GetMg())
    doc.InsertObject(res)
    doc.AddUndo(c4d.UNDOTYPE_NEW,res)
    doc.SetActiveObject(res)
    c4d.EventAdd()
    doc.EndUndo()

if __name__=='__main__':
    main()

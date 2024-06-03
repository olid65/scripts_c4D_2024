import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


"""Sélectionner le terrain à découper et rentrer le nombre de pièce en x et en z ci-dessous
   Crée un plan subdivisé si on met ensuite le terrain en enfant d'un objet Fracture Voronoi
   et que l'on met uniquement le plan dans sources -> découpe régulièrement le terrain
   Attention peut-être un peu long mais travaille en tâche de fond"""

def main() -> None:
    #A ADAPTER A ADAPTER A ADAPTER
    nb_x = 6
    nb_z = 4
    
    mg = op.GetMg()
    l_x = op.GetRad().x*2
    l_z = op.GetRad().z*2
    
    part_x = l_x/nb_x
    part_z = l_z/nb_z

    
    pos = c4d.Vector(-l_x/2+part_x/2,0,-l_z/2+part_z/2)
    nb_pts = nb_x*nb_z
    nb_polys = (nb_x-1)*(nb_z-1)
    res = c4d.PolygonObject(nb_pts,nb_polys)
    id_pt = 0
    id_poly = 0
    
    for i in range(nb_z):
        for n in range(nb_x):
            res.SetPoint(id_pt, c4d.Vector(pos))
            
            if i>0 and n>0:
                a = id_pt - nb_x -1
                b = a+1
                c = id_pt
                d=id_pt-1
                poly = c4d.CPolygon(a,b,c,d)
                res.SetPolygon(id_poly,poly)
                id_poly +=1
            id_pt +=1
            pos.x+= part_x
        pos.x = -l_x/2+part_x/2
        pos.z += part_z
            
    res.Message(c4d.MSG_UPDATE)
    res.SetMg(c4d.Matrix(mg))
    res.SetName(f'{op.GetName()}_{nb_x}x{nb_z}')        
    doc.InsertObject(res)
    c4d.EventAdd()
    
    


if __name__ == '__main__':
    main()
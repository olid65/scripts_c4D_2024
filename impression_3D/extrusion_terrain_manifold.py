from typing import Optional
import c4d

"""Sélectionner le ou les objet à extruder
   Crée un copie extrudée de chaque objet sélectionné"""

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


def get_rows_cols_number(op):
    zpred = op.GetPoint(0).z
    nb_pt_x = 0
    for p in op.GetAllPoints():
        if p.z == zpred:
            nb_pt_x+=1
        else: break
    nb_pts = op.GetPointCount()
    nb_pt_z = int(nb_pts/nb_pt_x)
    return nb_pt_x,nb_pt_z

def tag_poly_selection(op,name,id_dbt,id_fin):
    tag = c4d.SelectionTag(c4d.Tpolygonselection)
    bs = tag.GetBaseSelect()
    bs.DeselectAll()
    for i in range(id_dbt,id_fin):
        bs.Select(i)
    tag.SetName(name)
    op.InsertTag(tag)

def main() -> None:
    # Called when the plugin is selected by the user. Similar to CommandData.Execute.
    pred = None
    doc.StartUndo()
    for op in doc.GetActiveObjects(0):
        nrows,ncols = get_rows_cols_number(op)
        #print(nrows,ncols)
    
        polycnt = op.GetPolygonCount()
        ptcnt = op.GetPointCount()
        pts = op.GetAllPoints()
        
        new_poly_cnt = polycnt*2 + (nrows-1)*2 + (ncols-1)*2
        
        pts+=[c4d.Vector(p.x,0,p.z) for p in pts]
        res = c4d.PolygonObject(op.GetPointCount()*2,new_poly_cnt)
        res.SetName(op.GetName())
        res.SetAllPoints(pts)
        
        #dessus et dessous
        for i in range(op.GetPolygonCount()):
            poly = op.GetPolygon(i)
            res.SetPolygon(i,poly)
            poly2 = c4d.CPolygon(poly.d+ptcnt,poly.c+ptcnt,poly.b+ptcnt,poly.a+ptcnt,)
            res.SetPolygon(i+polycnt,poly2)
        
        tag_poly_selection(res,'mnt',0,polycnt)
        tag_poly_selection(res,'socle_laterall',polycnt*2,new_poly_cnt)
        
        id_poly = polycnt*2
        id_poly_dbt = id_poly
        tag_poly_selection(res,'base',polycnt,polycnt*2)
        #lateral
        #zmax
        for i in range(ncols-1):
            poly = c4d.CPolygon(i+ptcnt,i+ptcnt+1,i+1,i)
            res.SetPolygon(id_poly,poly)
            id_poly+=1
        tag_poly_selection(res,'zmax',id_poly_dbt,id_poly)
        id_poly_dbt = id_poly
        #xmin
        for i in range(nrows-1):
            a = i*ncols
            b= a+ncols
            c = b+ptcnt
            d = a+ptcnt
            poly = c4d.CPolygon(a,b,c,d)
            res.SetPolygon(id_poly,poly)
            id_poly+=1
        tag_poly_selection(res,'xmin',id_poly_dbt,id_poly)
        id_poly_dbt = id_poly
        #zmin
        for i in range(ncols-1):
            a= ptcnt-ncols+i
            b=a+1
            c = b+ptcnt
            d = a+ptcnt
            poly = c4d.CPolygon(a,b,c,d)
            res.SetPolygon(id_poly,poly)
            id_poly+=1
        tag_poly_selection(res,'zmin',id_poly_dbt,id_poly)
        id_poly_dbt = id_poly
        #xmax
        for i in range(nrows-1):
            a = i*ncols+nrows-1
            b= a+ncols
            c = b+ptcnt
            d = a+ptcnt
            poly = c4d.CPolygon(d,c,b,a)
            res.SetPolygon(id_poly,poly)
            id_poly+=1
        tag_poly_selection(res,'xmax',id_poly_dbt,id_poly)
        id_poly_dbt = id_poly
        
        res.SetMg(op.GetMg())
        
        res.Message(c4d.MSG_UPDATE)
        doc.InsertObject(res,pred = pred)
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,res)
        pred = res
    doc.EndUndo()
    c4d.EventAdd()
    
        
    
    
    

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
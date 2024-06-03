import c4d
from shapely.geometry import LineString,Point,MultiPoint,MultiLineString
from random import random

ROUND = 3


"""Sélectionner le null contenant les splines
   Attention que les splines s'intersectent bien sur un point
   Le script découpe au besoin en segments distincts chaque edge du graphe
   Un nouveau null est créé les splines originales restent intactes"""


def arrondi(v):
    return round(v.x,ROUND),round(v.z,ROUND)

def spline2linestring(sp):
    """la spline doit etre de type linear"""
    return LineString([arrondi(p*sp.GetMg()) for p in sp.GetAllPoints()])

def linestring2spline(l):
    pts = []
    for x,z in l.coords:
        pts.append(c4d.Vector(x,0,z))
    res = c4d.SplineObject(len(pts),c4d.SPLINETYPE_LINEAR)
    res.SetAllPoints(pts)
    res.Message(c4d.MSG_UPDATE)
    return res

def main():
    res = c4d.BaseObject(c4d.Onull)
    res.SetName('Graphe')
    lst_ls = []

    for sp in op.GetChildren():
        spnew = sp.GetCache()
        lst_ls.append(spline2linestring(spnew))

    l = lst_ls.pop(0)
    multi = MultiLineString(lst_ls)

    dif = l.symmetric_difference(multi)
    for i,geom in enumerate(dif.geoms):
        sp_res =  linestring2spline(geom)
        sp_res.SetName(str(i).zfill(4))
        sp_res.InsertUnderLast(res)


    doc.InsertObject(res)
    op.DelBit(c4d.BIT_ACTIVE)
    res.SetBit(c4d.BIT_ACTIVE)
    c4d.EventAdd()


if __name__=='__main__':
    main()
import c4d
import networkx as nx

RND = 3

"""Etape non obligatoire pour vérifier le système :
   les points d'arrivées (rouge), de départ (jaune) et les points de croisement (cyan)
   Pratique pour voir s'il faut tourner certaines splines ou si il y a des splines qui ne se touchent pas
   
   Utilise la librairie networkx -> voir pour l'utilisation plus poussée de graphes"""

def roundV(v,nb=RND):
    return c4d.Vector(round(v.x,nb),round(v.y,nb),round(v.z,nb))

def xz(v):
    return v.x,v.z

def path2sp(path):
    pts = [c4d.Vector(x,0,z) for x,z in path]
    sp = c4d.SplineObject(len(pts),c4d.SPLINETYPE_LINEAR)
    sp.SetAllPoints(pts)
    sp.Message(c4d.MSG_UPDATE)
    return sp


def main():
    pts_fin = []
    edges = []
    for sp in op.GetChildren():
        sph = c4d.utils.SplineHelp()
        sph.InitSpline(sp)
        lg = sph.GetSplineLength()
        pt_dbt = xz(roundV(sp.GetPoint(0)))
        pt_fin = xz(roundV(sp.GetPoint(sp.GetPointCount()-1)))
        edges.append((pt_dbt,pt_fin,lg))
        x,z = pt_fin
        pts_fin.append(c4d.Vector(x,0,z))

    graph = nx.Graph()
    graph.add_weighted_edges_from(edges)

    departs = c4d.BaseObject(c4d.Onull)
    departs.SetName('départs')

    arrivees = c4d.BaseObject(c4d.Onull)
    arrivees.SetName('arrivees')

    croisements = c4d.BaseObject(c4d.Onull)
    croisements.SetName('croisements')

    for node in graph.nodes():
        x,z = node
        onode = c4d.BaseObject(c4d.Onull)
        onode[c4d.NULLOBJECT_DISPLAY] = c4d.NULLOBJECT_DISPLAY_CIRCLE
        onode[c4d.NULLOBJECT_ORIENTATION] = c4d.NULLOBJECT_ORIENTATION_XZ
        onode[c4d.NULLOBJECT_RADIUS] = 20
        onode[c4d.ID_BASEOBJECT_USECOLOR] = c4d.ID_BASEOBJECT_USECOLOR_ALWAYS
        pos = c4d.Vector(x,0,z)
        onode.SetAbsPos(pos)
        onode.SetName(str(round(x,RND))+'_'+str(round(z,RND)))
        nb_voisins = len(list(graph.neighbors(node)))

        if nb_voisins>1:
            onode.InsertUnderLast(croisements)
            onode[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0,1,1)
        else :
            if pos in pts_fin:
                onode[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(1,0,0)
                onode.InsertUnderLast(arrivees)
            else:
                onode[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(1,1,0)
                onode.InsertUnderLast(departs)



    doc.InsertObject(croisements)
    doc.InsertObject(arrivees)
    doc.InsertObject(departs)
    c4d.EventAdd()


if __name__=='__main__':
    main()
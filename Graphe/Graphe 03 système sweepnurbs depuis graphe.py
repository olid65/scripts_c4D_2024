import c4d



"""Crée un système hiérarchique de sweepnurbs avec une copie des splines et comme section un n-sides
   depuis un graphe
   Le script va chercher un objet nommé 'Graphe' et un objet nommé 'arrivees'
   Le système part depuis les différent points d'arrivée et remonte
   les sement en amont viennet en enfant dans un neutre"""

#TODO : déplacer les null parent à l'emplacement de l'arrivée pour plus de clarté ...


ROUND = 3

SIDES = 6
RADIUS = 20


def sweepSystem(lst, dic, parent, name, sides = SIDES, radius = RADIUS ):

    for sp in lst:
        #NULLOBJECT
        nobj = c4d.BaseObject(c4d.Onull)
        #nobj.SetName(name)
        nobj.InsertUnderLast(parent)

        #SWEEPNURBS
        sweep = c4d.BaseObject(c4d.Osweep)
        sweep.InsertUnderLast(nobj)

        #N-SIDE
        nside = c4d.BaseObject(c4d.Osplinenside)
        nside.InsertUnder(sweep)
        nside[c4d.PRIM_NSIDE_SIDES] = sides
        nside[c4d.PRIM_NSIDE_RADIUS] = radius

        #CLONE DE LA SPLINE
        sp.GetClone(c4d.COPYFLAGS_NO_HIERARCHY).InsertUnderLast(sweep)

        #on prend le premier point
        #pour chercher les élément en amont
        pos = sp.GetPoint(0)*sp.GetMg()
        key = (round(pos.x,ROUND),round(pos.z,ROUND))
        lst2 = dic.get(key)
        if not lst2: continue
        sweepSystem(lst2, dic, nobj, name, sides = SIDES, radius = RADIUS )



# Main function
def main():
    null_end = doc.SearchObject('arrivees')
    null_graphe = doc.SearchObject('Graphe')

    res = c4d.BaseObject(c4d.Onull)
    res.SetName(f'{null_graphe.GetName()}_sweepnurbs')

    #dictionnaire des splines avec coordonnées dernier point en clé
    dic_sp = {}

    for sp in null_graphe.GetChildren():
        pos = sp.GetPoint(sp.GetPointCount()-1)*sp.GetMg()
        dic_sp.setdefault((round(pos.x,ROUND),round(pos.z,ROUND)),[]).append(sp)
        #dic_sp[(round(pos.x,ROUND),round(pos.z,ROUND))] = sp

    #print(dic_sp)
    for dprt_o in null_end.GetChildren():
        pos = dprt_o.GetMg().off
        key = (round(pos.x,ROUND),round(pos.z,ROUND))
        #print(key)
        lst = dic_sp.get(key)
        if not lst:
            print(f'pas de spline pour {key}')
            continue
        #pour chaque départ trouvé on crée un système avec un neutre et un sweep
        name = dprt_o.GetName()
        parent = res
        sweepSystem(lst, dic_sp, parent, name)

    doc.InsertObject(res)
    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()
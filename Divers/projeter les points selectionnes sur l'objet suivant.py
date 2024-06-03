#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals #test pour éviter les problèmes d'accent dans les chemins de fichier sous windows

import c4d

"""Projette verticalement les points de l'objet polygonal sélectionné (ou de la spline)  
   sur l'objet polygonal juste apres dans la hiérarchie
   Ne fonctionne pas avec les primitives"""
   


def main():
    if not op : 
        c4d.gui.MessageDialog("""Vous devez sélectionner un seul objet polygonal ou une spline""")
        return
    if not (op.CheckType(c4d.Opolygon) or  op.CheckType(c4d.Ospline)):
        c4d.gui.MessageDialog("""L'objet sélectionné doit être un objet polygonal ou une spline""")
        return
    mnt = op.GetNext()
    if not mnt or not mnt.CheckType(c4d.Opolygon):
        c4d.gui.MessageDialog("""L'objet suivant doit être un objet polygonal""")
        return
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE,op)
    grc = c4d.utils.GeRayCollider()
    grc.Init(mnt)
    
    mg_op = op.GetMg()
    mg_mnt = mnt.GetMg()
    invmg_mnt = ~mg_mnt
    invmg_op = ~op.GetMg()
    
    ray_dir = ((c4d.Vector(0,0,0)*invmg_mnt) - (c4d.Vector(0,1,0)*invmg_mnt)).GetNormalized()
    length = 1000000
    l2 = length*2
    
    

    bs = op.GetPointS()
    sel = bs.GetAll(op.GetPointCount())

    for i,(selected,p) in enumerate(zip(sel,op.GetAllPoints())):
        if not selected: continue
        p = p*mg_op
        dprt = c4d.Vector(p.x,length,p.z)*invmg_mnt
        intersect = grc.Intersect(dprt,ray_dir,l2)
        if intersect :
            pos = grc.GetNearestIntersection()['hitpos']
            op.SetPoint(i,pos*mg_mnt*invmg_op)
    doc.EndUndo()   
    op.Message(c4d.MSG_UPDATE)
    c4d.EventAdd()

if __name__=='__main__':
    main()

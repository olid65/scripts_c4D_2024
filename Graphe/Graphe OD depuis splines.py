import c4d





ARRONDI = 2
RAYON_CERCLE_NOEUD = 2

CLR_EMETTEUURS = c4d.Vector(1,1,0)
CLR_RECEPTEURS = c4d.Vector(0,1,1)
CLR_NOEUDS = c4d.Vector(1,0,1)

def v3Dto2D(v):
    return round(v.x,ARRONDI),round(v.z,ARRONDI)

class Graphe(object):
    """Graphe directionnel pour l'animation de voitures dans c4D"""
    
    def __init__(self,lst_splines):
        self.edges = []
        self.dic_nodes = {}
        for sp in lst_splines:
            #création d'un Edge por spline
            edge = Edge(sp)
            self.edges.append(edge)
            
            #pour chaque point de départ et d'arrivée on crée un noeud
            #si il n'existe pas, ou sinon on rajoute l'Edge au noeud qui existe
            #à l'emplacement soit en arrivée soit en départ
            if not self.dic_nodes.get(edge.start):
                self.dic_nodes[edge.start] = Node(edge.start,start = edge)
            else:
                self.dic_nodes[edge.start].addStart(edge)
                
            if not self.dic_nodes.get(edge.end):
                self.dic_nodes[edge.end] = Node(edge.end,end = edge)
            else:
                self.dic_nodes[edge.end].addEnd(edge)
    def getNodes(self):
        """renvoie une liste de tous les noeuds"""
        return self.dic_nodes.values()
    
    def getC4DNodes(self):
        res = c4d.BaseObject(c4d.Onull)
        res.SetName('graphe_NOEUDS')
        
        o_emetteurs = c4d.BaseObject(c4d.Onull)  
        o_emetteurs.SetName('emmeteurs')
        o_emetteurs[c4d.ID_BASEOBJECT_USECOLOR] = c4d.ID_BASEOBJECT_USECOLOR_ALWAYS
        o_emetteurs[c4d.ID_BASEOBJECT_COLOR] = CLR_EMETTEUURS
        #o_emetteurs[c4d.NULLOBJECT_ICONCOL] = True
        o_emetteurs.InsertUnderLast(res)
        
        o_recepteurs = c4d.BaseObject(c4d.Onull)  
        o_recepteurs.SetName('recepteurs')
        o_recepteurs[c4d.ID_BASEOBJECT_USECOLOR] = c4d.ID_BASEOBJECT_USECOLOR_ALWAYS
        o_recepteurs[c4d.ID_BASEOBJECT_COLOR] = CLR_RECEPTEURS
        #o_recepteurs[c4d.NULLOBJECT_ICONCOL] = True
        o_recepteurs.InsertUnderLast(res)
        
        
        o_noeuds = c4d.BaseObject(c4d.Onull)  
        o_noeuds.SetName('noeuds')
        o_noeuds[c4d.ID_BASEOBJECT_USECOLOR] = c4d.ID_BASEOBJECT_USECOLOR_ALWAYS
        o_noeuds[c4d.ID_BASEOBJECT_COLOR] = CLR_NOEUDS
        #o_noeuds[c4d.NULLOBJECT_ICONCOL] = True
        o_noeuds.InsertUnderLast(res)
        
        for n in self.getNodes():
            obj = n.getObjC4D()
            #emetteurs (jaune)
            if not n.ends:
                obj.InsertUnderLast(o_emetteurs)
                obj[c4d.ID_BASEOBJECT_COLOR] = CLR_EMETTEUURS
            #recepteurs (cyan)
            elif not n.starts:
                obj.InsertUnderLast(o_recepteurs)
                obj[c4d.ID_BASEOBJECT_COLOR] = CLR_RECEPTEURS
            #noeud intermédiaire (magenta)
            else:
                obj.InsertUnderLast(o_noeuds)
                obj[c4d.ID_BASEOBJECT_COLOR] = CLR_NOEUDS
        
        
        return res
                
                

class Edge(object):
    
    def __init__(self,sp):
        self.sp = sp
        mg = sp.GetMg()
        pts = sp.GetAllPoints()
        self.start = v3Dto2D(pts[0]*mg)
        self.end = v3Dto2D(pts[-1]*mg)
        
class Node(object):
    
    def __init__(self, pos, start = None, end = None):
        """pos est un tuple avec la valeur x et z"""
        self. pos = pos
        self.starts = []
        self.ends = []
        if start:
            self.starts.append(start)
        if end:
            self.ends.append(end)
    def addStart(self,edge):
        """rajoute un edge de départ"""
        self.starts.append(edge)
        
    def addEnd(self,edge):
        """rajoute un edge d'arrivée"""
        self.ends.append(edge)
        
    def getObjC4D(self):
        obj = c4d.BaseObject(c4d.Onull)
        obj.SetName(self.pos)
        x,z = self.pos
        obj.SetAbsPos(c4d.Vector(x,0,z))
        obj[c4d.NULLOBJECT_DISPLAY] = c4d.NULLOBJECT_DISPLAY_CIRCLE
        obj[c4d.NULLOBJECT_ORIENTATION] = c4d.NULLOBJECT_ORIENTATION_XZ
        obj[c4d.NULLOBJECT_RADIUS] = RAYON_CERCLE_NOEUD
        obj[c4d.ID_BASEOBJECT_USECOLOR] = c4d.ID_BASEOBJECT_USECOLOR_ALWAYS
        #obj[c4d.NULLOBJECT_ICONCOL] = True
        return obj

def main():
    
    g = Graphe(op.GetChildren())
    doc.StartUndo()
    
    res = g.getC4DNodes()    
    doc.InsertObject(res)
    doc.AddUndo(c4d.UNDOTYPE_NEW,res)
    
    doc.EndUndo()
    c4d.EventAdd()
    return
    doc.StartUndo()  
    o_emetteurs = c4d.BaseObject(c4d.Onull)  
    o_emetteurs.SetName('emmeteurs')
    doc.InsertObject(o_emetteurs)
    doc.AddUndo(c4d.UNDOTYPE_NEW,o_emetteurs)
    
    o_recepteurs = c4d.BaseObject(c4d.Onull)  
    o_recepteurs.SetName('recepteurs')
    doc.InsertObject(o_recepteurs)
    doc.AddUndo(c4d.UNDOTYPE_NEW,o_recepteurs)
    
    o_noeuds = c4d.BaseObject(c4d.Onull)  
    o_noeuds.SetName('noeuds')
    doc.InsertObject(o_noeuds)
    doc.AddUndo(c4d.UNDOTYPE_NEW,o_noeuds)
    
    
    
    doc.EndUndo()
    c4d.EventAdd()
    

if __name__=='__main__':
    main()

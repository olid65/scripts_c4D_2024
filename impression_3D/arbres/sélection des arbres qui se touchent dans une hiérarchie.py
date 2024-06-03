import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""sélectionner un arbre dans une hiérarchie
   Tous les arbres qui se touchent seront sélectionnés
   en partnt de celui sélectionné
   
   Si on veut une marge il faut mettre une distance au BUFFER"""
   
BUFFER = 0

class Arbre(object):
    
    def __init__(self,obj):
        self.obj = obj
        self.pos = c4d.Vector(obj.GetMg().off)
        self.pos.y = 0
        self.rayon = max(obj.GetRad().x, obj.GetRad().z)* obj.GetAbsScale().x
        self.r2 = self.rayon**2
        
    def __str__(self):
        return str(self.obj)
        
def touch(a1,a2):
    l2 = (a1.pos-a2.pos).GetLength()
    if l2<= a1.rayon+a2.rayon + BUFFER :
        return True


def get_touch(arbre,lst,res ):
    #print('lst ->',len(lst))
    to_remove = []
    for a2 in lst:
        if touch(arbre,a2):
            to_remove.append(a2)    
    for a2 in to_remove:
        lst.remove(a2)
    
    for a2 in to_remove:
        res.append(a2)
        get_touch(a2,lst, res)
    return res
    


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    arbre_dprt = Arbre(op)
    
    lst = [Arbre(o) for o in op.GetUp().GetChildren() if o!=op]
    #arbre = lst.pop()
    #print(arbre)
    res = [arbre_dprt]
    get_touch(arbre_dprt,lst, res = res)

    
    #op.DelBit(c4d.BIT_ACTIVE)
    for a in res:
        doc.SetActiveObject(a.obj,c4d.SELECTION_ADD)
    
    c4d.EventAdd()


if __name__ == '__main__':
    main()
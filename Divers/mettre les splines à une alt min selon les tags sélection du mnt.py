import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""Après le script 'selection de points par multi spline vers tag selection'
   Sélectionner le MNT qui contient les tags sélection de points
   L'objet avec les spline en enfants doit ^être juste après
   le lien entre tag et spline se fait par le nom
   
   TODO : fusionner les deux scripts"""

#Le buffer sert à laisser une marge d'altitude
#ATTENTION de mettre un nombre négatif si on veut avoir 
#un peu plus dessous

BUFFER = -0.2

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    splines = op.GetNext().GetChildren()
    dic_splines = {sp.GetName():sp for sp in splines}

    for tag in op.GetTags():
        if not tag.CheckType(c4d.Tpointselection):
            continue
        spline = dic_splines.get(tag.GetName(),None)
        if spline :
            bs = tag.GetBaseSelect()
            alt_min = min([p.y for i,p in enumerate(op.GetAllPoints()) if bs.IsSelected(i)])
            alt_min+=BUFFER
            mg = spline.GetMg()
            pos = mg.off
            pos.y = alt_min
            mg.off = pos
            spline.SetMg(mg)
    c4d.EventAdd()    

if __name__ == '__main__':
    main()
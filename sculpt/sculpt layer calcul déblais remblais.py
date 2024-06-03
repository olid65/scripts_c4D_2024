import c4d
from c4d import gui
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#ATTENTION pour que cela fonctionne il faut que la grille de base soit
#avec des pixels carrés et il ne faut pas de déformation en x et en z 
#calcul à partir du calque actif seulement (ne prend pas en compte les 
#autres calques -> TODO )
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Main function
def main():
    sculpt_op = c4d.modules.sculpting.GetSelectedSculptObject(doc)
    if not sculpt_op:
        return
    lyr = sculpt_op.GetCurrentLayer()
    
    
    polyo = sculpt_op.GetDisplayPolygonObject()
    
    dist =  (polyo.GetPoint(0)-polyo.GetPoint(1)).GetLength()
    surface_px = dist*dist

    deblais = 0
    remblais = 0

    for i in range(lyr.GetPointCount()):        
        diff_alt  = lyr.GetOffset(i).y
        
        if diff_alt <0:
            deblais+=diff_alt
        elif diff_alt >0:
            remblais+=diff_alt
            
    print(f'DEBLAIS = {round(deblais*surface_px,2)}')
    print(f'REMBLAIS = {round(remblais*surface_px,2)}')

    return

# Execute main()
if __name__=='__main__':
    main()
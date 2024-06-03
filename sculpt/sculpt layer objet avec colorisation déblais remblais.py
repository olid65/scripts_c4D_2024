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

    doc.StartUndo()
    polyo = sculpt_op.GetDisplayPolygonObject().GetClone()


    dif_alts = [lyr.GetOffset(i).y for i in range(lyr.GetPointCount()) ]

    #print( polyo.GetPointCount())
    #print(len(dif_alts))


    mini = min(dif_alts)
    maxi = max(dif_alts)
    

    tag = c4d.VariableTag(c4d.Tvertexcolor, polyo.GetPointCount())
    
    data = tag.GetDataAddressW()
    
        
    if tag:
        #tag[c4d.ID_VERTEXCOLOR_VERTEXCOLORMODE] = c4d.ID_VERTEXCOLOR_VERTEXCOLORMODE_POLYGON
        basecolor = c4d.Vector(0.8)
        for i,dif_alt in enumerate(dif_alts):

            if dif_alt ==0:
                color = c4d.Vector4d(basecolor)
            elif dif_alt <0:
                t = dif_alt/mini
                v = c4d.utils.MixVec(basecolor, c4d.Vector(1,1,0), t)
                color = c4d.Vector4d(v)
            elif dif_alt >0:
                t = dif_alt/maxi
                v = c4d.utils.MixVec(basecolor, c4d.Vector(1,0,0), t)
                color = c4d.Vector4d(v)
            
            c4d.VertexColorTag.SetPoint(data, None, None, i, color)

        #tag.SetAllHighlevelData(data)
        tag.Message(c4d.MSG_UPDATE)
        polyo.InsertTag(tag)
        
    #création du matériau pour que les couleurs s'affichent
    mat = c4d.BaseMaterial(c4d.Mmaterial)
    mat.SetName('déblais_remblais')
    shd =  c4d.BaseShader(c4d.Xvertexmap)
    shd[c4d.SLA_DIRTY_VMAP_OBJECT] = tag
    
    mat[c4d.MATERIAL_COLOR_SHADER] = shd
    mat.InsertShader(shd)
    mat.Message(c4d.MSG_UPDATE)
    mat.Update(True, True)
    
    #tag texture sur objet
    tag_tex = c4d.TextureTag()
    tag_tex.SetMaterial(mat)
    polyo.InsertTag(tag_tex)
    
    doc.InsertMaterial(mat)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,mat)

    doc.InsertObject(polyo)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,polyo)
    doc.EndUndo()
    c4d.EventAdd()


    return

# Execute main()
if __name__=='__main__':
    main()
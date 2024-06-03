import c4d
from c4d import gui
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

# Main function
def main():
    fn = '/Users/olivierdonze/Documents/TEMP/Pictet_Rochemont_01.jpg'

    doc.StartUndo()
    #MATERIAU
    mat = c4d.BaseMaterial(c4d.Mmaterial)

    shd = c4d.BaseList2D(c4d.Xbitmap)
    shd[c4d.BITMAPSHADER_FILENAME] = fn

    mat[c4d.MATERIAL_COLOR_SHADER] = shd
    mat.InsertShader(shd)
    mat[c4d.MATERIAL_PREVIEWSIZE]=12#taille de pr\visualisation
    mat.Message(c4d.MSG_UPDATE)
    mat.Update(True, True)
    #mat.SetName(nom_img)
    mat[c4d.MATERIAL_USE_REFLECTION] = False
    doc.InsertMaterial(mat)
    doc.AddUndo(c4d.UNDOTYPE_NEW,mat)


    #SPHERE environnement
    sphere = c4d.BaseObject(c4d.Osphere)
    sphere.InsertTag(c4d.BaseTag(c4d.Tphong))
    sphere.SetName('sphere_StreetView')
    sphere[c4d.PRIM_SPHERE_RAD] = 10000

    tg_tex = c4d.BaseTag(c4d.Ttexture)
    tg_tex[c4d.TEXTURETAG_MATERIAL] = mat
    tg_tex[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_SPHERICAL
    tg_tex[c4d.TEXTURETAG_LENGTHX] = -1 #pour que l'image soit dans le bon sens
    sphere.InsertTag(tg_tex)


    doc.InsertObject(sphere)
    doc.AddUndo(c4d.UNDOTYPE_NEW,sphere)

    #CAMERA
    bd = doc.GetRenderBaseDraw()

    cam = c4d.BaseObject(c4d.Ocamera)
    cam.SetName('camera_StreetView')
    #tag de protection
    tg_prot = c4d.BaseTag(c4d.Tprotection)
    tg_prot[c4d.PROTECTION_R_X] = False
    tg_prot[c4d.PROTECTION_R_Y] = False
    tg_prot[c4d.PROTECTION_R_Z] = False
    cam.InsertTag(tg_prot)

    bd.SetSceneCamera(cam)

    doc.InsertObject(cam)
    doc.AddUndo(c4d.UNDOTYPE_NEW,cam)


    doc.EndUndo()
    c4d.EventAdd()



# Execute main()
if __name__=='__main__':
    main()
import c4d
import json
from pathlib import Path

CONTAINER_ORIGIN = 1032159

NAME_PARENT = "SITG_rasters_collection"

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


def creer_mat(fn, doc, name_mat = None):
    relatif = False
    docpath = doc.GetDocumentPath()

    #TODO regarder si les textures sont dans le chemin
    #if c4d.IsInSearchPath(fn.name, docpath):
        #relatif = True
    mat = c4d.BaseMaterial(c4d.Mmaterial)
    if not name_mat : name_mat = fn.stem
    mat.SetName(name_mat)
    shd = c4d.BaseList2D(c4d.Xbitmap)

    if relatif:
        shd[c4d.BITMAPSHADER_FILENAME] = fn.name
    else:
        shd[c4d.BITMAPSHADER_FILENAME] = str(fn)

    mat[c4d.MATERIAL_COLOR_SHADER] = shd
    mat[c4d.MATERIAL_USE_REFLECTION] = False
    mat[c4d.MATERIAL_COLOR_MODEL] = c4d.MATERIAL_COLOR_MODEL_ORENNAYAR
    mat.InsertShader(shd)
    mat[c4d.MATERIAL_USE_SPECULAR]=False

    mat[c4d.MATERIAL_USE_ALPHA]=True
    
    #si on a une image .png c'est qu'il y a de la transparence
    #on fait un système avec un shader fusion pour pouvoir animer l'apparition'
    #qui contient le png dans le channel de base
    #et une couleur dans le channel mask
    if fn.suffix == '.png' :
        shd_fusion =  c4d.BaseList2D(c4d.Xfusion)      
        shd_a_bmp = c4d.BaseList2D(c4d.Xbitmap)
        shd_color = c4d.BaseList2D(c4d.Xcolor)
        if relatif:
            shd_a_bmp[c4d.BITMAPSHADER_FILENAME] = fn.name
        else:
            shd_a_bmp[c4d.BITMAPSHADER_FILENAME] = str(fn)
        shd_fusion[c4d.SLA_FUSION_BASE_CHANNEL] = shd_a_bmp
        shd_fusion[c4d.SLA_FUSION_USE_MASK] =True
        shd_fusion[c4d.SLA_FUSION_MASK_CHANNEL]  = shd_color
        shd_color[c4d.COLORSHADER_BRIGHTNESS] = 0.

        mat[c4d.MATERIAL_ALPHA_SHADER]=shd_fusion
        
        mat.InsertShader(shd_fusion)
        mat.InsertShader(shd_a_bmp)
        mat.InsertShader(shd_color)
    #pour les jpg on met jsute un couleur dans l'alpha pour pouvoir animer l'apparition'
    else:
        shd_color = c4d.BaseList2D(c4d.Xcolor)
        mat[c4d.MATERIAL_ALPHA_SHADER]=shd_color
        #j'inverse le masque pour avoir le m^ême principe de color brightness
        #que dans le système du png brightness 0 -> opaque brightnes 1 -> transparent
        mat[c4d.MATERIAL_ALPHA_INVERT] = True
        shd_color[c4d.COLORSHADER_BRIGHTNESS] = 0
        mat.InsertShader(shd_color)
    
    mat.Message(c4d.MSG_UPDATE)
    mat.Update(True, True)
    return mat


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    pth = Path('/Users/olivierdonze/Documents/TEMP/SITG_rasters_images_extraction/Meyrin')
    pth_catalogs = Path('/Users/olivierdonze/Documents/TEMP/SITG_rasters_catalogs')

    #lecture
    catalogs = {}
    for fn in pth_catalogs.glob('*.json'):
        with fn.open() as f:
            catalogs[fn.stem] = json.load(f)


    #lecture du fichier de calage
    fn_calage = pth / 'calage.json'
    with open(fn_calage) as f:
        calage = json.load(f)
        xmin,ymin,xmax,ymax = calage

    #Création du plan de base selon la bbox
    centre = c4d.Vector((xmin+xmax)/2,0,(ymin+ymax/2))
    plan = c4d.BaseObject(c4d.Oplane)
    plan[c4d.PRIM_AXIS] = c4d.PRIM_AXIS_YP
    plan[c4d.PRIM_PLANE_WIDTH] = xmax-xmin
    plan[c4d.PRIM_PLANE_HEIGHT] = ymax-ymin
    plan[c4d.PRIM_PLANE_SUBW] = 1
    plan[c4d.PRIM_PLANE_SUBH] = 1

    origin = doc[CONTAINER_ORIGIN]
    if not origin:
        origin = centre
        doc[CONTAINER_ORIGIN] = origin

    doc.StartUndo()

    #LAYER c4d parent
    lyr_parent =c4d.documents.LayerObject()
    lyr_parent.SetName(NAME_PARENT)
    lyr_parent.InsertUnder(doc.GetLayerObjectRoot())
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,lyr_parent)

    #OBJET PARENT
    null_obj = c4d.BaseObject(c4d.Onull)
    null_obj.SetAbsPos(origin-centre)
    null_obj.SetName(NAME_PARENT)
    null_obj[c4d.ID_LAYER_LINK]= lyr_parent

    #parcours des dossiers et import des images
    for dossier in pth.iterdir():
        if not dossier.is_dir(): continue

        #création d'un Layer par dossier
        layer_c4 =c4d.documents.LayerObject()
        layer_c4.SetName(dossier.name)
        parent = doc.GetLayerObjectRoot()
        layer_c4.InsertUnder(lyr_parent)
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,layer_c4)

        #copie du PLAN
        plan_clone = plan.GetClone()
        plan_clone.SetName(dossier.name)
        plan_clone.InsertUnder(null_obj)
        plan_clone[c4d.ID_LAYER_LINK]= layer_c4

        #print(dossier.stem)
        cat = catalogs[dossier.stem]
        lst = []
        lst_images = list(dossier.glob('*.png')) + list(dossier.glob('*.jpg'))
        for fn_img in lst_images:
            #rint(' '*4,img.stem)
            id_lyr = fn_img.stem.split('_')[0]
            len_id_lyr = len(id_lyr)
            id_lyr = int(id_lyr)
            name_lyr = fn_img.stem[len_id_lyr+1:]
            debut = cat['layers'][str(id_lyr)].get('DEBUT',None)
            #si on n'a pas de début on cherche la date dans le nom
            #je commence par prendre ce qui est compris dans l'avant dernier bloc entre _
            #si cela nefocntionne pas on prend le dernier
            #il y a des dates doubles et une couche qui fionit par NB
            # voir dans le fichier : CARTES_HISTORIQUES_COLLECTION.json
            if not debut:
                try : debut = int(name_lyr.split('_')[-2])
                except : debut = int(name_lyr.split('_')[-1])
            lst.append((debut,id_lyr,name_lyr,fn_img))
            #print('    ',id_lyr,name_lyr, debut,fn_img)

        for debut,id_lyr,name_lyr,fn_img in sorted(lst,reverse = True):

            #creation du MATERIAU
            mat = creer_mat(fn_img, doc, name_mat =name_lyr)
            mat[c4d.ID_LAYER_LINK] = layer_c4
            doc.InsertMaterial(mat)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,mat)

            #TEXTURE TAG
            tag = c4d.TextureTag()
            #pour l'instant je stocke l'année de début dans le nom du tag'
            tag.SetName(str(debut))
            tag.SetMaterial(mat)
            tag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
            tag[c4d.TEXTURETAG_TILE]=False
            plan_clone.InsertTag(tag)

    doc.InsertObject(null_obj)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,null_obj)
    doc.EndUndo()
    c4d.EventAdd()











if __name__ == '__main__':
    main()
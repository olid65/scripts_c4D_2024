from typing import Optional
import c4d
import os
from glob import glob
from shutil import copyfile

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

CONTAINER_ORIGIN =1026473

def importObj(fn_obj,doc,origin_obj):

    #mise en cm des option d'importation OBJ
    plug = c4d.plugins.FindPlugin(c4d.FORMAT_OBJ2IMPORT, c4d.PLUGINTYPE_SCENELOADER)
    if plug is None:
        print ("pas de module d'import obj")
        return
    op = {}
    transl = c4d.Vector(origin_obj)
    transl.z = -transl.z

    if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):

        import_data = op.get("imexporter",None)
        if not import_data:
            print ("pas de data pour l'import obj")
            return

        import_data[c4d.OBJIMPORTOPTIONS_POINTTRANSFORM_SWAPYZ] = True

        # Change 3DS import settings
        scale = import_data[c4d.OBJIMPORTOPTIONS_SCALE]
        #print(scale)
        scale.SetUnitScale(1,c4d.DOCUMENT_UNIT_M)
        import_data[c4d.OBJIMPORTOPTIONS_SCALE] = scale

    if c4d.documents.MergeDocument(doc, fn_obj, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS):
        obj = doc.GetFirstObject()
        obj.SetName(os.path.basename(fn_obj))
        pts = obj.GetAllPoints()

        #pas tout compris mais je dois inverser l'échelle z
        #à cause de la translation
        m = c4d.utils.MatrixScale(c4d.Vector(1,1,-1))
        pts = [(p-transl)*m for p in pts]
        obj.SetAllPoints(pts)

        obj.SetAbsPos(origin_obj-doc[CONTAINER_ORIGIN])
        #obj.SetAbsScale(c4d.Vector(1,1,-1))
        obj.Message(c4d.MSG_UPDATE)
        return obj

def main() -> None:

    res = c4d.BaseObject(c4d.Onull)
    res.SetName('photomaillage_SITG')
    doc.InsertObject(res)


    first_mat = doc.GetFirstMaterial()


    #si le document n'est pas enregistré on enregistre
    path_doc = doc.GetDocumentPath()
    while not path_doc:
        rep = c4d.gui.QuestionDialog(NOT_SAVED_TXT)
        if not rep : return
        c4d.documents.SaveDocument(doc, "", c4d.SAVEDOCUMENTFLAGS_DIALOGSALLOWED, c4d.FORMAT_C4DEXPORT)
        c4d.CallCommand(12098) # Enregistrer le projet
        path_doc = doc.GetDocumentPath()

    pth = os.path.join(path_doc,'photomaillage_SITG')
    #on crée un sous-dossier dans tex
    dir_tex = os.path.join(path_doc,'tex')
    if not os.path.isdir(dir_tex):
        os.mkdir(dir_tex)
    dir_imgs = os.path.join(dir_tex,res.GetName())
    if not os.path.isdir(dir_imgs):
        os.mkdir(dir_imgs)

    for fn_obj in sorted(glob(os.path.join(pth,'*.obj'))):
        x,y = [float(v) for v in os.path.basename(fn_obj)[:-4].split('_')]

        #IMPORT FICHIER OBJ
        origin_obj = c4d.Vector(x,0,y)
        origin = doc[CONTAINER_ORIGIN]
        if not origin:
             doc[CONTAINER_ORIGIN] = origin_obj

        obj = importObj(fn_obj,doc,origin_obj)
        obj.InsertUnderLast(res)

        #image pour la texture
        dirname = os.path.basename(fn_obj)[:-4]
        name_img = 'material_0.jpg'
        fn_img = os.path.join(pth,dirname,name_img)
        name_img_dst = dirname+name_img[-4:]
        fn_img_dst = os.path.join(dir_imgs,name_img_dst)
        #on copie l'image dans tex
        copyfile(fn_img,fn_img_dst)
        #print(os.path.isfile(fn_img))

    #TRAITEMENT DES MATERIAUX
    mat = doc.GetFirstMaterial()
    while mat:
        if mat == first_mat : break
        shd = mat.GetFirstShader()
        if shd.GetType()==c4d.Xbitmap:
            name = shd[c4d.BITMAPSHADER_FILENAME].replace('/material_0','')
            shd[c4d.BITMAPSHADER_FILENAME] = name
            shd.Message(c4d.MSG_UPDATE)

            mat.SetName(name[2:])
            mat[c4d.MATERIAL_USE_REFLECTION] =False
            mat[c4d.MATERIAL_COLOR_MODEL] = c4d.MATERIAL_COLOR_MODEL_ORENNAYAR

            mat.Message(c4d.MSG_UPDATE)
        mat = mat.GetNext()

    c4d.EventAdd()


"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
import c4d

SCALE = 25000
RES = 150 #pixel/pouce

#TODO tenir compte si on est en cm ou m !!!!!!

#Activer une camera vue de haut

def GetCamera(doc):
    """
    Returns the active camera.
    Will never be None.
    """
    bd = doc.GetRenderBaseDraw()
    cp = bd.GetSceneCamera(doc)
    if cp is None: cp = bd.GetEditorCamera()

    return cp

def main():
    #calcul de la taille de l'objet sélectionné
    mg = op.GetMg()
    centre = op.GetMp() *mg
    rad = op.GetRad()
    taille_objet = c4d.Vector(rad.x*2,0,rad.z*2)
    render_size = (taille_objet / SCALE *100)/2.54 *RES
    rd = doc.GetActiveRenderData()

    #ne pas utiliser ça -> pas de mise à jour
    #rd[c4d.RDATA_XRES] = int(round(render_size.x))
    #rd[c4d.RDATA_YRES]= int(round(render_size.z))

    # yesssss grâce à https://plugincafe.maxon.net/topic/9898/13335_solvedcreate-new-renderdata/2?_=1666102536483
    rd.SetParameter(c4d.RDATA_XRES_VIRTUAL, int(round(render_size.x)), c4d.DESCFLAGS_SET_USERINTERACTION)
    rd.SetParameter(c4d.RDATA_YRES_VIRTUAL, int(round(render_size.z)), c4d.DESCFLAGS_SET_USERINTERACTION)
    rd[c4d.RDATA_PIXELRESOLUTION] = RES
    rd.Message(c4d.MSG_UPDATE)

    cam = GetCamera(doc)
    cam.SetAbsPos(centre)
    bd = doc.GetRenderBaseDraw()

    #recuperation des donnes de la vue pour la taille de la zone
    position = bd.GetSafeFrame()
    left, top, right, bottom = position["cl"], position["ct"], position["cr"], position["cb"]
    larg_fen = (right-left)
    ht_fen = bottom-top
    #calcul de l'echelle souhaitee entre le monde et la vue
    scaleX = larg_fen/taille_objet.x

    cam[c4d.CAMERA_ZOOM] = 1/taille_objet.x*1024
    cam.Message(c4d.MSG_UPDATE)
    bd.Message(c4d.MSG_UPDATE)
    #rd.Message(c4d.MSG_UPDATE)
    c4d.EventAdd()


if __name__=='__main__':
    main()
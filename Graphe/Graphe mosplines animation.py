import c4d, math

#NE PAS SELECTIONNER TOUT LE Graphe_sweepnurbs de l'étape 3
#sélectionner uniquement un null en enfant contenant le système (= un graphe de rivière)
#l'outil a été créé pour des rivières donc le sens des splines va de l'amont vers l'aval
#il faut que chaque tronçon soit séparé et disposé selon l'arborescence suivante :

#objet null
#    sweep (avec hiérarchie spline)
#    null1 (si tronçon en amont qui contiendra le même type de hiérarchie)
#    null2 (si autre tronçon en amont)
#    ...

#Attention le temps d'Animation sera au final un peu plus grand car j'utilise chaque fois une frame
#avec l'arrondi supérieur pour éviter les problèmes avec les splines trop petites !

TEMPS_ANIMATION_SYSTEME = 80 #nombre de frame pour l'anim complète du système

DEBUT_ANIMATION = 25


def CreateKey(op,id,value,frame):

    # First check if the track type already exists, otherwise create it...
    track=op.FindCTrack(id)
    if not track:
        track=c4d.CTrack(op,id)
        op.InsertTrackSorted(track)

    curve=track.GetCurve()
    key=curve.AddKey(c4d.BaseTime(frame,doc.GetFps()))

    #ATTENTION SetValue est uniquement fait pour les float, ne marche pas avec des int !!!
    #
    if type(value)==float: #type(value)==int or
        key["key"].SetValue(curve,value)
        #print key["key"].GetValue(curve,value)
    else:
        key["key"].SetGeData(curve,value)


def CreateKeyGrowth(op,frame,growth = 0.0):
    # DESCID
    id_sweep_growth = c4d.DescID(c4d.DescLevel(c4d.MGMOSPLINEOBJECT_GROWTH_END,c4d.DTYPE_REAL,0))

    #création des clefs
    CreateKey(op,id_sweep_growth,growth,frame)

def DeleteAllGrowthKeys(op):
    #efface toutes les clefs d'une piste
    id_sweep_growth = c4d.DescID(c4d.DescLevel(c4d.MGMOSPLINEOBJECT_GROWTH_END,c4d.DTYPE_REAL,0))
    track=op.FindCTrack(id_sweep_growth)
    if track :
        curve=track.GetCurve()
        if curve:
            curve.FlushKeys()

def animationMospline(mospline,frame_dprt, frame_fin):


    #on effece les clés existantes
    DeleteAllGrowthKeys(mospline)
    CreateKeyGrowth(mospline,frame_dprt,growth = 1.0)
    CreateKeyGrowth(mospline,frame_fin,growth = 0.0)


    mospline.Message(c4d.MSG_UPDATE)


# Main function
def main():


    #calcul de longueur max du système (la longueur est le nom de la mospline)
    lg_max = max([float(o.GetName()) for o in op.GetChildren()])

    frame_fin =  DEBUT_ANIMATION + TEMPS_ANIMATION_SYSTEME

    #longueur par frame
    long_par_frame = lg_max/TEMPS_ANIMATION_SYSTEME

    for mospline in op.GetChildren():
        lg = float(mospline.GetName())
        #calcul de la frame de debut en fonction de la longueur
        nb_frames = int(round(lg/long_par_frame))

        frame_dprt = frame_fin-nb_frames
        #print(frame_dprt,frame_fin)
        #return
        animationMospline(mospline,frame_dprt, frame_fin)

        #clefs d'animation
        DeleteAllGrowthKeys(mospline)
        CreateKeyGrowth(mospline,frame_dprt,growth = 0.0)
        CreateKeyGrowth(mospline,frame_fin,growth = 1.0)
        mospline.Message(c4d.MSG_UPDATE)




    #ruse de sioux pour mettre le doc à jour !!!
    #t = doc.GetTime()
    #on avance d'une frame'
    #doc.SetTime(doc.GetTime()+c4d.BaseTime(1./doc.GetFps()))
    #et on revient
    #doc.SetTime(t)

    c4d.EventAdd()






# Execute main()
if __name__=='__main__':
    main()
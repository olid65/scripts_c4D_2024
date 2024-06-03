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

TEMPS_ANIMATION_SYSTEME = 600 #nombre de frame pour l'anim complète du système

DEBUT_ANIMATION = 0


def getMaxLength(obj, lst_lg, lg_init=0):

    sweep = obj.GetDown()
    sp = sweep.GetDown().GetNext()
    #longueur de la spline
    sph = c4d.utils.SplineHelp()
    sph.InitSplineWith(sp)
    lg_init += sph.GetSplineLength()

    null_o = sweep.GetNext()
    if not null_o :
        lst_lg.append(lg_init)
    while null_o:
        getMaxLength(null_o, lst_lg, lg_init)
        null_o = null_o.GetNext()

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
    id_sweep_growth = c4d.DescID(c4d.DescLevel(c4d.SWEEPOBJECT_STARTGROWTH,c4d.DTYPE_REAL,0))

    #création des clefs
    CreateKey(op,id_sweep_growth,growth,frame)

def DeleteAllGrowthKeys(op):
    #efface toutes les clefs d'une piste
    id_sweep_growth = c4d.DescID(c4d.DescLevel(c4d.SWEEPOBJECT_STARTGROWTH,c4d.DTYPE_REAL,0))
    track=op.FindCTrack(id_sweep_growth)
    if track :
        curve=track.GetCurve()
        if curve:
            curve.FlushKeys()

def animationSysteme(null_parent,frame_dprt, long_par_frame):
    sweep = null_parent.GetDown()
    sp = sweep.GetDown().GetNext()


    #longueur de la spline
    sph = c4d.utils.SplineHelp()
    sph.InitSplineWith(sp)
    long_sp =  sph.GetSplineLength()

    #pour la frame de fin j'arrondi à la frame supérieure (math.ceil)
    #pour éviter les problèmes en cas de spline trop courtes
    #(->la frame de fin = celle du début et le sweep reste apparent)
    frame_fin = frame_dprt + math.ceil(long_sp/long_par_frame)



    #on effece les clés existantes
    DeleteAllGrowthKeys(sweep)
    CreateKeyGrowth(sweep,frame_dprt,growth = 1.0)
    CreateKeyGrowth(sweep,frame_fin,growth = 0.0)

    sweep.Message(c4d.MSG_UPDATE)

    #ensuite recursion si il y a des enfants
    null_parent = sweep.GetNext()

    frame_dprt = frame_fin

    while null_parent:
        animationSysteme(null_parent,frame_dprt, long_par_frame)
        null_parent = null_parent.GetNext()


# Main function
def main():

    #calcul de longueur max du systèm
    lst_lg = []
    getMaxLength(op, lst_lg, lg_init=0)
    lg_max = max(lst_lg)

    #longueur par frame
    long_par_frame = lg_max/TEMPS_ANIMATION_SYSTEME

    #récursion pour animer les sweep
    frame_dprt = DEBUT_ANIMATION
    animationSysteme(op,frame_dprt, long_par_frame)

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
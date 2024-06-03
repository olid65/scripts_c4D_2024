import c4d
import shapefile

NB_FRAME_TRANSITION = 25

""" Régler d'abord la durée de l'animation
    Sélectionner l'objet parent contenant tous les rasters
    crée un animation d'apparition des différentes années
    depuis l'année la plus ancienne (frame 0)
    jusqu'à l'année la plus récente (frame max)"""

def getCurveDeleted(op,canal):
    """renvoie la curve en effecant toutes les clefs"""
    descId = c4d.DescID(canal)
    track = op.FindCTrack(descId)
    #si on ne trouve pas la piste on la crée
    if not track:
        track = c4d.CTrack(op,descId)
        op.InsertTrackSorted(track)
    curve = track.GetCurve()
    #effacement des clefs existantes
    curve.FlushKeys()
    return track,curve

def addKey(doc,op,track,curve,frame,value):
    keyDict = curve.AddKey(c4d.BaseTime(float(frame)/doc.GetFps()))
    key = keyDict["key"]
    track.FillKey(doc,op,key)
    key.SetGeData(curve,value)

def addKeyFloat(doc,op,track,curve,frame,value):
    keyDict = curve.AddKey(c4d.BaseTime(float(frame)/doc.GetFps()))
    key = keyDict["key"]
    track.FillKey(doc,op,key)
    key.SetValue(curve, value)

def apparition_with_sel_restriction(tag,frame_dbt):
    track,curve = getCurveDeleted(tag,c4d.TEXTURETAG_RESTRICTION)
    addKey(doc,tag,track,curve,frame_dbt-1,'xxxxx')
    addKey(doc,tag,track,curve,frame_dbt,'')

def apparition_with_color_shader(shd,frame_dbt):
    track,curve = getCurveDeleted(shd,c4d.COLORSHADER_BRIGHTNESS)
    addKeyFloat(doc,shd,track,curve,frame_dbt-NB_FRAME_TRANSITION,1.0)
    addKeyFloat(doc,shd,track,curve,frame_dbt,0.0)

def main():

    tags = []
    for o in op.GetChildren():
        tags += [t for t in o.GetTags() if t.CheckType(c4d.Ttexture)]
    annees = [int(t.GetName()) for t in tags]
    an_dbt = min(annees)
    an_fin = max(annees)
    print(an_dbt,an_fin)
    nb_annees = an_fin-an_dbt

    fmin = doc.GetMinTime().GetFrame(doc.GetFps())
    fmax = doc.GetMaxTime().GetFrame(doc.GetFps())
    nb_frames = fmax-fmin

    frames_apparition = [int(round((an-an_dbt)*(nb_frames/nb_annees)+fmin)) for an in annees]
    for tag,frame in zip(tags,frames_apparition):
        #apparition_with_sel_restriction(tag,frame)
        mat = tag[c4d.TEXTURETAG_MATERIAL]
        if mat:
            shd = mat.GetFirstShader()
            while shd:
               if shd.CheckType(c4d.Xcolor):
                   shd[c4d.COLORSHADER_BRIGHTNESS] = 0.5
                   apparition_with_color_shader(shd,frame)
               shd = shd.GetNext()
            
            

    c4d.EventAdd()
    return


    shd = mat.GetFirstShader()
    while shd:
       if shd.CheckType(c4d.Xcolor):
           shd[c4d.COLORSHADER_BRIGHTNESS] = 0.0
       shd = shd.GetNext()
    c4d.EventAdd()

if __name__=='__main__':
    main()
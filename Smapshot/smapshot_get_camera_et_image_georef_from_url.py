import c4d
from urllib.request import urlopen
import json
from pathlib import Path
import math



doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

CONTAINER_ORIGIN = 1026473

#chemin pour enregister l'image si le doc n'est pas enregistré
pth_if_not_saved = Path('/Users/olivierdonze/Downloads')

def wgs84_to_lv95(lon,lat):
    """converti de wgs84 en chlv95 via une requete REST
       sur l'outil en ligne de swisstopo"""
    url = f'http://geodesy.geo.admin.ch/reframe/wgs84tolv95?easting={lon}&northing={lat}&format=json'
    site = urlopen(url)
    data =  json.load(site)
    return float(data['easting']),float(data['northing'])

def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)

def ATR_to_HPB(azimuth_deg, tilt_deg, roll_deg):
    # Conversion en radians
    azimuth_rad = -degrees_to_radians(azimuth_deg)
    tilt_rad = degrees_to_radians(tilt_deg)
    roll_rad = degrees_to_radians(roll_deg)

    # Normalisation des angles en radians entre -pi et pi
    #h = -(((azimuth_rad + math.pi) % (2 * math.pi)) - math.pi)
    #p = ((tilt_rad + math.pi) % (2 * math.pi)) - math.pi
    #b = ((roll_rad + math.pi) % (2 * math.pi)) - math.pi

    h = azimuth_rad
    p = tilt_rad
    b = roll_rad

    return c4d.Vector(h,p,b)

def set_new_renderdata(doc,name,width,height):
    rd = doc.GetActiveRenderData().GetClone()
    #rd = c4d.documents.RenderData()
    rd.SetName(name)
    rd[c4d.RDATA_LOCKRATIO] = False

    rd[c4d.RDATA_XRES] = width
    rd[c4d.RDATA_YRES] = height
    #ATTENTION NE PAS OUBLIER DE MODIFIER LE RATIO DU FILM SINON NE MET PAS A JOUR !!!!!!!!
    rd[c4d.RDATA_FILMASPECT] = float(width)/height

    doc.InsertRenderDataLast(rd)
    rd.Message(c4d.MSG_UPDATE)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, rd)
    return rd


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    # on peut avoir copié tout l'url -> 'https://smapshot.heig-vd.ch/visit/20290'
    # ou seulement l'id -> '20290'

    cboard = c4d.GetStringFromClipboard()
    #cboard = 'https://smapshot.heig-vd.ch/visit/20290'

    if not cboard:
        return
    id_img = None

    if cboard.isnumeric():
        id_img = int(cboard)
    elif len(cboard)>5 and cboard[:5]=='https':

        try : id_img = int(cboard.split('/')[-1])
        except : id_img = None
    if not id_img:
        return
    doc.StartUndo()
    #récupération de l'image en 1024px et l'url pour télécharger l'image full
    url = f'https://smapshot.heig-vd.ch/api/v1/images/{id_img}/attributes?lang=fr&image_width=1024'
    response = urlopen(url)
    data = json.loads(response.read())
    media = data.get('media')
    group_gltf = None
    rect_gltf = None
    if media:
        url_img = media.get('image_url')
        if url_img:
            absolu = True
            # si le doc est enregistré, on sauvegarde l'image dans le dossier tex de ce doc
            #sinon on enregistre dans pth_if_not_saved
            if doc.GetDocumentPath() :
                fn_img = Path(doc.GetDocumentPath()) / 'tex' / Path(str(id_img)+'.jpg')
                absolu = False
            else:
                fn_img = pth_if_not_saved / Path(str(id_img)+'.jpg')

            #au besoin on crée les dossiers
            fn_img.parent.mkdir(parents=True, exist_ok=True)
            #print(fn_img)
            #on enregistre l'image si elle n'existe pas
            if not fn_img.exists():
                with open(fn_img, 'wb') as f:
                    f.write(urlopen(url_img).read())

            #on crée un matériau avec l'image
            mat = c4d.BaseMaterial(c4d.Mmaterial)
            mat.SetName(id_img)
            shd = c4d.BaseList2D(c4d.Xbitmap)
            mat.InsertShader(shd)
            mat[c4d.MATERIAL_USE_LUMINANCE] = True
            mat[c4d.MATERIAL_USE_REFLECTION] = False
            mat[c4d.MATERIAL_USE_COLOR] = False
            mat[c4d.MATERIAL_LUMINANCE_SHADER] = shd
            mat[c4d.MATERIAL_PREVIEWSIZE] = c4d.MATERIAL_PREVIEWSIZE_NO_SCALE
            if absolu:
                shd[c4d.BITMAPSHADER_FILENAME] = str(fn_img)
            else:
                shd[c4d.BITMAPSHADER_FILENAME] = fn_img.name

            mat.Message(c4d.MSG_UPDATE)
            doc.InsertMaterial(mat)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, mat)

        #téléchargement du gltf
        url_gltf = media.get('model_3d_url')
        if url_gltf:
            if doc.GetDocumentPath() :
                fn_gltf = Path(doc.GetDocumentPath()) / 'tex' / Path(str(id_img)+'.gltf')
            else:
                fn_gltf = pth_if_not_saved / Path(str(id_img)+'.gltf')
            fn_gltf.parent.mkdir(parents=True, exist_ok=True)
            #print(fn_gltf)
            if not fn_gltf.exists():
                with open(fn_gltf, 'wb') as f:
                    f.write(urlopen(url_gltf).read())
            #import du gltf dans le doc
            c4d.documents.MergeDocument(doc,str(fn_gltf), c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS|c4d.SCENEFILTER_MERGESCENE, None)
            #on récupère le nom du groupe
            group_gltf = doc.GetFirstObject()
            if group_gltf:
                group_gltf.SetName(id_img)
                try : rect_gltf = group_gltf.GetDown().GetDown()
                except : rect_glt = None


    #URL pour télécharger manuellement l'image en full resolution'
    download_link = data.get('download_link')
    if download_link:
        print(download_link)

    #DONNEES DE POSE
    pose = data.get('pose')
    if pose:
        alt = pose.get('altitude')
        lat = pose.get('latitude')
        lon = pose.get('longitude')
        #conversion en ch1903
        easting,northing = wgs84_to_lv95(lon,lat)
        position = c4d.Vector(easting,alt,northing)

        # Les angles de départ en degrés
        azimuth_deg = pose.get('azimuth')
        tilt_deg = pose.get('tilt')
        roll_deg = pose.get('roll')

        # Conversion des angles ATR en HPB
        rot = ATR_to_HPB(azimuth_deg, tilt_deg, roll_deg)

        origin = doc[CONTAINER_ORIGIN]
        if not origin :
            doc[CONTAINER_ORIGIN] = c4d.Vector(easting,0,northing)
            origin = doc[CONTAINER_ORIGIN]

        #on met le groupe gltf à la même position que la caméra
        if group_gltf:
            group_gltf.SetAbsPos(position-origin)
            #on tourne de 90°en H
            group_gltf.SetAbsRot(c4d.Vector(math.pi/2,0,0))
        #on applique le materiau en projection UVW au rectangle
        tag_mat = c4d.BaseTag(c4d.Ttexture)
        if rect_gltf:
            rect_gltf.InsertTag(tag_mat)
            tag_mat[c4d.TEXTURETAG_MATERIAL] = mat
            tag_mat[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, tag_mat)

        if rect_gltf and group_gltf:

            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, rect_gltf)
            #on calcule la taille de l'image et la focale
            mg = rect_gltf.GetMg()
            pts = [p*mg for p in rect_gltf.GetAllPoints()]
            centre = sum(pts) / len(pts)

            #dimensions du rectangle pour les préférences de rendu
            width = c4d.Vector.GetDistance(pts[0], pts[3])
            height = c4d.Vector.GetDistance(pts[0], pts[2])
            fact = 1024/max((width,height))

            px_width = int(round(width*fact))
            px_height = int(round(height*fact))
            print(f'{px_width=},{px_height=}')



            #on crée un rendu avec les bonnes dimensions
            #RENDERDATA
            rd = set_new_renderdata(doc,id_img,px_width,px_height)

            doc.SetActiveRenderData(rd)


            #création de la caméra Cinema 4D (ATTENTION à créer la caméra après le renderdata)

            cam = c4d.BaseObject(c4d.Ocamera)
            cam.SetAbsPos(position -origin)
            cam.SetAbsRot(rot)
            cam.SetName(id_img)

            #Tag protection contre les mouvements
            tag = c4d.BaseTag(c4d.Tprotection)
            cam.InsertTag(tag)
            doc.InsertObject(cam)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, cam)
            doc.SetActiveObject(cam)
            #on active la caméra
            bd = doc.GetRenderBaseDraw()
            bd.SetSceneCamera(cam)

            #calcul de Field of view
            pos_cam = cam.GetMg().off
            dist_cam_centre = c4d.Vector.GetDistance(pos_cam, centre)

            angle = math.atan((width/2) / dist_cam_centre)*2
            print(f'{c4d.utils.Deg(angle)=}')
            cam[c4d.CAMERAOBJECT_FOV] = angle


            #on crée un Take pour la caméra
            takeData = doc.GetTakeData()
            if takeData is None:
                raise RuntimeError("Failed to retrieve the take data.")
            newTake = takeData.AddTake(id_img, None, None)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,newTake)
            newTake.SetChecked(True)
            newTake.SetCamera(takeData,cam)
            newTake.SetRenderData(takeData,rd)
            if newTake is None:
                raise RuntimeError("Failed to add a new take.")

            #on met le rectangle en enfant de la caméra
            mg_rect = rect_gltf.GetMg()
            rect_gltf.InsertUnder(cam)
            rect_gltf.SetMg(mg_rect)

            #on suprimme le groupe gltf
            if group_gltf:
                group_gltf.Remove()

    #creation d'un tag texture en mode projection caméra avec le matériau
    #que l'on pose sur la camera (pour que l'utilisateur puisse le mettre ensuite sur un objet)
    tag_mat = c4d.BaseTag(c4d.Ttexture)
    tag_mat[c4d.TEXTURETAG_MATERIAL] = mat
    tag_mat[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_CAMERAMAP
    tag_mat[c4d.TEXTURETAG_TILE] = False
    tag_mat[c4d.TEXTURETAG_CAMERA_FILMASPECT] = float(px_width)/px_height
    tag_mat[c4d.TEXTURETAG_CAMERA] = cam
    cam.InsertTag(tag_mat)




    doc.EndUndo()
    c4d.EventAdd()


if __name__ == '__main__':
    main()
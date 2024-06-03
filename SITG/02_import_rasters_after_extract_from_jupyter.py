import c4d
from pathlib import Path

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

CONTAINER_ORIGIN =1026473

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    path = Path('/Users/olivierdonze/Documents/TEMP/C4D_BBox')
    file_bbox = '__bbox_c4d__.txt'
    dir_imgs = 'extract'
    format_img = '*.png'

    origin = doc[CONTAINER_ORIGIN]
    with open(path/file_bbox) as f:
        xmin,ymin,xmax,ymax =[float(s) for s in f.read().split()]

    centre = c4d.Vector((xmin+xmax)/2,0,(ymin+ymax)/2)
    width = xmax-xmin
    height = ymax-ymin

    #création du plan
    plane = c4d.BaseObject(c4d.Oplane)
    plane[c4d.PRIM_PLANE_SUBW] = 1
    plane[c4d.PRIM_PLANE_SUBH] = 1
    plane[c4d.PRIM_PLANE_WIDTH]= width
    plane[c4d.PRIM_PLANE_HEIGHT] = height
    if origin:
        plane.SetAbsPos(centre-origin)

    #images et matériaux
    pth_img = path/dir_imgs
    for fn in pth_img.glob(format_img):
        mat = c4d.BaseMaterial(c4d.Mmaterial)
        shd = c4d.BaseShader(c4d.Xbitmap)
        shd[c4d.BITMAPSHADER_FILENAME] = str(fn)
        mat.InsertShader(shd)
        mat[c4d.MATERIAL_COLOR_SHADER]=shd
        mat[c4d.MATERIAL_COLOR_MODEL] = c4d.MATERIAL_COLOR_MODEL_ORENNAYAR
        mat[c4d.MATERIAL_USE_REFLECTION] = False
        mat.Message(c4d.MSG_UPDATE)
        mat.SetName(fn.stem)
        doc.InsertMaterial(mat)

    #tag texture
    tag = c4d.BaseTag(c4d.Ttexture)
    tag[c4d.TEXTURETAG_MATERIAL]=mat
    tag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
    plane.InsertTag(tag)

    doc.InsertObject(plane)
    c4d.EventAdd()



if __name__ == '__main__':
    main()
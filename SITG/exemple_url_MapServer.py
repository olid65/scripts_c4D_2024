import c4d
from c4d import gui

CONTAINER_ORIGIN =1026473



def main():
    #url = 'https://ge.ch/sitgags2/rest/services/RASTER/{shortname}/MapServer/export?bbox={xmin}%2C{ymin}%2C{xmax}%2C{ymax}&size=4096,4096&format=jpg&f=image'
    url = 'https://raster.sitg.ge.ch/arcgis/rest/services/{shortname}/MapServer/export?bbox={xmin}%2C{ymin}%2C{xmax}%2C{ymax}&size=4096,4096&format=jpg&f=image'
    o = doc[CONTAINER_ORIGIN]
    pos = op.GetMg().off
    mp = op.GetMp()
    rad = op.GetRad()

    centre = o+pos+mp

    xmin =  centre.x-rad.x
    ymin = centre.z-rad.z
    xmax = centre.x+rad.x
    ymax = centre.z+rad.z
    url_rest = url.format(shortname = "ORTHOPHOTOS_2021_EPSG2056", xmin=xmin,ymin=ymin,xmax=xmax,ymax=ymax)
    print(url_rest)
    c4d.CopyStringToClipboard(url_rest)
    return

if __name__=='__main__':
    main()
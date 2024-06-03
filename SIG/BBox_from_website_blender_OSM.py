import c4d
import urllib,json, webbrowser


doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


def wgs84_to_lv95(lat,lon):
    """converti de wgs84 en chlv95 via une requete REST 
       sur l'outil en ligne de swisstopo"""
    url = f'http://geodesy.geo.admin.ch/reframe/wgs84tolv95?easting={lat}&northing={lon}&format=json'
    site = urllib.request.urlopen(url)
    data =  json.load(site)
    return data['easting'],data['northing']

def open_webpage_prochitecture():
    url = "http://prochitecture.com/blender-osm/extent/"
    webbrowser.open_new_tab(url)

def main() -> None:
    #open_webpage_prochitecture()

    coords = c4d.GetStringFromClipboard()
    print(coords)
    coords = tuple( map(lambda s: float(s), coords.split(',')) )
    lat_min,lon_min,lat_max,lon_max = coords
    
    xmin,ymin = wgs84_to_lv95(lat_min,lon_min)
    xmax,ymax = wgs84_to_lv95(lat_max,lon_max)
    
    print(xmin,ymin,xmax,ymax)


if __name__ == '__main__':
    main()
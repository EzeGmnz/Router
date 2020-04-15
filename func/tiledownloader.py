import os
from urllib.request import urlretrieve

def getArea(topleft, rightbottom):
    directory = "SAMPLE"
    filename = os.path.join(directory, "data.osm")

    if not os.path.exists(directory):
        os.makedirs(directory)

    urlretrieve("https://api.openstreetmap.org/api/0.6/map?bbox={0},{1},{2},{3}".format(rightbottom[0], rightbottom[1], topleft[0], topleft[1]), filename)

    self.loadOsm(filename, "xml")

getArea([-78.662109,-55.478853],[-52.734375,-21.043491])
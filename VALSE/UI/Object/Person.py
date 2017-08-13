from UI.Object import Marker
from Common import CommonTools

class Person:
    name=''
    data=[]
    id=0
    def __init__(self, _id, _name, _color, _shape):
        self.id=_id
        self.name=_name
        self.marker=Marker.Marker(_color, _shape)

    def SetMarker(self,_color, _shape):
        self.marker.SetMarker(_color, _shape)

    def SetName(self, _name):
        self.name=_name
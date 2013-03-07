from PyQt4.QtCore import *
from numpy import *
class distance(object):
       def __init__(self,a,angle,distance):
             self.a = a.asPoint()
             self.xori = self.a[0]
             self.yori = self.a[1]
             self.angle = angle
             self.distance = distance
             self.xfinal =0
             self.yfinal = 0
             self.dist_x = 0
             self.dist_y = 0
             self.fet = QgsFeature()
             self.vl = QgsVectorLayer("LineString", "temporary_lines", "memory")
             self.pr = self.vl.dataProvider()
       @property
       def resultat(self):
             self.dist_x, self.dist_x = (self.distance * sin(radians(self.angle)),self.distance * cos(radians(self.angle)))
             self.xfinal, self.yfinal = (self.xori + self.dist_x, self.yori + self.dist_x)
             return self.xfinal, self.yfinal
       @property
       def x(self):
             return self.resultat[0]
       @property
       def y(self):
             return self.resultat[1]
       @property
       def final(self):
             return QgsGeometry.fromPoint(QgsPoint(self.x,self.y))
       @property
       def trace(self):
             #self.vl
             fields = { 0 : QgsField("first", QVariant.Int) }
             #pr = vl.dataProvider()
             self.pr.addAttributes( [ QgsField("first", QVariant.Int)])
             self.fet.setGeometry(QgsGeometry.fromPolyline( [ QgsPoint(self.xori , self.yori ), QgsPoint(self.x, self.y) ] ))
             self.pr.addFeatures( [ self.fet ] )
             self.vl.updateExtents()
             self.vl.updateFieldMap()
             QgsMapLayerRegistry.instance().addMapLayer(self.vl)

resultat
>>> p = distance(a, 20, 100)
>>> p.trace
>>> p.origine
>>> p.arrive
>>> z = distance(a,95, 100)
>>> z.trace
>>> z.origine
>>> z.arrive
>>> z.x
231109.35646980916
>>> z.y
110759.10542572523
>>> f = distance(a,25, 100)
>>> f.trace
>>> f.origine
>>> f.arrive
>>> l = distance(a,25, 230)
>>> l.trace
>>> l = distance(a,230,100)
>>> l.trace
>>> l.origine
>>> l.arrive
>>> l = distance(a,310,100)
>>> l.trace
>>> g = distance(a,310,100)
>>> g.trace
>>> g.origine
>>> g.arrive
>>> i = distance(a,0,100)
>>> i.trace
>>> i.origine
>>> i.arrive
>>> e = distance(a,90,100)
>>> e.trace
>>> e.origine
>>> e.arrive
t = distance(a,180,100)
t.trace
t.origine
t.arrive
#cheminement
a1 = distance(t.final,50,100)
a1.trace
a1.origine
a1.arrive
a2 = distance(a1.final,110,100)
a2.trace
a3 = distance(a2.final,210,100)
a3.trace

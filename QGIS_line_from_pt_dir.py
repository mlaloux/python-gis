''' création d'une ligne à partir d'un point, d'une direction (en degrés) et d'une distance
line creation from a point, a direction (in degrees) and a distance
for QGIS master with the new python API
M. Laloux 2013'''



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
>>> pt = QgsGeometry.fromPoint(QgsPoint(231009.737,110767.821))
>>> newp = distance(pt,20,100)
>>> pt.resultat
(231043.93901433257, 110861.79026207859)
>>> pt.x
231043.93901433257
>>> pt.y
110861.79026207859
>>> p.final
<qgis.core.QgsGeometry object at 0x12afd9200>
>>> pt.trace
>>> pt.origine
>>> pt.arrive
>>> z = distance(pt,95, 100)
>>> z.trace
>>> z.origine
>>> z.arrive
>>> z.x
231109.35646980916
>>> z.y
110759.10542572523

# cheminement 
>>> q = distance(pt.final,80,200)
>>> q.x
231240.900564935
>>> q.y
110896.51989761197
>>> q.trace
>>> 
 
 
 
 
 

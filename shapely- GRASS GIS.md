 One thing that is not enough highlighted is the ability to use  the Python geospatial modules like Shapely of Sean Gillies or PySAL in GRASS GIS. It brings very interesting complementary treatments.

In the Python shell:   

    import grass.script as grass
    gisbase = os.environ['GISBASE']
    gisdb="/Users/me/grassdata"
    location="geol"
    mapset="faults"
    import grass.script.setup as gsetup
    gsetup.init(gisbase, gisdb, location, mapset)
    vector="mypoints"
    mypt = grass.read_command("v.to.db", flags="p", map=vector, type="point", option="coor", units="meters", quiet="True")
    mypt = mypt.split("\n")
    xyz = []
    for i in mypt:
      xyz.append(mypt[i].split("|")



and now it is possible to use Shapely:

    from shapely.geometry import Point
    point = Point(float(xyz[0][1]),float(xyz[0][2]))
    point.wkt
    'POINT (115421.3014247910032282 116774.7652432390023023)' 











2) Finally, switching from Shapely geometries to GRASS GIS vector is not very complicated
 - A single line in Shapely:
 
    >>>  line.wkt
    'LINESTRING (122286.3249999999970896 120453.2514999999984866, 123404.2657999999937601 119175.6049000000057276, 123510.7363999999943189 117445.4584000000031665, 124362.5007999999943422 115875.0178000000014435)'
            or
    >>> list(line.coords)
    [(122286.325, 120453.2515), (123404.26579999999, 119175.60490000001), (123510.73639999999, 117445.4584), (124362.50079999999, 115875.0178)]

- therefore with Grass temporary files:

1) creation of a vector layer:    

    >>> grass.read_command("v.edit",tool="create",map="testfromshapely")
    >
2) creation of the temporary file  

    >>> tempfile = grass.tempfile()
    >>> pfish = open(tempfile, 'w')
    >>> print>> pfish, "L", str(len(line.coords)), "1"
    >>> for i in line.coords:
          print>> pfish,str(i[0]),str(i[1])
          ...
    >>> print>> pfish, "1", 1
    >>> pfish.close()

3) the resulting temporary file 

    L 4 1
    122286.325 120453.2515
    123404.2658 119175.6049
    123510.7364 117445.4584
    124362.5008 115875.0178
    1 1

4) adding the temporary file to the vector layer:

    >>> grass.run_command("v.edit", input=tempfile, flags="n", tool="add", map="testfromshapely", snap="node", thresh="1")
    1 features added
    Building topology for vector map <testfromshapely>...
    Registering primitives...
    1 primitives registered
    4 vertices registered
    ...
    Number of nodes: 2
    ...

5) you can also create a point layer with the vertices

    >>> grass.read_command("v.edit",tool="create",map="points_shapely")
    >>> tempfile = grass.tempfile()
    >>> pfish = open(tempfile, 'w')
    >>> for index, i in enumerate(line.coords):
    ...      print>> pfish,"P 1 1"
    ...      print>> pfish,str(i[0]),str(i[1])...      print>> pfish, "1 " + str(index+1)...
    >>> pfish.close()

6) the resulting temporary file

    P 1 1
    122286.325 120453.2515
    1 1
    P 1 1
    123404.2658 119175.6049
    1 2
    P 1 1
    123510.7364 117445.4584
    1 3
    P 1 1
    124362.5008 115875.0178
    1 4

7) adding the temporary file to the vector layer:

    >>> grass.run_command("v.edit", input=tempfile, flags="n", tool="add", map="points_shapely", snap="node", thresh="1")
    4 features added
    Building topology for vector map <points_shapely>...
    Registering primitives...
    4 primitives registered
    4 vertices registered
    ...
    Number of nodes: 4
    .... 
Results:

![](http://osgeo-org.1560.x6.nabble.com/file/n4985178/resultshapely_grass.jpg)

You can use all the functions of Shapely and add the results to the associated table , if you want:

    >>> line.length
    5217.6727474454265
etc.

You can also transform the lines in a Graph with the networkx module and the distances between the points as weight (see http://doc.lizardsystem.nl/libs/nens/_modules/nens/geom.html)

    >>> from shapely.geometry import Point
    >>> import networkx as nx
1) creation of a graph  

    >>> G = nx.Graph()
    >>> from shapely.geometry.point import Point
    >>> points = [i for i in line.coords]
2) adding the points to the graph with the distance between the points as weight

    >>> for D, A in zip(points, points[1:]):
    ...       G.add_edge(D, A, {'weight': Point(D).distance(Point(A))})
...
3) results

    >>> G.number_of_edges()
    3
    >>> G.number_of_nodes()
    4
    >>> G.adjacency_list()
    [[(123510.73639999999, 117445.4584)], [(123510.73639999999, 117445.4584), (122286.325, 120453.2515)], [(123404.26579999999, 119175.60490000001), (124362.50079999999, 115875.0178)], [(123404.26579999999, 119175.60490000001)]]

and return the results in GRASS GIS with the same temporary files method.

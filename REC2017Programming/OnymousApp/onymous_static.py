#the following program gets data from the csv file provided and created a dictionary of the data
#it is then sent a to an open source Dijksta function
#the function uses a class called priorityDictionary which is also open source

import sys
from priodict import priorityDictionary
import Dijkstra

# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002
def Dijkstra(G, start, end=None):
    """
    Find shortest paths from the  start vertex to all vertices nearer
    than or equal to the end.

    The input graph G is assumed to have the following representation: A
    vertex can be any object that can be used as an index into a
    dictionary. G is a dictionary, indexed by vertices.  For any vertex
    v, G[v] is itself a dictionary, indexed by the neighbors of v.  For
    any edge v->w, G[v][w] is the length of the edge. This is related to
    the representation in <http://www.python.org/doc/essays/graphs.html>
    where Guido van Rossum suggests representing graphs as dictionaries
    mapping vertices to lists of outgoing edges, however dictionaries of
    edges have many advantages over lists: they can store extra
    information (here, the lengths), they support fast existence tests,
    and they allow easy modification of the graph structure by edge
    insertion and removal. Such modifications are not needed here but
    are important in many other graph algorithms. Since dictionaries
    obey iterator protocol, a graph represented as described here could
    be handed without modification to an algorithm expecting Guido's
    graph representation.

    Of course, G and G[v] need not be actual Python dict objects, they
    can be any other type of object that obeys dict protocol, for
    instance one could use a wrapper in which vertices are URLs of web
    pages and a call to G[v] loads the web page and finds its outgoing
    links.

    The output is a pair (D,P) where D[v] is the distance from start to
    v and P[v] is the predecessor of v along the shortest path from s to
    v.

    Dijkstra's algorithm is only guaranteed to work correctly when all
    edge lengths are positive. This code does not verify this property
    for all edges (only the edges examined until the end vertex is
    reached), but will correctly compute shortest paths even for some
    graphs with negative edges, and will raise an exception if it
    discovers that a negative edge has caused it to make a mistake.
    """

    D = {}  # dictionary of final distances
    P = {}  # dictionary of predecessors
    Q = priorityDictionary()  # estimated distances of non-final vertices
    Q[start] = 0

    for v in Q:
        D[v] = Q[v]
        if v == end:
            break

        for w in G[v]:
            vwLength = D[v] + G[v][w]
            if w in D:
                if vwLength < D[w]:
                    raise ValueError("Dijkstra: found better path to already-final vertex")
            elif w not in Q or vwLength < Q[w]:
                Q[w] = vwLength
                P[w] = v

    return (D, P)


def shortestPath(G, start, end):
    """
    Find a single shortest path from the given start vertex to the given
    end vertex. The input has the same conventions as Dijkstra(). The
    output is a list of the vertices in order along the shortest path.
    """

    D, P = Dijkstra(G, start, end)
    Path = []
    while 1:
        Path.append(end)
        if end == start:
            break
        end = P[end]
    Path.reverse()
    return Path






FROM_NODE = 0
TO_NODE = 1
AVG_KMH = 2
DIST_METRES = 3
edge_wts = {}
with open('5x5.csv') as f:
	lines = f.read().splitlines()
	for line in lines:
		edge = line.split(',')
		et_sec = 3600.0*int(edge[DIST_METRES])*1000.0/float(edge[AVG_KMH])
		edge_wts[edge[FROM_NODE],edge[TO_NODE]] = et_sec

	start_node = 22
	end_node = 2
print(edge_wts)
print(type(edge_wts))
graph_dict = {  "0":{"2": 28375316.1 , "5": 10878460.9},
                "2":{"0": 25715051.04, "4": 28081670.86},
		"4":{"2": 28081670.86, "9": 16886675.55},
		"5":{"0": 27118473.83, "6": 11622713.8, "10": 17378780.99},
		"6":{"5": 21331858.54, "7": 19296223.84, "11": 19970598.84},
		"7":{"6": 14081339.29, "8": 8904682.791},
		"8":{"7": 12517784.24, "9": 9134486.28},
		"9":{"14": 8905765.865},
		"10":{"5": 11228303.64, "11": 12882140.34},
		"11":{"6": 14941582.56, "10": 11076099.47 , "12": 20231917.72, "16": 14067033.32},
		"12":{"7": 11246544.03, "11": 15722583.74 , "13": 10661717.52},
		"13":{"8": 11234201.9, "14": 14701728.47 , "18": 16557814.37},
		"14":{"8": 21221305.8, "19": 26369762.67, "9": 15262213.3},
		"15":{"10": 9743906.675},
		"16":{"11": 11143613.32, "17": 18992684.3},
		"17":{"12": 10846749.49, "16": 11692455.93},
		"18":{"5": 21331858.54, "6": 19296223.84, "17": 12434123.61},
		"19":{"14": 22897364.68, "18": 15058088.67},
		"20":{"21": 16550709.54},
		"21":{"16": 21331858.54, "20": 19296223.84, "22": 21331858.54},
		"22":{"17": 16550709.54, "21": 35116241.26, "24": 28676595.05},
		"24":{"16": 18131985.75}
	}
a = shortestPath(graph_dict,0,24)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libraries
import igraph as ig
import pandas as pd
import numpy as np
import json
import re
import sys
import argparse
from datetime import datetime
from copy import deepcopy

# import compiled library
# https://github.com/franktakes/teexgraph
from pyteexgraph import Graph, Scope


# import custom library
import common

def compute_graph(source: str)->ig.Graph:
    """
    Parse all AS pathes to build the ASes graph
    """
    g = ig.Graph()
    edges = []
    vertices = []
    count = 0

    start_time = datetime.now()

    with open(source,'r') as s:
        for l in s:
            if count % 10000==0:
                common.Affich.success(0,"Nb of pathes : " + str(count))
                common.Affich.success(1,"Nb of vertices : " + str(len(vertices)))
                common.Affich.success(1,"Nb of edges : " + str(len(edges)))

            path = l.strip().split(' ')
            if len(path) > 1:
                for i in range(len(path)-1):
                    if path[i]!=path[i+1] and (path[i], path[i+1]) not in edges:
                        edges.append((path[i], path[i+1]))
                        if path[i] not in vertices:
                            vertices.append(path[i])
                        if path[i+1] not in vertices:
                            vertices.append(path[i+1])
            count+=1

    common.Affich.success(0,"Nb of pathes : " + str(count))
    common.Affich.success(1,"Nb of vertices : " + str(len(vertices)))
    common.Affich.success(1,"Nb of edges : " + str(len(edges)))

    g.add_vertices(vertices)
    g.add_edges(edges)

    common.Affich.success(0,"Graph extracted successfully")
    common.Affich.success(1,"Nb of vertices : " + str(g.vcount()))
    common.Affich.success(1,"Nb of edges : " + str(g.ecount()))
    end_time = datetime.now()
    common.Affich.success(0,"Duration: {}".format(end_time - start_time))
    return g

def compute_graph_fr(source: str)->ig.Graph:
    """
    Parse all AS pathes to build the ASes graph of french ASes
    Keep all french ASes seen in bview
    But only links between two french ASes
    """
    g = ig.Graph()
    edges = []
    vertices = []
    count = 0

    as_fr = common.load_json_file(common.DATAS_DIR+"AS_FR.json")

    start_time = datetime.now()

    with open(source,'r') as s:
        for l in s:
            if count % 10000==0:
                common.Affich.success(0,"Nb of pathes : " + str(count))
                common.Affich.success(1,"Nb of vertices : " + str(len(vertices)))
                common.Affich.success(1,"Nb of edges : " + str(len(edges)))

            path = l.strip().split(' ')
            if len(path) > 1:
                for i in range(len(path)-1):
                    # both neighbors are french ASes
                    if path[i] in as_fr and path[i+1] in as_fr and path[i]!=path[i+1] and (path[i], path[i+1]) not in edges and (path[i+1], path[i]) not in edges:
                        edges.append((path[i], path[i+1]))
                    if path[i] in as_fr and path[i] not in vertices:
                        vertices.append(path[i])
                    if path[i+1] in as_fr and path[i+1] not in vertices:
                        vertices.append(path[i+1])
            count+=1

    common.Affich.success(0,"Nb of pathes : " + str(count))
    common.Affich.success(1,"Nb of vertices : " + str(len(vertices)))
    common.Affich.success(1,"Nb of edges : " + str(len(edges)))

    g.add_vertices(vertices)
    g.add_edges(edges)

    common.Affich.success(0,"Graph extracted successfully")
    common.Affich.success(1,"Nb of vertices : " + str(g.vcount()))
    common.Affich.success(1,"Nb of edges : " + str(g.ecount()))
    end_time = datetime.now()
    common.Affich.success(0,"Duration: {}".format(end_time - start_time))
    return g


def load_graph(source: str)->ig.Graph:
    """
    Load a graph from the given source file
    """
    g = ig.Graph.Read_GML(source)
    common.Affich.success(0,"Graph loaded successfully")
    common.Affich.success(1,"Nb of vertices : " + str(g.vcount()))
    common.Affich.success(1,"Nb of edges : " + str(g.ecount()))
    return g

def getArgParser():
    """
    Manage command line arguments
    """
    argparser = argparse.ArgumentParser( add_help=True, description="""Compute graph""" )
    argparser.add_argument("-c", "--compute", dest="compute", help="Compute graph of ASes from dump file")
    argparser.add_argument("-f", "--fr", dest="fr", help="Compute graph of french ASes from dump file")
    argparser.add_argument("-l", "--load", dest="load", help="Load graph from graph file")
    return argparser

def edges_2_txtfile(g:ig.Graph, filename:str):
    """
    Write graph into text file
    1 edge per line
    """
    with open(filename,"w") as f:
        for e in g.get_edgelist():
            f.write(str(e[0]) + " " + str(e[1]) + "\n")


def calc_diameter(f:str):
    """
    Graph diameter using pyteexgraph
    Input file needs to be a text file with one egde per line
    """
    g = Graph(filename=f, directed=False)
    common.Affich.success(0,"Loaded : " + str(g.isLoaded()))
    common.Affich.success(0, "Average Degree : " + str(g.averageDegree(Scope.FULL)))

    g_undirected = deepcopy(g)
    g_undirected.makeUndirected()
    g_undirected.computeWCC()
    common.Affich.success(0, "Diameter BD : " + str(g_undirected.diameterBD()))

def vertices_above_degree(g:ig.Graph, d:int):
    count = 0
    common.Affich.success(0, "Vertices with degree above : " + str(d))
    for v in g.vs:
        if g.degree(v) > d:
            count += 1
            common.Affich.success(1, "AS" + str(v['name']))
    common.Affich.success(1, "Total : " + str(count))

def vertices_under_degree(g:ig.Graph, d:int):
    count = 0
    common.Affich.success(0, "Vertices with degree under : " + str(d))
    for v in g.vs:
        if g.degree(v) <= d:
            count += 1
            #common.Affich.success(1, "AS" + str(v['name']))
    common.Affich.success(1, "Total : " + str(count))

if __name__ == "__main__":

    common.setup()
    args = getArgParser().parse_args()

    if args.compute:
        g = compute_graph(args.compute)
        g.write_gml("bgp_GML.gml")

    if args.fr:
        g = compute_graph_fr(args.fr)
        g.write_gml("bgp_fr_GML.gml")

    if args.load:
        g = load_graph(args.load)

    common.Affich.success(0,"Max degree : " + str(g.maxdegree()))
    common.Affich.success(0,"Diameter : " + str(g.diameter()))
    #edges_2_txtfile(g, "bgp_graph.txt")

    #calc_diameter("bgp_graph.txt")

    #vertices_above_degree(g, 100)
    #vertices_under_degree(g, 0)




    #g.simplify()
    #common.Affich.success(0,"Graph simplified")
    #common.Affich.success(1,"Nb of vertices : " + str(g.vcount()))
    #common.Affich.success(1,"Nb of edges : " + str(g.ecount()))

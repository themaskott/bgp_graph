#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import igraph as ig
import pandas as pd
import numpy as np
import json
import re
import sys

import argparse
from datetime import datetime

import common


def compute_graph(source: str)->ig.Graph:
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

def load_graph(source: str)->ig.Graph:

        g = ig.Graph()
        g.Read_GraphML(source)
        common.Affich.success(0,"Graph loaded successfully")

        return g




def getArgParser():
    """
    Manage command line arguments
    """

    argparser = argparse.ArgumentParser( add_help=True, description="""Compute graph""" )

    argparser.add_argument("-c", "--compute", dest="compute", help="Compute graph from dump file")
    argparser.add_argument("-l", "--load", dest="load", help="Load graph from graph file")

    return argparser


if __name__ == "__main__":


    common.setup()

    args = getArgParser().parse_args()

    if args.compute:
        g = compute_graph(args.compute)
        g.write_graphml("bgp_graph.gml")


    if args.load:
        g = load_graph(args.load)

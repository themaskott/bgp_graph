#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import igraph as ig
import pandas as pd
import numpy as np
import json
import re
import sys
import common
from datetime import datetime


def compute_graph(source: str)->ig.Graph:
    g = ig.Graph()
    edges = []
    vertices = []
    k = 0
    with open(source,'r') as s:
        for l in s:
            if k % 10000==0:
                common.Affich.success(0,"Nb of pathes : " + str(k))
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
            k+=1

    common.Affich.success(0,"Nb of pathes : " + str(k))
    common.Affich.success(1,"Nb of vertices : " + str(len(vertices)))
    common.Affich.success(1,"Nb of edges : " + str(len(edges)))

    g.add_vertices(vertices)
    g.add_edges(edges)

    common.Affich.success(0,"Graph extracted successfully")
    common.Affich.success(1,"Nb of vertices : " + str(g.vcount()))
    common.Affich.success(1,"Nb of edges : " + str(g.ecount()))

    return g





if __name__ == "__main__":


    common.setup()

    # source file :
    # bgpdump -M -O dump.txt bview.gz
    # cut -d "|" 2022-07-18-rrc06-dump.txt -f7 | sort | uniq > uniq_path.txt
    source = sys.argv[1]
    start_time = datetime.now()
    g = compute_graph(source)
    end_time = datetime.now()
    g.write_graphml("bgp_graph.xml")
    common.Affich.success(0,"Duration: {}".format(end_time - start_time))

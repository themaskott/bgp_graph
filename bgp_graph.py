#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import python libraries
import argparse

# import custom library
import common, autnums
from compute import *


def getArgParser():
    """
    Manage command line arguments
    """
    argparser = argparse.ArgumentParser( add_help=True, description="""Compute graph""" )
    argparser.add_argument("-c", "--compute", dest="compute", help="Compute graph of ASes from dump file")
    argparser.add_argument("-f", "--fr", dest="fr", help="Compute graph of french ASes from dump file")
    argparser.add_argument("-fa", "--frall", dest="fr_all", help="Compute graph of french ASes and foreign neighbor from dump file")
    argparser.add_argument("-l", "--load", dest="load", help="Load graph from graph file")
    return argparser


if __name__ == "__main__":

    common.setup()
    args = getArgParser().parse_args()

    if args.compute:
        g = compute_graph(args.compute)
        g.write_gml(common.RESULTS_DIR+"bgp_GML.gml")
        edges_2_txtfile(g, common.RESULTS_DIR+"bgp_graph.txt")
        calc_diameter(common.RESULTS_DIR+"bgp_graph.txt")


    if args.fr:
        g = compute_graph_fr_only(args.fr)
        g.write_gml(common.RESULTS_DIR+"bgp_fr_GML.gml")
        edges_2_txtfile(g, common.RESULTS_DIR+"bgp_fr_graph.txt")
        calc_diameter(common.RESULTS_DIR+"bgp_fr_graph.txt")

    if args.fr_all:
        g = compute_graph_fr_all(args.fr_all)
        g.write_gml(common.RESULTS_DIR+"bgp_fr_all_GML.gml")
        edges_2_txtfile(g, common.RESULTS_DIR+"bgp_fr_all_graph.txt")
        calc_diameter(common.RESULTS_DIR+"bgp_fr_all_graph.txt")
        count_country(g)


    if args.load:
        g = load_graph(args.load)


    add_vertices_attributes(g)

    #metrics(g)

    #print(g.degree_distribution())


    #g.simplify()
    #common.Affich.success(0,"Graph simplified")
    #common.Affich.success(1,"Nb of vertices : " + str(g.vcount()))
    #common.Affich.success(1,"Nb of edges : " + str(g.ecount()))

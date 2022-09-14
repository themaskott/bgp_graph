#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from os import path
import json

import autnums

DATAS_DIR = "datas/"
RESULTS_DIR = "results/"

def setup():
    """
    Check for existing input and output directories
    Set output filenames
    """

    if not path.isdir(DATAS_DIR): mkdir("datas", 0o755)
    if not path.isdir(RESULTS_DIR): mkdir(RESULTS_DIR, 0o755)
    if not path.isfile(DATAS_DIR+"AS_FR.json"): autnums.extract_AS(autnums.update_AS(), True)
    if not path.isfile(DATAS_DIR+"AS.json"): autnums.extract_AS(autnums.update_AS(), False)


def load_json_file(source:str)->dict:
    """
    Load a json file into a dict
    """
    with open(source, "r") as jf:
        return json.load(jf)


def save_json_file(d:dict, name:str):
    """
    Save dict to json file
    """
    with open(name,"w") as jf:
        json.dump(d, jf, indent=4)

class Affich(Enum):
    """
    Code inspired by https://github.com/MrrRaph
    """
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    @staticmethod
    def success(indent:int, msg:str):
        print("\t" * indent + f"[{Affich.GREEN.value}+{Affich.RESET.value}] {msg}")

    @staticmethod
    def info(indent:int, msg:str):
        print("\t" * indent + f"[{Affich.BLUE.value}*{Affich.RESET.value}] {msg}")

    @staticmethod
    def error(indent:int, msg:str):
        print("\t" * indent + f"[{Affich.RED.value}!{Affich.RESET.value}] {msg}")

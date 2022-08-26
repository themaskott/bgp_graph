#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from os import path

DATAS_DIR = "datas/"
RESULTS_DIR = "results/"

def setup():
    """
    Check for existing input and output directories
    Set output filenames
    """

    if not path.isdir(DATAS_DIR): mkdir("datas", 0o755)
    if not path.isdir(RESULTS_DIR): mkdir(RESULTS_DIR, 0o755)


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

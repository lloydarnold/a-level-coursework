import matplotlib.pyplot as plt
import sys
import numpy as np
import os
import re

PROJECT_NAME = "test_project"


def label_graph(title=None, xLabel=None, yLabel=None):
    if not (title and xLabel and yLabel):
        return
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)


def find_dirs():
    base_path = os.path.join(os.getcwd(), PROJECT_NAME)
    try:
        directories = [f.path for f in os.scandir(base_path) if f.is_dir()]
    except FileNotFoundError:
        print("error, file path specified does not exist. epoch number entered was %s" %genReached)
        print("file path was %s " % path)
        return None
    return directories


def get_meta(directories=None):
    rawMeta = []
    for dir in directories:
        fMeta = open(dir + "/meta.txt", "r")
        rawMeta.append(fMeta.readlines())
        fMeta.close()
    return rawMeta


def format_data(data=None):
    print(data)
    print(re.split("\d\d+[a-zA-Z]", strip_brackets_and_whitespace(data)))
    return re.split("\d\d+[a-zA-Z]", strip_brackets_and_whitespace(data))


def strip_brackets_and_whitespace(input):
    return input.rstrip().replace('[', '').replace(']', '')


def format_meta(raw=None):
    meta = []
    print(raw)
    for genMeta in raw:
        meta.append(format_data(str(genMeta)))
    return meta


def get_x():
    dirs = find_dirs()
    meta = get_meta(dirs)
    print(meta)
    meta = format_meta(meta)
    print(meta)


def get_y():
    pass


def main():
    get_x()
    x = [1,2,3]
    y = [2,4,1]

    label_graph("Graph1", "Generations", "Win Rate")
    plt.plot(x, y)
    plt.show()




if __name__ == "__main__":
        main()

import matplotlib.pyplot as plt
import sys
import numpy as np
import os
import re

PROJECT_NAME = "opti_reversi2"


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
        print("error, file path specified does not exist")
        print("file path was %s " % path)
        return None
    return directories


def read_meta(directories=None):
    rawMeta = []
    for dir in directories:
        fMeta = open(dir + "/meta.txt", "r")
        rawMeta.append(fMeta.readlines())
        fMeta.close()
    return rawMeta


def add_separators(char1=None, char2=None, separator=None):
    if re.match("\d", char1) and re.match("[a-zA-Z]", char2):
        return ("%s%s" % (char1, separator))
    else:
        return char1


def format_data(data=None):
    newData = ""
    for i in range(0, len(data)-1):
        one, two = data[i:i+2]
        newData+= add_separators(one, two, "~")
    temp = newData + data[-1]
    return re.split("~", temp)


def strip_brackets_and_whitespace(input=None):
    return input.rstrip().replace('[', '').replace(']', '').replace('\'', '')


def format_meta(raw=None):
    meta = []
    for genMeta in raw:
        meta.append(format_data(strip_brackets_and_whitespace(str(genMeta))))
    return meta


def get_meta():
    dirs = find_dirs()
    meta = read_meta(dirs)
    meta = format_meta(meta)
    return meta


def get_num(input=""):
    tempStr = ""
    for char in input:
        if re.match("\d|\.|-", char):
            tempStr += char
    return float(tempStr)


def pick_meta(indexes=(), meta=None):
    values = [len(indexes)]
    for generation in meta:
        temp = []
        for i in indexes:
            temp.append(get_num(generation[i]))
        values.append(temp)
    return values


def get_y():
    metaData = get_meta()
    y = pick_meta((0,1), metaData)
    return y


def get_x(y):
    return list(range(1, len(y)))


def read_y_set(index, arr):
    j = []
    for item in arr:
        j.append(item[index])
    return j


def plot_data(x=None,y=None,labels=()):
    for i in range(0, y[0]):
        temp = y[1:]
        print(temp)
        plottableY = read_y_set(i, temp)
        print(x)
        print(plottableY)
        plt.plot(x, plottableY, label=labels[i])


def main():
    y = get_y()
    x = get_x(y)

    label_graph("Generations vs. Win Rate", "Generations", "Win Rate")
    plot_data(x, y, ("top win rate", "bottom win rate"))
    plt.show()


if __name__ == "__main__":
        print(get_num("wdbhhdsjbd 77811.0"))
        main()

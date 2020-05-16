import math
from pymatrix import Matrix, matrix as pymatrix


def compute_distance(vector: Matrix):
    squares = sum(x * x for x in vector.elements())
    return math.sqrt(squares)


def matrix(coordinates: tuple):
    return pymatrix([list(coordinates)])

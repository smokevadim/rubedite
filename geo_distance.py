from geopy.distance import geodesic
import numpy as np
import pandas as pd
from datetime import datetime


def calc_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        print('Function {} runs in {}'.format(func, datetime.now() - start_time))
        return result

    return wrapper


@calc_time
def load_cities():
    """
    Read data from file
    :return:
    """
    f = pd.read_excel('Населенные_пункты_РФ_название_адрес_координаты_1.xlsx', sheet_name='Лист1')
    return f


@calc_time
def make_matrix(cities, max_records=1000):
    """
    Calculate distance and fill matrix
    :param cities:
    :param max_records:
    :return:
    """
    count = len(cities) if len(cities) < max_records else max_records
    matrix = np.zeros((count, count), dtype=int)

    for x in range(count):
        a = " ".join([cities.point[x].split(' ')[1], cities.point[x].split(' ')[0]])
        for y in range(count):
            b = " ".join([cities.point[y].split(' ')[1], cities.point[y].split(' ')[0]])
            if matrix[y][x] > 0:
                matrix[x][y] = matrix[y][x]
            if a != b:
                dist = int(geodesic(b, a, ellipsoid='WGS-84').km)
                matrix[x][y] = dist
    return matrix


@calc_time
def save_matrix(matrix):
    """
    Write matrix to csv
    :param matrix:
    :return:
    """
    df = pd.DataFrame(matrix)
    df.to_csv('matrix_cities.csv', encoding='utf-8', index=False)


if __name__ == '__main__':
    cities = load_cities()
    matrix_cities = make_matrix(cities)
    save_matrix(matrix_cities)

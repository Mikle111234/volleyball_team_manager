import math
import numpy as np
from models import Metric


def evklid_func(players):
    Matrix = []
    for player_x in players:
        arr = []
        for player_y in players:
            if player_x != player_y:
                sum = 0
                for metric in player_x.metrics.all():
                    sum += math.pow(metric.value - player_y.metrics.get(parameter_id=metric.parameter_id).value, 2)
                arr.append(math.sqrt(sum))
        Matrix += arr
    dest_matrix = np.array(Matrix)
    return dest_matrix


def distribute(players):
    pass
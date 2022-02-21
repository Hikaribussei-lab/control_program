# This is test script.

import numpy as np
import random

class MercuryTestController:
    """
    テスト用のクラス
    sin関数から呼び出しのたびに一つ値を出力する。
    """

    # def __init__(self):
    #     st = np.linspace(0, 2*np.pi, 100)
    #     self.sin = np.sin(self.t)
    
    def get_data_from_mercury(self):
        return round(random.random(), 2)

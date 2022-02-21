from datetime import datetime
# import numpy as np
import random

class MercuryController:
    """
    テスト用のクラス
    sin関数から呼び出しのたびに一つ値を出力する。
    """

    # def __init__(self):
    #     st = np.linspace(0, 2*np.pi, 100)
    #     self.sin = np.sin(self.t)
    
    def get_data_from_mercury(self):
        pass
    
    def randomtest(self):
        return f"{round(random.random(), 2)}"
    
    def constanttest(self):
        return "123"
    
    def timetest(self):
        return datetime.now().strftime('%Y/%m/%d %H:%M:%S')

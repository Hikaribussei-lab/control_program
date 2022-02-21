from datetime import datetime
# import numpy as np
import random

class MercuryController:
    """
    Mercuryをコントロールするための実行クラス。
    """
    
    def get_temperature(self):
        return f"{round(random.random(), 2)}"
    
    def get_power(self):
        return f"{round(random.random(), 2)}"

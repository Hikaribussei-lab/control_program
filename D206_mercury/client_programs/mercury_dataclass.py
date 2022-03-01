from dataclasses import dataclass
import time
from typing import List

@dataclass
class MercuryData:
    """
    Mercuryから受け取ったデータを格納する。

    Attributes
    -----------
    inst_time : float
        インスタンス化されたときのUnix時間。

    temperature : List
        温度が格納されるリスト。

    power : List
        パワーが格納されるリスト。

    get_time : List
        パワーが格納されるリスト。

    elapsed_time: List
        経過時間が格納されるリスト。
    
    Methods
    -----------
    add_datas(temp: 温度, pow: パワー, gt: 取得時間)
        データをリスト型のオブジェクト変数に追加する。
    """

    inst_time: float = time.time()
    temperature: List = []
    power: List = []
    get_time: List = []
    elapsed_time: List = []

    def add_datas(self, temp: float, pow: float, gt: float):
        """
        取得したデータをオブジェクト変数に追加する。

        Args:
            temp (float): 温度
            pow (float): パワー
            gt (flaot): データ取得時間
        """

        self.temperature.append(temp)
        self.power.append(pow)
        self.get_time.append(gt)
        self._add_elapesd_time(gt)

    def _add_elapesd_time(self, time: float):
        """
        self.get_time最初の時間から、最後の時間を引いて経過時間(elapsed_time)を追加する。

        Args:
            time (float): データ取得時時間
        """

        if len(self.get_time) == 1:  # 初めの処理
            elapsed = 0.
        else:
            start = self.get_time[0]
            elapsed = time - start

        self.elapsed_time.append(elapsed)

from dataclasses import dataclass, field
from typing import List

@dataclass
class MercuryData:
    """
    Mercuryから受け取ったデータを格納する。

    Attributes
    -----------
    date_time : List
        データ取得日時(秒まで)

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

    date_time: list[str] = field(default_factory=list)
    temperature: list[float] = field(default_factory=list)
    power: list[float] = field(default_factory=list)
    get_time: list[float] = field(default_factory=list)
    elapsed_time: list[float] = field(default_factory=list)

    def add_datas(self, date: str, time: str, temp: float, pow: float, gt: float):
        """
        取得したデータをオブジェクト変数に追加する。

        Args:
            date (str): 日付
            time (str): 時間(秒まで)
            temp (float): 温度
            pow (float): パワー
            gt (flaot): データ取得時間
        """
        self.date_time.append(f"{date} {time}")
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

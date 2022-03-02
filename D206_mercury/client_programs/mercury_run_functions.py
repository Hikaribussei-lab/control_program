import csv
import igorwriter
import numpy as np

from mercury_client import MercuryClient
from mercury_dataclass import MercuryData

class UpdateGraph:
    def __init__(self) -> None:
        self.tmerge = 0.5  # mergin size of plot range

    def update_graph(self):
        """
        グラフを書く
        """
        self.MplWidget.canvas.axes1.clear()
        self.MplWidget.canvas.axes2.clear()

        et = self.data.elapsed_time

        self.MplWidget.canvas.axes1.plot(
            et, self.data.temperature, marker="o")
        self.MplWidget.canvas.axes2.plot(
            et, self.data.power, marker="o")

        self.update_plot_range(et)

        self.MplWidget.canvas.axes2.set_xlabel("Elapsed time (s)")
        self.MplWidget.canvas.axes1.set_ylabel("Temperature (K)")
        self.MplWidget.canvas.axes2.set_ylabel("Power (W)")


        self.MplWidget.canvas.draw()

    def update_plot_range(self, elapsed_time):
        """
        グラフの横軸幅を固定し、データ取得毎に更新する。

        Args:
            elapsed_time (List)): 経過時間のリスト
        """
        plot_range = float(self.plotrange.text())

        tmax = elapsed_time[-1] + self.tmerge
        if tmax < plot_range:
            tmax = plot_range

        tmin = tmax - plot_range - self.tmerge
        self.MplWidget.canvas.axes1.set_xlim(tmin, tmax)
        self.MplWidget.canvas.axes2.set_xlim(tmin, tmax)

class GetDatas(UpdateGraph):
    """
    データを取得し整形する。
    """
    def __init__(self):

        UpdateGraph.__init__(self)

        self.kinds = ["TEMP", "POW"]  # 取得するデータの名前

        self.mc = MercuryClient()
        self.data = MercuryData()

    def get_data_plot(self, order):
        """
        実際にデータを取得し描画する関数。
        RepeatedTIimer内で定期実行される。

        Args:
            order (string): Mercuryへの命令文 ex)TEMP;POW
        """
        data_string = self.mc.client_main(order)  # get data from Mersury
        if data_string != "ERROR":
            self._make_datas(data_string)
            self.update_graph()

    def _make_datas(self, data_string):
        """
        1ループ分のデータを辞書型で受け取り、今までのものと結合する。

        Args:
            data_string (string): ex) DATE:20220221,TIME:16-31-52,GETTIME:13200224.2464,TEMP:302.1,POW:120.3
        """
        data_dict = {}
        for content in data_string.split(","):
            _kind = content.split(":")[0]
            _value = content.split(":")[1]
            data_dict[_kind] = _value
        
        self.data.add_datas(date=data_dict["DATE"],
                            time=data_dict["TIME"],
                            temp=float(data_dict["TEMP"]),
                            pow=float(data_dict["POW"]),
                            gt=float(data_dict["GETTIME"]))
    
    def data_init(self):
        self.__init__()

class DownLoad:
    
    def __init__(self) -> None:
        self.csv = 1
        self.itx = 1
    
    def download(self):
        name = self.name.text()
        data_list = self.fix_data_for_download()

        if self.csv:
            self.download_as_csv(name, data_list)

        if self.itx:
            self.download_as_itx(name, data_list)

    def csv_check_action(self, state):
        if state == 2:
            self.csv = 1
        else:
            self.csv = 0

    def itx_check_action(self, state):
        if state == 2:
            self.itx = 1
        else:
            self.itx = 0

    def fix_data_for_download(self):
        data_array = np.array([], dtype="U1")
        for v in self.datas.values():
            data_array = np.append(data_array, v)

        rsize = len(self.datas.keys())
        csize = int(data_array.shape[0] / rsize)
        data_array = data_array.reshape(rsize, csize)

        return data_array

    def download_as_csv(self, name, data):
        path = f"{self.download_root}/{name}.csv"

        data_list = data.T.tolist()

        with open(path, mode="w") as f:
            writer = csv.writer(f)
            writer.writerow(self.datas.keys())
            writer.writerows(data_list)

    def download_as_itx(self, name, data):
        path = f"{self.download_root}/{name}.itx"
        wave_names = self.datas.keys()
        with open(path, mode="w") as f:
            for _wn, _d in zip(wave_names, data):
                if _wn not in ["DATE", "TIME"]:  # only for not string data
                    wave = igorwriter.IgorWave(
                        np.array(_d, dtype=float), name=_wn)
                    wave.save_itx(f)

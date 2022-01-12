"""Pythonで制御する
コントローラー:
    OptoSigma,  GSC-01  (シグマ光機，1軸ステージコントローラ GSC-01
"""
import time
import serial


class AutoStage(serial.Serial):
    """自動偏光子ホルダーに命令を送信する
    Attributes
    ----------
    is_sleep_until_stop : bool
        ステージを動かしたときに待つかのフラグ

    Methods
    -------
    raw_command(cmd)
        コントローラにコマンドを送信
    reset()
        機械原点復帰命令を送信
    jog_plus()
        +方向にジョグ運転
    jog_minus()
        -方向にジョグ運転
    stop(immediate=False)
        停止命令を送信
    is_stopped()
        ステージが停止しているかを取得
    sleep_until_stop()
        ステージが停止するまで待つ
    set_speed(spd_min=500, spd_max=5000, acceleration_time=200)
        速度設定命令を送信
    """

    # ステージを動かしたときに待つかどうかのフラグ
    is_sleep_until_stop = True

    # ステージの向きを反転させるかどうかのフラグ
    # 向きによって回転角度が反転するため，このフラグで補正する
    flip_front = False

    @property
    def um_per_pulse(self):
        return 1  # [um/pulse]

    def __del__(self):
        try:
            self.close()
        except AttributeError:
            pass

    def raw_command(self, cmd):
        """コントローラにコマンドを送信
        "OK"はTrue，"NG"はFalseと変換して返す．
        例外として，"OK"や"NG"以外の文字列が送られてきた場合は，そのままの文字列を返す．
        ret : bool or str
            OKなら``True``
            NGなら``False``
        """
        self.write(cmd.encode())
        self.write(b"\r\n")
        return_msg = self.readline().decode()[:-2]  # -2: 文字列に改行コードが含まれるため，それ以外を抜き出す．
        return (
            True
            if return_msg == "OK" 
            else False 
            if return_msg == "NG" 
            else return_msg
        )

    def reset(self):
        """機械原点復帰命令を送信"""
        ret = self.raw_command("H:1")
        if self.is_sleep_until_stop:
            self.sleep_until_stop()
        return ret

    def jog_plus(self):
        """+方向にジョグ運転を行います．
        """
        ret = self.raw_command("J:1+")
        if ret:
            return self.raw_command("G:")
        else:
            return False

    def jog_minus(self):
        """-方向にジョグ運転
        """
        ret = self.raw_command("J:1-")
        if ret:
            return self.raw_command("G:")
        else:
            return False

    def stop(self, immediate=False):
        """停止命令を送信
        """
        return (
            self.raw_command("L:1") 
            if immediate == False 
            else self.raw_command("L:E")
        )

    def is_stopped(self):
        """ステージが停止しているかを取得
        """
        return_msg = self.raw_command("!:")
        return (
            True
            if return_msg == "R"
            else False  # Ready
            if return_msg == "B"
            else return_msg  # Busy
        )

    def sleep_until_stop(self):
        """ステージが停止するまで待つ"""
        while not self.is_stopped():
            time.sleep(0.01)

    def set_speed(self, spd_min=500, spd_max=5000, acceleration_time=200):
        """速度設定命令を送信

        速度には3つのパラメータがあり，全て一括で設定します．

        Parameters
        ----------
        spd_min : int
          最小速度
          設定範囲：100～20000（単位：PPS）
        spd_max : int
          最大速度
          設定範囲：100～20000（単位：PPS）
        acceleration_time : int
          加減速時間
          設定範囲：0～1000（単位：mS）

        Notes
        -----
        最大速度は必ず最小速度以上の値を設定
        速度の設定は 100[PPS]単位、100[PPS]未満の値は切り捨て
        """
        clip = lambda v, v_min, v_max: max(v_min, min(v_max, v))
        spd_max = max(spd_max, spd_min)  # 最大速度は必ず最小速度以上の値を設定
        spd_min = clip(int(spd_min), 100, 20000)
        spd_max = clip(int(spd_max), 100, 20000)
        acceleration_time = clip(int(acceleration_time), 0, 1000)
        return self.raw_command(f"D:1S{spd_min}F{spd_max}R{acceleration_time}")

    @property
    def um(self):
        """現在のステージの position を返す"""
        pos = self._position2um(self._get_position())
        return pos
        
    @um.setter
    def um(self, pos_dst):
        """ステージを指定したpositionに動かす
        """
        pos_src = self.um
        position = self._um2position(pos_dst-pos_src)
        self._set_position_relative(position)

    def _set_position_relative(self, position):
        """相対移動パルス数設定命令と駆動命令を実行"""
        sign = "+" if position >= 0 else "-"
        ret = self.raw_command("M:1" + sign + "P" + str(abs(position)))
        if ret == False:
            return False

        ret = self.raw_command("G:")
        if self.is_sleep_until_stop:
            self.sleep_until_stop()
        return ret

    def _set_position_absolute(self, position):
        """絶対移動パルス数設定命令と駆動命令を実行"""
        sign = "+" if position >= 0 else "-"
        ret = self.raw_command("A:1" + sign + "P" + str(abs(position)))
        if ret == False:
            return False

        ret = self.raw_command("G:")
        if self.is_sleep_until_stop:
            self.sleep_until_stop()
        return ret

    def _get_position(self):
        """ステータス確認1命令を実行し，現在の座標値を取得
        Notes
        -----
        失敗することがあったので，tryで回避するようにしてforで何度か見るようにしています．
        """
        for i in range(5):
            return_msg = self.raw_command("Q:")
            try:
                return int(return_msg.split(",")[0].replace(" ", ""))
            except:
                continue

    def _um2position(self, pos):
        """角度（度）からステージ位置（移動パルス数）に変換"""
        return int(pos / self.um_per_pulse)

    def _position2um(self, position):
        """ステージ位置（移動パルス数）から角度（度）に変換"""
        return (position / self.um_per_pulse) 


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "um", 
        type=int, 
        help="angle of stage [um]"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=str,
        default="/dev/ttyUSB0",
        help="srial port name",
    )
    parser.add_argument(
        "-r",
        "--reset",
        action="store_true",
        help="determines whether to perform a reset",
    )
    args = parser.parse_args()

    # command line arguments
    port = args.port
    pos = args.um
    is_reset = args.reset

    # connect to the stage
    stage = AutoStage(port=port)

    # set speed as default
    #stage.set_speed()

    # reset (if required)
    if is_reset:
        stage.reset()

    # rotate the stage
    stage.um = pos


if __name__ == "__main__":
    main()
    
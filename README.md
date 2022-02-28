# control_program

実験装置や測定装置の制御を行うプログラム。  

# 目次
* [プログラム名と機能](#program)
    * [D206_mercury](#mercury)
* [動作環境作成・インストール](#makeenv)
    * [仮想環境構築と起動](#makepyenv)
    * [Pythonモジュールのインストール](#installmodules)
* [プログラミングメモ](#note)
    * [マルチスレッド処理と定期実行](#mlitthread)
    * [高DPI対応](#hightdpi)
* [既知の問題](#problem)
    * [pyvisaでのTimeout](#timeoutinpyvisa)
* [作成者](#author)

<h1 id="program">プログラム名と機能</h1>

<h2 id="mercury">D206_mercury</h2>

D206にある温度計「Mercury」を制御する。  
クライアントPCからsocket通信でRaspberryPiに命令を出し、RaspberryPiがMercuryとシリアル通信を行う。
命令に沿って取得されたデータをGUI画面上にプロットする。
収集したデータは、CSVとitx形式で保存可能。  
2022年2月時点では温度とパワーを設定時間(Interval)毎に取得するようになっている。
取得時間はUnix時間で記録される。
経過時間で更生したいときには、初めのデータ取得時間とそれ以降の時間の差を取れば良い。
日付に直したいときには、「Unix時間　変換」で調べると出てくる。

<h3>PC毎に変更すべき箇所</h3>
client_programs/mercury_main.py内のインスタンス変数

```bash
self.mercury_root = (Path to your D206_mercury directry)
self.download_root = (Path to your Download directry)
```

<h3>起動方法</h3>

contorol_programディレクトリまで移動。  

<クライアントPC側>  
```bash
% python3 D206_mercury/client_programs/mercury_main.py
```
GUI画面が起動する。

<RaspberryPi側>  
VNC Viewerを使って、リモートデスクトップから実行する。
```bash
% python3 D206_mercury/raspi_programs/mercury_server.py
```
socket通信待ちの状態に入る。

<h1 id="makeenv">動作環境作成</h1>

<h2 id="makepyenv">仮想環境構築と起動</h2>
グローバル環境にPythonがインストール済みであることが前提。  
仮想環境を作りたいディレクトリに移動。

```bash
% python3 -m venv (環境名)
```
(カレントディレクトリ)/(環境名)というパスを持つPythonの仮想環境が作られる。環境名は自分で決められる。  
コマンドプロンプトで仮想環境を起動するには以下のコマンドを実行。

```bash
% (仮想環境までのパス)/Scripts/activate.bat
```
仮想環境ディレクトリ内のScripts/activate.batをコマンドプロンプトにドラッグアンドドロップしてEnterを押せばよい。

```bash
(環境名) (カレントディレクトリのパス)>
```
となっていれば成功。  
環境から出るには、Scripts/deactivate.batを同様に実行すれば良い。

<h2 id="installmodules">Pythonモジュールのインストール</h2>

<クライアントPC側>  
matplotlibをインストール。同時にnumpyモジュールもインストールされる。
```bash
% pip install matplotlib
```
PyQt5をインストール。
```bash
% pip install pyqt5
```
igorwriterをインストール。
```bash
% pip install igorwriter
```

<RaspberryPi側>  
pyvisaをインストール。
```bash
% pip3 install pyvisa
```

<h1 id="note">プログラミングメモ</h1>

<h2 id="mlitthread">マルチスレッド処理と定期実行</h2>
GUI画面上でグラフを動的に描画するには、画面表示とは別のスレッドで実行する必要がある。
これをしないと応答なしになる。
下記のWebサイトを参考に、定期的に別スレッドで指定の関数を実行するようにしている。

<a href="https://ja.stackoverflow.com/questions/24508/python%E3%81%AEthreading-timer%E3%81%A7%E5%AE%9A%E6%9C%9F%E7%9A%84%E3%81%AB%E5%87%A6%E7%90%86%E3%82%92%E5%91%BC%E3%81%B3%E5%87%BA%E3%81%99%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB" target="_blank">マルチスレッド処理と定期実行の参考</a>

<h2 id="hightdpi">高DPI対応</h2>
ウィンドウを高いDPIを持つ画面(ノートPCなど)で表示するとUIが崩れる(モニターで作ったため)。
これを防ぐために高DPIに対応させる必要がる。
下記のWebサイトを参考に、対応させた。

<a href="https://leomoon.com/journal/python/high-dpi-scaling-in-pyqt5/" target="_blank">高DPI対応の参考</a>  


<h1 id="problem">既知の問題</h1>
<h2 id="timeoutinpyvisa">pyvisaでのTimeout</h2>
サーバ側で「Timeout expired before operation completed.」が表示され、エラー終了する。  
クライアント側のデータ取得間隔(Interval)を長くするとうまく動く。
ネット回線のスピードが問題で、命令がきちんとした間隔でMercuryに送られていないと思われる。
RaspberryPiをD206に置くと安定した。

<h1 id="author">作成者</h1>

* 作成者１ : 大和田 清貴
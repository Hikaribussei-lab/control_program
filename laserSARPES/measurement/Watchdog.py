# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# 標準ライブラリ
#
from __future__ import print_function

import os
import re
import time
import datetime
import subprocess
import logging

#
# 追加ライブラリ
#
#ファイル・フォルダ監視用
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# 監視対象ディレクトリを指定する
target_dir = 'Z:'

#イベントハンドラ
class ChangeHandler(FileSystemEventHandler):        
    #ファイルやフォルダが作成された場合
    def on_created(self, event):
        now = datetime.datetime.now()
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print(now.strftime('%Y-%m-%d %H:%M.%S ')+'%s was made.' % filename)
        os.system("print.py")
        #proc.communicate()
        
#メイン処理
if __name__ == '__main__':
 
    #起動ログ
    print('start watching the data folder')
 
    #現在のフォルダパスを取得する(プログラムが実行されているフォルダパス)
    #current_directory = os.path.dirname(os.path.abspath(__file__))
 
    #インスタンス作成
    event_handler = ChangeHandler()
    observer = Observer()
 
    #フォルダの監視
    observer.schedule(event_handler, target_dir, recursive=True)
 
    #監視の開始
    observer.start()
 
    try:
        #無限ループ
        while True:
            #待機
            time.sleep(0.05)
 
    except KeyboardInterrupt:
 
        #監視の終了
        observer.stop()
        
        #スレッド停止を待つ
        observer.join()
 
        #終了ログ
        print('stop watching the data folder')

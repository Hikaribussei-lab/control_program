Set WshShell = WScript.CreateObject("WScript.Shell")


WshShell.Run "python -c " & """import SARPES_client_mode; h=SARPES_client_mode.ARPES(); h.ARPESmap()""", 1, True
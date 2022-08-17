Set WshShell = WScript.CreateObject("WScript.Shell")

Do Until WshShell.AppActivate("SES")
WScript.Sleep 100
Loop

WshShell.SendKeys "^x"
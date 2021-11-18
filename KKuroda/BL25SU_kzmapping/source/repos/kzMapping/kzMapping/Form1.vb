Imports System.IO

Public Class Form1
    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        r1 = My.Settings.r1 : r2 = My.Settings.r2 : density = My.Settings.density : theta = My.Settings.theta : gs2 = My.Settings.gs2 : MirrGra = My.Settings.MirrGra : ExeFolder = My.Settings.ExeFolder
        calib_a = My.Settings.calib_a : calib_b = My.Settings.calib_b
        'put 
        r1set.Text = r1 : r2set.Text = r2 : densityset.Text = density : thetaset.Text = theta : gs2set.Text = gs2 : CurrentMirrGr.Text = MirrGra : ExeFolderset.Text = ExeFolder
        CalibAset.Text = calib_a : CalibBset.Text = calib_b
        hnVal.Text = 600 : ResVal.Text = 10000
        txSet.Text = 0 : tySet.Text = 0
        ExeFolderset.Text = My.Settings.ExeFolder : VBSset.Text = My.Settings.vbsFile
    End Sub

    Private Sub CallChangePanel_Click(sender As Object, e As EventArgs) Handles CallChangePanel.Click
        Dim f As New Form2()
        f.Show()
    End Sub

    Private Sub PutValue_Click(sender As Object, e As EventArgs) Handles PutValue.Click
        calculation()
    End Sub

    Private Sub hnChange_Click(sender As Object, e As EventArgs) Handles hnChange.Click
        Dim id1, id2, Gr, s1, s2 As Double
        Dim folder As String
        folder = ExeFolderset.Text
        calculation()
        id1 = id1display.Text : id2 = id2display.Text : s1 = s1Val.Text : s2 = s2Val.Text : Gr = GrVal.Text
        Dim obj As New IWshRuntimeLibrary.WshShell
        Dim ret As Long
        'change ids
        System.Threading.Thread.Sleep(300)
        ret = obj.Run(folder & "\Gap_cmd.exe " & id1 & " " & id2, 1, True)
        'MsgBox(folder & "\Gap_cmd.exe " & id1 & " " & id2)
        'change s1/s2
        System.Threading.Thread.Sleep(800)
        ret = obj.Run(folder & "\S1S2_cmd.exe " & s1 & " " & s2, 1, True)
        'MsgBox(folder & "\S1S2_cmd.exe " & s1 & " " & s2)
        'change Gr
        System.Threading.Thread.Sleep(800)
        ret = obj.Run(folder & "\GrRy_cmd.exe " & Gr - 1000, 1, True)
        'MsgBox(folder & "\Gr_cmd.exe " & Gr - 1000)
        System.Threading.Thread.Sleep(800)
        ret = obj.Run(folder & "\GrRy_cmd.exe " & Gr, 1, True)
        'MsgBox(folder & "\Gr_cmd.exe " & Gr)
    End Sub

    Private Sub CancelParam_Click(sender As Object, e As EventArgs) Handles CloseButton.Click
        Me.Close()
    End Sub

    Private Sub DataFolderButton_Click_1(sender As Object, e As EventArgs) Handles DataFolderButton.Click
        Dim fd As New FolderBrowserDialog
        fd.Description = "Select the folder for exe files "
        fd.RootFolder = Environment.SpecialFolder.Desktop
        fd.SelectedPath = "D:\191219_LABVIEW_Kuroda"
        fd.ShowNewFolderButton = True
        If fd.ShowDialog(Me) = DialogResult.OK Then
            DataFolderset.Text = fd.SelectedPath
            My.Settings.DataFolder = fd.SelectedPath
        End If
    End Sub

    Private Sub ExeFolderButton_Click(sender As Object, e As EventArgs) Handles ExeFolderButton.Click
        Dim fd As New FolderBrowserDialog
        fd.Description = "Select the folder for exe files "
        fd.RootFolder = Environment.SpecialFolder.Desktop
        fd.SelectedPath = "D:\191219_LABVIEW_Kuroda"
        fd.ShowNewFolderButton = True
        If fd.ShowDialog(Me) = DialogResult.OK Then
            ExeFolderset.Text = fd.SelectedPath
            My.Settings.ExeFolder = fd.SelectedPath
        End If
    End Sub

    Private Sub ScriptButton_Click(sender As Object, e As EventArgs) Handles ScriptButton.Click
        Dim Ret As DialogResult
        Using Dialog As New OpenFileDialog()
            With Dialog
                .Title = "VBS file selection"
                .CheckFileExists = True
                .Filter = "vbs files (*.vbs)|*.vbs"
            End With
            Ret = Dialog.ShowDialog()

            If Ret = DialogResult.OK Then
                VBSset.Text = Dialog.FileName
                My.Settings.vbsFile = VBSset.Text
            End If
        End Using
    End Sub

    Private Sub GrChange_Click(sender As Object, e As EventArgs) Handles GrChange.Click
        Dim Gr As Double
        Dim folder As String
        Dim obj As New IWshRuntimeLibrary.WshShell
        Dim ret As Long
        folder = ExeFolderset.Text
        Gr = GrVal.Text
        System.Threading.Thread.Sleep(300)
        ret = obj.Run(folder & "\GrRy_cmd.exe " & Gr, 1, True)
    End Sub

    Private Sub slitChange_Click(sender As Object, e As EventArgs) Handles slitChange.Click
        Dim s1, s2 As Double
        Dim folder As String
        Dim obj As New IWshRuntimeLibrary.WshShell
        Dim ret As Long
        folder = ExeFolderset.Text
        s1 = s1Val.Text : s2 = s2Val.Text
        System.Threading.Thread.Sleep(300)
        ret = obj.Run(folder & "\S1S2_cmd.exe " & s1 & " " & s2, 1, True)
    End Sub

    Private Sub IDChange_Click(sender As Object, e As EventArgs) Handles GapChange.Click
        Dim id1, id2 As Double
        Dim folder As String
        Dim obj As New IWshRuntimeLibrary.WshShell
        Dim ret As Long
        folder = ExeFolderset.Text
        id1 = id1display.Text : id2 = id2display.Text
        System.Threading.Thread.Sleep(300)
        ret = obj.Run(folder & "\Gap_cmd.exe " & id1 & " " & id2, 1, True)
    End Sub

    Private Sub kzStartButton_Click(sender As Object, e As EventArgs) Handles kzStartButton.Click
        Dim hn, res, id1, id2, s1, s2, Gr As Double
        Dim hnStart, hnEnd, hnStep, ScanStart, ScanEnd, scan_low, scan_high, tx, ty As Double
        Dim setGap, setGr, setSlit, slow_write, shigh_write, sfix_write As String
        hnStart = hnStartSet.Text : hnEnd = hnEndSet.Text : hnStep = hnStepSet.Text : tx = txSet.Text : ty = tySet.Text
        ScanStart = ScanStartSet.Text : ScanEnd = ScanEndSet.Text
        Dim vbsFile As String = VBSset.Text
        Dim newvbsFile As String = vbsFile.Replace(".vbs", "_kz.vbs")
        Dim datafolder As String = DataFolderset.Text
        Dim newdataFolder As String = datafolder.Replace("\", "\\\\")
        Dim obj As New IWshRuntimeLibrary.WshShell
        Dim ret As Long
        res = Val(ResVal.Text)
        'Copy vbs
        FileCopy(vbsFile, newvbsFile)
        'write vbs
        My.Computer.FileSystem.WriteAllText(newvbsFile, "foldername = " + Chr(34) + newdataFolder + Chr(34), True)
        My.Computer.FileSystem.WriteAllText(newvbsFile, "" & Environment.NewLine, True)
        My.Computer.FileSystem.WriteAllText(newvbsFile, "" & Environment.NewLine, True)

        Dim i As Integer = 0
        For hn = hnStart To hnEnd + hnStep Step hnStep
            scan_low = ScanStart + hnStep * i : scan_high = ScanEnd + hnStep * i
            slow_write = "call LowEnergy_seq(seq_file," + String.Format("{0}", scan_low) + ")"
            shigh_write = "call HighEnergy_seq(seq_file," + String.Format("{0}", scan_high) + ")"
            sfix_write = "call FixEnergy_seq(seq_file," + String.Format("{0}", scan_low) + ")"
            'calc
            phi = (Math.Asin((density * 1000) * (0.000001239824 / hn) / (2 * Math.Cos(theta * Math.PI / 180)))) * 180 / Math.PI
            alpha = theta + phi : beta = -theta + phi
            mag2 = r2 / r1
            magGr = Math.Cos(alpha * Math.PI / 180) / Math.Cos(beta * Math.PI / 180)
            'ID gaps
            id1 = Math.Round(-14.72215 * Math.Log(1000 * 4.64502 / hn - 1) + 74.60872, 3, MidpointRounding.AwayFromZero)
            id2 = Math.Round(-14.77956 * Math.Log(1000 * 4.65704 / hn - 1) + 74.79523, 3, MidpointRounding.AwayFromZero)
            setGap = "call SetGap(" + String.Format("{0}", id1) + ", " + String.Format("{0}", id2) + ")"
            'S1/S2
            s2 = Math.Round(hn / 0.001239824 * gs2 * (Math.Sin(beta * Math.PI / 180) + Math.Sin(alpha * Math.PI / 180)) ^ 2 / (density * res * Math.Cos(beta * Math.PI / 180)) * 1000, 0, MidpointRounding.AwayFromZero)
            s1 = Math.Round(s2 / (mag2 * magGr), 0, MidpointRounding.AwayFromZero)
            setSlit = "call SetSlit(" + String.Format("{0}", s1) + ", " + String.Format("{0}", s2) + ")"
            'Gr
            Gr = Math.Round(-calib_a / hn + calib_b)
            setGr = "call SetGrRy(" + String.Format("{0}", Gr) + ")"
            My.Computer.FileSystem.WriteAllText(newvbsFile, "Wscript.sleep(500)" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, setGap & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "Wscript.sleep(500)" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, setSlit & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "Wscript.sleep(500)" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, setGr & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "Wscript.sleep(2000)" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, slow_write & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "Wscript.sleep(2000)" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, shigh_write & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "Wscript.sleep(2000)" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "readSeq()" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "Wscript.sleep(1000)" & Environment.NewLine, True)
            If DAcheck.Checked = True Then
                My.Computer.FileSystem.WriteAllText(newvbsFile, "call setDA(" + String.Format("{0}", tx) + "," + String.Format("{0}", ty) + ")" & Environment.NewLine, True)
            End If
            My.Computer.FileSystem.WriteAllText(newvbsFile, "Wscript.sleep(3000)" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "TakeSES()" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "" & Environment.NewLine, True)
            i += 1
        Next
        System.Threading.Thread.Sleep(2000)
        ret = obj.Run(newvbsFile, 1, True)
    End Sub

    Private Sub seqStopButton_Click(sender As Object, e As EventArgs) Handles seqStopButton.Click
        Dim obj As New IWshRuntimeLibrary.WshShell
        Dim ret As Long
        ret = obj.Run("taskkill /f /im wscript.exe", 0, True)
    End Sub

    Private Sub calculation()
        Dim hn, res, id1, id2, s1, s2, Gr As Double
        hn = Val(hnVal.Text)
        res = Val(ResVal.Text)
        'calc
        phi = (Math.Asin((density * 1000) * (0.000001239824 / hn) / (2 * Math.Cos(theta * Math.PI / 180)))) * 180 / Math.PI
        alpha = theta + phi : beta = -theta + phi
        mag2 = r2 / r1
        magGr = Math.Cos(alpha * Math.PI / 180) / Math.Cos(beta * Math.PI / 180)
        'ID gaps
        id1 = -14.72215 * Math.Log(1000 * 4.64502 / hn - 1) + 74.60872
        id2 = -14.77956 * Math.Log(1000 * 4.65704 / hn - 1) + 74.79523
        id1display.Text = Math.Round(id1, 3, MidpointRounding.AwayFromZero)
        id2display.Text = Math.Round(id2, 3, MidpointRounding.AwayFromZero)
        'S1/S2
        s2 = hn / 0.001239824 * gs2 * (Math.Sin(beta * Math.PI / 180) + Math.Sin(alpha * Math.PI / 180)) ^ 2 / (density * res * Math.Cos(beta * Math.PI / 180)) * 1000
        s1 = s2 / (mag2 * magGr)
        s1Val.Text = Math.Round(s1, 0, MidpointRounding.AwayFromZero)
        s2Val.Text = Math.Round(s2, 0, MidpointRounding.AwayFromZero)
        'Gr
        Gr = -calib_a / hn + calib_b
        GrVal.Text = Math.Round(Gr)
    End Sub



End Class

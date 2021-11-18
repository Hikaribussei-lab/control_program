Public Class Form1
    Private Sub DoButton_Click(sender As Object, e As EventArgs) Handles DoButton.Click
        Dim texFile As String = texset.Text
        Dim newtexFile As String = texFile.Replace(".vbs", "_kz.vbs")
        Dim datafolder As String = DataFolderset.Text
        Dim obj As New IWshRuntimeLibrary.WshShell
        Dim ret As Long
        'Copy vbs
        FileCopy(texFile, newvbsFile)
        'write vbs
        My.Computer.FileSystem.WriteAllText(newtexFile, "foldername = " + Chr(34) + newdataFolder + Chr(34), True)
        My.Computer.FileSystem.WriteAllText(newtexFile, "" & Environment.NewLine, True)
        My.Computer.FileSystem.WriteAllText(newtexFile, "" & Environment.NewLine, True)

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
            setBackGr = "call SetGrRy(" + String.Format("{0}", Gr - 2000) + ")"
            My.Computer.FileSystem.WriteAllText(newvbsFile, "Wscript.sleep(500)" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, setGap & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "Wscript.sleep(500)" & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, setSlit & Environment.NewLine, True)
            My.Computer.FileSystem.WriteAllText(newvbsFile, "Wscript.sleep(500)" & Environment.NewLine, True)
            If hnStep < 0 Then
                My.Computer.FileSystem.WriteAllText(newvbsFile, setGr & Environment.NewLine, True)
            Else
                My.Computer.FileSystem.WriteAllText(newvbsFile, setBackGr & Environment.NewLine, True)
                My.Computer.FileSystem.WriteAllText(newvbsFile, setGr & Environment.NewLine, True)
            End If
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

End Class

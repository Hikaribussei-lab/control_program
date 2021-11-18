Public Class Form2
    Private Sub Form2_Load(ByVal sender As Object, ByVal e As EventArgs) Handles MyBase.Load
        r1 = My.Settings.r1 : r2 = My.Settings.r2 : density = My.Settings.density : theta = My.Settings.theta : gs2 = My.Settings.gs2 : MirrGra = My.Settings.MirrGra
        calib_a = My.Settings.calib_a : calib_b = My.Settings.calib_b
        alpha = theta + phi : beta = -theta + phi
        mag2 = r2 / r1
        magGr = Math.Cos(alpha * Math.PI / 180) / Math.Cos(beta * Math.PI / 180)
        'put textbox
        CalibAset.Text = calib_a : CalibBset.Text = calib_b
        r1set.Text = r1 : r2set.Text = r2 : Densityset.Text = density : Thetaset.Text = theta : GS2set.Text = gs2
        MirrGraBox.Text = MirrGra
    End Sub
    Private Sub ComboBox1_Load(sender As Object, e As EventArgs) Handles Me.Load
        With Me.MirrGraBox
            .DropDownStyle = ComboBoxStyle.DropDownList
            .Items.Add("M21a-G2a")
            .Items.Add("M21a-G3a")
            .Items.Add("M21a-G4a")
        End With
        MirrGraBox.Text = Module1.MirrGra
    End Sub
    Private Sub MirrGraBox_SelectedIndexChanged(sender As Object, e As EventArgs) Handles MirrGraBox.SelectedIndexChanged
        If MirrGraBox.Text = "M21a-G2a" Then
            r1set.Text = 6.855 : r2set.Text = 11.146 : Densityset.Text = 1000 : Thetaset.Text = 87.96 : GS2set.Text = 10000
        ElseIf MirrGraBox.Text = "M21a-G3a" Then
            r1set.Text = 6.855 : r2set.Text = 11.146 : Densityset.Text = 300 : Thetaset.Text = 87.96 : GS2set.Text = 10000
        ElseIf MirrGraBox.Text = "M21a-G4a" Then
            r1set.Text = 6.855 : r2set.Text = 11.146 : Densityset.Text = 600 : Thetaset.Text = 87.96 : GS2set.Text = 10000
        End If
    End Sub
    Private Sub ChangeParam_Click(sender As Object, e As EventArgs) Handles ChangeParam.Click
        calib_a = CalibAset.Text
        calib_b = CalibBset.Text
        'panel2 
        r1 = r1set.Text : r2 = r2set.Text : density = Densityset.Text : theta = Thetaset.Text : gs2 = GS2set.Text
        MirrGra = MirrGraBox.Text
        'my.setting
        My.Settings.r1 = r1 : My.Settings.r2 = r2 : My.Settings.density = density : My.Settings.theta = theta : My.Settings.gs2 = gs2 : My.Settings.MirrGra = MirrGra
        My.Settings.calib_a = calib_a : My.Settings.calib_b = calib_b
        'panel1
        Form1.CalibAset.Text = calib_a : Form1.CalibBset.Text = calib_b
        Form1.CurrentMirrGr.Text = MirrGra
        Form1.r1set.Text = r1 : Form1.r2set.Text = r2 : Form1.densityset.Text = density : Form1.thetaset.Text = theta
        Me.Close()
    End Sub

    Private Sub CancelParam_Click(sender As Object, e As EventArgs) Handles CancelParam.Click
        Me.Close()
    End Sub
End Class
<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Form2
    Inherits System.Windows.Forms.Form

    'フォームがコンポーネントの一覧をクリーンアップするために dispose をオーバーライドします。
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Windows フォーム デザイナーで必要です。
    Private components As System.ComponentModel.IContainer

    'メモ: 以下のプロシージャは Windows フォーム デザイナーで必要です。
    'Windows フォーム デザイナーを使用して変更できます。  
    'コード エディターを使って変更しないでください。
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(Form2))
        Me.CalibAset = New System.Windows.Forms.TextBox()
        Me.CalibBset = New System.Windows.Forms.TextBox()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.Label2 = New System.Windows.Forms.Label()
        Me.ChangeParam = New System.Windows.Forms.Button()
        Me.CancelParam = New System.Windows.Forms.Button()
        Me.MirrGraBox = New System.Windows.Forms.ComboBox()
        Me.r1set = New System.Windows.Forms.TextBox()
        Me.r2set = New System.Windows.Forms.TextBox()
        Me.Densityset = New System.Windows.Forms.TextBox()
        Me.Thetaset = New System.Windows.Forms.TextBox()
        Me.GS2set = New System.Windows.Forms.TextBox()
        Me.Label3 = New System.Windows.Forms.Label()
        Me.Label4 = New System.Windows.Forms.Label()
        Me.Label5 = New System.Windows.Forms.Label()
        Me.Label6 = New System.Windows.Forms.Label()
        Me.Label7 = New System.Windows.Forms.Label()
        Me.GroupBox1 = New System.Windows.Forms.GroupBox()
        Me.GroupBox1.SuspendLayout()
        Me.SuspendLayout()
        '
        'CalibAset
        '
        Me.CalibAset.Location = New System.Drawing.Point(133, 39)
        Me.CalibAset.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.CalibAset.Name = "CalibAset"
        Me.CalibAset.Size = New System.Drawing.Size(187, 31)
        Me.CalibAset.TabIndex = 12
        '
        'CalibBset
        '
        Me.CalibBset.Location = New System.Drawing.Point(133, 84)
        Me.CalibBset.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.CalibBset.Name = "CalibBset"
        Me.CalibBset.Size = New System.Drawing.Size(187, 31)
        Me.CalibBset.TabIndex = 13
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(9, 43)
        Me.Label1.Margin = New System.Windows.Forms.Padding(2, 0, 2, 0)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(120, 25)
        Me.Label1.TabIndex = 15
        Me.Label1.Text = "calib factor A:"
        '
        'Label2
        '
        Me.Label2.AutoSize = True
        Me.Label2.Location = New System.Drawing.Point(7, 87)
        Me.Label2.Margin = New System.Windows.Forms.Padding(2, 0, 2, 0)
        Me.Label2.Name = "Label2"
        Me.Label2.Size = New System.Drawing.Size(118, 25)
        Me.Label2.TabIndex = 16
        Me.Label2.Text = "calib factor B:"
        '
        'ChangeParam
        '
        Me.ChangeParam.Location = New System.Drawing.Point(334, 37)
        Me.ChangeParam.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.ChangeParam.Name = "ChangeParam"
        Me.ChangeParam.Size = New System.Drawing.Size(107, 35)
        Me.ChangeParam.TabIndex = 17
        Me.ChangeParam.Text = "Change"
        Me.ChangeParam.UseVisualStyleBackColor = True
        '
        'CancelParam
        '
        Me.CancelParam.Location = New System.Drawing.Point(334, 84)
        Me.CancelParam.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.CancelParam.Name = "CancelParam"
        Me.CancelParam.Size = New System.Drawing.Size(107, 35)
        Me.CancelParam.TabIndex = 18
        Me.CancelParam.Text = "Cancel"
        Me.CancelParam.UseVisualStyleBackColor = True
        '
        'MirrGraBox
        '
        Me.MirrGraBox.FormattingEnabled = True
        Me.MirrGraBox.Location = New System.Drawing.Point(133, 130)
        Me.MirrGraBox.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.MirrGraBox.Name = "MirrGraBox"
        Me.MirrGraBox.Size = New System.Drawing.Size(187, 33)
        Me.MirrGraBox.TabIndex = 19
        '
        'r1set
        '
        Me.r1set.Enabled = False
        Me.r1set.HideSelection = False
        Me.r1set.Location = New System.Drawing.Point(90, 57)
        Me.r1set.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.r1set.Name = "r1set"
        Me.r1set.ShortcutsEnabled = False
        Me.r1set.Size = New System.Drawing.Size(86, 31)
        Me.r1set.TabIndex = 17
        '
        'r2set
        '
        Me.r2set.Enabled = False
        Me.r2set.Location = New System.Drawing.Point(90, 107)
        Me.r2set.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.r2set.Name = "r2set"
        Me.r2set.Size = New System.Drawing.Size(86, 31)
        Me.r2set.TabIndex = 18
        '
        'Densityset
        '
        Me.Densityset.Enabled = False
        Me.Densityset.Location = New System.Drawing.Point(303, 57)
        Me.Densityset.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.Densityset.Name = "Densityset"
        Me.Densityset.Size = New System.Drawing.Size(86, 31)
        Me.Densityset.TabIndex = 19
        '
        'Thetaset
        '
        Me.Thetaset.Enabled = False
        Me.Thetaset.Location = New System.Drawing.Point(303, 107)
        Me.Thetaset.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.Thetaset.Name = "Thetaset"
        Me.Thetaset.Size = New System.Drawing.Size(86, 31)
        Me.Thetaset.TabIndex = 20
        '
        'GS2set
        '
        Me.GS2set.Enabled = False
        Me.GS2set.Location = New System.Drawing.Point(303, 159)
        Me.GS2set.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.GS2set.Name = "GS2set"
        Me.GS2set.Size = New System.Drawing.Size(86, 31)
        Me.GS2set.TabIndex = 21
        '
        'Label3
        '
        Me.Label3.AutoSize = True
        Me.Label3.Location = New System.Drawing.Point(55, 57)
        Me.Label3.Margin = New System.Windows.Forms.Padding(2, 0, 2, 0)
        Me.Label3.Name = "Label3"
        Me.Label3.Size = New System.Drawing.Size(32, 25)
        Me.Label3.TabIndex = 26
        Me.Label3.Text = "r1:"
        '
        'Label4
        '
        Me.Label4.AutoSize = True
        Me.Label4.Location = New System.Drawing.Point(55, 112)
        Me.Label4.Margin = New System.Windows.Forms.Padding(2, 0, 2, 0)
        Me.Label4.Name = "Label4"
        Me.Label4.Size = New System.Drawing.Size(32, 25)
        Me.Label4.TabIndex = 27
        Me.Label4.Text = "r2:"
        '
        'Label5
        '
        Me.Label5.AutoSize = True
        Me.Label5.Location = New System.Drawing.Point(225, 59)
        Me.Label5.Margin = New System.Windows.Forms.Padding(2, 0, 2, 0)
        Me.Label5.Name = "Label5"
        Me.Label5.Size = New System.Drawing.Size(75, 25)
        Me.Label5.TabIndex = 28
        Me.Label5.Text = "Density:"
        '
        'Label6
        '
        Me.Label6.AutoSize = True
        Me.Label6.Location = New System.Drawing.Point(193, 109)
        Me.Label6.Margin = New System.Windows.Forms.Padding(2, 0, 2, 0)
        Me.Label6.Name = "Label6"
        Me.Label6.Size = New System.Drawing.Size(105, 25)
        Me.Label6.TabIndex = 29
        Me.Label6.Text = "Theta (deg):"
        '
        'Label7
        '
        Me.Label7.AutoSize = True
        Me.Label7.Location = New System.Drawing.Point(244, 165)
        Me.Label7.Margin = New System.Windows.Forms.Padding(2, 0, 2, 0)
        Me.Label7.Name = "Label7"
        Me.Label7.Size = New System.Drawing.Size(55, 25)
        Me.Label7.TabIndex = 30
        Me.Label7.Text = "G-S2:"
        '
        'GroupBox1
        '
        Me.GroupBox1.Controls.Add(Me.Label7)
        Me.GroupBox1.Controls.Add(Me.Label6)
        Me.GroupBox1.Controls.Add(Me.Label5)
        Me.GroupBox1.Controls.Add(Me.Label4)
        Me.GroupBox1.Controls.Add(Me.Label3)
        Me.GroupBox1.Controls.Add(Me.GS2set)
        Me.GroupBox1.Controls.Add(Me.Thetaset)
        Me.GroupBox1.Controls.Add(Me.Densityset)
        Me.GroupBox1.Controls.Add(Me.r2set)
        Me.GroupBox1.Controls.Add(Me.r1set)
        Me.GroupBox1.Location = New System.Drawing.Point(12, 174)
        Me.GroupBox1.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.GroupBox1.Name = "GroupBox1"
        Me.GroupBox1.Padding = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.GroupBox1.Size = New System.Drawing.Size(443, 301)
        Me.GroupBox1.TabIndex = 14
        Me.GroupBox1.TabStop = False
        Me.GroupBox1.Text = "Mirro-Grating parameters"
        '
        'Form2
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(10.0!, 25.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(478, 486)
        Me.Controls.Add(Me.MirrGraBox)
        Me.Controls.Add(Me.CancelParam)
        Me.Controls.Add(Me.ChangeParam)
        Me.Controls.Add(Me.Label2)
        Me.Controls.Add(Me.Label1)
        Me.Controls.Add(Me.GroupBox1)
        Me.Controls.Add(Me.CalibBset)
        Me.Controls.Add(Me.CalibAset)
        Me.Icon = CType(resources.GetObject("$this.Icon"), System.Drawing.Icon)
        Me.Margin = New System.Windows.Forms.Padding(2, 2, 2, 2)
        Me.Name = "Form2"
        Me.Text = "Chang parameters"
        Me.GroupBox1.ResumeLayout(False)
        Me.GroupBox1.PerformLayout()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub

    Friend WithEvents CalibAset As TextBox
    Friend WithEvents Label1 As Label
    Friend WithEvents Label2 As Label
    Friend WithEvents ChangeParam As Button
    Friend WithEvents CancelParam As Button
    Friend WithEvents MirrGraBox As ComboBox
    Friend WithEvents CalibBset As TextBox
    Friend WithEvents r1set As TextBox
    Friend WithEvents r2set As TextBox
    Friend WithEvents Densityset As TextBox
    Friend WithEvents Thetaset As TextBox
    Friend WithEvents GS2set As TextBox
    Friend WithEvents Label3 As Label
    Friend WithEvents Label4 As Label
    Friend WithEvents Label5 As Label
    Friend WithEvents Label6 As Label
    Friend WithEvents Label7 As Label
    Friend WithEvents betaVal As TextBox
    Friend WithEvents GroupBox1 As GroupBox
End Class

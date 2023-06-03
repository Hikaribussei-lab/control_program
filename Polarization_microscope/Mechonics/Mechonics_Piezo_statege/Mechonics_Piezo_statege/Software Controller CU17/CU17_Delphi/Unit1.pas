unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  Buttons, StdCtrls, ExtCtrls, CU80USB1DLL, ComCtrls, Spin, Grids ;

type
    TForm1 = class(TForm)
    Memo1: TMemo;
    Timer1: TTimer;
    Label7: TLabel;
    Label1: TLabel;
    StringGrid1: TStringGrid;
    TrackBar1: TTrackBar;
    TrackBar2: TTrackBar;
    TrackBar3: TTrackBar;
    TrackBar4: TTrackBar;
    TrackBar5: TTrackBar;
    TrackBar6: TTrackBar;
    Label2: TLabel;
    Label3: TLabel;
    Label4: TLabel;
    Label5: TLabel;
    Label6: TLabel;
    Label8: TLabel;
    TrackBar7: TTrackBar;
    Label9: TLabel;
    Label10: TLabel;
    Label11: TLabel;
    Label12: TLabel;
    Label13: TLabel;
    StatusBar1: TStatusBar;


    procedure FormClose(Sender: TObject; var Action: TCloseAction);

    procedure FormCreate(Sender: TObject);
    
    procedure Timer1Timer(Sender: TObject);
    procedure TrackBar1Change(Sender: TObject);
    procedure TrackBar2Change(Sender: TObject);
    procedure TrackBar3Change(Sender: TObject);
    procedure TrackBar4Change(Sender: TObject);
    procedure TrackBar5Change(Sender: TObject);
    procedure TrackBar6Change(Sender: TObject);

    procedure StringGrid1MouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure StringGrid1SelectCell(Sender: TObject; ACol, ARow: Integer;
      var CanSelect: Boolean);
    procedure StringGrid1MouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure TrackBar7Change(Sender: TObject);


  private
    { Private-Deklarationen }
  public
    { Public-Deklarationen }
  end;


var
  Form1: TForm1;
  Speed: byte;
  USB01: DeviceRec;
  bin3: array[0..8191] of byte;
  br: ByteRec64;
  TVel:integer;
  TPos:longint;
  Axis,PAxis:byte;
  StepVel:word;
  StepNumber:integer;
  vel,pvel,univel,counter: integer;
  v1,v2,v3,vel1,vel2,vel3,dv1,dv2,dv3,CU80Voltage: integer;
  procedure GetFileVersionInfoDelphi;

implementation

{$R *.DFM}



procedure TForm1.FormClose(Sender: TObject; var Action: TCloseAction);
begin
   CU80DCDCOff(USB01);
   CU80Close(USB01);
   beep;
end;



{$R+}


procedure TForm1.FormCreate(Sender: TObject);
var lw: longword;
    b:byte;
    s: string;
    sc: PChar256;
    EP: USBEEProm;
    i: integer;
    MaxIndex:word;
    BinBuffer: ByteRec8192;
    inf: inforec;
begin
   USB01.USBInstance:=0;
   USB01.USBVersion:=1;
   USB01.DevID:=2;
   USB01.EEID:=0;

   sc:=CU80Open(USB01);
   s:=string(sc);
   if s<>'' then
   begin
      if Application.MessageBox(PChar(s),'USB Error',MB_OK) = IDOK then halt;
   end;
   TVel:=0;
   TPos:=0;

   EP:=GetUSBEEPromInfo(USB01);
   memo1.Lines.Insert(0,' '+EP.ProductStr);
   memo1.Lines.Insert(1,' DeviceID: '+inttostr(EP.DeviceID));
   memo1.Lines.Insert(2,' EEPromID: '+inttostr(EP.EEPromID));
   memo1.Lines.Insert(3,' SerialNumber: '+inttostr(EP.SerialNumber));
   memo1.Lines.Insert(4,' Date: '+EP.Date);
   pvel:=0;
   univel:=0;


   trackbar1.Position:=63; Label1.Caption:=inttostr(trackbar1.Position);
   trackbar2.Position:=63; Label2.Caption:=inttostr(trackbar2.Position);
   trackbar3.Position:=63; Label3.Caption:=inttostr(trackbar3.Position);
   trackbar4.Position:=0; Label4.Caption:=inttostr(trackbar4.Position);
   trackbar5.Position:=0; Label5.Caption:=inttostr(trackbar5.Position);
   trackbar6.Position:=0; Label6.Caption:=inttostr(trackbar6.Position);
   trackbar7.Position:=38; Label9.Caption:=inttostr(trackbar7.Position);

   vel1:=trackbar1.Position;
   vel2:=trackbar2.Position;
   vel3:=trackbar3.Position;
   dv1:=0; dv2:=0; dv3:=0;
   v1:=trackbar7.Position;
   v2:=v1;v3:=v1;
   CU80PiezoMove(USB01,1,0,v1);  {Sets Voltage}
   CU80DCDCon(USB01);
   StringGrid1.Cells[0,0]:='<<<';
   StringGrid1.Cells[1,0]:=' <<';
   StringGrid1.Cells[2,0]:=' <';
   StringGrid1.Cells[3,0]:='  X';
   StringGrid1.Cells[4,0]:=' >';
   StringGrid1.Cells[5,0]:=' >>';
   StringGrid1.Cells[6,0]:='>>>';

   StringGrid1.Cells[0,2]:='<<<';
   StringGrid1.Cells[1,2]:=' <<';
   StringGrid1.Cells[2,2]:=' <';
   StringGrid1.Cells[3,2]:='  Y';
   StringGrid1.Cells[4,2]:=' >';
   StringGrid1.Cells[5,2]:=' >>';
   StringGrid1.Cells[6,2]:='>>>';

   StringGrid1.Cells[0,4]:='<<<';
   StringGrid1.Cells[1,4]:=' <<';
   StringGrid1.Cells[2,4]:=' <';
   StringGrid1.Cells[3,4]:='  Z';
   StringGrid1.Cells[4,4]:=' >';
   StringGrid1.Cells[5,4]:=' >>';
   StringGrid1.Cells[6,4]:='>>>';
   GetFileVersionInfoDelphi;

end;


procedure TForm1.Timer1Timer(Sender: TObject);
begin
   CU80PiezoMove(USB01,PAxis,Pvel,CU80Voltage);
end;


function GetVoltage(ax,vel:integer):integer;
(*****************************************)
const scalefactor=0.01;
var sig,v,dv: integer;
    scale: double;
begin
   if ax=1 then begin v:=v1; dv:=dv1; end;
   if ax=2 then begin v:=v2; dv:=dv2; end;
   if ax=3 then begin v:=v3; dv:=dv3; end;
   if vel<0 then sig:=-1 else sig:=1;

   scale:=sig*scalefactor*dv;
   scale:=scale+1;
   result:=round(scale*v);
end;


procedure TForm1.StringGrid1SelectCell(Sender: TObject; ACol,
  ARow: Integer; var CanSelect: Boolean);
var i:integer;  
begin
   case ARow of
   0: begin paxis:=1; univel:=vel1; end;
   2: begin paxis:=2; univel:=vel2; end;
   4: begin paxis:=3; univel:=vel3; end;
   end;

   case ACol of
   0: pvel:=-univel;
   1: pvel:=-univel div 4;
   2: pvel:=-1;
   4: pvel:=1;
   5: pvel:=univel div 4;
   6: pvel:=univel;
   else pvel:=0; end;
   
   CU80Voltage:=GetVoltage(paxis,pvel);
   {form1.Caption:=inttostr(CU80Voltage);}

   if abs(pvel)=1 then
   begin
      timer1.Enabled:=false;
      CU80PiezoMove(USB01,PAxis,Pvel,CU80Voltage);
   end
   else
   timer1.Enabled:=true;
end;

procedure TForm1.StringGrid1MouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
begin
   {form1.Caption:=inttostr(x)+' '+inttostr(y);}
end;

procedure TForm1.StringGrid1MouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
   pvel:=0; PAxis:=1;
end;



procedure TForm1.TrackBar1Change(Sender: TObject);
begin
   vel1:=Trackbar1.Position;
   Label1.Caption:=inttostr(vel1);
end;

procedure TForm1.TrackBar2Change(Sender: TObject);
begin
   vel2:=Trackbar2.Position;
   Label2.Caption:=inttostr(vel2);
end;

procedure TForm1.TrackBar3Change(Sender: TObject);
begin
   vel3:=Trackbar3.Position;
   Label3.Caption:=inttostr(vel3);
end;



procedure TForm1.TrackBar4Change(Sender: TObject);
begin
   dv1:=Trackbar4.Position;
   Label4.Caption:=inttostr(dv1);
end;

procedure TForm1.TrackBar5Change(Sender: TObject);
begin
   dv2:=Trackbar5.Position;
   Label5.Caption:=inttostr(dv2);
end;

procedure TForm1.TrackBar6Change(Sender: TObject);
begin
   dv3:=Trackbar6.Position;
   Label6.Caption:=inttostr(dv3);
end;

procedure TForm1.TrackBar7Change(Sender: TObject);
begin
   v1:=trackbar7.Position;
   v2:=v1;v3:=v1;
   Label9.Caption:=inttostr(v3);
end;

procedure GetFileVersionInfoDelphi;
const
  infoString: String ='StringFileInfo\040904E4\FileVersion';
var
  S: string;
  n,Len: DWORD;
  Buf: PChar;
  Value: PChar;
  VersionValue,aFileVersion: AnsiString;
  bfind: LongBool;
begin
   S := Application.ExeName;
   n := GetFileVersionInfoSize(PChar(S), n);
   if n > 0 then
   begin
     Buf := AllocMem(n);
     GetFileVersionInfo(PChar(S), 0, n, Buf);
     if VerQueryValue(Buf, '\VarFileInfo\Translation', Pointer(Value), Len) then
     begin
       VersionValue := '\StringFileInfo\' +
                      IntToHex(LoWord(LongInt(Pointer(Value)^)), 4) +
                      IntToHex(HiWord(LongInt(Pointer(Value)^)), 4) + '\';
       Len:=0;
       bfind:=VerQueryValue(
       Buf, PChar(VersionValue + 'FileVersion'), Pointer(Value), Len );
       aFileVersion := AnsiString(Value);
       aFileVersion := Trim(aFileVersion);
       Form1.StatusBar1.Panels[0].Text:='File version:   ' + aFileVersion;
     end ;
     FreeMem(Buf, n);
   end
end;

end.



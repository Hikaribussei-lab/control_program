unit CU80USB1DLL;

{$Align on}

interface
uses Windows,SysUtils;

type PChar16 =  array[0..31]  of char;
     PChar32 =  array[0..31]  of char;
     PChar256 = array[0..255] of char;


     USBEEProm = record
        USBVendorID:   dword;
        USBProductID:  dword;
        USBDeviceID:   dword;
        DeviceID:      dword;
        EEPromID:      dword;
        Version:       dword;
        SerialNumber:  dword;
        CustomerID:    dword;
        Company:       PChar16;
        Date:          PChar16;
        ProductStr:    PChar32;
        Customer:      PChar32;
        CustomerStr:   PChar32;
     end;

     ByteRec64 = Array [0..63] of Byte;
     ByteRec1024 = Array [0..1024] of Byte;
     ByteRec8192 = Array [0..8191] of Byte;
     InfoRec = record Vendor,Product,Device,DeviceID,EEPromID,USB,Hnd,Res:dword; end;
     DeviceRec = record USBInstance,USBVersion,DevID,EEID:dword; end;


function  GetUSBEEPromInfo(MUSBDeviceID:DeviceRec): USBEEProm;    stdcall
          {Liest EEProm Inhalt vom USB-Controler in den Record USBEEProm}
function  Echo(MUSBDeviceID:DeviceRec;w: dword):dword;            stdcall
          {Liefert gesendetes dword zurück (zu Testzwecken)}
function  CU80Open(var MUSBDeviceID:DeviceRec):PChar256;          stdcall
{Input:  DeviceRec:  USBInstance,USBVersion,DevID,EEID:dword;
         USBInstance wird von der Routine zurückgegeben (0..15)
         EEID bezeichnen das anzusprechende Gerät (0..15)
         Die Parameter USBVersion,DevID sind in der Routine bereits
         auf das Gerät Servo3AxUSB2 vorgesetzt (falsche Eingaben werden überschrieben.
 Output: Fehlermeldung als nullterminierter String
         Wenn kein Fehler aufgetreten ist bleibt der String leer}
procedure CU80Close(MUSBDeviceID:DeviceRec);                      stdcall
{Input:  DeviceRec wie von CU80Open erzeugt
         (gilt auch für alle folgenden Routinen) }
procedure CU80PiezoStop(MUSBDeviceID:DeviceRec);                  stdcall
          {Beendet jede Bewegung}
procedure CU80DCDCon(MUSBDeviceID:DeviceRec);                     stdcall
          {Schaltet DCDC-Wandler ein}
procedure CU80DCDCoff(MUSBDeviceID:DeviceRec);                    stdcall
          {Schaltet DCDC-Wandler aus}
procedure CU80PiezoMove(MUSBDeviceID:DeviceRec; Axis,Velocity,Voltage:longint);   stdcall
          {Fahrbefehl:
           Axis: 1,2 oder 3
           Velocity: -63 .. bis .. 63; +-1 ist Single-Step Mode, 0 ist Stop
           Voltage: 22 .. bis .. 82, definiert maximale Piezospannung }



implementation

function  GetUSBEEPromInfo;   external 'CU80USB1.DLL'
function  Echo;               external 'CU80USB1.DLL'
function  CU80Open;           external 'CU80USB1.DLL'
procedure CU80Close;          external 'CU80USB1.DLL'
procedure CU80PiezoStop;      external 'CU80USB1.DLL'
procedure CU80DCDCon;         external 'CU80USB1.DLL'
procedure CU80DCDCoff;        external 'CU80USB1.DLL'
procedure CU80PiezoMove;      external 'CU80USB1.DLL'


end.




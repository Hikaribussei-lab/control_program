program CU17;

uses
  Forms,
  Unit1 in 'Unit1.pas' {Form1};

{$R *.RES}

begin
  Application.Initialize;
  Application.Title := 'Mechonics ControlPanel';
  Application.CreateForm(TForm1, Form1);
  Application.Run;
end.

program kf532;

uses crt, sysutils;


const cmdNOP     = 0;

const cmdNOT     = 1;
const cmdFETCH   = 2;
const cmdSHL     = 3;
const cmdSHR     = 4;
const cmdSHRA    = 5;
const cmdINPORT  = 6;

const cmdSWAP    = 7;

const cmdDUP     = 8;
const cmdOVER    = 9;
const cmdFROMR   = 10;
const cmdLOOP    = 11;
const cmdSYSREG  = 12;

const cmdPLUS    = 13;
const cmdMINUS   = 14;
const cmdAND     = 15;
const cmdOR      = 16;
const cmdXOR     = 17;
const cmdEQUAL   = 18;
const cmdLESSER  = 19;
const cmdGREATER = 20;
const cmdMULT    = 21;

const cmdDROP    = 22;
const cmdJMP     = 23;
const cmdCALL    = 24;
const cmdRJMP    = 25;
const cmdTOR     = 26;

const cmdSTORE   = 27;
const cmdDO      = 28;

const cmdRIF     = 29;
const cmdUNTIL   = 30;

const cmdRET     = 31;

const MAXCODE = 131072;
const MAXDATA = 65536;
const MAXWORDS = 10000;

var Code : array[0.. MAXCODE - 1] of integer;
var Data : array[0.. MAXDATA - 1] of integer;

var CodePtr, DataPtr, WordPtr : integer;

var ch: char;

var filename, outfilename, lstfilename, Tib,Token : string;

var hf, hlst : text;

procedure pak;
begin
  repeat until KeyPressed;
end;

procedure ProcessParamStr;
var i : integer;
begin
  if ParamCount > 0 then
  begin
    for i := 1 to ParamCount do
    begin
      if ParamStr(i) = '-list' then lstfilename := ParamStr(i+1);
      if Copy(ParamStr(i), 1, 1) <> '-' then filename := ParamStr(i);
    end;
  end;
end;

procedure InitCompiler;
begin
  CodePtr := 0;
  DataPtr := 0;
  WordPtr := 0;
  Code[4] := cmdJMP;
  CodePtr := 5;
end;

procedure ProcessFile;
begin
  Assign(hf, filename);
  Reset(hf);
  while(not(Eof(hf))) do
  begin
    readln(hf, Tib);
    writeln(Tib);
  end;

  Close(hf);
end;

procedure ReportAll;
begin
  Writeln('Code size is: ' + IntToStr(CodePtr));
end;


begin
  ExitCode := 0;
  writeln('Kf532 compiler');
  ProcessParamStr;
  writeln('Source text is: ' + filename);
  if ((filename <> '') and (FileExists(filename))) then
  begin
    InitCompiler;
    ProcessFile;
    ReportAll;
  end else
  begin
    writeln('No valid source file specified. Pass filename as a parameter.');
    ExitCode := 1;
  end;
  writeln('Press any key to exit...');
  pak;

  exit;
end.


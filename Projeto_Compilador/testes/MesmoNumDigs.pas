program MesmoNumeroDigitos;
var
  a, b: integer;
  contA, contB: integer;
begin
  readln(a);
  readln(b);
  contA := 0;
  while a <> 0 do
  begin
    contA := contA + 1;
    a := a div 10;
  end;
  contB := 0;
  while b <> 0 do
  begin
    contB := contB + 1;
    b := b div 10;
  end;
  if contA = contB then
    writeln('Têm o mesmo número de dígitos.')
  else
    writeln('Têm número de dígitos diferente.');
end.

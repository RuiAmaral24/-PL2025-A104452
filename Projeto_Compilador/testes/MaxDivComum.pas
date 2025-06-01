program GCDInline;
var
  x, y, r, resultado: integer;
begin
  readln(x);
  readln(y);
  while y <> 0 do
  begin
    r := x mod y;
    x := y;
    y := r;
  end;
  resultado := x;
  writeln('Máximo divisor comum: ', resultado);
end.
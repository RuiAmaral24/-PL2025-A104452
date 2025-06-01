program SomatorioPares;
var
  numero, resultado, i, soma: integer;
begin
  readln(numero);
  soma := 0;
  i := 0;
  while i <= numero do
  begin
    if i mod 2 = 0 then
      soma := soma + i;
    i := i + 1;
  end;
  resultado := soma;
  writeln('Soma dos pares até ', numero, ': ', resultado);
end.

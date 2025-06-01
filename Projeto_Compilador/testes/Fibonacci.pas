program FibonacciInline;
var
  n, i, a, b, tmp, resultado: integer;
begin
  readln(n);
  if n < 2 then
    resultado := n
  else
  begin
    a := 0;
    b := 1;
    for i := 2 to n do
    begin
      tmp := a + b;
      a := b;
      b := tmp;
    end;
    resultado := b;
  end;
  writeln('Fib(', n, ') = ', resultado);
end.

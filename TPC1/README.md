# TPC1

## Rui Filipe Mesquita Amaral

### Resumo:

Este programa lê o STDIN caracter por caracter, mantendo dois buffers para armazenar os últimos caracteres lidos. 
O primeiro buffer guarda os dois últimos caracteres para verificar se a palavra "on" foi escrita, enquanto o segundo buffer 
armazena os três últimos caracteres para detectar a palavra "off". Ambas as palavras são verificadas sem distinção entre 
maiúsculas e minúsculas.

Se "on" for identificado, a soma dos números lidos é ativada; se "off" for encontrado, a soma é desativada. 
Enquanto a soma estiver ativa, os números detectados são acumulados. Quando um "=" é encontrado, o total acumulado até 
o momento é exibido. No final da leitura, o programa imprime o valor total acumulado.
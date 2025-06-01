# Projeto Compilador Pascal

> **Disciplina**: Processamento de Linguagens 2024/25  
> **Grupo**: 59  
> - a104447 - Rodrigo Abreu Correia Domingues  
> - a104085 - Rafael Azevedo Correia  
> - a104452 - Rui Filipe Mesquita Amaral  

---

## 1. Introdução

Este relatório descreve a implementação de um compilador simples para Pascal que gera código para a **EWVM**.  
Apresentamos a arquitetura geral, as fases de análise e geração de código, bem como exemplos de programas de teste.

---

## 2. Arquitetura Geral

O compilador é organizado em quatro fases principais:

1. **Análise Léxica** – Tokenização do código-fonte Pascal (`pascal_lex.py`).  
2. **Análise Sintática** – Construção de AST via Yacc/PLY (`pascal_yacc.py`).  
3. **Análise Semântica** – Verificação de tipos, escopos e declaração de variáveis (`pascal_seman.py`).  
4. **Geração de Código** – Emissão de instruções EWVM (`pascal_codegen.py`).  

Fluxo de dados:

```
.ficheiro .pas  
    └─▶ Lexer ──▶ Parser ──▶ AST ──▶ Semant ──▶ CodeGen ──▶ .vm  
```

---

## 3. Componentes Detalhados

### 3.1 Análise Léxica (`pascal_lex.py`)

1. **Definição de padrões**  
   - **Identificadores**: `[A-Za-z][A-Za-z0-9]*`.  
   - **Números inteiros**: `[0-9]+`.  
   - **Strings**: delimitadas por aspas simples ('...').
   - **Comentários**: `{ ... }`, ignorados.

2. **Tokenização**  
   - Converte pedaços em **tokens** `(TIPO, valor)`.  
   - Exemplo de tokenização:  
    - `"readln"` → `('READLN', 'readln')`  
    - `"123"` → `('NUM', 123)`

3. **Tratamento de erros**  
   - Caracteres inesperados são ignorados após aviso, mantendo a análise.

---

### 3.2 Análise Sintática (`pascal_yacc.py`)

1. **Gramática**  
   - Regras para `program`, `declarações`, `comandos`, `expressões`.

2. **Construção da AST**  
   - Cada nó vira uma **tupla** aninhada.  
     ```python
     ('assign', 'x', ':=', ('num', 42))
     ```

3. **Precedência e associatividade**  
   - Define nível de `*`,`/` > `+`,`-` > comparadores > lógicos.

4. **Recuperação de erro**  
   - A função p_error é usada para detetar erros de sintaxe, indicar a linha do erro (se possível) e permitir que o analisador continue a interpretação do programa sempre que possível.

---

### 3.3 Análise Semântica (`pascal_seman.py`)

1. **Tabela de símbolos**  
   - Regista variáveis e funções com tipo e, para arrays, limites `(low, high)`.

2. **Verificações**  
   - **Declaração prévia**: uso só após `var`.  
   - **Tipos compatíveis**: atribuições, condicionais e expressões.  
   - **Índices de array** dentro de `low..high`.

3. **Escopos de funções**  
   - Nova tabela local para parâmetros e variáveis internas.

4. **Erros detectados**  
   - Não declarados, incompatibilidade de tipo, acesso fora de limites.

---

### 3.4 Geração de Código EWVM (`pascal_codegen.py`)

1. **Mapeamento de variáveis**  
   - Cada variável global → um **GP slot** (`var_slots[name]`).

2. **Inicialização**  
   - Antes do `start`, empilha cada slot com `0` ou `""`:
     ```vm
     pushi 0
     storeg 3
     ```

3. **Instruções principais**  
   - **Empilhar**: `pushi`, `pushs`, `pushg`.  
   - **Armazenar**: `storeg`.  
   - **Entrada/Saída**:  
     - `read` → string, `atoi` → inteiro  
     - `writes` → string, `writei` → inteiro, `writeln` → nova linha  
   - **Operações**: `add`, `sub`, `mul`, `div`, `mod`, comparadores, lógicos, `strlen`, `charat`.

4. **Rótulos**  
   - `nova_label()` gera nomes únicos: `WHILE0`, `FOR1`, `ELSE2`, etc.

5. **Estrutura de repetição genérico**  
   - **Inicialização** do contador  
   - **Teste** de condição (`infeq`, `supeq`)  
   - **Corpo** do loop 
   - **Passo** (incremento/decremento)  
   - **Repetição** (jump para o início)

6. **Detecção de soma de array**  
   - Reconhece padrão `for i := 1 to N do read; soma := soma + …`  
   - Gera um `while` decremental num contador genérico.

---

## 4. Estrutura de Ficheiros

```
.
├── pascal_lex.py        # Lexer
├── pascal_yacc.py       # Parser → AST
├── pascal_seman.py      # Verificador semântico
├── pascal_codegen.py    # Gerador de código EWVM
├── teste_codegen.py     # Script de testes automáticos
└── testes/
    ├── HelloWorld.pas
    ├── Fatorial.pas
    ├── Maior3.pas
    ├── BinPraInt.pas
    ├── SomaArray.pas
    └── … outros exemplos
```

Os arquivos `.vm` gerados ficam guardados em `codigoVM/`.

---

## 5. Exemplos de Programas

### 5.1 HelloWorld.pas

```pascal
program HelloWorld;
begin
  writeln('Ola, Mundo!');
end.
```

### 5.2 SomaArray.pas

```pascal
program SomaArray;
var
  numeros: array[1..5] of integer;
  soma: integer;
begin
  soma := 0;
  writeln('Introduza 5 números inteiros:');
  for i := 1 to 5 do
    readln(numeros[i]);
  writeln('Soma = ', soma);
end.
```

---

## 6. Conclusões e Trabalhos Futuros

- O compilador suporta a linguagem Pascal e produz corretamente o código correspondente para a máquina virtual EWVM.
- **Limitações**:
  - Não suporta geração de chamadas a funções recursivas.  
  - Arrays são traduzidos apenas no padrão de soma; acesso aleatório não é suportado.  
- **Possíveis extensões**:
  - Suporte completo a **call** de funções.  
  - Otimizações de expressões e loops.  
  - Implementação de variáveis locais e escopos aninhados.  

---

> **Observação:** Para detalhes de uso, consulte o README e o script `teste_codegen.py`.  

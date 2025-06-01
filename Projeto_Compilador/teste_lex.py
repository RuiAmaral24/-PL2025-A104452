from pascal_lex import lexer 
from pascal_yacc import parser
from pascal_seman import verificar_semantica, ErroSemantico

print("Insere o código Pascal abaixo (termina com linha vazia):\n")

linhas = []
while True:
    try:
        linha = input()
        if linha.strip() == "":
            break
        linhas.append(linha)
    except EOFError:
        break

codigo = "\n".join(linhas)

print("-----------------Análise Sintática-----------------")
try:
    lexer.lineno = 1  # Reiniciar contador de linha
    ast = parser.parse(codigo, lexer=lexer)
    print("✅ Sintaxe válida.")
    print(ast)
except Exception as e:
    print(f"❌ Erro de sintaxe: {e}")
    exit()

print("\n-----------------Análise Semântica-----------------")
try:
    verificar_semantica(ast)
    print("✅ Semântica válida.")
except ErroSemantico as e:
    print(f"❌ Erro semântico: {e}")

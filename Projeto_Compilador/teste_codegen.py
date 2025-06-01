import os
from pascal_lex import lexer
from pascal_yacc import parser
from pascal_codegen import gerar_codigo

def correr_codigo_vm(ficheiro_pas):
    with open("testes/" + ficheiro_pas) as f:
        codigo = f.read()

    try:
        lexer.lineno = 1
        ast = parser.parse(codigo, lexer=lexer)
        #print(ast)
        gerar_codigo(ast, ficheiro_pas)
        print(f"[✔] Código VM gerado para {ficheiro_pas}, verifique na pasta 'codigoVM'.")
    except Exception as e:
        print(f"[✘] Erro ao gerar código para {ficheiro_pas} → {e}")

# Single test case
#filename = "HelloWorld" + ".pas"
#correr_codigo_vm(filename)

# Test all files in the "testes" directory
for ficheiro in os.listdir("testes"):
    #if ficheiro.endswith(".pas") and not(ficheiro.startswith("Erro")):
    if ficheiro.endswith(".pas"):
        correr_codigo_vm(ficheiro)
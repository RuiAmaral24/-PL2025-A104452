import os
from pascal_yacc import parser
from pascal_lex import lexer
from pascal_seman import verificar_semantica, ErroSemantico

def correr_teste(path):
    with open(path) as f:
        codigo = f.read()
    try:
        lexer.lineno = 1  # Reiniciar o número da linha
        ast = parser.parse(codigo, lexer=lexer)

        try:
            verificar_semantica(ast)
            print(f"[✔] {os.path.basename(path)}")
        except ErroSemantico as sem_e:
            print(f"[✘] {os.path.basename(path)} → Erro semântico: {sem_e}")
        
        # Opcional: imprime AST
        #print(ast)

    except SyntaxError as e:
        print(f"[✘] {os.path.basename(path)} → {e}")

def main():
    pasta = "testes"
    for ficheiro in sorted(os.listdir(pasta)):
        if ficheiro.endswith(".pas") and not ficheiro.startswith("Erro"):
            correr_teste(os.path.join(pasta, ficheiro))

        #if ficheiro == "SomaArray.pas":
        #    correr_teste(os.path.join(pasta, ficheiro))

if __name__ == "__main__":
    main()

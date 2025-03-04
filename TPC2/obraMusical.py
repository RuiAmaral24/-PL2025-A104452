import re

def carregar_dados(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8-sig') as arquivo:
        conteudo = arquivo.read()
    
    linhas_brutas = re.findall(r'(?:".*?"|[^\n])+', conteudo, re.DOTALL)
    linhas = [' '.join(linha.strip().splitlines()) for linha in linhas_brutas]
    
    cabecalho = linhas[0].strip().split(';')
    registros = [linha.strip().split(';') for linha in linhas[1:] if linha.strip()]
    return cabecalho, registros

def linha_valida(registro):
    if len(registro) != 7:
        return False
    
    _, _, _, periodo, compositor, _, _ = [campo.strip() for campo in registro]
    
    if not re.match(r'^[A-Za-záéíóúãõçÁÉÍÓÚÀà\s]+$', periodo):
        return False
    
    if not re.match(r'^[A-Za-záéíóúãõçÁÉÍÓÚÀà\s,]+$', compositor):
        return False
    
    return True

def analisar_dados(registros):
    compositores = set()
    contagem_periodo = {}
    obras_por_periodo = {}
    linhas_descartadas = []
    
    registros_validos = [linha for linha in registros if linha_valida(linha)]
    linhas_descartadas = [linha for linha in registros if not linha_valida(linha)]
    
    for registro in registros_validos:
        titulo, _, _, periodo, compositor, _, _ = [campo.strip() for campo in registro]
        
        compositores.update(map(str.strip, compositor.split(',')))
        
        contagem_periodo[periodo] = contagem_periodo.get(periodo, 0) + 1
        
        if periodo not in obras_por_periodo:
            obras_por_periodo[periodo] = []
        obras_por_periodo[periodo].append(titulo)
    
    return (
        sorted(compositores),
        contagem_periodo,
        {k: sorted(v) for k, v in obras_por_periodo.items()},
        len(linhas_descartadas),
        linhas_descartadas
    )

def executar():
    arquivo = 'obras.csv'
    cabecalho, registros = carregar_dados(arquivo)
    
    compositores, distribuicao, obras_ordenadas, descartadas, detalhes_descartadas = analisar_dados(registros)
    
    print("Lista de compositores ordenada:")
    for compositor in compositores:
        print(f"- {compositor}")
    
    print("\nNúmero de obras por período:")
    for periodo, quantidade in distribuicao.items():
        print(f"{periodo}: {quantidade} obras")
    
    print("\nObras organizadas por período:")
    for periodo, obras in obras_ordenadas.items():
        print(f"{periodo}:")
        for obra in obras:
            print(f"  - {obra}")
    
    if descartadas > 0:
        print(f"\nAviso: {descartadas} linha(s) foram ignoradas devido a formatação incorreta.")
        # print("\nLinhas ignoradas:")
        # for linha in detalhes_descartadas:
        #     print(f"- {linha}")

if __name__ == "__main__":
    executar()